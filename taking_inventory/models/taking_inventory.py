# -*- coding: utf-8 -*-


from odoo import models, fields, api

class TakingInventory(models.Model):
    _name = "taking.inventory"
    _description = 'Inventory for partners'




    
    name = fields.Char()
    taking_inventory_line_ids = fields.One2many('taking.inventory.line', 'taking_inventory_id', string="Lineas Product")
    
    partner_id = fields.Many2one(
        string='Cliente',
        comodel_name='res.partner',
        ondelete='restrict',
        required=True,
        readonly=True
        # compute="_compute_partner_id",
    )
    inventory_date = fields.Date(
        string='Fecha de Inventario',
        default=fields.Date.context_today,
    )
    
    sale_order_id = fields.Many2one(
        string='Order Pedido',
        comodel_name='sale.order',
        ondelete='restrict',
        required=True,
        readonly=True
    )

    description = fields.Text()


    @api.model
    def create(self, vals):
        """Create Sequence"""
        sequence_code = "taking.inventory.sequence"
        vals["name"] = self.env["ir.sequence"].next_by_code(sequence_code)
        return super(TakingInventory, self).create(vals)
    

    
    