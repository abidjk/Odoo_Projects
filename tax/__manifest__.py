# -*- coding: utf-8 -*-
{
    'name': 'Default Tax',
    'version': '18.0.1.0.0',
    'application': True,
    'depends': [
        'hr', 'base', 'sale'
    ],
    'author': 'Abid',
    'category': 'Sales',
    'summery': 'Default Tax',
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/tax_menu.xml'
    ],

}