from email.policy import default

from dateutil.relativedelta import relativedelta
from dateutil.utils import today
from reportlab.graphics.transform import inverse
from odoo.exceptions import ValidationError

from odoo import fields,models
from odoo.api import depends
from dateutil.utils import today
from odoo.tools import date_utils


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status",copy=False,
                              selection=[('accepted','Accepted'),('refused','Refused')])
    partner_id = fields.Many2one("res.partner",required=True)
    property_id=fields.Many2one("estate.properties")
    deadline = fields.Date(compute="_compute_deadline",inverse="_inverse_deadline")
    validity = fields.Integer(string="validity")
    created_date=fields.Date(default=today())

    @depends("validity","created_date")
    def _compute_deadline(self):
        for record in self:
            record.deadline=date_utils.add(today(),days=record.validity)
    def _inverse_deadline(self):
        for record in self:
            record.validity=(record.deadline - record.created_date).days
    def offer_accepted(self):
        status_list=self.property_id.offer_id.mapped('status')
        print(status_list)
        for record in status_list:
            if record=='accepted':
                raise ValidationError("Already accepted")
        self.status='accepted'
        self.property_id.selling_price=self.price
        self.property_id.buyer=self.partner_id
    def offer_refused(self):
        self.status='refused'
    def offer_none(self):
        self.status=''
    _sql_constraints = [
        ('offer_price','CHECK(price > 0)','The offer price should be positive')
    ]
