# -*- coding: utf-8 -*-
{
    "name": "Freight Management",
    "version": "16.0.1.0.0",
    "summary": "Module for Managing All Frieght Operations",
    "description": "Module for Managing All Frieght Operations",
    "author": "David Edgardo Garcia Bata",
    "maintainer": "David Edgardo Garcia Bata",
    "company": "Iancarina C.A",
    "website": "https://www.alimentosmary.com/iancarina/",
    "depends": ["base", "fleet", "sale"],
    "images": ["static/description/fletes.png"],
    "data": [
        "security/security_acceso.xml",
        "security/ir.model.access.csv",
        "data/freight_order_data.xml",
        "data/data_organizacion.xml",
        # "security/ir_rules.xml",
        # "security/res_grups.xml",
        "report/sale_order.xml",
        
        "views/fleet_vehicle.xml",
        "views/sale_order.xml",
        "views/product_template.xml",
        "views/res_partner.xml",
        "views/res_users.xml",
        "views/menu_sale_order_line.xml",
        "views/sale_order_line.xml",
        "views/web_service.xml",
        "views/freight_order_view.xml",
        "views/back_order.xml",
        "views/organizacion_view.xml",
        "views/c_doctype.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "AGPL-3",
}
