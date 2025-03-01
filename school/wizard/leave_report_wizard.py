import io
import json
import xlsxwriter
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, Command, _
import datetime
from datetime import datetime


class LeaveReport(models.TransientModel):
    """this model is used for leave report"""
    _name = "leave.report.wizard"
    _description = "Leave Report"

    report_type = fields.Selection(
        selection=[('month', 'Month'), ('week', 'Week'), ('day', 'Day'), ('custom', 'Custom')])
    from_date = fields.Date()
    to_date = fields.Date()
    applied_on = fields.Selection(selection=[('class', 'Class'), ('student', 'Student')])
    class_ids = fields.Many2many("school.class")
    student_ids = fields.Many2many("school.students")

    def fetch_query(self):
        """fetching the required query"""
        query = """select student_id,first_name,start_date,end_date,school_leave.class_id,total_days,reason,res_company.name as school_name,school_class.name as class_name from school_leave
                inner join school_class on school_leave.class_id=school_class.id
                inner join school_students on school_leave.student_id=school_students.id
                inner join res_company on school_students.school_id=res_company.id
                """
        if self.report_type == 'month':
            start_day = (datetime.now().strftime('%Y-%m-01'))
            end_day = ((datetime.now() + relativedelta(months=1)).strftime('%Y-%m-01'))
            query += """where start_date >= '%s' AND end_date < '%s'""" % (start_day, end_day)
        elif self.report_type == 'week':
            start_day = (datetime.today() - relativedelta(weeks=1, weekday=0)).strftime('%Y-%m-%d')
            end_day = (datetime.now() + relativedelta(weeks=0, weekday=-7)).strftime('%Y-%m-%d')
            query += """where start_date >= '%s' AND end_date < '%s'""" % (start_day, end_day)
        elif self.report_type == 'day':
            start_day = datetime.now().strftime('%Y-%m-%d')
            end_day = datetime.now().strftime('%Y-%m-%d')
            query += """where start_date <= '%s' AND end_date >= '%s'""" % (start_day, end_day)
        elif self.report_type == 'custom':
            if self.from_date and self.to_date:
                query += """where start_date >= '%s' AND end_date <= '%s'""" % (self.from_date, self.to_date)
            elif self.from_date and not self.to_date:
                query += """where start_date >= '%s' OR end_date >= '%s'""" % (self.from_date, self.from_date)
            elif self.to_date and not self.from_date:
                query += """where start_date <= '%s' OR end_date <= '%s'""" % (self.to_date, self.to_date)
            else:
                query += """"""
        else:
            query += """"""
        if self.applied_on == 'class':
            if len(tuple(self.class_ids.ids)) == 1:
                query += f"""and school_leave.class_id = {self.class_ids.id}"""
            elif len(tuple(self.class_ids.ids)) > 1:
                query += f"""and school_leave.class_id IN {tuple(self.class_ids.ids)}"""
            else:
                query += """"""
        elif self.applied_on == 'student':
            if len(tuple(self.student_ids.ids)) == 1:
                query += f"""and school_leave.student_id = {self.student_ids.id}"""
            elif len(tuple(self.student_ids.ids)) > 1:
                query += f"""and school_leave.student_id IN {tuple(self.student_ids.ids)}"""
            else:
                query += """"""
        else:
            query += """"""
        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()

    def action_print_leave_report(self):
        """action on printing report"""
        report = self.fetch_query()
        if self.applied_on == 'student':
            students = set([record['first_name'] for record in report])
            data = {}
            [data.update({i: []}) for i in students]
            [data[i['first_name']].append(i) for i in report]
        elif self.applied_on == 'class':
            classes = set([record['class_name'] for record in report])
            data = {}
            [data.update({i: []}) for i in classes]
            [data[i['class_name']].append(i) for i in report]
        else:
            classes = set([record['class_name'] for record in report])
            data = {}
            [data.update({i: []}) for i in classes]
            [data[i['class_name']].append(i) for i in report]
        data = {
            'data_len': len(data),
            'applied_on': self.applied_on,
            'report': data,
        }
        return self.env.ref('school.school_leave_report_action').report_action(self, data=data)

    def action_print_leave_report_excel(self):
        """action on printing excel"""
        report = self.fetch_query()
        if self.applied_on == 'student':
            students = set([record['first_name'] for record in report])
            data = {}
            [data.update({i: []}) for i in students]
            [data[i['first_name']].append(i) for i in report]
        elif self.applied_on == 'class':
            classes = set([record['class_name'] for record in report])
            data = {}
            [data.update({i: []}) for i in classes]
            [data[i['class_name']].append(i) for i in report]
        else:
            classes = set([record['class_name'] for record in report])
            data = {}
            [data.update({i: []}) for i in classes]
            [data[i['class_name']].append(i) for i in report]
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'leave.report.wizard',
                     'options': json.dumps(data, default=str),
                     'applied_on': self.applied_on,
                     'output_format': 'xlsx',
                     'report_name': 'Leaves Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response, applied_on):
        """odoo workbook"""
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
        sheet.merge_range('C3:D4', 'LEAVE REPORT', head)
        sheet.merge_range('A1:C1',self.env.company.name, heading)
        sheet.merge_range('A2:C2',current_date, heading)
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
                sheet.write(row - 1, col + 2, 'Class', heading)
                sheet.write(row - 1, col + 3, line, heading)
            else:
                sheet.write(row - 1, col + 2, line, heading)
            row += 1
            sheet.write(row, col, 'Serial NO', heading)
            sheet.write(row, col + 1, 'Students', heading)
            sheet.write(row, col + 2, 'From', heading)
            sheet.write(row, col + 3, 'To', heading)
            sheet.write(row, col + 4, 'Days', heading)
            sheet.write(row, col + 5, 'Reason', heading)
            row += 1
            serial_no = 1
            for student in data[line]:
                sheet.write(row, col, serial_no, cell_format)
                sheet.write(row, col + 1, student['first_name'], cell_format)
                sheet.write(row, col + 2, student['start_date'], cell_format)
                sheet.write(row, col + 3, student['end_date'], cell_format)
                sheet.write(row, col + 4, student['total_days'], cell_format)
                sheet.write(row, col + 5, student['reason'], cell_format)
                serial_no += 1
                row += 1
            row += 2
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
