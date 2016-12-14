# -*- coding: utf-8 -*-
######################################################################################################################################################
#  @version     : 1.0                                                                                                                                #
#  @autor       : SUPERMAS-ARC                                                                                                                       #
#  @creación    : 2015-09-10                                                                                                                         #
#  @linea       : Maximo 150 chars                                                                                                                   #
######################################################################################################################################################
import time
from datetime import date
from openerp.report import report_sxw
from openerp.osv import osv
from openerp import pooler

class move_stock_user(report_sxw.rml_parse):
  #variable que define al reporte
  _name = "move_stock_user"
  _description = "stock movimientos"

  #######################################################################################################################
  #                                Metodos Privados (Independientes al API de OpenERP)                                  #
  ####################################################################################################################### 
  #----------------------------------------------------------------------------------------------------------------------
  def __init__( self, cr, uid, name, context = None ) :
    """
    Método "__init__" para instanciar objetos a partir de esta clase y pasar de formato rml a pdf
    * Argumentos OpenERP: [cr, uid, ids, name, context]	
    """
    if context is None:
      context = {}
    super( move_stock_user, self ).__init__( cr, uid, name, context = context )
    self.localcontext.update({
      'time': time,
      'nombre_mes': self.nombre_mes,
      'get_datos': self.get_datos,
    })
    self.context = context
    
  #----------------------------------------------------------------------------------------------------------------------
  def nombre_mes( self, data ) :
    """
    Método que obtiene el nombre del reporte
    @return (str)
    """        
    mes=''
    nombre_mes=''
    codigo=''
    Mes = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
            "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    if data.get('form', False) and data['form'].get('month', False):
        mes=int(data['form'].get('month',False))
        nombre = 'del Mes de ' + str(Mes[mes-1]) 
    if data.get('form', False) and data['form'].get('ean13', False):
        codigo=int(data['form'].get('ean13',False))
        nombre = nombre + ' del Producto con codigo ' + str(codigo)

    return nombre   

  #----------------------------------------------------------------------------------------------------------------------
  def get_datos(self, data) :
    
    current_date=date.today()
    year=str(current_date.year)
    self.query = ""
    fecha=''
    mes=''
    day=''
    ean=''
    resultado =''
    
    if data.get('form', False) and data['form'].get('ean13', False):
      ean=data['form'].get('ean13',False)
      self.query = self.query + "p.ean13='"+ean+"'"
      if data.get('form', False) and data['form'].get('select_option', False):
         opcion=data['form'].get('select_option', False)
         if opcion == 'x_month':
            if data.get('form', False) and data['form'].get('month', False):
              mes=data['form'].get('month',False)
      
              if data.get('form', False) and data['form'].get('year_previous', False):
                year_bool = data['form'].get('year_previous',False)
                print year_bool
                if year_bool==False :
                  year=current_date.year
                else:
                  year=current_date.year -1
     
              self.query = self.query + " and TO_CHAR(s.create_date,'YYYY-MM')='"+str(year)+"-"+str(mes)+"'"
        
         if opcion == 'x_day':  
            if data.get('form', False) and data['form'].get('date_now', False):
               day=data['form'].get('date_now',False)
               # print day
               self.query = self.query + " and TO_CHAR(s.create_date,'YYYY-MM-DD')='"+str(day)+"'"   
               # print self.query
      #consulta a la base de datos
      self.cr.execute(
        """
        SELECT
        TO_CHAR(s.create_date,'DD-MM-YYYY') AS fecha_creacion,
        pa.name AS name_login,
        s.name AS name_move, 
        s.picking_id AS referencia,
        s.origin AS origen,
        p.name_template AS producto,
        s.product_qty AS cantidad,
        p.ean13 AS ean, 
        l.complete_name AS localizacion,
        ls.complete_name AS destino,
        CASE WHEN s.state='done' THEN 'Realizado'
             WHEN s.state='assigned' THEN 'Reservado'
             WHEN s.state='confirmed' THEN 'Confirmado'
             WHEN s.state='waiting' THEN 'Esperando'
             WHEN s.state='cancel' THEN 'Cancelado'
             ELSE 'Nuevo'
        END As estado
        from stock_move s
        INNER JOIN product_product p
        ON s.product_id = p.id
        INNER JOIN res_users u
        ON s.create_uid = u.id
        INNER JOIN res_partner pa
        ON u.partner_id = pa.id
        INNER JOIN stock_location l
        ON s.location_id = l.id
        INNER JOIN stock_location ls
        ON s.location_dest_id = ls.id
        WHERE 
        %s
        ORDER BY s.create_date
        """%(self.query,)
      )
      resultado = self.cr.dictfetchall()
      if ( len( resultado ) > 0 ):
        return resultado
      else:
        return { 'value' : {} }
    else:
        return { 'value' : {} }  

#########################################################################################################################
#------------------------------------------------------------------------------------------------------------------------
report_sxw.report_sxw('report.move_stock_user',
                      'stock.move',
                      'addons/sm_reports/move_stock_user/report/move_stock_user.rml',
                      parser = move_stock_user,
                      header=False
                      )