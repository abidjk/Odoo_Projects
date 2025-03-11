# -*- coding: utf-8 -*-
from odoo import models,fields
try:
  import qrcode
except ImportError:
  qrcode = None
try:
  import base64
except ImportError:
  base64 = None
from io import BytesIO
class QrcodeGenerate(models.Model):
    _name = 'qrcode.generate'

    qr_code = fields.Binary("QR Code", compute='compute_qr_code')
    text = fields.Text()

    def compute_qr_code(self):
        for rec in self:
            if qrcode and base64:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=3,
                    border=4,
                )
                qr.add_data(rec.name)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                rec.update({'qr_code': qr_image})