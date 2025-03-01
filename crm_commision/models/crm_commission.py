# -*- coding: utf-8 -*-
from email.policy import default
from unicodedata import category

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class CrmCommission(models.Model):
    """defining the details and fields of the model"""
    _name = "crm.commission"
    _description = "CRM Commission"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    from_date = fields.Date()
    to_date = fields.Date()
    commission_type = fields.Selection(selection=[('product_wise', 'Product Wise'), ('revenue_wise', 'Revenue Wise')])
    product_wise_ids = fields.One2many('product.wise', 'commission_id')
    revenue_wise_ids = fields.One2many('revenue.wise', 'commission_id')
    revenue_wise_type = fields.Selection(selection=[('straight', 'Straight'), ('graduated', 'Graduated')],
                                         required=True)

    @api.constrains("product_wise_ids")
    def _constrains_product_wise_ids(self):
        """for checking uniqueness of products and categories"""
        products = []
        categories = []
        for record in self:
            for line in record.product_wise_ids:
                if line.product_id in products and line.category_id.id in categories:
                    raise ValidationError("Lines should be unique")
                products.append(line.product_id)
                categories.append(line.category_id.id)
