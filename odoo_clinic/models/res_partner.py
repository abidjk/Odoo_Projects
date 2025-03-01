from email.policy import default
from odoo import fields, models, api
from dateutil.utils import today

class TestModel(models.Model):
    _inherit = "res.partner"
    age=fields.Integer(string="Age",readonly=True,compute="_calculate_age")
    dob=fields.Date(string="Date of birth")
    gender=fields.Selection(string="Gender", selection=[('male','Male'),('female','Female')])
    blood_group=fields.Selection(string="Blood Group", selection=[('o+ve','O+ve'),('o-ve','O-ve'),('a+ve','A-ve'),('a-ve','A-ve'),('b+ve','B+ve'),('b-ve','B-ve')])
    current_date=fields.Date(default=fields.Datetime.now)
    patient_id=fields.Integer(string="patient id")

    @api.depends("current_date","dob")
    def _calculate_age(self):
        for record in self:
            if record.dob:
                    record.age=((record.current_date-record.dob).days)/365
            else:
                record.age=False

    _sql_constraints = [
        ('patient_id', 'UNIQUE(patient_id)', 'The PATIENT ID should be unique'),

    ]



