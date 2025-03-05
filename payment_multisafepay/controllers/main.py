import logging
import pprint
from pickle import FALSE

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class MultisafepayController(http.Controller):
    _return_url = '/payment/multisafepay/return'
    # _webhook_url = '/payment/mollie/webhook'

    @http.route(_return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False, save_session=False)
    def multisafepay_return_from_checkout(self, **data):
        _logger.info("handling redirection from Multisafepay with data:\n%s", pprint.pformat(data))
        request.env['payment.transaction'].sudo()._handle_notification_data('multisafepay', data)
        return request.redirect('/payment/status')