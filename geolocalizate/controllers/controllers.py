# -*- coding: utf-8 -*-
# from odoo import http


# class Geolocalizate(http.Controller):
#     @http.route('/geolocalizate/geolocalizate', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/geolocalizate/geolocalizate/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('geolocalizate.listing', {
#             'root': '/geolocalizate/geolocalizate',
#             'objects': http.request.env['geolocalizate.geolocalizate'].search([]),
#         })

#     @http.route('/geolocalizate/geolocalizate/objects/<model("geolocalizate.geolocalizate"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('geolocalizate.object', {
#             'object': obj
#         })
