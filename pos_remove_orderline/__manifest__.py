{
    'name': 'Pos Orderline Remove',
    'version': '18.0.1.0.0',
    'application': True,
    'depends': [
        'point_of_sale',
    ],
    'data': [

        ],
    'assets': {
        'point_of_sale._assets_pos': [
                    'pos_remove_orderline/static/src/**/*',
                ],
        },
}