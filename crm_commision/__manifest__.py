# -*- coding: utf-8 -*-
{
    'name': 'CRM Commission',
    'version': '18.0.1.0.0',
    'application': True,
    'depends': [
        'hr', 'base', 'sale'
    ],
    'author': 'Abid',
    'category': 'Sales',
    'summery': 'CRM commission',
    'data': [
        'security/ir.model.access.csv',
        'views/crm_commission_views.xml',
        'views/product_wise_views.xml',
        'views/revenue_wise_views.xml',
        'views/res_users_views.xml',
        'views/crm_team_views.xml',
        # 'views/sale_order_views.xml',
        'data/ir_sequence_data.xml',
        'views/crm_commission_menu.xml',
    ]
}