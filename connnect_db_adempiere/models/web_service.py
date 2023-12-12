
from odoo import models, fields, api,_
from odoo.exceptions import  ValidationError

class InheritWebService(models.Model):
    _inherit = 'web.service.eng'
    
    connect_adempiere_id = fields.Many2one(
        string='Coneccion Adempiere',
        comodel_name='connnect.adempiere',
        ondelete='restrict',
        domain="[('company_id','=',company_id)]"
    )
    
    def botonnn(self):    
        iancarina_adem = self.env["connnect.adempiere"].search([("company_id.name","=","IANCARINA")])

        cursor = iancarina_adem.conection_db(database=iancarina_adem.database,
                                            user=iancarina_adem.user,
                                            password=iancarina_adem.password,
                                            host=iancarina_adem.host,port=iancarina_adem.port)
        sql= "SELECT name, value FROM c_bpartner"
        where = "WHERE value like '%24320818%'"
        result =iancarina_adem.sql_adempiere(cursor=cursor,sql=sql,where=where)
        raise ValidationError(result)
     
    def consult_intancia_atribute_id(self,product_id,price_list_id,conection):

        iancarina_adem = self.env["connnect.adempiere"].search([("code","=",conection)])

        cursor = iancarina_adem.conection_db(database=iancarina_adem.database,
                                            user=iancarina_adem.user,
                                            password=iancarina_adem.password,
                                            host=iancarina_adem.host,port=iancarina_adem.port)
        sql=f'''SELECT listp.m_pricelist_id,listp.name,listv.m_pricelist_version_id,ppro.M_Product_ID, ppro.M_AttributeSetInstance_ID,matt.description
                FROM M_PriceList as listp
                JOIN M_PriceList_Version as listv on listv.m_pricelist_id = listp.m_pricelist_id
                JOIN (SELECT "max"(w.ValidFrom) as datev, w.m_pricelist_id  FROM M_PriceList_Version as w where w.m_pricelist_id = {price_list_id} GROUP BY w.m_pricelist_id) as date_version  on date_version.datev::DATE = listv.ValidFrom::DATE and listp.m_pricelist_id=date_version.m_pricelist_id
                JOIN M_ProductPrice as ppro on ppro.M_PriceList_Version_id = listv.M_PriceList_Version_id
                JOIN M_AttributeSetInstance as matt on matt.M_AttributeSetInstance_id=ppro.M_AttributeSetInstance_id
                WHERE ppro.M_Product_ID = {product_id}
                GROUP BY listp.m_pricelist_id,listp.name,listv.m_pricelist_version_id,ppro.M_Product_ID,ppro.M_AttributeSetInstance_ID,matt.description'''
        result =iancarina_adem.sql_adempiere(cursor=cursor,sql=sql)  

        # raise ValidationError(type(str(result[0][4])))
        atribute_instance_id = int(result[0][4])
        return str(atribute_instance_id)
    