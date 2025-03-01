# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.api import readonly, depends


class SaleOrder(models.Model):
    """defining the details and field of the model"""
    _inherit = 'sale.order'

    new_state = fields.Selection(selection=[('open', 'Open'), ('close', 'Close')] , compute="_compute_new_state", readonly=False,defalt='open',store=True)
    my_field = fields.Boolean(default=False)

    @api.depends("delivery_status")
    def _compute_new_state(self):
        for record in self:
            if record.state == 'sale' and record.delivery_status == 'full':
                record.new_state = "close"
                record.my_field = True
            elif record.state == 'sale' and record.delivery_status != 'full':
                record.new_state = record.new_state













