# -*- coding: utf-8 -*-
from email.policy import default

from odoo import fields, models


class ProductWise(models.Model):
    """defining the details and fields of the model"""
    _name = "product.wise"
    _description = "Product Wise"

    applied_on = fields.Selection(selection=[('product', 'Product'), ('category', 'Category')], required=True, default='product')
    category_id = fields.Many2one('product.category')
    product_id = fields.Many2one('product.template')
    rate = fields.Float()
    max_commission_amt = fields.Float(string="Maximum Commission")
    commission_id = fields.Many2one('crm.commission')
