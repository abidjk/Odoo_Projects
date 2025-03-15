{
    'name': 'Counter',
    'version': '18.0.1.0.0',
    'application': True,
    'depends': [

    ],
    'data': [
     'views/counter_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'counter/static/src/js/counter_calc.js',
            'counter/static/src/js/reset_calc.js',
            'counter/static/src/xml/counter_calc.xml',
            'counter/static/src/xml/reset_calc.xml'
        ],
    },
}