from email.policy import default

from dateutil.relativedelta import relativedelta
from dateutil.utils import today
from odoo.exceptions import ValidationError

from odoo import fields, models, api
from odoo.addons.test_new_api.models.test_new_api import Selection


class TestModel(models.Model):
    _name = "estate.properties"
    _description = "properties"

    name = fields.Char(string='Name', required=True, help='Enter the name')
    description= fields.Text(string='Description', help='Enter the description')
    postcode= fields.Char(string='Postcode', required=True)
    date_availability=fields.Date(string='Date',copy=False,default=today()+relativedelta(months=3))
    selling_price=fields.Float(string='Selling Price', required=True,copy=False,default=1000,readonly=True)
    expected_price=fields.Float(string='Expected Price')
    bedrooms=fields.Integer(string='Bedrooms',default=2)
    living_area=fields.Integer(string='Living Area')
    garage=fields.Boolean(string='is it a garage')
    garden=fields.Boolean(string='is it a garden')
    garden_area=fields.Integer(string='garden area')
    garden_orientation=fields.Selection(string='Garden Orientation',
                                        selection=[('north','North'),('south','South'),('east','East'),('west','West')],copy=False)
    total_area=fields.Integer(string="Total Area",compute="_compute_total")
    best_offer=fields.Char(string="Best Offer",compute="_best_offer")
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancel', 'Cancel')

        ],
        string='Status',
        required=True,
        copy=False,
    )
    active = fields.Boolean('Active', default=True)
    buyer = fields.Many2one("res.partner", copy=False)
    salesperson = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
    property_type=fields.Many2one("estate.property.type")
    property_tag=fields.Many2many("estate.property.tag")
    offer_id=fields.One2many("estate.property.offer",'property_id')

    @api.depends("living_area","garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area=record.living_area+record.garden_area
    @api.depends("offer_id")
    def _best_offer(self):
        for record in self:
            if record.offer_id:
                record.best_offer = max(record.offer_id.mapped('price'))
            else:
                record.best_offer=0
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area=0
            self.garden_orientation = ""

    def sold_state(self):
        staatus_list=self.offer_id.mapped('status')
        print(staatus_list)
        if self.state!='cancel':
            if 'accepted' not in staatus_list:
                raise ValidationError('One offer should be accepted')
            elif 'accepted' in staatus_list:
                self.state='sold'
        else:
            raise ValidationError("Cannot sold the canceled properties")


    def cancel_state(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'cancel'
            else:
                raise ValidationError("Cannot cancel the sold properties")

    @api.constrains('expected_price','selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price<0.9*record.expected_price:
                raise ValidationError("The selling price should be at least 90 % of the expected price")

    _sql_constraints = [
        ('expected_price', 'CHECK(expected_price > 0)', 'The expected price should be positive'),
        ('selling_price', 'CHECK(selling_price > 0)', 'The selling price should be positive'),
        ('property_name', 'unique(name)', 'The name should be unique'),

    ]







