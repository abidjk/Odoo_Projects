# -*- coding: utf-8 -*-
from odoo import fields, models


class SchoolClub(models.Model):
    """Defining the details and fields of the model"""
    _name = "school.club"
    _description = "School club"
    _inherit = "mail.thread"

    name = fields.Char(required=True)
    student_ids = fields.Many2many("school.students", relation="school_students_clubs", column1="club_id",
                                   column2="student_id", readonly=True, domain=[('status', '=', 'registration')])
    events = fields.Integer(string="Events", compute='_compute_events')
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company.id)

    def _compute_events(self):
        """generating the count of events"""
        for record in self:
            record.events = self.env['school.event'].search_count([('club_id', '=', record.id)])

    def action_school_club_event_btn(self):
        """defining the views of smart button events"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Events',
            'view_mode': 'list,form',
            'res_model': 'school.event',
            'domain': [('club_id', '=', self.id)],
            'context': "{'create': False}"
        }
