{
    'name': 'Payment Provider: Multisafepay',
    'version': '2.0',
    'category': 'Accounting/Payment Providers',
    'depends': ['payment'],
    'data': [
        'views/payment_multisafepay_templates.xml',
        'views/payment_provider_views.xml',
        'data/payment_provider_data.xml',
        'data/payment_method_data.xml',
    ],
}