from dateutil.utils import today

from odoo import fields,models

class ClinicConsultation(models.Model):
    _name = "clinic.consultation"
    _description = "Clinic Consultation"

    op_ticket=fields.Many2one("op.registration")
    patient_name=fields.Many2one(string="Patient Name", related="op_ticket.patient_name")
    doctor_name=fields.Many2one(string="Doctor Name",related="op_ticket.doctor_name")
    gender=fields.Selection(string="Gender",related="op_ticket.gender")
    age=fields.Integer(string="Age", related="op_ticket.age")
    dateandtime=fields.Datetime(string="Date and Time", default=today())
    serial_no=fields.Integer(string="Serial No")
    weight=fields.Float(string="Weight")
    spo2=fields.Integer(string="SPO2")
    blood_pressure=fields.Float(string="Blood Pressure")
    body_temperature=fields.Integer(string="Temperature")
    diagnose=fields.Char(string="Diagnose")
    prescription_id=fields.One2many("clinic.prescription","consultation_no")
