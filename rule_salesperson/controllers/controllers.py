# -*- coding: utf-8 -*-
# from odoo import http


# class RuleSalesperson(http.Controller):
#     @http.route('/rule_salesperson/rule_salesperson', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rule_salesperson/rule_salesperson/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rule_salesperson.listing', {
#             'root': '/rule_salesperson/rule_salesperson',
#             'objects': http.request.env['rule_salesperson.rule_salesperson'].search([]),
#         })

#     @http.route('/rule_salesperson/rule_salesperson/objects/<model("rule_salesperson.rule_salesperson"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rule_salesperson.object', {
#             'object': obj
#         })
