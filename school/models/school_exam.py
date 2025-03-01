# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SchoolExam(models.Model):
    """defining the details and field of the model"""
    _name = "school.exam"
    _description = "Exam"
    _inherit = "mail.thread"

    name = fields.Char()
    class_id = fields.Many2one("school.class")
    paper_ids = fields.One2many("school.paper", "exam_id")
    student_ids = fields.Many2many("school.students")
    exam_status = fields.Selection(selection=[('created', 'Created'), ('assigned', 'Assigned')], string="Status",
                                   tracking=True)
    start_date = fields.Datetime(required=True)
    end_date = fields.Datetime(required=True)
    exam_assigned = fields.Boolean()
    company_id = fields.Many2one("res.company", default=lambda self:self.env.company.id)

    def create(self, vals):
        """changing the exam status"""
        vals['exam_status'] = 'created'
        return super().create(vals)

    def action_add_exams(self):
        """Button action for adding the exams to students"""
        students = [self.class_id.student_ids]
        [std.update({'exam_ids': [fields.Command.link(self.id)]}) for std in students]
        self.exam_status = 'assigned'

    def action_add_exams_to_new_studs(self):
        print(self.class_id.student_ids.exam_ids)
        """Button action for adding exams to the newly added students"""
        new_students = [self.class_id.student_ids.filtered(lambda stud: self.id not in stud.exam_ids.ids)]
        [std.update({'exam_ids': [fields.Command.link(self.id)]}) for std in new_students]
