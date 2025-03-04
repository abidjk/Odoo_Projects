# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductProduct(models.Model):
    """Inherit the custom model to add a new field and add the field to the pos"""
    _inherit = "product.product"

    description = fields.Text()

    @api.model
    def _load_pos_data_fields(self, config_id):
        """for loading fields"""
        data = super()._load_pos_data_fields(config_id)
        data += ['description']
        return data
