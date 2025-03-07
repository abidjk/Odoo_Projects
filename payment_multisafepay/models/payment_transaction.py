import logging
import pprint

from werkzeug import urls

from odoo.addons.payment.const import CURRENCY_MINOR_UNITS
from odoo.addons.payment_multisafepay import const
from odoo.addons.payment_multisafepay.controllers.main import MultisafepayController
from odoo import models

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'multisafepay':
            return res
        payload = self._multisafepay_prepare_payment_request_payload()
        _logger.info("sending '/payments' request for link creation:\n%s", pprint.pformat(payload))
        payment_data = self.provider_id._multisafepay_make_request(f'/orders?api_key={self.provider_id.multisafepay_api_key}', data=payload)
        print(payment_data)
        # self.provider_reference = payment_data.get('id')
        #
        redirect_url = payment_data['data']['payment_url']
        # parsed_url = urls.url_parse(checkout_url)
        # url_params = urls.url_decode(parsed_url.query)
        return {'api_url': redirect_url}

    def _multisafepay_prepare_payment_request_payload(self):
        """ Create the payload for the payment request based on the transaction values.

        :return: The request payload
        :rtype: dict
        """
        user_lang = self.env.context.get('lang')
        base_url = self.provider_id.get_base_url()
        redirect_url = urls.url_join(base_url, MultisafepayController._return_url)
        # webhook_url = urls.url_join(base_url, MollieController._webhook_url)
        # decimal_places = CURRENCY_MINOR_UNITS.get(
        #     self.currency_id.name, self.currency_id.decimal_places
        # )
        return {
            'type': "redirect",
            'order_id': self.reference,
            "gateway": "",
            'currency': self.currency_id.name,
            'amount': round(self.amount),
            "description": self.reference,
            "payment_options": {
                # "notification_url": "https://www.example.com/client/notification?type=notification",
                # "notification_method": "POST",
                "redirect_url": redirect_url,
                    # "cancel_url": "https://www.example.com/client/notification?type=cancel",
                    # "close_window": true
            },
            "customer": {
                "locale": user_lang if user_lang in const.SUPPORTED_LOCALES else 'en_US',
            },
        }

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        res = super()._get_tx_from_notification_data(provider_code, notification_data)
        print("provider code:",provider_code,"notification data:",notification_data)
        transaction_id = self.env['payment.transaction'].search([('reference','=',notification_data.get('transactionid'))])
        return transaction_id

    def _process_notification_data(self, notification_data):
        res = super()._process_notification_data(notification_data)
        transaction_id = self.env['payment.transaction'].search([('reference','=',notification_data.get('transactionid'))])
        transaction_id.state = "done"


