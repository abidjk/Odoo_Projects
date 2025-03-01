# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SchoolDepartment(models.Model):
    """defining the details and field of the model"""
    _name = "school.department"
    _description = "School Department"
    _inherit = "mail.thread"

    name = fields.Char(string="Name")
    hod_id = fields.Many2one("hr.employee")
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company.id)
