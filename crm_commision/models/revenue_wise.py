# -*- coding: utf-8 -*-
from venv import create
from odoo import fields, models, api
from odoo.api import readonly


class RevenueWise(models.Model):
    _name = "revenue.wise"
    _description = "Revenue Wise"

    sequence = fields.Char(readonly=True)
    from_amount = fields.Float()
    to_amount = fields.Float()
    rate = fields.Float()
    commission_id = fields.Many2one('crm.commission')
    revenue_wise_type = fields.Selection(related='commission_id.revenue_wise_type',
                                         required=True)

    @api.model_create_multi
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('revenue.wise')
        return super().create(vals)
