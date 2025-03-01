# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CrmTeam(models.Model):
    """defining the details and fields of the model"""
    _inherit = "crm.team"

    commission_id = fields.Many2one('crm.commission')

