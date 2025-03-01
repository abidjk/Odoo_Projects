from odoo import models,api
from odoo.models import AbstractModel


class SchoolLeaveReport(models.AbstractModel):
    _name = 'report.school.report_leave'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['school.leave'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'school.leave',
            'docs': docs,
            'data': data['report']
        }