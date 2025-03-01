# -*- coding: utf-8 -*-
from odoo import fields, models


class SchoolPaper(models.Model):
    """defining the details and field of the model"""
    _name = "school.paper"
    _description = "Paper"
    _inherit = "mail.thread"

    name = fields.Many2one("school.subject")
    pass_mark = fields.Float()
    max_mark = fields.Float()
    exam_id = fields.Many2one("school.exam")
    company_id = fields.Many2one("res.company", default=lambda self:self.env.company.id)
