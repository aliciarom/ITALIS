# coding: utf-8

#########################################################################################################################
#  @version  : 1.0                                                                                                      #
#  @autor    : Alicia Romero                                                                                            #
#  @creacion : 2015-12-01 (aaaa/mm/dd)                                                                                  #
#  @linea    : Máximo, 121 caracteres                                                                                   #
#  @descripcion: Wizard para captura la cantidad y ubicacion de producto por tienda                                                             #
#########################################################################################################################

#Importando las clases necesarias
import time
from osv import fields, osv
import time
import datetime
import pooler
from openerp.tools.translate import _

#Modelo : Registro de inventario Producto
class inventario_registro(osv.TransientModel):
# class inventario_captura(osv.osv_memory):
 
  _description = 'Registro de producto'
  
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS                                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def botonAceptar(self, cr, uid, ids,context = { }):
    """
    Metodo del botón "aceptar" para obtener el almacen de la tienda
    """
    datos=self.pool.get( self._name ).browse( cr, uid, ids[0] )
    tienda=datos.almacen_m2o_id.id
    self.write(cr, uid, ids, {
            'almacen_m2o_id': tienda,
            'state': 'producto',
        }, context=context)
    this = self.browse(cr, uid, ids)[0]
    return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'res_model': 'inventario_registro',
            'target': 'new',
            }


  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def onchange_obtenerProducto(self, cr, uid, ids, ean13_producto):
    """
    Función del Botón objeto objeto "obtenerProducto" con etiqueta "Buscar"
    para obtener y actualizar los datos del producto
    * Para OpenERP [button]
    * Argumentos OpenERP: [cr, uid, ids, ean13_ubicacion]			
    @param ean13_ubicacion: (char) Codigo de la ubicacion de la tienda
    @return dict
    """
    context = { }
    datos=self.pool.get( self._name ).browse( cr, uid, ids[0] )
    tienda=datos.almacen_m2o_id.id
    print ean13_producto
    print "**********"
    if ean13_producto:
        #valida que el codigo sea digitos y sean 13
        if len(ean13_producto) == 13 and ean13_producto.isdigit() == True:
          self.write(cr, uid, ids, {
                    'almacen_m2o_id': tienda,
                    'ean13_producto': ean13_producto,
                    'state': 'producto',
                }, context=context)

          return {
            'value' : {}
            }  
              
              
        else:
          return {
              'warning' : {
                'title' : '¡Corriga Codigo Producto!',
                'message' : 'El codigo debe contener 13 digitos, sin espacios ni letras' ,
              }  
            } 

             
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def obtenerProducto(self, cr, uid, ids, ean13_producto):
    """
    Función del Botón objeto objeto "obtenerProducto" con etiqueta "Buscar"
    para obtener y actualizar los datos del producto
    * Para OpenERP [button]
    * Argumentos OpenERP: [cr, uid, ids, ean13_ubicacion]			
    @param ean13_ubicacion: (char) Codigo de la ubicacion de la tienda
    @return dict
    """
    context = { }
    datos=self.pool.get( self._name ).browse( cr, uid, ids[0] )
    tienda=datos.almacen_m2o_id.id
    ean13_producto=datos.ean13_producto
    print ean13_producto
    print "FUNCION"
    
    if ean13_producto:
          #consulta obtener datos del producto apartir del codigo
          cr.execute(
              """
                SELECT p.name_template,
                p.image_small,
                p.id,
                pt.list_price AS precio,
                pu.name AS medida,
                pt.uom_id
                FROM product_product p
                INNER JOIN product_template pt
                ON p.product_tmpl_id=pt.id
                INNER JOIN product_uom pu
                ON pt.uom_id=pu.id
                WHERE p.active=True
                AND
                ean13 =%s
                order by p.id desc
                limit 1
              """,(ean13_producto,))
          producto = cr.fetchall()
          print producto
          # valida producto exista
          
          if producto != [] and type( producto ) in ( list, tuple, dict ):
            producto = producto[0]
            id_producto=producto[2]
          
            #Proceso completo hacer:    
            self.write(cr, uid, ids, {
                  'almacen_m2o_id': tienda,
                  'ean13_producto': ean13_producto,
                  'producto_m2o_id': id_producto,
                  'imagen': producto[1],
                  'medida_m2o_id' :producto[5],
                  'state': 'conteo',
            }, context=context)
                  
            this = self.browse(cr, uid, ids)[0]
            return {
                      'type': 'ir.actions.act_window',
                      'view_type': 'form',
                      'view_mode': 'form',
                      'res_id': this.id,
                      'views': [(False, 'form')],
                      'res_model': 'inventario_registro',
                      'target': 'new',
                   }
          
          # else:
          #   this = self.browse(cr, uid, ids)[0]
          #   return {
          #             'type': 'ir.actions.act_window',
          #             'view_type': 'form',
          #             'view_mode': 'form',
          #             'res_id': this.id,
          #             'views': [(False, 'form')],
          #             'res_model': 'inventario_registro',
          #             'target': 'new',
          #          }  
            # return {
            #         'warning' : {
            #           'title' : '¡El Producto No Existe!',
            #           'message' : 'El codigo ean13 no pertenece a ningun '+
            #           'producto ¡Intente con otro codigo!',
            #         }  
            #       }
        

    this = self.browse(cr, uid, ids)[0]
    return {
              'type': 'ir.actions.act_window',
              'view_type': 'form',
              'view_mode': 'form',
              'res_id': this.id,
              'views': [(False, 'form')],
              'res_model': 'inventario_registro',
              'target': 'new',
           }  
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def guardarConteo(self, cr, uid, ids, ean13_ubicacion, context = { } ):
    """
    Función del Botón objeto objeto "obtenerProducto" con etiqueta "Buscar"
    para obtener y actualizar los datos del producto
    * Para OpenERP [button]
    * Argumentos OpenERP: [cr, uid, ids, ean13_producto]			
    @param ean13_producto: (char) Codigo del producto
    @return dict
    """
    datos=self.pool.get( self._name ).browse( cr, uid, ids[0] )
    if ean13_ubicacion != False :
      if ean13_ubicacion:
          ean13_ubicacion = ean13_ubicacion
      else:
          ean13_ubicacion = datos.ean13_ubicacion
    
      tienda=datos.almacen_m2o_id.id
      ean13_producto=datos.ean13_producto
      print ean13_ubicacion
      id_producto=datos.producto_m2o_id.id
      imagen=datos.imagen
      medida=datos.medida_m2o_id.id
      if len(ean13_producto) == 13 and ean13_producto.isdigit() == True:
        #consulta para obtener id de la ubicacion apartir del codigo
        cr.execute(
        """
          SELECT id
          FROM stock_location
          WHERE active=True and
          x_ean13_location_correct = %s
        """,(ean13_producto,))
        ubica = cr.fetchall()
        
        if ubica != None and type( ubica ) in ( list, tuple, dict ) and ubica != [] :
              ubica = ubica[0]
              #Variable con el id de la ubicacion
              id_locali= ubica[0]
              #objeto de stock_location "Ubicaciones"
              location_pool = self.pool.get('stock.location')
              #nombre completo de la ubicacion para mostrar
              muestra_local = location_pool.browse(cr, uid, id_locali, context=context).complete_name
              #consulta para obtener el id de la "ubicacion de exitencias" de la tienda y obtener los hijos de esta para
              #comparar y validar que el "codigo de ubicacion" del producto pertenesca a la tienda seleccionada.
              cr.execute(
                      """
                      SELECT
                      s.lot_stock_id
                      from stock_warehouse s 
                      INNER JOIN stock_location se
                      ON s.lot_stock_id = se.id
                      WHERE s.id= %s
                      """,(tienda,))
              id_ubic_exist_tienda=cr.fetchone()
              #toma el valor del id de la ubicacion
              id_ubic_exist_tienda=id_ubic_exist_tienda[0]
              #Se obtienen los hijos apartir de la ubicacion padre
              local_hijos_tienda = location_pool.search(cr, uid, [('location_id', 'child_of', [id_ubic_exist_tienda])], context=context)
              #Se declara variable
              pertenece_ubicacion=False
              #recorre lista de ubicaciones de la tienda "local_hijos_tienda" y si encuentra que uno de los id coincide con el id de la
              # ubicacion cambia la variable de pertenece_ubicacion a true.
              for id_ubica in local_hijos_tienda:
                if id_ubica == id_locali:
                  pertenece_ubicacion=True
              #Valida que la ubicacion pertenesca a la tienda
              if pertenece_ubicacion == True:
                #Consulta para validar que exista el producto en la ubicacion
                cr.execute(
                  """
                  SELECT location_id, product_id, trunc(qty, 3) 
                  FROM stock_report_prodlots 
                  WHERE location_id = %s and qty >0
                  AND product_id = %s
                  """,(id_locali, id_producto))
                existe_producto = cr.fetchall()
                if existe_producto != None and type(existe_producto) in ( list, tuple, dict ) and existe_producto != [] :
                  existe_producto = existe_producto[0]
                  cantidad_en_ubicacion= existe_producto[2]
                  #se crea clave
                  ide_wizard = ids[0]
                  datos=self.pool.get( self._name ).browse( cr, uid, ids[0] )
                  clave_destino=str(datos.destino_mov_m2o_id.name)
                  clave_sep = clave_destino.split()
                  clave_sepa = clave_sep[1]
                  clave = clave_sep[0].upper()+clave_sepa[:3].upper() + str(ide_wizard)
                  
                  self.write(cr, uid, ids, {
                      'almacen_m2o_id': tienda,
                      'ean13_producto': ean13_producto,
                      'producto_m2o_id': id_producto,
                      'imagen': imagen,
                      'medida_m2o_id' :medida,
                      'cant_sistema' : cantidad_en_ubicacion,
                      'localizacion_m2o_id':id_locali,
                      'muestra_localizacion' : muestra_local,
                      'state': 'conteo',
                  }, context=context)
                
                  this = self.browse(cr, uid, ids)[0]
                  return {
                            'type': 'ir.actions.act_window',
                            'view_type': 'form',
                            'view_mode': 'form',
                            'res_id': this.id,
                            'views': [(False, 'form')],
                            'res_model': 'merma_wizard_productos',
                            'target': 'new',
                         }
                else:
                  return {
                    'warning' : {
                      'title' : '¡No hay producto!',
                      'message' : 'En la ubicación seleccionada no hay existencia '+
                                  'del producto',
                    }  
                  }
                
              else:
                  return {
                    'warning' : {
                      'title' : '¡Error! Código de Ubicación',
                      'message' : 'La ubicación NO pertenece a la tienda ' +
                      'seleccionada',
                    }  
                  }
            
        else:
            return {
              'warning' : {
                'title' : '¡La Ubicación No Existe!',
                'message' : 'El codigo de la ubicación no pertenece a ninguna '+
                            'Ubicacion',
              }  
            }
          
      else:
          return {
              'warning' : {
                'title' : '¡Corriga Codigo Ubicación!',
                'message' : 'El código debe contener 13 digitos, sin espacios ni letras' ,
              }  
            }
                  
      #             
      # self.write(cr, uid, ids, {
      #       'almacen_m2o_id': tienda,
      #       'ean13_producto': ean13_producto,
      #       'producto_m2o_id': id_producto,
      #       'imagen': imagen,
      #       'medida_m2o_id' :medida,
      #       'state': 'conteo',
      #   }, context=context)
      
      
      
    this = self.browse(cr, uid, ids)[0]
    return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'res_model': 'inventario_registro',
            'target': 'new',
          }

  #---------------------------------------------------------------------------------------------------------------------------------------------------    
  def botonRegresar(self, cr, uid, ids, context = { }):
    """
    Función del Botón objeto objeto "botonRegresar" con etiqueta "Regresar"
    para regresar al estado 'producto' y poder a modificar el producto.
    * Para OpenERP [button]
    * Argumentos OpenERP: [cr, uid, ids, context]
    """
    #creacion del objeto
    datos=self.pool.get( self._name ).browse( cr, uid, ids[0] )
    tienda=datos.almacen_m2o_id.id
    #se rescriben los datos
    self.write(cr, uid, ids, {
            'almacen_m2o_id': tienda,
            'ean13_producto': '',
            'ean13_ubicacion': '',
            'state': 'producto',
        }, context=context)
    this = self.browse(cr, uid, ids)[0]
    return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'res_model': 'inventario_registro',
            'target': 'new',
            }   

	### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
	###                                                                                                                 ###
	###                                       Atributos Básicos del Modelo OpenERP                                      ###
	###                                                                                                                 ###
	### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###

  #Nombre del Modelo
  _name = 'inventario_registro'
  _table = 'inventario_registro'
  _columns = {
    
  # ==========================  Campos OpenERP Básicos (integer, char, text, float, etc...)  ======================== #
   # 'clave_ide' : fields.char( 'Clave de Lista' ),
   'ean13_producto':fields.char("Código Producto", size=13, required=False),
   'ean13_ubicacion':fields.char("Código Ubicación", size=13, required=False),
   'imagen': fields.binary( 'Imagen', readonly=True, help='photo'),
   'muestra_localizacion':fields.char("Localizacion", required=False),
   'cant_sistema':fields.float('Cantidad Registrada', required=False),
   'cant_contado':fields.float('Cantidad Contada', required=False),
   'cant_ajustar':fields.float('Cantidad de Ajuste', required=False),
   
   'state': fields.selection([
                              ('tienda', '  Tienda'),
                              ('producto', 'Producto'),
                              ('conteo', 'Guardar Conteo'),
                            ],'estado' ),
   
  # ======================================  Relaciones OpenERP [one2many](o2m) ====================================== #

   'almacen_m2o_id': fields.many2one(
      'stock.warehouse',
      'Tienda',
      required=True
    ),
   
   'producto_m2o_id': fields.many2one(
      'product.product',
      'Id Producto'
    ),
   
   'medida_m2o_id': fields.many2one('product.uom', 'Unidad de Medida'),
   
   'localizacion_m2o_id': fields.many2one(
      'stock.location',
      'Localización'
    ),
   
  # ======================================  Function ====================================== # 
    # 'empleado_autor' : fields.function(
    #   _obtenerIdLogueado,
    #   type = 'text',
    #   method = True,
    #   string = 'Autor',
    #   change_default = True,
    #   store = False,
    #   readonly = True,
    #   required = False
    # ),
  # ======================================  Function ====================================== # 

  }

  #Valores por defecto de los elementos del arreglo [_columns]
  _defaults = {
    'state': 'tienda',
  }
   
  #Reestricciones desde código
  _constraints = [ ]

  #Reestricciones desde BD
  _sql_constraints = [ ]

inventario_registro()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
