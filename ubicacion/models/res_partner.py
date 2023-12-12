from odoo import models, fields, api

from odoo.exceptions import UserError, ValidationError



class ResPartner(models.Model):
    _inherit = 'res.partner'

    
   
    ubicacion = fields.Char()
   
    