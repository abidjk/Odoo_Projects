# -*- coding: utf-8 -*-
from odoo import fields, models, Command


class ResPartner(models.Model):
    """defining the details and field of the model"""
    _inherit = 'res.partner'

    partner_type = fields.Selection(
        selection=[('teacher', 'Teacher'), ('student', 'Student'), ('office_staff', 'Office Staff')])
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company.id)
    choose_type = fields.Selection(selection=[('product', 'Product'), ('category', 'Category')])
    allowed_product_ids = fields.Many2many('product.template'   )
    allowed_category_ids = fields.Many2many('product.public.category')

    _sql_constraints = [
        ('partner_unique', 'unique(complete_name, email)', "multiple partners with same email cannot be allowed")
    ]

    def action_create_user_on_partner(self):
        """action for creating user when creating an employee"""
        if self.partner_type == 'teacher':
            self.env['res.users'].create([{
                'name': self.complete_name,
                'login': self.email,
                'partner_id': self.id,
                'groups_id': [Command.link(self.env.ref('school.teacher_group_manager').id)]
            }])
        elif self.partner_type == 'office_staff':
            self.env['res.users'].create([{
                'name': self.complete_name,
                'login': self.email,
                'partner_id': self.id,
                'groups_id': [Command.link(self.env.ref('base.group_user').id),
                              Command.link(self.env.ref('school.office_staff_group_manager').id)]
            }])
