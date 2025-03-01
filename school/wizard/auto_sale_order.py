from email.policy import default
from odoo import fields, models, api, Command


class AutoSaleOrder(models.TransientModel):
    """this model is used for automatic sale order"""
    _name = "auto.sale.order"
    _description = "Automatic Sale Order"

    product_id = fields.Many2one("product.template", readonly=True)
    customer_id = fields.Many2one("res.partner")
    price = fields.Float(related="product_id.list_price")
    quantity = fields.Integer()
    tot_price = fields.Float(compute="_compute_tot_price")

    @api.depends("price", "quantity")
    def _compute_tot_price(self):
        """To compute the total price of the product"""
        self.tot_price = self.price * self.quantity

    def action_auto_sale_order(self):
        """Button action to create automatic sale order"""
        product = (self.env['product.product'].search([('product_tmpl_id', '=', self.product_id.id)], limit=1)).id
        order = self.env['sale.order'].search([('partner_id', '=', self.customer_id.id), ('state', '=', 'draft')],
                                                    limit=1)
        if order:
            order.write({
                'order_line': [Command.create({
                    'product_id': product,
                    'product_uom_qty': self.quantity
                })]
            })
            order.action_confirm()
        else:
            order = self.env['sale.order'].create({
                'partner_id': self.customer_id.id,
                'order_line': [Command.create({
                    'product_id': product,
                    'product_uom_qty': self.quantity
                })],
            })
            order.action_confirm()
