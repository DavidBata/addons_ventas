# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class ResPartnerGeolicalizate(models.Model):
    _inherit = 'res.partner'

    gelocalizate = fields.Char(
        string='gelocalizate',
    )
    
    def geolocalizate(self):

        raise ValidationError('geolocalizate')
        # return self.gelocalizat