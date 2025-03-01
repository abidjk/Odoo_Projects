# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SchoolAcademic(models.Model):
    """defining the details and field of the model"""
    _name = "school.academic"
    _description = "School Academic"
    _inherit = "mail.thread"

    start_date = fields.Date(string="Start date", required=True)
    end_date = fields.Date(string="End date")
    name = fields.Char(string="Academic year")
    start_date_year = fields.Char()
    end_date_year = fields.Char()
    seperator = fields.Char(default=" - ")
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company.id)

    @api.onchange("start_date", "end_date")
    def _onchange_start_date(self):
        """fetching year and month"""
        if self.start_date and self.end_date:
            self.start_date_year = self.start_date.year
            self.end_date_year = self.end_date.year
            self.name = self.start_date_year + self.seperator + self.end_date_year
        else:
            self.name = ""
