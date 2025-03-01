from dateutil.utils import today

from odoo import fields,models

class FlatManagement(models.Model):
    _name = "flat.management"
    _description = "Flat Management"

    name=fields.Char()
    description=fields.Text()
    amount=fields.Float()
    flat_sale_id=fields.Many2one("flat.sale")
