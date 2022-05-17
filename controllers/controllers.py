# -*- coding: utf-8 -*-
# from odoo import http


# class TemplateSa(http.Controller):
#     @http.route('/template_sa/template_sa/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/template_sa/template_sa/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('template_sa.listing', {
#             'root': '/template_sa/template_sa',
#             'objects': http.request.env['template_sa.template_sa'].search([]),
#         })

#     @http.route('/template_sa/template_sa/objects/<model("template_sa.template_sa"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('template_sa.object', {
#             'object': obj
#         })
