# -*- coding: utf-8 -*-

######################################################################################################################################################
#  @version     : 1.0                                                                                                                                #
#  @autor       : SUPERMAS-ARC                                                                                                                       #
#  @creación    : 2015-05-12                                                                                                                         #
#  @linea       : Maximo 150 chars                                                                                                                   #
######################################################################################################################################################

#OpenERP Imports
from osv import fields, osv
from datetime import datetime, date
import re
from openerp.tools.translate import _

#Modulo ::
class hardware(osv.osv):
  #--------------------------------------------------------Variables Privadas y Publicas--------------------------------------------------------------
  STATUS = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('repair', 'In repair'),
    ('warranty', 'In warranty'),
    ('donated', 'Donated'),
    ('discarded', 'discarded')
  ]
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS                                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  #--------------------------------------------------Metodo Function-------------------------------------------------------------------------------------------------
  def _functGetKey( self, cr, uid, ids, name, arg, context = {} ) :
    """
    Funcion que obtiene la clave
    * Para OpenERP [field.function]
    * Argumentos OpenERP: [cr, uid, ids, name, arg, context]
    :return dict
    """     
    result = {}
    for record in self.browse( cr, uid, ids, context ) :
      codigo_device = ''
      if (record.dispositivo_m2o_id) != 0: 
        codigo_device = str( record.dispositivo_m2o_id.codigo )
      codigo_store = ''
      if (record.sucursal_m2o_id) != 0: 
        codigo_store = str( record.sucursal_m2o_id.codigo )
      number = ''
      if (record.key_number) != 0: 
        number = record.key_number
      #añadiendo un 0 si es menor a 10
      number_n = str( ("0" + str(number)) if (number < 10) else number)
      # concatenando clave
      key_complet = str( codigo_store + codigo_device + number_n )
      #convirtiendo a mayúsculas
      key = key_complet.upper()

      result [record.id] = key

    return result
  
  #---------------------------------------------------------Metodos Privados--------------------------------------------------------------------------

  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS ONCHANGE                                                             ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ### 
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def onchange_model( self, cr, uid, ids, model ) :
    """
    Evento OnChange del campo "model" con etiqueta "Model" que Convierte el texto en Mayúsculas
    * Para OpenERP [onchange]
    * Argumentos OpenERP: [cr, uid, ids]
    @param key: (string) Model
    @return dict
    """
    #Conversión en mayúsculas
    if model :
      return {
        'value' : {
          'model' : model.upper()
        }
      }
    return { 'value' : {} }
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def onchange_serial_number( self, cr, uid, ids, serial_number ) :
    """
    Evento OnChange del campo "serial_number" con etiqueta "Serial Number" que Convierte el texto en Mayúsculas
    * Para OpenERP [onchange]
    * Argumentos OpenERP: [cr, uid, ids]
    @param serial_number: (string) serial_number
    @return dict
    """
    #Conversión en mayúsculas
    if serial_number :
      return {
        'value' : {
          'serial_number' : serial_number.upper()
        }
      }
    return { 'value' : {} }
  
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def onchange_mac( self, cr, uid, ids, mac ) :
    """
    Evento OnChange del campo "mac" con etiqueta "Mac" que Convierte el texto en Mayúsculas
    * Para OpenERP [onchange]
    * Argumentos OpenERP: [cr, uid, ids]
    @param mac: (string) mac
    @return dict
    """
    #Conversión en mayúsculas
    if mac :
      return {
        'value' : {
          'mac' : mac.upper()
        }
      }
    return { 'value' : {} }
  
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def onchange_mac_wifi( self, cr, uid, ids, mac_wifi ) :
    """
    Evento OnChange del campo "mac_wifi" con etiqueta "Mac Wi-Fi" que Convierte el texto en Mayúsculas
    * Para OpenERP [onchange]
    * Argumentos OpenERP: [cr, uid, ids]
    @param mac_wifi: (string) mac_wifi
    @return dict
    """
    #Conversión en mayúsculas
    if mac_wifi :
      return {
        'value' : {
          'mac_wifi' : mac_wifi.upper()
        }
      }
    return { 'value' : {} }
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS ORM                                                                  ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ### 
 #--------------------------------------------------------------------------------------------------------------------------------------------------- 
  def create(self, cr, uid, vals, context = None ):
    """   
    Método "create" que se ejecuta justo antes (o al momento) de CREAR un nuevo registro en OpenERP.    
    * Argumentos OpenERP: [cr, uid, vals, context]    
    @param  
    @return bool    
    """
    nuevo_id = None
   
    if vals['key_number'] == 0:
      raise osv.except_osv(_( 'Notice!' ),_( 'Please fill fields "Key Number" ' ) )

    nuevo_id = super( hardware, self ).create( cr, uid, vals, context = context )
    return nuevo_id  

  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                  Atributos basicos de un modelo OPENERP                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  
  #Nombre del modelo
  _name = 'hardware'
  #Nombre de la tabla
  _table = 'hardware'
  #Ordenar la vista
  _order = 'key'
 
  _columns = {
        
    'key':fields.char("Key", size=10, required=False),
    'key_number':fields.integer("Key Number", size=4, required=True ),
    'brad':fields.char("Brand", size=50, required=True),
    'model':fields.char("Model", size=50, required=False),
    'serial_number':fields.char("Serial Number", size=50, required=True),
    'description':fields.text("Description"),
    # 'location':fields.char("Location", size=5, requires=True),
    'mac':fields.char("MAC Ethernet", size=50, required=False),
    'mac_wifi':fields.char("MAC Wi-Fi", size=50, required=False),
    'ram':fields.integer("RAM", required=False),
    'hd_capacity':fields.integer("HD Capacity", required=False),
    'last_maintenance_date':fields.date("Last Maintenance Date", required=False),
    'next_maintenance_date':fields.date("Next Maintenance", required=False),
    'status_dic':fields.selection(STATUS, 'Status', required =True ),
    'cost_hardware':fields.float('Cost Hardware', required=False),
    # 'store' : fields.selection(
    #   (
    #     ( 'sm1', 'SM1'),
    #     ( 'sm2', 'SM2' ),
    #     ( 'sm3', 'SM3' ),
    #     ( 'sm4', 'SM4' ),
    #     ( 'sm5', 'SM5' ),
    #   ),
    #   'Location',	required = True,
    # ),
  # ================================ Relaciones [one2many](o2m) =====================================================================================#
    'dispositivo_m2o_id': fields.many2one(
      'cat_dispositivos',
      'Device Type',
      required = True
    ),
    
    'sucursal_m2o_id': fields.many2one(
      'sucursal',
      'Location',
      required = True
    ),
  # ================================== Campos Function ==============================================================================================#  
    'func_key' : fields.function(
      _functGetKey,
      method = True,
      type = 'char',
      string = 'Key',
      store = True,
    ),
    
  }
    
  #Valores por defecto de los campos del diccionario [_columns]
  _defaults = {
    'status_dic' : 'active',
  }

#se cierra la clase
hardware() 


