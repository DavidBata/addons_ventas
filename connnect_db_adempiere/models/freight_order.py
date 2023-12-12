from odoo import models, fields, api,_
from odoo.exceptions import  ValidationError
class InheritFreightOrder(models.Model):

    _inherit = 'freight.order'


    def get_data_info_client (self):
        for rec in self:
            rifs = []
            record = []
            for line in rec.sale_order_line_ids:
                if line.vat not in rifs:
                    # raise ValidationError(line.city)
                    dic= {
                        'rif':line.vat,
                        'direccion' : line.order_partner_id.city
                    }
        return dic
    def get_data_info_user (self):
        for rec in self:
            
            dic = {
                'user': self.env.user.login
            }
        return dic

    def export_other_companies(self):
        for rec in self:
            company_conection= rec.crear_c_order_in_id.connect_adempiere_id.company_id

            connec_db_adempiere = self.env['connnect.adempiere'].search([('company_id','=', company_conection.id)])
            # raise ValidationError(connec_db_adempiere.name)
            cursor=connec_db_adempiere.conection_db(database=connec_db_adempiere.database,
                                            user=connec_db_adempiere.user,
                                            password=connec_db_adempiere.password,
                                            host=connec_db_adempiere.host,port=connec_db_adempiere.port)

            get_data_cliente = rec.get_data_info_client()
            get_data_user=rec.get_data_info_user()
            
            direcion = get_data_cliente['direccion']
            rif = get_data_cliente['rif']
            user = get_data_user['user']

            sql= f'''SELECT cb.c_bpartner_id as c_bpartner_id, 
                    docb.C_DocBaseType_ID tipo_document_base, 
                    loc.name as direccion_entrega,
                    reg.Link_Org_ID as org_id_client, 
                    org.name as org_client,
                    usr."value" as code_usuario,
                    usr.ad_user_id::int as usuario_id,
                    usracc.ad_org_id as org_id_usuario,
                    "numeric"(rol.ad_role_id) as  rol_usuario
                    --almacc as alamecen_usuario


                    --org.ad_org_id as id
                    FROM c_bpartner as cb 
                    LEFT JOIN  C_DocBaseType as docb on docb.name = 'Sales Order'
                    LEFT JOIN  C_BPartner_Location as loc on loc.c_bpartner_id = cb.c_bpartner_id and loc.isactive='Y'
                    LEFT JOIN C_SalesRegion  as reg on reg.C_SalesRegion_ID =loc.c_salesregion_id  

                    LEFT JOIN AD_Org as org on org.isactive='Y' and org.issummary = 'N' and org.ad_org_id = reg.Link_Org_ID

                    LEFT JOIN ad_user as usr on usr.isactive='Y' and usr.value ='DDrosario' 
                    LEFT JOIN AD_User_OrgAccess as usracc on usracc.ad_user_id = usr.ad_user_id and usracc.isactive='Y' and usracc.ad_org_id = reg.Link_Org_ID

                    LEFT JOIN AD_User_Roles as rol on rol.ad_user_id= usr.ad_user_id and rol.isactive='Y'
                    LEFT JOIN ad_role as roles on rol.AD_Role_ID = roles.ad_role_id --and roles.name='Fuerza de Ventas'
                    --left join AD_User_WarehouseAccess as almacc on usr.ad_user_id=almacc.ad_user_id
                    WHERE cb.taxid ='J298287713'-- and loc.name = 'Caracas'
            '''
            # where = "WHERE value like '%24320818%'"
            result =connec_db_adempiere.sql_adempiere(cursor=cursor,sql=sql)
            for x in result: 
                dic={
                    'c_bpartner_id':x[0],
                    'tipo_document_base':x[1],
                    'direccion_entrega':x[2],
                    'org_id_client':x[3],
                    'org_client':x[4],
                    'code_usuario':x[5],
                    'usuario_id':x[6],
                    'org_id_usuario':x[7],
                    'rol_usuario':int(x[8])
                }
        return dic
