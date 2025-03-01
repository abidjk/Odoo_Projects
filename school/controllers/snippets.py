from odoo import http
from odoo.http import request


class DynamicSnippets(http.Controller):
    """This class is for the getting values for dynamic school event snippets"""

    @http.route('/school_events', type='json', auth='public')
    def school_events(self):
        """Function for getting the School Events
            Return
                  School Events
            """
        school_events = request.env['school.event'].sudo().search_read([],
                                                                       ['name', 'club_id', 'description', 'start_date',
                                                                        'end_date'], order='create_date desc', limit=10)
        return school_events

    @http.route('/event-form/<int:id>', type='http', auth='public', website=True)
    def selected_event(self, id):
        """function for getting the selected event details"""
        selected_event = request.env['school.event'].search([('id', '=', id)])
        return http.request.render('school.selected_event', {'selected_event': selected_event})
