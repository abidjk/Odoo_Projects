# -*- coding: utf-8 -*-
from odoo import models, _


class ProductTemplate(models.Model):
    """defining the details and field of the model"""
    _inherit = "product.template"

    def action_auto_sale_order(self):
        return {'type': 'ir.actions.act_window',
                'name': _('Automatic Sale Order'),
                'res_model': 'auto.sale.order',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_product_id': self.id}
        }