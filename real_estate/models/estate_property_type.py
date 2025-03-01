from odoo import fields,models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "types"

    name = fields.Char(string="Property Type", required=True)
    property_id=fields.One2many("estate.property")

    _sql_constraints = [
        ('property_type', 'UNIQUE(name)', 'type should be unique')
    ]