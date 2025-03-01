# -*- coding: utf-8 -*-
from dateutil.utils import today
from odoo.exceptions import ValidationError
from odoo import fields, models, api, Command


class SchoolStudents(models.Model):
    """defining the details and field of the model"""
    _name = "school.students"
    _description = "School Students"
    _rec_name = "first_name"
    _inherit = "mail.thread"

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name")
    father = fields.Char(string="Father")
    mother = fields.Char(string="Mother")
    comm_address = fields.Text(string="Communication Address")
    same_as_comm = fields.Boolean(string="Same as communication address")
    perm_address = fields.Text(string="Permanent Address")
    email = fields.Char(string="Email", required=True)
    phone = fields.Integer(string="Phone")
    dob = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", readonly=True, compute='_compute_age', store=True)
    current_date = fields.Date(default=fields.Datetime.now)
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female')], string="Gender")
    reg_date = fields.Date(string="Registration Date", default=today())
    photo = fields.Image(string="Image")
    prev_academic_dept = fields.Many2one("school.department")
    prev_class = fields.Many2one("school.class")
    tc = fields.Many2many('ir.attachment', string='TC')
    aadhar_no = fields.Integer(string="Aadhar No", copy=False)
    sequence = fields.Char(string="Reg No", readonly=True)
    admission_no = fields.Char(string="Admission No", readonly=True)
    status = fields.Selection(selection=[('draft', 'Draft'), ('registration', 'Registration')], string="Status",
                              tracking=True)
    school_id = fields.Many2one('res.company', store=True, copy=False,
                                string="School",
                                default=lambda self: self.env.company.id)
    class_id = fields.Many2one("school.class")
    prev_school_id = fields.Many2one("res.company")
    club_ids = fields.Many2many("school.club", relation="school_students_clubs", column1="student_id",
                                column2="club_id")
    exam_ids = fields.Many2many("school.exam", domain=[('exam_status', '=', 'assigned')])
    attendance = fields.Selection(selection=[('present', 'Present'), ('absent', 'Absent')], default="present")
    leave_ids = fields.One2many("school.leave", "student_id")
    user_id = fields.Many2one("res.partner")
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company.id)
    website_registration = fields.Boolean()

    @api.constrains("prev_academic_dept", "prev_class")
    def _check_class(self):
        """Validation of prev class based on prev dept"""
        if self.prev_academic_dept != self.prev_class.department_id:
            raise ValidationError("Department and class is not Matching")

    _sql_constraints = [
        ('unique_aadhar', 'unique(aadhar_no)', 'Aadhar Number should be unique')
    ]

    @api.depends("dob")
    def _compute_age(self):
        """age calculating based on onchange of dob"""
        if self.dob:
            temp_age = ((self.current_date - self.dob).days) / 365
            if temp_age > 5:
                self.age = temp_age
            else:
                raise ValidationError("Minimum age is 5")
        else:
            self.age = False

    @api.model
    def create(self, vals_list):
        """generating sequence number"""
        vals_list['sequence'] = self.env['ir.sequence'].next_by_code('school.students')
        vals_list['status'] = 'draft'
        return super().create(vals_list)

    def action_registration_state(self):
        """status changing and generating sequence number to the students when clicking register button"""
        self.status = 'registration'
        self.admission_no = self.env['ir.sequence'].next_by_code('school.students.admission')

    def action_create_user(self):
        """action for creating user when creating a student"""
        if self.status == 'registration':
            user = self.env['res.users'].create([{
                'name': self.first_name,
                'login': self.email,
                'groups_id': [Command.link(self.env.ref('base.group_user').id),
                              Command.link(self.env.ref('school.student_group_manager').id)]
            }])
            user.partner_id.write({'partner_type': 'student'})
            # self.user_id = user.id
