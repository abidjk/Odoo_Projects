from dateutil.utils import today

from odoo import fields,models

class FlatSale(models.Model):
    _name = "flat.sale"
    _description = "Flat Sale"

    name = fields.Char()
    flat_ids = fields.One2many("flat.management","flat_sale_id")