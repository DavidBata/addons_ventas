from werkzeug import urls
import requests
import xml.etree.ElementTree as El
from odoo import api, fields, models, _

from odoo.exceptions import ValidationError


class ResPartnerAggSaleOrder(models.Model):
    _inherit = "res.partner"

    canal_sale = fields.Char(
        string="Tipo de Canal", 
        compute="_compute_canal_sale", 
        readonly=True
    )
    
    responsable_id = fields.Many2one(
        'res.users',
        string='responsable',
    )
    
    is_opl = fields.Boolean(
        string='Cliente Opl(Adempiere)', 
        default=False
    )
    
    organizacion_id = fields.Many2one(
        string='Organizacion',
        comodel_name='organizacion.admp',
        store=True
        # ondelete='restrict',
    )
    
    
    
    # types_document = fields.Selection(
    #     # selection=[('1','1')],
    #     selection="_type_documet_fieds",
    #     # compute="_compute_documet_type",
    #     # [("sad","asdas")],
    #     string='Tipos de Docuemntos',
    #     store=True,

    # )
    

    @api.depends("vat")
    def _compute_canal_sale(self):
        for rec in self:
            
            try:
                url = "http://adempiere-engine.iancarina.com.ve/ADInterface/services/ModelADService"
                vat = rec.vat
                payload = f"""<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:_0=\"http://3e.pl/ADInterface\">\r\n   <soapenv:Header/>\r\n   <soapenv:Body>\r\n     <_0:queryData>\r\n       <_0:ModelCRUDRequest>\r\n         <_0:ModelCRUD>\r\n           <_0:serviceType>CanalSales</_0:serviceType>\r\n          <_0:DataRow>\r\n            <_0:field column=\"TaxID\">\r\n                        <_0:val>{vat}</_0:val>\r\n            </_0:field>\r\n          </_0:DataRow>\r\n         </_0:ModelCRUD>\r\n         <_0:ADLoginRequest>\r\n           <_0:user>dGarcia</_0:user>\r\n           <_0:pass>dGarcia</_0:pass>\r\n           <_0:lang>es_VE</_0:lang>\r\n           <_0:ClientID>1000000</_0:ClientID>\r\n           <_0:RoleID>1000000</_0:RoleID>\r\n           <_0:OrgID>0</_0:OrgID>\r\n           <_0:WarehouseID>0</_0:WarehouseID>\r\n           <_0:stage>0</_0:stage>\r\n         </_0:ADLoginRequest>\r\n       </_0:ModelCRUDRequest>\r\n     </_0:queryData>\r\n   </soapenv:Body>\r\n </soapenv:Envelope>"""
                headers = {"Content-Type": "application/xml"}
                response = requests.request("POST", url, headers=headers, data=payload)
                xml = "<?xml version='1.0' encoding='UTF-8'?>" + response.text
                canal_id = rec.env["web.service.eng"].get_data_response(xml=xml)
                if canal_id:
                    id = canal_id[0]
                else:
                    id = ""
                canal = rec.canal_venta(c_chanel=id)
                rec.canal_sale = canal
                
            except :
                rec.canal_sale=" "
                
    def canal_venta(self, c_chanel):
        url = "http://adempiere-engine.iancarina.com.ve/ADInterface/services/ModelADService"

        payload = f"""<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:_0=\"http://3e.pl/ADInterface\">\r\n   <soapenv:Header/>\r\n   <soapenv:Body>\r\n     <_0:queryData>\r\n       <_0:ModelCRUDRequest>\r\n         <_0:ModelCRUD>\r\n           <_0:serviceType>NombreCanalVenta</_0:serviceType>\r\n          <_0:DataRow>\r\n            <_0:field column=\"C_Channel_ID\">\r\n                        <_0:val>{c_chanel}</_0:val>\r\n            </_0:field>\r\n          </_0:DataRow>\r\n         </_0:ModelCRUD>\r\n         <_0:ADLoginRequest>\r\n           <_0:user>dGarcia</_0:user>\r\n           <_0:pass>dGarcia</_0:pass>\r\n           <_0:lang>es_VE</_0:lang>\r\n           <_0:ClientID>1000000</_0:ClientID>\r\n           <_0:RoleID>1000000</_0:RoleID>\r\n           <_0:OrgID>0</_0:OrgID>\r\n           <_0:WarehouseID>0</_0:WarehouseID>\r\n           <_0:stage>0</_0:stage>\r\n         </_0:ADLoginRequest>\r\n       </_0:ModelCRUDRequest>\r\n     </_0:queryData>\r\n   </soapenv:Body>\r\n </soapenv:Envelope>"""
        headers = {"Content-Type": "application/xml"}

        response = requests.request("POST", url, headers=headers, data=payload)
        xml = "<?xml version='1.0' encoding='UTF-8'?>" + response.text
        canal = self.env["web.service.eng"].get_data_response(xml=xml)

        return canal
    
    def type_documet_fieds(self):
        id_focus= self.id_focus()
        # raise ValidationError(id_focus)
        if self.organizacion_id :
            sale_order = self.env['sale.order']
            # raise ValidationError("lista_tipo_cocumento")
            ids_org_client= sale_order.org_cliente_despacho(org_name=self.organizacion_id.name)
            objerto_carga = self.env['web.service.eng']
            orgs = sale_order.consul_user()
            # raise ValidationError(orgs)
            typebase= sale_order.consult_typedocumet_base(name='Sales Order')
            # raise ValidationError(orgs)
            lista_tipo_cocumento = []
            for org in orgs:
                tipo_docuemto =objerto_carga.consul_documet_type(org_id=org, typebase=typebase[0])
                lista_tipo_cocumento.append(tipo_docuemto)
            # raise ValidationError("lista_tipo_cocumento")
            sel = []
            if len(lista_tipo_cocumento) >= 1:
                names = []
                ids = []
                for obj_documnt in lista_tipo_cocumento:
                    select = [(obj_documnt[rec], rec)for rec in obj_documnt]
                    sel += select
                # raise ValidationError(sel)
                for doc in sel:
                    for do in doc:
                        try:
                            i = int(do)
                            if type(i) is int:
                                ids.append(do)
                        except ValueError:
                            names.append(do)
                dic = dict(zip(names, ids))
                field_select = [(dic[x], x)for x in dic]
                
                return field_select
            else:
            # raise ValidationError("Usuario no Posee Organizacion Asignada en Adempiere. o la plataforma de consulta esa caida.") 
                field_select = [(tipo_docuemto[r],r)
                                for r in tipo_docuemto]
            # raise ValidationError(field_select)

                return field_select

    def id_focus(self):
        id = self.id
        return self.id
    def _type_documet_fieds(self):
        if self.organizacion_id != '':
            # raise ValidationError(self.organizacion_id)
            objerto_carga = self.env['web.service.eng']
            sale_order = self.env['sale.order']
            orgs = sale_order.consul_user()
            # id_focus = self.id_focus()
            
            ids_org_client= sale_order.org_cliente_despacho(org_name="VALENCIA")
            # raise ValidationError(orgs)
            typebase= sale_order.consult_typedocumet_base(name='Sales Order')
            # raise ValidationError(ids_org_client)
            lista_tipo_cocumento = []
            for org in ids_org_client:
                tipo_docuemto =objerto_carga.consul_documet_type(org_id=org, typebase=typebase[0])
                lista_tipo_cocumento.append(tipo_docuemto)
            # raise ValidationError(tipo_docuemto)
            sel = []
            # if len(lista_tipo_cocumento) >= 1:
            names = []
            ids = []
            for obj_documnt in lista_tipo_cocumento:

                select = [(obj_documnt[rec], rec)for rec in obj_documnt]
                sel += select
            for doc in sel:
                for do in doc:
                    try:
                        i = int(do)
                        if type(i) is int:
                            ids.append(do)
                    except ValueError:
                        names.append(do)
            dic = dict(zip(names, ids))
            field_select = [(dic[x], x)for x in dic]
            tupla=('holaaaaaaa','siiiiiiiiii')
            field_select.append(tupla)
            # raise ValidationError(field_select)
            return field_select
            
            
            # else:
            #     # raise ValidationError(tipo_docuemto)
            #     field_select = [(tipo_docuemto[r], r)
            #                     for r in tipo_docuemto]
            #     return field_select    
        
            # raise ValidationError("Usuario no Posee Organizacion Asignada en Adempiere. o la plataforma de consulta esa caida.") 
        # if self.organizacion_id :
        #     sale_order = self.env['sale.order']
        #     # raise ValidationError("lista_tipo_cocumento")
        #     ids_org_client= sale_order.org_cliente_despacho(org_name=self.organizacion_id.name)
        #     objerto_carga = self.env['web.service.eng']
        #     orgs = sale_order.consul_user()
        #     # raise ValidationError(orgs)
        #     typebase= sale_order.consult_typedocumet_base(name='Sales Order')
        #     # raise ValidationError(orgs)
        #     lista_tipo_cocumento = []
        #     for org in orgs:
        #         tipo_docuemto =objerto_carga.consul_documet_type(org_id=org, typebase=typebase[0])
        #         lista_tipo_cocumento.append(tipo_docuemto)
        #     # raise ValidationError("lista_tipo_cocumento")
        #     sel = []
        #     if len(lista_tipo_cocumento) >= 1:
        #         names = []
        #         ids = []
        #         for obj_documnt in lista_tipo_cocumento:
        #             select = [(obj_documnt[rec], rec)for rec in obj_documnt]
        #             sel += select
        #         for doc in sel:
        #             for do in doc:
        #                 try:
        #                     i = int(do)
        #                     if type(i) is int:
        #                         ids.append(do)
        #                 except ValueError:
        #                     names.append(do)
        #         dic = dict(zip(names, ids))
        #         field_select = [(dic[x], x)for x in dic]
        #         # raise ValidationError(dic.items())
        #         return field_select
        #     else:
        #     # raise ValidationError("Usuario no Posee Organizacion Asignada en Adempiere. o la plataforma de consulta esa caida.") 
        #         field_select = [(tipo_docuemto[r],r)
        #                         for r in tipo_docuemto]
        #     # raise ValidationError(field_select)

        #         return field_select
        