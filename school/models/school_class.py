# -*- coding: utf-8 -*-
from odoo import fields, models


class SchoolClass(models.Model):
    """defining the details and field of the model"""
    _name = "school.class"
    _description = "School Class"
    _inherit = "mail.thread"

    name = fields.Char(string="Class name")
    department_id = fields.Many2one("school.department")
    hod_id = fields.Many2one(string="HOD", related="department_id.hod_id", readonly=False)
    student_ids = fields.One2many("school.students", "class_id", domain=[('status', '=', 'registration')])
    exam_ids = fields.One2many("school.exam", "class_id")
    leave_ids = fields.One2many("school.leave", "class_id")
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company.id)
