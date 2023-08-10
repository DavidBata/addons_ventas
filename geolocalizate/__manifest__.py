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
    'depends': ['base','web'],


    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/res_partner_views.xml',
        'views/res_partner_views.xml',
        # 'views/templates.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'geolocalizate/static/src/js/geolocalizate.js',
            'geolocalizate/static/src/js/res_partner_form_view.xml',
            
            
        ],
        
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
