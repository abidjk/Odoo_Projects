from odoo import fields,models
from dateutil.utils import today

class ClinicPrescription(models.Model):
    _name = "clinic.prescription"
    _description = "Clinic Description"

    consultation_no=fields.Many2one("clinic.consultation")
    patient_name=fields.Many2one(string="Patient Name", related="consultation_no.patient_name")
    medicine=fields.Many2one("product.template",required=True)
    quantity=fields.Integer(string="Quantity")
    dosage=fields.Text(string="Dosage")