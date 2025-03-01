{
    'name': 'Product Details',
    'version': '18.0.1.0.0',
    'application': True,
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'views/product_product_views.xml',
        ],
    'assets': {
        'point_of_sale._assets_pos': [
                    'product_details/static/src/**/*',
                ],
        },
}