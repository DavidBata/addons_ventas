import requests
import xml.etree.ElementTree as El
from werkzeug import urls
from odoo import api, fields, models, _

from odoo.exceptions import ValidationError
import re
# from READONLY_FIELD_STATES import sale


READONLY_FIELD_STATES = {
    state: [('readonly', True)]
    for state in {'sale', 'done', 'cancel','import_salesperson'}
}


class OrderLineFreight(models.Model):
    _inherit = "sale.order"

    delivery_address_id = fields.Many2one(
        "res.partner",
        string="",
        domain="[('type', '=', 'delivery'), ('is_company', '!=', 'is_company'),('user_id','=', user_id)]",
        default=False,
        states=READONLY_FIELD_STATES,
    )
    name_document = fields.Char(string="Tipo/Documento", related='c_doctype_id.c_doctype_id', tracking=True, store=True)
    caleta = fields.Selection(
        [("si", "SI"), ("no", "NO")],  tracking=True, states=READONLY_FIELD_STATES,required=True
    )
    mota_carga = fields.Selection(
        [("si", "SI"), ("no", "NO")],  tracking=True, states=READONLY_FIELD_STATES,required=True
    )

    state = fields.Selection(
        selection=[
            ("draft", "Pedido"),
            ("sent", "Pedido Enviado"),
            ("uploaded", "Pendiente Por Aprobar"),
            ("sale", "Sales Order"),
            ("done", "Locked"),
            ("cancel", "Cancelled"),
            ("import_salesperson", "Importado Vendedor"),
        ],
        tracking=True,
        # states=READONLY_FIELD_STATES,
    )
    canal_sale = fields.Char(
        string="Tipo de Canal",
        related="partner_id.canal_sale",
        store=True,
        readonly=True,

    )

    # document_type = fields.Selection(
    # # selection=[('draft', "draft")],
    # # related='partner_id.types_document',
    # '_okledamos_field',
    # readonly=False,
    # string="Tipo de Documento", store=True, states=READONLY_FIELD_STATES)


    c_doctype_id = fields.Many2one(
        'c.doctype',
        string='Tipo de Documento',
        ondelete='restrict',
        required=True,
        states=READONLY_FIELD_STATES
        
    )
    
    weight_product = fields.Float(
        string='Peso Total',
        compute='_compute_field_order_line_weight'
        
    )
    bultos = fields.Float(
        string='Bultos Totales',
        compute='_compute_field_order_line_weight'
    )
    
    organizacion_id = fields.Many2one(
        string='Organizacion',
        related='partner_id.organizacion_id',
        ondelete='restrict',
        store=True
    )
    
    @api.depends('order_line')
    def _compute_field_order_line_weight(self):
        peso=0
        bultos=0
        for rec in self:
            for line in rec.order_line :
                peso += line.product_template_id.weight * line.product_uom_qty
                bultos+= line.product_uom_qty
            rec.weight_product= peso
            rec.bultos= bultos
        
    def pendiente_aprobar(self):
        """confir Para la aprobacion del Gerente de Vendedor O el Que sea"""
        for rec in self:
            if (not rec.partner_id or len(rec.order_line) < 1):
                raise ValidationError(
                    _(
                        "Para Confirmar tu Pedido, debe Tener, Lineas De Producto, Direccion de entrega y Cliente"
                    )
                )
            else:
                rec.state = "uploaded"

    def pedir_autorizacion(self):
        # for rec in self:
        #     product_ids = []
        #     for order_line in rec.order_line:
        #         sale_price = order_line.product_template_id.list_price_limit
        #         if order_line.price_unit < sale_price:
        #             product_ids.append(order_line.product_template_id.name)
        #         if len(product_ids) > 0:
        #             raise ValidationError(
        #                 "El Precio Del Producto, No esta Permitido, Comunique con su Superior y que el Confirme Este Pedido"
        #             )
            
            self.action_confirm()

    def consul_user(self):
        recordpro = self.env["web.service.eng"].search(
            [("code", "=", "IANCARINA C.A_QA")]
        )
        code = self.env.user.login

        url = recordpro.url

        payload = f"""<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:_0=\"http://3e.pl/ADInterface\">\r\n   <soapenv:Header/>\r\n   <soapenv:Body>\r\n     <_0:queryData>\r\n       <_0:ModelCRUDRequest>\r\n         <_0:ModelCRUD>\r\n           <_0:serviceType>ConsulUsuario</_0:serviceType>\r\n          <_0:DataRow>\r\n            <_0:field column=\"Value\">\r\n                        <_0:val>{code}</_0:val>\r\n            </_0:field>\r\n          </_0:DataRow>\r\n         </_0:ModelCRUD>\r\n         <_0:ADLoginRequest>\r\n           <_0:user>dGarcia</_0:user>\r\n           <_0:pass>dGarcia</_0:pass>\r\n           <_0:lang>es_VE</_0:lang>\r\n           <_0:ClientID>1000000</_0:ClientID>\r\n           <_0:RoleID>1000000</_0:RoleID>\r\n           <_0:OrgID>0</_0:OrgID>\r\n           <_0:WarehouseID>0</_0:WarehouseID>\r\n           <_0:stage>0</_0:stage>\r\n         </_0:ADLoginRequest>\r\n       </_0:ModelCRUDRequest>\r\n     </_0:queryData>\r\n   </soapenv:Body>\r\n </soapenv:Envelope>"""
        headers = {"Content-Type": "application/xml"}

        response = requests.request("POST", url, headers=headers, data=payload)

        xml = "<?xml version='1.0' encoding='UTF-8'?>" + response.text

        doc_xml = El.fromstring(xml)
        doc_xml.items()
        print(doc_xml.items)
        data_cbpart = []
        dic = {}
        cont = 0
        for x in doc_xml.iter():
            # print(x.attrib)
            if x.attrib and len(x.attrib) <= 2:
                data_cbpart.append(x.attrib)
            cont = 0
            lista = []
        for part in data_cbpart:
            for cont, value in part.items():
                dic = {
                    cont: value,
                }
            for valida in dic.values():
                lista.append(valida)

        lista.sort()
        # raise ValidationError(lista)
        objerto_carga = self.env["web.service.eng"]
        org_user = objerto_carga.consul_organiz_user_acc(org_acc=lista[0], url=url)
        return org_user
    # @api.onchange('pricelist_id')
    def id_price_list(self):
        if self.pricelist_id:
            for rec in self:
                if rec.pricelist_id :    
                    web_service = self.env['web.service.eng'].search([])
                    id_lista_precio = web_service.lista_precio(price_list=rec.pricelist_id.name)
        id_list =id_lista_precio[0]        
        # raise ValidationError(id_lista_precio)
        return id_list
    @api.onchange('order_line.product_id')
    def onchange_product_template_id(self):
        strin = " - "
        web_service = self.env['web.service.eng'].search([])
        if self.order_line.product_template_id:
            lista_code_pr=[]
            indice = self.product_template_id.name.find(strin)
            lista_code_pr.append(self.product_template_id.name[:indice])
            # line.product_template_id.name 
            id_product= web_service.consul_id_product(codigos=lista_code_pr)
            raise ValidationError(id_product)
            
            
            
    def code_product (self, product):
        lista_produdctos_registrados = []
        lista_code_pr = []
        strin = " - "
        indice = product.find(strin)
        lista_code_pr.append(product[:indice])
        return lista_code_pr
        
    
    def consult_typedocumet_base(self, name):
        url = "http://adempiere-engine.iancarina.com.ve/ADInterface/services/ModelADService"

        payload = f"""<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:_0=\"http://3e.pl/ADInterface\">\r\n   <soapenv:Header/>\r\n   <soapenv:Body>\r\n     <_0:queryData>\r\n       <_0:ModelCRUDRequest>\r\n         <_0:ModelCRUD>\r\n           <_0:serviceType>TypeDocumentBase</_0:serviceType>\r\n          <_0:DataRow>\r\n            <_0:field column=\"Name\">\r\n                        <_0:val>{name}</_0:val>\r\n            </_0:field>\r\n          </_0:DataRow>\r\n         </_0:ModelCRUD>\r\n         <_0:ADLoginRequest>\r\n           <_0:user>dGarcia</_0:user>\r\n           <_0:pass>dGarcia</_0:pass>\r\n           <_0:lang>es_VE</_0:lang>\r\n           <_0:ClientID>1000000</_0:ClientID>\r\n           <_0:RoleID>1000000</_0:RoleID>\r\n           <_0:OrgID>0</_0:OrgID>\r\n           <_0:WarehouseID>0</_0:WarehouseID>\r\n           <_0:stage>0</_0:stage>\r\n         </_0:ADLoginRequest>\r\n       </_0:ModelCRUDRequest>\r\n     </_0:queryData>\r\n   </soapenv:Body>\r\n </soapenv:Envelope>"""
        headers = {"Content-Type": "application/xml"}
        response = requests.request("POST", url, headers=headers, data=payload)
        xml = "<?xml version='1.0' encoding='UTF-8'?>" + response.text
        typebase = self.env["freight.order"].get_data_response(xml=xml)
        # raise ValidationError(typebase)        
        return typebase

    def org_cliente_despacho(self,org_name):

        url = "http://adempiere-engine.iancarina.com.ve/ADInterface/services/ModelADService"
        payload = f"""<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:_0=\"http://3e.pl/ADInterface\">\r\n   <soapenv:Header/>\r\n   <soapenv:Body>\r\n     <_0:queryData>\r\n       <_0:ModelCRUDRequest>\r\n         <_0:ModelCRUD>\r\n           <_0:serviceType>consul_organiz_user_acc</_0:serviceType>\r\n          <_0:DataRow>\r\n <_0:field column=\"IsActive\">\r\n                        <_0:val>Y</_0:val>\r\n            </_0:field>\r\n            <_0:field column=\"Name\">\r\n                        <_0:val>{org_name}</_0:val>\r\n            </_0:field>\r\n          </_0:DataRow>\r\n         </_0:ModelCRUD>\r\n         <_0:ADLoginRequest>\r\n           <_0:user>dGarcia</_0:user>\r\n           <_0:pass>dGarcia</_0:pass>\r\n           <_0:lang>es_VE</_0:lang>\r\n           <_0:ClientID>1000000</_0:ClientID>\r\n           <_0:RoleID>1000000</_0:RoleID>\r\n           <_0:OrgID>0</_0:OrgID>\r\n           <_0:WarehouseID>0</_0:WarehouseID>\r\n           <_0:stage>0</_0:stage>\r\n         </_0:ADLoginRequest>\r\n       </_0:ModelCRUDRequest>\r\n     </_0:queryData>\r\n   </soapenv:Body>\r\n </soapenv:Envelope>"""
        headers = {"Content-Type": "application/xml"}

        response = requests.request("POST", url, headers=headers, data=payload)

        xml = "<?xml version='1.0' encoding='UTF-8'?>" + response.text

        doc_xml = El.fromstring(xml)
        doc_xml.items()
        # print(doc_xml.iter)
        data_cbpart = []
        dic = {}
        cont = 0
        for x in doc_xml.iter():
            # print(x.attrib)
            if x.attrib and len(x.attrib) <= 2:
                data_cbpart.append(x.attrib)
            cont = 0
            lista = []
        for part in data_cbpart:
            for cont, value in part.items():
                dic = {
                    cont: value,
                }

            for valida in dic.values():
                lista.append(valida)
        # raise ValidationError(response.text) 
        return lista

   
    

    
    # @api.depends('partner_id','organizacion_id')
    # def _compute_documet_type(self):
    #     if self.partner_id:
    #         for rec in self:
    #             rec.document_type_dev=self._okledamos_field()
    
    # @api.onchange('partner_id','document_type')
    # def field_select_onchange_partner_id(self):
    #     if self.partner_id  :
    #         self._okledamos_field()
    #         # self.document_type.

    @api.depends('partner_id')
    def _relo_document_type(self):
        if self.partner_id  :
            self._okledamos_field()
    
   

     

    # @api.onchange('c_doctype_id')
    # def onchange_document_type(self):
    #     for rec in self:
    #         if rec.c_doctype_id:
    #             rec.name_document = rec.c_doctype_id.c_doctype_id


    # @api.constrains('document_type')
    # def _check_document_type_false(self):
    #     for rec in self:
    #         if rec.document_type:
    #             rec.name_document = rec.document_type
    #             rec.document_type = False
    # hago el calculo para el precio



    # @api.onchange('order_line')
    # def onchange_standard_price(self):
    #     for rec in self:
    #         for line in rec.order_line:
    #             intems=[]

    #             vals = {
    #                 'costo_unit' : line.price_unit/line.unidad_bulto
    #             }
    #             intems.append(0,0,vals)
    #             # line.costo_unit=line.price_unit/line.unidad_bulto



    # Esta Funcion Estara de Prueba Comentada Para el Campo select document_type 
    # no se va usar Por ahora
    def _okledamos_field(self):
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