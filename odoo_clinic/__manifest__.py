{
    'name': 'Odoo Clinic',
    'version': '18.0',
    'application': True,
    'depends': [
        'hr'
    ],
    'data': [
            'security/ir.model.access.csv',
            'views/op_registration.xml',
            'views/patient_registration.xml',
            'views/clinic_consultation.xml',
            'views/clinic_prescription.xml',
            'data/ir_sequence_data.xml',
            'views/clinic_menu.xml',

        ]
}