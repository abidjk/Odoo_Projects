{
    'name': 'Payment Provider: Multisafepay',
    'version': '2.0',
    'category': 'Accounting/Payment Providers',
    # 'sequence': 350,
    # 'summary': "A Dutch payment provider covering Europe and the US.",
    # 'description': " ",  # Non-empty string to avoid loading the README file.
    'depends': ['payment'],
    'data': [
        # 'views/payment_adyen_templates.xml',
        'views/payment_multisafepay_templates.xml',
        'views/payment_provider_views.xml',
        'data/payment_provider_data.xml',
        'data/payment_method_data.xml',

        # 'wizards/payment_capture_wizard_views.xml',
    ],
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
    # 'assets': {
    #     'web.assets_frontend': [
    #         'payment_adyen/static/src/js/payment_form.js',
    #     ],
    # },
    # 'license': 'LGPL-3',
}