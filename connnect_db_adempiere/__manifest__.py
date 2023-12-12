# -*- coding: utf-8 -*-
{
    'name': "connnect_db_adempiere",


    'description': """
      Esta aplicacion es una extension para consultas directas adempiere para automatizar mas las consultas
    """,

    'author': "David Bata",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','freight_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/connnect_adempiere.xml',
        'views/freight_order.xml',
        'views/web_service.xml',
        'data/data_db.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
