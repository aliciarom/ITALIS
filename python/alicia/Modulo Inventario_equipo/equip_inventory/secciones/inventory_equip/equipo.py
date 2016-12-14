# -*- coding: utf-8 -*-

######################################################################################################################################################
#  @version     : 1.0                                                                                                                                #
#  @autor       : SUPERMAS-Alicia Romero                                                                                                             #
#  @creación    : 2015-08-20                                                                                                                         #
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
class equipo(osv.osv):
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
  def getNextModelFolio( cr, equip, suc ) :
    """
    Metodo que obtiene el numero de clave siguiente
    * Para OpenERP [field.function]
    * Argumentos OpenERP: [cr, tabla,nombre_campo]
    :return dict
    """ 
    print equip
    #Consultando cuál sería el nuevo numero
    cr.execute( """
               SELECT ( MAX( key_number ) + 1 ) AS next_number
               FROM equipo
               WHERE cat_equipo_m2o_id = %s and sucursales_m2o_id = %s
               """ ,(equip, suc ) )
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
      if (record.cat_equipo_m2o_id) != 0: 
        codigo_device = str( record.cat_equipo_m2o_id.codigo )
      codigo_store = ''
      if (record.sucursales_m2o_id) != 0: 
        codigo_store = str( record.sucursales_m2o_id.codigo )
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
    Funcion que redimensiona la imagen de origen del equipo a grandes , medianas y pequeñas
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
    Funcion que redimensiona la imagen del equipo a tamaño grande: 1024x1024px
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
  def onchange_func(self, cr, uid, ids, cat_equipo_m2o_id):
    if cat_equipo_m2o_id:
      for obj in self.pool.get('cat_equipo').browse(cr, uid, [cat_equipo_m2o_id]):
        return {
          'value': {
            'descripcion': obj.descripcion
          }
        }
    
    return { 'value': { 'descripcion': '' } }
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
    equip=vals['cat_equipo_m2o_id']
    suc=vals['sucursales_m2o_id']
    vals['key_number'] = self.getNextModelFolio( cr, equip, suc )

    nuevo_id = super( equipo, self ).create( cr, uid, vals, context = context )
    return nuevo_id
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                  Atributos basicos de un modelo OPENERP                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  
  #Nombre del modelo
  _name = 'equipo'
  #Nombre de la tabla
  _table = 'equipo'
  #Nombre de la descripcion al usuario en las relaciones m2o hacia este módulo
  _rec_name = 'func_key'
  #Ordenar la vista
  _order = 'sucursales_m2o_id'
 
  _columns = {
        
    # 'key':fields.char("Key", size=10, required=False),
    'key_number':fields.integer("Key Number", size=4 ),
    'brad':fields.char("Brand", size=50),
    'model':fields.char("Model", size=50, required=False),
    'serial_number':fields.char("Serial Number", size=50),
    'description':fields.text("Description", required=True),
    'status_dic':fields.selection(STATUS, 'Status'),
    'cost_equipo':fields.float('Cost of equipment', required=False),
    'name_equip':fields.char("Name", size=50, required=True),
    'descripcion': fields.related('cat_equipo_m2o_id', 'descripcion', type="char", relation='cat_equipo', readonly=True, string="descripcion"),
    
    #Este campo contiene la imagen utilizada como imagen para el producto, limitado a 1024x1024px
    'image': fields.binary("Image"),
  # ================================ Relaciones [one2many](o2m) =====================================================================================#
    'cat_equipo_m2o_id': fields.many2one(
      'cat_equipo',
      'Maintenance Group',
      required = True
    ),

    'sucursales_m2o_id': fields.many2one(
      'sucursal',
      'Location',
      required = True
    ),
    # 'sucursal_m2o_id': fields.many2one(
    #   'cat_sucursal',
    #   'Location',
    #   required = True
    # ),

    'maintenance_equip_o2m_ids': fields.one2many('maintenance_equip', 'equipo_m2o_id', 'Maintenance'),
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
                                      'equipo': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
                                    }, ),
    #Imagen de tamaño pequeño. Es de forma automática redimensionada como imagen de 64x64px, utilizada cuando la imagen pequeña sea requerida
    'image_small': fields.function(_get_image,
                                   fnct_inv=_set_image,
                                   string="Small-sized image",
                                   type="binary",
                                   multi="_get_image",
                                   store={
                                      'equipo': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
                                  },),
    
    
  }
    
  #Valores por defecto de los campos del diccionario [_columns]
  _defaults = {
    'status_dic' : 'active',
    # 'maintenance_o2m_ids': _GetKeyDefault
  }

#se cierra la clase
equipo() 


