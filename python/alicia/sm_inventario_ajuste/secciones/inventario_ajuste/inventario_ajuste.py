# -*- coding: utf-8 -*-

######################################################################################################################################################
#  @version     : 1.0                                                                                                                                #
#  @autor       : Alicia Romero                                                                                                                      #
#  @creacion    : 2015-12-05 (aaaa/mm/dd)                                                                                                            #
#  @linea       : Maximo 150 chars                                                                                                                   #
#  @descripcion: Modelo para almacenamiento de datos capturados en wizard de registro de Productos                                                   #
######################################################################################################################################################

#OpenERP imports
from osv import fields, osv

#Modulo :: Lista de Registro de Productos
class inventario_ajuste( osv.osv ) :

  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                  Atributos basicos de un modelo OPENERP                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  
  #Nombre del modelo
  _name = 'inventario_ajuste'
  
  #Nombre de la tabla
  _table = 'inventario_ajuste'
  
  #Nombre de la descripcion al usuario en las relaciones m2o hacia este módulo
  # _rec_name = 'producto'
  
  #Cláusula SQL "ORDER BY"
  _order = 'id DESC'

  #Columnas y/o campos Tree & Form
  _columns = {
    
    # =========================================  OpenERP Campos Basicos (integer, char, text, float, etc...)  ====================================== #
    'clave_ide' : fields.char( 'Clave' ),
    'ide_wizard' : fields.integer( 'ID Registro' ),
    'fecha_creacion':fields.date("Fecha", required=False),
    'name_login' : fields.char("Empleado", required=False),
    'ean13_producto':fields.char("EAN13", required=False),
    'cant_sistema':fields.float('Cantidad Registrada', required=False),
    'cant_contada':fields.float('Cantidad Contada', required=False),
    'unidad_med':fields.char("Medida", required=False),
    'estado':fields.char("Estado", required=False),
    'cant_ajuste':fields.float('Cantidad Ajuste', required=False),

    # ========================================================  Relaciones [many2many](m2m) ======================================================== #
    'almacen_m2o_id': fields.many2one('stock.warehouse','Tienda'),
    'location_id': fields.many2one('stock.location', 'Ubicación Origen', select=True),
    'usuario_m2o_id': fields.many2one( 'res.users', 'Usuario'),
    'producto_m2o_id': fields.many2one( 'product.product', 'Producto'),
    'med_m2o_id': fields.many2one('product.uom', 'Medida'),
    
    
  }
  
  #Valores por defecto de los campos del diccionario [_columns]
  _defaults = {
  }

inventario_ajuste()
