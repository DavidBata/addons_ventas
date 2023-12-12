# -*- coding: utf-8 -*-
# from odoo import http


# class ConnnectDbAdempiere(http.Controller):
#     @http.route('/connnect_db_adempiere/connnect_db_adempiere', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/connnect_db_adempiere/connnect_db_adempiere/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('connnect_db_adempiere.listing', {
#             'root': '/connnect_db_adempiere/connnect_db_adempiere',
#             'objects': http.request.env['connnect_db_adempiere.connnect_db_adempiere'].search([]),
#         })

#     @http.route('/connnect_db_adempiere/connnect_db_adempiere/objects/<model("connnect_db_adempiere.connnect_db_adempiere"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('connnect_db_adempiere.object', {
#             'object': obj
#         })
