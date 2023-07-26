# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrderInheritRuleVendedorStandar(models.Model):
    _inherit = 'sale.order'

    def import_adempier_salesperson_regular(self):
        for rec in self:
            web_service = self.env['web.service.eng'].search([("code", "=", "IANCARINA_QA")])
            user = self.env.user.login
            ad_client="<_0:field column=\"AD_Client_ID\">\r\n   <_0:val>1000000</_0:val>\r\n</_0:field>\r\n "
            user_admpiere = web_service.consul_user(code=user,ad_client=ad_client, url=web_service.url)
            # raise ValidationError(user_admpiere)  

            # id de partner adempiere
            admpiere_partner_id = web_service.consul_cb_partner(CI=rec.partner_id.vat, url=web_service.url)

            # identificar la direccion de entrega
            direcion_entrega = web_service.direccion_entrega(cb_partner_id=admpiere_partner_id["partner"],name_direccion=rec.partner_id.city.upper(),url=web_service.url)

            # raise ValidationError(direcion_entrega)
            c_order_admpiere = web_service.web_service_c_order(
                    user=user,
                    clave=user,
                    ClientID="1000000",
                    RoleID= user_admpiere["rol_id"],
                    OrgID=user_admpiere["ad_org_id"],
                    WarehouseID=user_admpiere["almacen"],
                    C_BPartner_ID= admpiere_partner_id["partner"],
                    C_Campaign_ID="1000000",
                    C_Project_ID="1000018",
                    M_Warehouse_ID=user_admpiere["almacen"],
                    Description= rec.name +' '+ " Import_Ws -Regular ",
                    C_DocTypeTarget_ID=rec.name_document,
                    AD_Client_ID="1000000",
                    url=web_service.url,
                )
            # raise ValidationError(c_order_admpiere)  
                
            actulizacio=web_service.update_direccion_entrega(order_id=c_order_admpiere[0],C_BPartner_Location_ID=direcion_entrega,url=web_service.url)

            lista_productos_registrados=[]    
      
            for line in rec.order_line:
                QtyEntered= line.product_uom_qty
                PriceEntered=line.price_unit
                PriceActual=line.price_unit
                producto_ad_id=web_service.consul_id_product( code=line.product_id.default_code, url=web_service.url)
                create_order_line = web_service.create_order_line(
                    order_id=c_order_admpiere[0],
                    clave=user,
                    user=user,
                    ClientID="1000000",
                    RoleID=user_admpiere["rol_id"],
                    OrgID=user_admpiere["ad_org_id"],
                    WarehouseID=user_admpiere["almacen"],
                    producto_ad_id= producto_ad_id[0],
                    url=web_service.url,QtyEntered=QtyEntered,PriceEntered=PriceEntered,PriceActual=PriceActual
                )
                record_adempiere= web_service.get_data_response(xml=create_order_line[0])
                lista_productos_registrados.append(record_adempiere[0])
            
            # raise ValidationError(lista_productos_registrados)
            if  len(rec)>=1 and int(lista_productos_registrados[0])>1:
                rec.state="done"
                return {
                    "type": "ir.actions.client",
                    "tag": "display_notification",
                    "params": {
                        "type": "success",
                        "message": ("Las Ordenes Fueron Creadas."),
                        'next': {'type': 'ir.actions.act_window_close'},
                    },
                }
            else:
                raise ValidationError(("Algo Salio Mal, en Las lineas",lista_productos_registrados[0]))
