# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SaleOrder(models.Model):
    """defining the details and field of the model"""
    _inherit = 'sale.order'

    my_commission = fields.Float(compute="_compute_my_commission", string="Commission")

    @api.depends("user_id", "team_id")
    def _compute_my_commission(self):
        """for computing the commission on particular sale order"""
        for record in self:
            record.my_commission = 0
            commission_plan = record.user_id.commission_id if record.user_id.commission_id else record.team_id.commission_id
            if record.state == 'sale' and commission_plan.active:
                if commission_plan.commission_type == 'product_wise':
                    product_lines = commission_plan.product_wise_ids
                    achieved_commission = []
                    for order_lines in record.order_line:
                        commission_lines = product_lines.filtered(lambda
                                                                      r: r.product_id == order_lines.product_template_id or r.category_id == order_lines.product_template_id.categ_id)
                        max_commission = commission_lines.max_commission_amt if commission_lines.max_commission_amt != 0 else False
                        commission = order_lines.price_subtotal * commission_lines.rate
                        achieved_commission.append(commission if commission <= max_commission else max_commission) if (
                            max_commission) else achieved_commission.append(commission)
                    record.my_commission = sum(achieved_commission)
                else:
                    sale_order_lines_amount = record.order_line.mapped('price_subtotal')
                    if commission_plan.revenue_wise_type == 'straight':
                        rate = commission_plan.revenue_wise_ids.rate
                        record.my_commission = (sum(sale_order_lines_amount)) * rate
                    else:
                        total_amount = sum(sale_order_lines_amount)
                        tot_commission = []
                        balance = []
                        if total_amount != 0:
                            for line in commission_plan.revenue_wise_ids:
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
