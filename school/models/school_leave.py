# -*- coding: utf-8 -*-
from dateutil.utils import today
from odoo import fields, models, api
from datetime import datetime, timedelta


class SchoolLeave(models.Model):
    """defining the details and field of the model"""
    _name = "school.leave"
    _description = "School Leave"
    _inherit = "mail.thread"
    _rec_name = "student_id"

    student_id = fields.Many2one("school.students", ondelete="cascade", domain=[('status', '=', 'registration')],
                                 required=True, create=False)
    class_id = fields.Many2one(related="student_id.class_id",store=True)
    start_date = fields.Datetime(default=today())
    end_date = fields.Datetime(default=today())
    total_days = fields.Float(default=1, compute="_compute_total_days",store=True)
    half_day = fields.Boolean()
    half_day_type = fields.Selection(selection=[('fn', 'FN'), ('an', 'AN')])
    reason = fields.Char(required=True)
    leave_status = fields.Selection(selection=[('present', 'Present'), ('absent', 'Absent')])
    company_id = fields.Many2one("res.company", default=lambda self:self.env.company.id)

    @api.depends("start_date", "end_date", "half_day")
    def _compute_total_days(self):
        """function for computing the total days of leave"""
        for record in self:
            if record.half_day:
                record.total_days = 0.5
            elif record.start_date == record.end_date:
                record.total_days = 1
            elif record.start_date and record.end_date:
                current_date = record.start_date
                record.total_days = 0
                while current_date <= record.end_date:
                    if current_date.weekday() not in (5, 6):
                        record.total_days += 1
                    current_date += timedelta(days=1)

    _sql_constraints = [
        ('minimum_leave', 'CHECK(total_days >= 0.5 )', 'Minimum leave should 0.5')
    ]

    @api.onchange("start_date", "end_date")
    def _onchange_start_date(self):
        """function for setting the current day attendance based on the dates"""
        for leave in self:
            if leave.start_date == datetime.date(today()) or leave.end_date == datetime.date(today()):
                leave.leave_status = 'absent'
            elif leave.start_date < datetime.today() < leave.end_date:
                leave.leave_status = 'absent'
            else:
                leave.leave_status = 'present'

    def _cron_student_leave(self):
        """crone for checking the current day attendance based on the dates"""
        current_day = fields.Date.today()
        for record in self.search([]):
            if record.start_date.date() == current_day == record.end_date.date():
                record.leave_status = "absent"
                record.student_id.attendance = 'absent'
            elif record.start_date.date() < current_day < record.end_date.date():
                record.leave_status = "absent"
                record.student_id.attendance = 'absent'
            else:
                record.leave_status = "present"
                record.student_id.attendance = 'present'
