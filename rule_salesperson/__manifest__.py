# -*- coding: utf-8 -*-
{
    'name': "Rule Salesperson",

    
    'description': """
    Reglas para vendedor stanar de iancarina
    """,

    'author': "David Bata",
    # 'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        'views/sale_order_view.xml',
        'security/rule_sale_person_regular.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
