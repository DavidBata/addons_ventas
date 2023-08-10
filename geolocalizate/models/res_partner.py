# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class ResPartnerGeolicalizate(models.Model):
    _inherit = 'res.partner'

    gelocalizate = fields.Char(
        string='gelocalizate',
    )
    
        
    def geolocalizateme(self,geo=''):
        self.gelocalizateee(geo=geo)
        msg="ok"
        return msg
  
        
    def gelocalizateee(self,geo=False):
        if geo:
            geoloca=""
            for x in geo:
                geoloca += x
            self.gelocalizate= geoloca
        else:
            self.gelocalizate=str(geo)