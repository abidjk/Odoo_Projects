# -*- coding: utf-8 -*-
from odoo import fields, models


class SchoolSubject(models.Model):
    """defining the details and field of the model"""
    _name = "school.subject"
    _description = "school_subject"
    _inherit = "mail.thread"

    name = fields.Char(string="Subject Name")
    department_id = fields.Many2one("school.department")
    company_id = fields.Many2one("res.company", default=lambda self:self.env.company.id)
