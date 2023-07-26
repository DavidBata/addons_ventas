from odoo import models, fields, api
class SaleOrderTakingInventary(models.Model):
    _inherit = 'sale.order'

    
    def register_inventory(self):
        
        return {
        "name":("Toma de Inventario"),
        "res_model": "taking.inventory",
        "view_mode": "form",
        "target": "new",
        "type": "ir.actions.act_window",
        "context": {'default_sale_order_id':self.id,'default_partner_id':self.partner_id.id},
        
        }
