from email.policy import default

from reportlab.graphics.transform import inverse

from odoo import fields, models, api
from odoo.api import readonly


class ProductTemplate(models.Model):
    """defining the details and field of the model"""
    _inherit = 'product.template'
    _name = 'product.template'

    taxes_id = fields.Many2many("account.tax", compute='_compute_default_tax', store=True, readonly=False)
    type = fields.Selection(selection=[('consu', 'Goods'), ('service', 'Service'), ('combo', 'Combo')])

    @api.depends("type")
    def _compute_default_tax(self):
        serv_id = self.env['account.tax'].search([('tax_scope', '=', 'service')]).id
        sale_id = self.env['account.tax'].search([('tax_scope', '=', 'consu')]).id

        if self.type == 'service':
            self.write({
                'taxes_id': [(fields.Command.clear())]
            })
            self.write({
                'taxes_id': [(fields.Command.link(serv_id))]
            })
        elif self.type == 'consu':
            self.write({
                'taxes_id': [(fields.Command.clear())]
            })
            self.write({
                'taxes_id': [(fields.Command.link(sale_id))]
            })
