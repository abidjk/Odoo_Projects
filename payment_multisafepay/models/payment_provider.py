import logging
import pprint

import requests
from werkzeug import urls

from odoo import _,fields, models, service
from odoo.addons.payment_multisafepay import const
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('multisafepay', "Multisafepay")], ondelete={'multisafepay': 'set default'})
    multisafepay_api_key = fields.Char(
        string="Multisafepay API Key",
        help="The Test or Live API Key depending on the configuration of the provider",
        required_if_provider="multisafepay", groups="base.group_system"
    )

    def _get_supported_currencies(self):
        """ Override of `payment` to return the supported currencies. """
        supported_currencies = super()._get_supported_currencies()
        print('hi')
        if self.code == 'multisafepay':
            supported_currencies = supported_currencies.filtered(
                lambda c: c.name in const.SUPPORTED_CURRENCIES
            )
        print(supported_currencies)
        return supported_currencies

    def _multisafepay_make_request(self, endpoint, data=None, method='POST'):
        self.ensure_one()
        endpoint = f'/v1/json/{endpoint.strip("/")}'
        url = urls.url_join('https://testapi.multisafepay.com/', endpoint)

        # odoo_version = service.common.exp_version()['server_version']
        # module_version = self.env.ref('base.module_payment_multisafepay').installed_version
        headers = {
            "Accept": "application/json",
            # "Authorization": f'Bearer {self.multisafepay_api_key}',
            "Content-Type": "application/json",
            # See https://docs.mollie.com/integration-partners/user-agent-strings
            # "User-Agent": f'Odoo/{odoo_version} MollieNativeOdoo/{module_version}',
        }

        try:
            response = requests.request(method, url, json=data, headers=headers, timeout=60)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                _logger.exception(
                    "Invalid API request at %s with data:\n%s", url, pprint.pformat(data)
                )
                raise ValidationError(
                    "Multisafepay: " + _(
                        "The communication with the API failed. Multisafepay gave us the following "
                        "information: %s", response.json().get('detail', '')
                    ))
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            _logger.exception("Unable to reach endpoint at %s", url)
            raise ValidationError(
                "Multisafepay: " + _("Could not establish the connection to the API.")
            )
        return response.json()

    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'multisafepay':
            return default_codes
        return const.DEFAULT_PAYMENT_METHOD_CODES