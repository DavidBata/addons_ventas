
from odoo import models, fields, api

class TakingInventoryLine(models.Model):
    _name = "taking.inventory.line"
    _description = 'line Inventory for partners'

    taking_inventory_id = fields.Many2one(
        string='Inventario',
        comodel_name='taking.inventory',
        ondelete='restrict',
    )
    quantity = fields.Float(
        string='cantidad',
    )
    product_id = fields.Many2one(
        string='product',
        comodel_name='product.product',
        ondelete='restrict',
    )
    medida = fields.Selection(
        string='medida',
        selection=[('kg', 'kgs'), ('bultos', 'bultos'),('unidad', 'Undidades')]
    )
    

