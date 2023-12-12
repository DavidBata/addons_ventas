from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class CDocumentType(models.Model):
    _name = "c.doctype"
    
    _description = "Type Document"



    name = fields.Char(
        string='Nombre')

    c_doctype_id = fields.Char(
        string='Ref. adempiere')
    
    organizacion_id = fields.Many2one(
        string='Organizacion',
        comodel_name='organizacion.admp',
        ondelete='restrict',
    )
    