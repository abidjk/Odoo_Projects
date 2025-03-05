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
        payment_data = self.provider_id._multisafepay_make_request('/payments', data=payload)




    def _multisafepay_prepare_payment_request_payload(self):
        """ Create the payload for the payment request based on the transaction values.

        :return: The request payload
        :rtype: dict
        """
        user_lang = self.env.context.get('lang')
        base_url = self.provider_id.get_base_url()
        redirect_url = urls.url_join(base_url, MultisafepayController._return_url)
        # webhook_url = urls.url_join(base_url, MollieController._webhook_url)
        decimal_places = CURRENCY_MINOR_UNITS.get(
            self.currency_id.name, self.currency_id.decimal_places
        )
        return {
            'description': self.reference,
            'amount': {
                'currency': self.currency_id.name,
                'value': f"{self.amount:.{decimal_places}f}",
            },
            'locale': user_lang if user_lang in const.SUPPORTED_LOCALES else 'en_US',
            'method': [const.PAYMENT_METHODS_MAPPING.get(
                self.payment_method_code, self.payment_method_code
            )],
            # Since Mollie does not provide the transaction reference when returning from
            # redirection, we include it in the redirect URL to be able to match the transaction.
            'redirectUrl': f'{redirect_url}?ref={self.reference}',
            # 'webhookUrl': f'{webhook_url}?ref={self.reference}',
        }