import json
import logging
import pprint
from importlib.resources._common import _

import requests
from werkzeug import urls

from odoo.addons.payment_multisafepay import const
from odoo.addons.payment_multisafepay.controllers.main import MultisafepayController
from odoo import models

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    """inheriting payment transaction"""
    _inherit = "payment.transaction"

    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return Multisafepay-specific rendering values."""
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'multisafepay':
            return res
        payload = self._multisafepay_prepare_payment_request_payload()
        _logger.info("sending '/payments' request for link creation:\n%s", pprint.pformat(payload))
        payment_data = self.provider_id._multisafepay_make_request(f'/orders?api_key={self.provider_id.multisafepay_api_key}', data=payload)
        redirect_url = payment_data['data']['payment_url']
        return {'api_url': redirect_url}

    def _multisafepay_prepare_payment_request_payload(self):
        """ Create the payload for the payment request based on the transaction values.
        :return: The request payload
        :rtype: dict
        """
        user_lang = self.env.context.get('lang')
        base_url = self.provider_id.get_base_url()
        redirect_url = urls.url_join(base_url, MultisafepayController._return_url)
        return {
            'type': "redirect",
            'order_id': self.reference,
            "gateway": "",
            'currency': self.currency_id.name,
            'amount': round(self.amount),
            "description": self.reference,
            "payment_options": {
                "redirect_url": redirect_url,
            },
            "customer": {
                "locale": user_lang if user_lang in const.SUPPORTED_LOCALES else 'en_US',
            },
        }

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Override of payment to find the transaction based on multisafepay data."""
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'multisafepay' or len(tx) == 1:
            return tx
        tx = self.search([('reference','=',notification_data.get('transactionid'))])
        return tx

    def _process_notification_data(self, notification_data):
        """ Override of payment to process the transaction based on Multisafepay data."""
        super()._process_notification_data(notification_data)
        if self.provider_code != 'multisafepay':
            return
        url = f'https://testapi.multisafepay.com/v1/json/orders/{notification_data.get('transactionid')}?api_key={self.provider_id.multisafepay_api_key}'
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        response = json.loads(response.text)
        status = response['data']['status']

        if status == 'uncleared':
            self._set_pending()
        elif status == 'initialized':
            self._set_authorized()
        elif status == 'completed':
            self.provider_reference = f"multisafepay-{notification_data.get('transactionid')}"
            self._set_done()
        elif status in ['expired', 'cancelled', 'declined', 'void']:
            self._set_canceled("Multisafepay: " + _("Cancelled payment with status: %s", status))
        else:
            _logger.info(
                "received data with invalid payment status (%s) for transaction with reference %s",
                status, self.reference
            )
            self._set_error(
                "Multisafepay: " + _("Received data with invalid payment status: %s", status)
            )
