import requests
import xml.etree.ElementTree as El
from werkzeug import urls
from odoo import api, fields, models, _

from odoo.exceptions import ValidationError
import re

class OrganizationAdmpiere(models.Model):
    _name = "organizacion.admp"

    
    name = fields.Char(
        string='Sucursal',
    )
    
    country_id = fields.Many2one(
        string='Pais',
        comodel_name='res.country',
        ondelete='restrict',
    )

    
    stated_id = fields.Many2one(
        string='Estado',
        comodel_name='res.country.state',
        ondelete='restrict',
    )
    
    


