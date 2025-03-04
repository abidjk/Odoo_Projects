from odoo import fields, models


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('multisafepay', "Multisafepay")], ondelete={'multisafepay': 'set default'})