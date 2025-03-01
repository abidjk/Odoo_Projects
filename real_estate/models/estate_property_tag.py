from odoo import fields,models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'tags'

    name = fields.Char(string="Name", required=True)

    _sql_constraints = [
        ('property_tag','UNIQUE(name)','the tags should be unique'),
    ]