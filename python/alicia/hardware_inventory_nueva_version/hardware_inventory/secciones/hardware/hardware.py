# -*- coding: utf-8 -*-

######################################################################################################################################################
#  @version     : 1.0                                                                                                                                #
#  @autor       : SUPERMAS-Alicia Romero                                                                                                                       #
#  @creación    : 2015-05-12                                                                                                                         #
#  @linea       : Maximo 150 chars                                                                                                                   #
######################################################################################################################################################

#OpenERP Imports
from osv import fields, osv
from datetime import datetime, date

import math
import re

from openerp import tools, SUPERUSER_ID
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
  #----------------------------------------------------------------------------------------------------------------------
  @staticmethod
  def getNextModelFolio( cr, device, suc ) :
    """
    Metodo que obtiene el numero de clave siguiente
    * Para OpenERP [field.function]
    * Argumentos OpenERP: [cr, tabla,nombre_campo]
    :return dict
    """ 
    print device
    #Consultando cuál sería el nuevo numero
    cr.execute( """
               SELECT ( MAX( key_number ) + 1 ) AS next_number
               FROM hardware
               WHERE dispositivo_m2o_id = %s and sucursal_m2o_id = %s
               """ ,(device, suc ) )
    registro_consultado = cr.fetchone()
    #Retornando el nuevo folio
    return (
      1
    ) if (
      registro_consultado is None
    ) else (
      1 if ( registro_consultado[0] is None ) else ( int( registro_consultado[0] ) )
    )	
  #--------------------------------------------------Metodo Function----------------------------------------------------------------------------------
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
  def _get_image(self, cr, uid, ids, name, args, context=None):
    """
    Funcion que redimensiona la imagen de origen del hardware a grandes , medianas y pequeñas
    * Para OpenERP [field.function]
    * Argumentos OpenERP: [cr, uid, ids, name, arg, context]
    :return dict
    """  
    result = dict.fromkeys(ids, False)
    for obj in self.browse(cr, uid, ids, context=context):
      #Función estándar que devuelve un diccionario que contiene versiones grandes , medianas y pequeñas de la imagen de origen . 
      result[obj.id] = tools.image_get_resized_images(obj.image, avoid_resize_medium=True)
    return result
  #---------------------------------------------------------Metodos Privados--------------------------------------------------------------------------
  def _set_image(self, cr, uid, id, name, value, args, context=None):
    """
    Funcion que redimensiona la imagen del hardware a tamaño grande: 1024x1024px
    * Para OpenERP [field.function]
    * Argumentos OpenERP: [cr, uid, ids, name, arg, context]
    :return dict
    """
    #para redimensionar las imágenes más grandes que el estándar 'grande'
    return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
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
    #Creando la clave siguiente para este registro
    device=vals['dispositivo_m2o_id']
    suc=vals['sucursal_m2o_id']
    print suc
    print device
    vals['key_number'] = self.getNextModelFolio( cr, device, suc )

    nuevo_id = super( hardware, self ).create( cr, uid, vals, context = context )
    return nuevo_id

  def show_fields_responsible(self, cr, uid, context = None):
    return False
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                  Atributos basicos de un modelo OPENERP                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  
  #Nombre del modelo
  _name = 'hardware'
  #Nombre de la tabla
  _table = 'hardware'
  #Nombre de la descripcion al usuario en las relaciones m2o hacia este módulo
  _rec_name = 'func_key'
  #Ordenar la vista
  _order = 'sucursal_m2o_id'
 
  _columns = {
        
    'key':fields.char("Key", size=10, required=False),
    'key_number':fields.integer("Key Number", size=4 ),
    'brad':fields.char("Brand", size=50, required=True),
    'model':fields.char("Model", size=50, required=False),
    'serial_number':fields.char("Serial Number", size=50, required=True),
    'description':fields.text("Description"),
    'mac':fields.char("MAC Ethernet", size=50, required=False),
    'mac_wifi':fields.char("MAC Wi-Fi", size=50, required=False),
    'ram':fields.integer("RAM", required=False),
    'hd_capacity':fields.integer("HD Capacity", required=False),
    'status_dic':fields.selection(STATUS, 'Status', required =True ),
    'cost_hardware':fields.float('Cost Hardware', required=False),
    'show_responsible': fields.boolean('Responsible'),
    
    #Este campo contiene la imagen utilizada como imagen para el producto, limitado a 1024x1024px
    'image': fields.binary("Image"),
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

    'maintenance_o2m_ids': fields.one2many('maintenance', 'hardware_m2o_id', 'Maintenance'),
  # ================================== Campos Function ==============================================================================================#  
    'func_key' : fields.function(
      _functGetKey,
      method = True,
      type = 'char',
      string = 'Key',
      store = True,
    ),
    
    #Imagen de tamaño mediano. Es de forma automática redimensionada como imagen de 128x128px, Utilizado en las vistas de formulario 
    'image_medium': fields.function(_get_image,
                                    fnct_inv=_set_image,
                                    string="Medium-sized image",
                                    type="binary",
                                    multi="_get_image",
                                    store={
                                      'hardware': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
                                    }, ),
    #Imagen de tamaño pequeño. Es de forma automática redimensionada como imagen de 64x64px, utilizada cuando la imagen pequeña sea requerida
    'image_small': fields.function(_get_image,
                                   fnct_inv=_set_image,
                                   string="Small-sized image",
                                   type="binary",
                                   multi="_get_image",
                                   store={
                                      'hardware': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
                                  },),
    'format_responsibility': fields.binary('Format responsibility', required=False),
    'responsible': fields.many2one('res.users',"User responsible", required=False),
    
  }
    
  #Valores por defecto de los campos del diccionario [_columns]
  _defaults = {
    'status_dic' : 'active',
    # 'maintenance_o2m_ids': _GetKeyDefault
  }

#se cierra la clase
hardware() 


