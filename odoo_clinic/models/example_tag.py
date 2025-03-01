from odoo import fields,models,api
from dateutil.utils import today


class ExampleTag(models.Model):
    _name = "example.tag"
    _description = "Example Tag"

    name = fields.Char()
    color = fields.Integer()