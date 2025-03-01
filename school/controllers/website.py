# -*- coding: utf-8 -*-
import base64
from odoo import http, fields
from odoo.http import request


class School(http.Controller):
    """website controller"""
    @http.route('/student-form', type="http", auth="public", website=True)
    def student_form(self, **kw):
        """defining students registration form"""
        classes = request.env['school.class'].sudo().search([])
        clubs = request.env['school.club'].sudo().search([])
        return http.request.render('school.create_student', {'classes': classes, 'clubs': clubs})

    @http.route('/get-clubs', type="json", auth="public", website=True)
    def get_clubs(self, clubs):
        """getting clubs for student registration"""
        if clubs:
            club_ids = [int(club) for club in clubs if club != ""]
            return {'club_ids': club_ids}

    @http.route('/create-student', type="http", auth="public", methods=['POST'], website=True)
    def create_student(self, **post):
        """Creating student record"""
        if post.get('club_ids'):
            club_ids = post.get('club_ids')
            ids = [int(id) for id in club_ids if id != ',']
        else:
            ids = []
        if post.get('tc'):
            attachment = post.get('tc')
            attachment_id = request.env['ir.attachment'].sudo().create({
                'name': post.get('tc').filename,
                'type': 'binary',
                'res_model': 'school.students',
                'datas': base64.b64encode(attachment.read()),
            })
        else:
            attachment_id = False
        new_student = request.env['school.students'].sudo().create({
            'first_name': post.get('first_name'),
            'last_name': post.get('last_name'),
            'father': post.get('father'),
            'mother': post.get('mother'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'class_id': post.get('class_id'),
            'club_ids': [(fields.Command.link(id)) for id in ids if ids],
            'aadhar_no': post.get('aadhar_no'),
            'dob': post.get('dob'),
            'gender': post.get('gender'),
            'tc': attachment_id,
            'website_registration': True
        })
        new_student.action_registration_state()
        admission_no = request.env['school.students'].sudo().search([('id', '=', new_student.id)]).admission_no
        return request.render('school.student_thanks', {'admission_no': admission_no})

    @http.route('/student-list', type="http", auth="public", website=True)
    def student_list(self, **kw):
        """List view of registered students"""
        students = request.env['school.students'].sudo().search([('website_registration','=',True)])
        return http.request.render('school.student_list', {'students':students})

    @http.route('/leave-form', type="http", auth="public", website=True)
    def leave_form(self, **kw):
        """defining leaves registration form"""
        students = request.env['school.students'].sudo().search([('status', '=', 'registration')])
        return http.request.render('school.create_leave', ({'students': students}))

    @http.route('/get-class', type='json', auth='public', website=True)
    def get_class(self, action):
        """Taking class of corresponding student"""
        student_class = request.env['school.students'].sudo().browse(action).class_id
        class_name = student_class.name
        class_id = student_class.id
        return {'class_name': class_name, 'class_id': class_id}

    @http.route('/create-leave', type="http", auth="public", website=True)
    def create_leave(self, **kw):
        """Creating leave record"""
        admission_no = request.env['school.students'].sudo().search([('id','=',kw.get('student_id'))]).admission_no
        request.env['school.leave'].sudo().create(kw)
        return request.render('school.leave_thanks', {'admission_no': admission_no,'days':kw.get('total_days')})

    @http.route('/event-form', type="http", auth="public", website=True)
    def event_form(self, **kw):
        """defining events registration form"""
        clubs = request.env['school.club'].sudo().search([])
        return http.request.render('school.create_event', {'clubs': clubs})

    @http.route('/create-event', type="http", auth="public", website=True)
    def create_event(self, **kw):
        """Creating event record"""
        request.env['school.event'].sudo().create(kw)
        return request.render('school.event_thanks', {'event': kw.get('name')})
