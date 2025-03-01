import datetime
import io
import json
from datetime import datetime
import xlsxwriter
from odoo import fields, models


class LeaveReport(models.TransientModel):
    """this model is used for leave report"""
    _name = "student.report.wizard"
    _description = "Student Report"

    report_type = fields.Selection(selection=[('class', 'Class'), ('department', 'Department'), ('club', 'Club')])
    class_ids = fields.Many2many("school.class")
    department_ids = fields.Many2many("school.department")
    club_ids = fields.Many2many("school.club")

    def fetch_query(self):
        """fetching the required query"""
        query = """SELECT students.first_name, 
               students.admission_no, 
               students.email,students.school_id,
               school_class.name AS class_name, 
               school_department.name AS department_name
                FROM school_students AS students
                INNER JOIN school_class ON students.class_id = school_class.id
                INNER JOIN school_department ON school_class.department_id = school_department.id
                """
        if self.report_type == 'class':
            if len(tuple(self.class_ids.ids)) == 1:
                query += f"""where students.class_id = {self.class_ids.id}"""
            elif len(tuple(self.class_ids.ids)) > 1:
                query += f"""where students.class_id IN {tuple(self.class_ids.ids)}"""
            else:
                query += """"""
        elif self.report_type == 'department':
            if len(tuple(self.department_ids.ids)) == 1:
                query += f"""where school_class.department_id = {self.department_ids.id}"""
            elif len(tuple(self.department_ids.ids)) > 1:
                query += f"""where school_class.department_id IN {tuple(self.department_ids.ids)}"""
            else:
                query += """"""
        elif self.report_type == 'club':
            query = """
                        SELECT students.first_name, 
                       students.admission_no, 
                       students.email,students.school_id,
                       school_class.name AS class_name, 
                       school_department.name AS department_name,
                       school_club.name AS club_name
                        FROM school_students AS students
                        INNER JOIN school_class ON students.class_id = school_class.id
                        INNER JOIN school_department ON school_class.department_id = school_department.id
                        INNER JOIN school_students_clubs AS student_club ON students.id = student_club.student_id
                        INNER JOIN school_club ON school_club.id = student_club.club_id
                    """
            if len(tuple(self.club_ids.ids)) == 1:
                query += f"""where school_club.id = {self.club_ids.id}"""
            elif len(tuple(self.club_ids.ids)) > 1:
                query += f"""where school_club.id IN {tuple(self.club_ids.ids)}"""
            else:
                """"""
        else:
            query += """"""
        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()

    def action_print_student_report(self):
        """action on printing a report"""
        report = self.fetch_query()
        if self.report_type == 'class':
            classes = set([record['class_name'] for record in report])
            data = {}
            [data.update({i: []}) for i in classes]
            [data[i['class_name']].append(i) for i in report]
        elif self.report_type == 'department':
            departments = set([record['department_name'] for record in report])
            data = {}
            [data.update({i: []}) for i in departments]
            [data[i['department_name']].append(i) for i in report]
        elif self.report_type == 'club':
            clubs = set([record['club_name'] for record in report])
            data = {}
            [data.update({i: []}) for i in clubs]
            [data[i['club_name']].append(i) for i in report]
        else:
            classes = set([record['class_name'] for record in report])
            data = {}
            [data.update({i: []}) for i in classes]
            [data[i['class_name']].append(i) for i in report]
        data = {
            'data_len': len(data),
            'report_type': self.report_type,
            'report': data,
        }
        return self.env.ref('school.school_student_report_action').report_action(self, data=data)

    def action_print_student_report_excel(self):
        """action on printing excel"""
        report = self.fetch_query()
        if self.report_type == 'class':
            classes = set([record['class_name'] for record in report])
            data = {}
            [data.update({i: []}) for i in classes]
            [data[i['class_name']].append(i) for i in report]
        elif self.report_type == 'department':
            departments = set([record['department_name'] for record in report])
            data = {}
            [data.update({i: []}) for i in departments]
            [data[i['department_name']].append(i) for i in report]
        elif self.report_type == 'club':
            clubs = set([record['club_name'] for record in report])
            data = {}
            [data.update({i: []}) for i in clubs]
            [data[i['club_name']].append(i) for i in report]
        else:
            classes = set([record['class_name'] for record in report])
            data = {}
            [data.update({i: []}) for i in classes]
            [data[i['class_name']].append(i) for i in report]
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'student.report.wizard',
                     'options': json.dumps(data, default=str),
                     'applied_on': self.report_type,
                     'output_format': 'xlsx',
                     'report_name': 'Student Report Excel'
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response, applied_on):
        """xlsx workbook"""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        heading = workbook.add_format(
            {'font_size': '11px', 'bold': True, 'font_color': '#FFFFFF', 'align': 'center', 'bg_color': '#000000'})
        current_date = datetime.today().strftime('%Y-%m-%d')
        sheet.merge_range('C3:D4', 'STUDENT REPORT', head)
        sheet.merge_range('A1:C1', self.env.company.name, heading)
        sheet.merge_range('A2:C2', current_date, heading)
        row = 6
        col = 0
        for line in data:
            sheet.set_column('A:A', 20)
            sheet.set_column('B:B', 20)
            sheet.set_column('C:C', 20)
            sheet.set_column('D:D', 20)
            sheet.set_column('E:F', 20)
            sheet.set_column('G:G', 20)
            sheet.set_column('H:H', 20)
            if applied_on == 'class' or applied_on == 'false':
                sheet.write(row - 1, col + 2, 'class', heading)
                sheet.write(row - 1, col + 3, line, heading)
            else:
                sheet.write(row - 1, col + 2, line, heading)
            row += 1
            sheet.write(row, col, 'Serial NO', heading)
            sheet.write(row, col + 1, 'Admission NO', heading)
            sheet.write(row, col + 2, 'Students', heading)
            sheet.write(row, col + 3, 'Department', heading)
            sheet.write(row, col + 4, 'Email', heading)
            row += 1
            serial_no = 1
            for student in data[line]:
                sheet.write(row, col, serial_no, cell_format)
                sheet.write(row, col + 1, student['admission_no'], cell_format)
                sheet.write(row, col + 2, student['first_name'], cell_format)
                sheet.write(row, col + 3, student['department_name'], cell_format)
                sheet.write(row, col + 4, student['email'], cell_format)
                serial_no += 1
                row += 1
            row += 2
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
