from email.policy import default

from odoo import fields,models,api
from dateutil.utils import today

class OpRegistration(models.Model):
    _name = "op.registration"
    _description = "OP Registration"
    _rec_name = "serial_no"

    serial_no=fields.Char('Sequence', default="new")
    patient_name=fields.Many2one("res.partner")
    age=fields.Integer(string="Age", readonly="True", related="patient_name.age", store="True")
    gender=fields.Selection(string="Gender", related="patient_name.gender")
    doctor_name=fields.Many2one("hr.employee")
    op_date_time=fields.Date(string="OP Date",default=today())
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    fee=fields.Monetary(string="fee", related="doctor_name.hourly_cost")
    token_no=fields.Integer(string="Token No", default=1)

    @api.model
    def create(self,vals_list):
        vals_list['serial_no']=self.env['ir.sequence'].next_by_code('op.registration')
        return super().create(vals_list)

    # def _auto_age(self):
    #     self.age=
