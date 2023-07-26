# -*- coding: utf-8 -*-
# from odoo import http


# class TakingInventory(http.Controller):
#     @http.route('/taking_inventory/taking_inventory', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/taking_inventory/taking_inventory/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('taking_inventory.listing', {
#             'root': '/taking_inventory/taking_inventory',
#             'objects': http.request.env['taking_inventory.taking_inventory'].search([]),
#         })

#     @http.route('/taking_inventory/taking_inventory/objects/<model("taking_inventory.taking_inventory"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('taking_inventory.object', {
#             'object': obj
#         })
