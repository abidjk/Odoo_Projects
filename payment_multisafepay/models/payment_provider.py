from werkzeug import urls

from odoo import fields, models, service


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('multisafepay', "Multisafepay")], ondelete={'multisafepay': 'set default'})
    multisafepay_api_key = fields.Char(
        string="Multisafepay API Key",
        help="The Test or Live API Key depending on the configuration of the provider",
        required_if_provider="multisafepay", groups="base.group_system"
    )

    def _multisafepay_make_request(self, endpoint, data=None, method='POST'):
        self.ensure_one()
        endpoint = f'/v2/{endpoint.strip("/")}'
        url = urls.url_join('https://testapi.multisafepay.com/', endpoint)
        print(url)

        odoo_version = service.common.exp_version()['server_version']
        print(odoo_version)