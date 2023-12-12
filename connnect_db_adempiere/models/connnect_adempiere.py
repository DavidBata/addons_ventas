from odoo import models, fields, api,_
import psycopg2
class ConnnectDBAdempiere(models.Model):
    _name = 'connnect.adempiere'
    # _description = ''



    name = fields.Char(
        string='Name',
    )
    description = fields.Text(
        string='Description',
    )
    
    database = fields.Char(
        string='Base de Datos',
    )
    user = fields.Char(
        string='Usuario',
    )
    password = fields.Char("Password")
    
    
    host = fields.Char(
        string='host',
    )
    
    port = fields.Char(
        string='port',
    )

    
    code = fields.Char(
        string='code',
        compute='_value_code' 
    )
    
    company_id = fields.Many2one(
        string='Company', 
        comodel_name='res.company', 
        required=True, 
        default=lambda self: self.env.user.company_id
    )
    

    @api.depends('company_id')
    def _value_code(self):
        for record in self:
            record.code = record.company_id.name+"Code"


       
    def conection_db (self,database,user,password,host,port):
        con = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = con.cursor()
        return cursor

    def sql_adempiere(self, cursor,sql,where=""):
        cursor.execute(sql +" "+ where)
        result = cursor.fetchall()
        return result 

 