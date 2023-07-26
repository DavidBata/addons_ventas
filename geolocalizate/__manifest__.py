# -*- coding: utf-8 -*-
{
    'name': "Gelocalization partner and sale ",

    'description': """
        Geolocalization partner and sale, used for displaying information gelocalization
    """,
    'author': "David Bata",
    'category': 'Uncategorized',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base'],


    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        # 'views/templates.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'geolocalizate/static/src/js/geolocalizate.js',
        ],
        
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
