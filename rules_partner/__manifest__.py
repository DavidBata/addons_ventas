
{
    'name': 'Reglas Partner',
    'version': '1.0',
    'summary': 'rules partner',
    'description': """
    Reglas para los partner solo vista de su comercial
    """,
    'depends': ['base','freight_management'],
    'data': [
        'views/search_res_partner.xml',
        'security/rules_groups.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
