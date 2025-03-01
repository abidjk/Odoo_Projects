from odoo import models,api
from odoo.models import AbstractModel


class SchoolStudentReport(models.AbstractModel):
    _name = 'report.school.report_student'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['school.students'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'school.students',
            'docs': docs,
            'data': data['report']
        }