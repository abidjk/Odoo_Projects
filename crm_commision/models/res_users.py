# -*- coding: utf-8 -*-
from odoo import models, fields, api
import dateutil.parser
from odoo.addons.test_convert.tests.test_env import record


class ResUsers(models.Model):
    """defining the details and fields of the model"""
    _inherit = "res.users"

    commission_id = fields.Many2one('crm.commission')
    my_commission = fields.Float(compute="_compute_my_commission")

    @api.depends("commission_id")
    def _compute_my_commission(self):
        """computing commission based on the product"""
        for record in self:
            from_date = record.commission_id.from_date
            to_date = record.commission_id.to_date
            record.my_commission = 0
            order_line = record.env['sale.order'].search([('user_id', '=', record.id), ('state', '=', 'sale'),
                        ("date_order", ">=", from_date),("date_order", "<=", to_date)]).mapped('order_line')
            if record.commission_id.active:
                if record.commission_id.commission_type == 'product_wise':
                    product_lines = record.commission_id.product_wise_ids
                    order_line_ids = [order_line_id for order_line_id in order_line]
                    order_line_products = order_line_ids.filtered(
                        lambda r: r.product_template_id in product_lines.mapped(
                            'product_id') or r.product_template_id.categ_id in product_lines.mapped('category_id'))
                    achieved_commission = []
                    for order_lines in order_line_products:
                        commission_lines = product_lines.filtered(lambda
                                                                      r: r.product_id == order_lines.product_template_id or r.category_id == order_lines.product_template_id.categ_id)
                        max_commission = commission_lines.max_commission_amt if commission_lines.max_commission_amt != 0 else False
                        commission = order_lines.price_subtotal * commission_lines.rate
                        achieved_commission.append(
                            commission if commission <= max_commission else max_commission) if max_commission else achieved_commission.append(
                            commission)
                    record.my_commission = sum(achieved_commission)
                else:
                    sale_order_lines_amount = order_line.mapped('price_subtotal')
                    if record.commission_id.revenue_wise_type == 'straight':
                        rate = record.commission_id.revenue_wise_ids.rate
                        record.my_commission = (sum(sale_order_lines_amount)) * rate
                    else:
                        total_amount = sum(sale_order_lines_amount)
                        tot_commission = []
                        balance = []
                        if total_amount != 0:
                            for line in record.commission_id.revenue_wise_ids:
                                if line.from_amount < total_amount < line.to_amount and not balance:
                                    tot_commission.append(total_amount * line.rate)
                                    break
                                else:
                                    if not balance:
                                        tot_commission.append(line.to_amount * line.rate)
                                        balance.append(total_amount - line.to_amount)
                                    elif balance[-1] > line.to_amount - line.from_amount:
                                        commission = (line.to_amount - line.from_amount) * line.rate
                                        tot_commission.append(commission)
                                        balance.append(total_amount - line.to_amount)
                                    else:
                                        tot_commission.append(balance[-1] * line.rate)
                                        break
                            record.my_commission = sum(tot_commission)
