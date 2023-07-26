# -*- coding: utf-8 -*-
{
    'name': "Taking Inventory",

    

    'description': """
        customer inventory load partner
    """,

    'author': "David Bata",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/view_staking_inventory.xml',
        'data/secuencia_taking_inventory.xml',
        'views/sale_order_view.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
