# -*- coding: utf-8 -*-
######################################################################################################################################################
#  @version     : 1.0                                                                                                                                #
#  @autor       : Alicia Romero                                                                                                                       #
#  @creación    : 2015-11-18                                                                                                                         #
#  @linea       : Maximo 150 chars                                                                                                                   #
######################################################################################################################################################

import time
from datetime import date
from openerp.report import report_sxw
from openerp.osv import osv
from openerp import pooler

class reporte_bancoo(report_sxw.rml_parse):
  #variable que define al reporte
  _name = "reporte_bancoo"
  _description = "Reporte Banco de Alimentos"

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
    super( reporte_bancoo, self ).__init__( cr, uid, name, context = context )
    self.localcontext.update({
      'time': time,
      'nombre_reporte': self.nombre_reporte,
      'clave_registro':self.clave_registro,
      'get_datos_merma': self.get_datos_merma,
      'fecha_mov':self.fecha_mov,
      'realizo':self.realizo,
      'get_sumas_merma' : self.get_sumas_merma,
      
      
    })
    self.context = context
  #----------------------------------------------------------------------------------------------------------------------
  def get_datos_merma( self, data ):
    id_control_merma=0
    if data.get('form', False) and data['form'].get('id', False):
      id_control_merma = int(data['form'].get('id',False))
      self.cr.execute(
        """
        SELECT m.clave_numer,
        s.clave_ide AS clave, 
        s.fecha_creacion AS fecha_creacion, 
        s.name_login AS name_login, 
        s.ean13 AS codigo, 
        s.producto AS producto, 
        s.cantidad AS cantidad, 
        s.unidad_med AS unidad, 
        s.precio_prod AS precio, 
        l.complete_name AS origen,
        ll.complete_name AS destino,
        s.se_llevo AS llevo,
        s.fecha_realizo AS fecha_realizo,
        s.cantidad_banco AS cantidad_banco
        FROM merma m
        INNER JOIN merma_m2m_selec_merma r
        ON r.merma_m2o_id=m.id
        INNER JOIN merma_seleccion s
        ON r.select_merma_m2o_id=s.id
        INNER JOIN stock_location l
        ON s.location_id=l.id
        INNER JOIN stock_location ll
        ON s.destino_id=ll.id
        WHERE m.id = %s
        order by s.id ASC
        """,(id_control_merma,)
      )
      datos = self.cr.dictfetchall()
      if ( len( datos ) > 0 ):
        return datos
      else:
        return { 'value' : {} }   
  #----------------------------------------------------------------------------------------------------------------------
  def nombre_reporte( self, data ) :
    """
    Método que obtiene el nombre del reporte
    @return (str)
    """        
    clave=''
    nombre=''
    if data.get('form', False) and data['form'].get('loc_final_dic', False):
        local=str(data['form'].get('loc_final_dic',False))
        nombre = 'REPORTE DE ' + local.upper()
    return nombre
  #----------------------------------------------------------------------------------------------------------------------
  def clave_registro( self, data ) :
    """
    Método que obtiene la clave
    @return (str)
    """        
    clave=''
    nombre=''
    if data.get('form', False) and data['form'].get('clave_numer', False):
        clave=str(data['form'].get('clave_numer',False))
        nombre = 'CLAVE: ' + clave
    return nombre
  #----------------------------------------------------------------------------------------------------------------------
  def fecha_mov( self, data ) :
    """
    Método que obtiene la fecha
    @return (str)
    """        
    dia=''
    fecha=''
    if data.get('form', False) and data['form'].get('se_creo', False):
        dia=str(data['form'].get('se_creo',False))
        fecha = 'FECHA: ' + dia
    return fecha
  #----------------------------------------------------------------------------------------------------------------------
  def realizo( self, data ) :
    """
    Método que obtiene la fecha
    @return (str)
    """        
    nombre=''
    realizo=''
    if data.get('form', False) and data['form'].get('n_usuario', False):
        nombre=str(data['form'].get('n_usuario',False))
        realizo = 'REALIZO: ' + nombre
    return realizo
  #----------------------------------------------------------------------------------------------------------------------
  def get_sumas_merma( self, data ):
    id_control_merma=0
    if data.get('form', False) and data['form'].get('id', False):
      id_control_merma = int(data['form'].get('id',False))
      self.cr.execute(
        """
        SELECT 
        Sum(s.cantidad) AS cantidad_product,
        Sum(s.cantidad_banco) AS cantidad_banco
        FROM merma m
        INNER JOIN merma_m2m_selec_merma r
        ON r.merma_m2o_id=m.id
        INNER JOIN merma_seleccion s
        ON r.select_merma_m2o_id=s.id
        INNER JOIN stock_location l
        ON s.location_id=l.id
        WHERE m.id = %s
        GROUP BY m.id
        """,(id_control_merma,)
      )
      sumas = self.cr.dictfetchall()
      if ( len( sumas ) > 0 ):
        return sumas
      else:
        return { 'value' : {} }    

#########################################################################################################################
#------------------------------------------------------------------------------------------------------------------------
#Nombre del reporte, nombre del modelo,ruta del rml, parser con el nombre de la clase y header el encabezado del reporte
#para emplear el template rml definido
report_sxw.report_sxw('report.reporte_bancoo',
                      'merma',
                      'addons/sm_merma/secciones/reporte/reporte_bancoo.rml',
                      parser = reporte_bancoo,
                      header=False
                      )

