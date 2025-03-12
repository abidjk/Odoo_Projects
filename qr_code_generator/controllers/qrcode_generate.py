# -*- coding: utf-8 -*-
# import base64
import base64
from io import BytesIO
import qrcode

from odoo import http


class QrCodeController(http.Controller):
    """QR Code generator"""

    @http.route('/get/qr', type='json', auth='public')
    def compute_qr_code(self, text):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        print(img)
        # qr_image = base64.b64encode(temp.getvalue()).decode("utf-8")
        return {'qr_image': img}
