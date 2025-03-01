# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from dateutil.utils import today


class SchoolEvent(models.Model):
    """defining the details and field of the model"""
    _name = "school.event"
    _description = "School Event"
    _inherit = "mail.thread"

    name = fields.Char()
    club_id = fields.Many2one('school.club', string='Club')
    start_date = fields.Date(default=today())
    end_date = fields.Date(default=today())
    event_status = fields.Selection(selection=[('upcoming', 'Upcoming'), ('ongoing', 'Ongoing'), ('over', 'Over')],
                                    string="Status", tracking=True, compute="_compute_event_status")
    event_image = fields.Image()
    description = fields.Text()
    active = fields.Boolean(default=True)
    partner_id = fields.Many2one("res.partner")
    user_id = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user.id)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company.id)

    @api.depends("start_date", "end_date")
    def _compute_event_status(self):
        """for computing event status"""
        current_date = today().date()
        for record in self:
            if current_date < record.start_date:
                record.event_status = 'upcoming'
            elif current_date > record.end_date:
                record.event_status = 'over'
            else:
                record.event_status = 'ongoing'

    def _cron_event_draft(self):
        """cron for the status of the event based on the current date"""
        for record in self.search([]):
            if record.start_date.date() > fields.Date.today():
                record.event_status = "upcoming"
            elif record.end_date.date() < fields.Date.today():
                record.event_status = "over"
                record.active = False
            else:
                record.event_status = "ongoing"

    def _cron_event_mail(self):
        """crone for sending mails to the employees before 2 days of the event"""
        partners = self.env['res.partner'].search(
            ["|", ("partner_type", "=", "teacher"), ("partner_type", "=", "office_staff")])
        for record in self.search([]):
            if record.start_date.date() - relativedelta(days=2) == fields.Date.today():
                for partner in partners:
                    self.env.ref('school.school_event_mail').send_mail(partner.id, force_send=True)
