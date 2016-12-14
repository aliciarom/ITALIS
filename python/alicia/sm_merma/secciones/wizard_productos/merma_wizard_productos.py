# coding: utf-8

#########################################################################################################################
#  @version  : 1.0                                                                                                      #
#  @autor    : Alicia Romero                                                                                            #
#  @creacion : 2015-11-04 (aaaa/mm/dd)                                                                                  #
#  @linea    : Máximo, 121 caracteres                                                                                   #
#  @descripcion: Wizard para captura de producto por tienda                                                             #
#########################################################################################################################

#Importando las clases necesarias
from osv import fields, osv
import time
import datetime
import pooler
from openerp.tools.translate import _

#Modelo : Registro de Producto
class merma_wizard_productos(osv.TransientModel):
 
  _description = 'Wizard Productos'
  
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS                                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  def guardarProducto(self, cr, uid, ids, cantidad_mover=0.0, context = { }):
    """
    Función del Botón objeto "guardarProducto" con etiqueta "Guardar" 
    para almacenar los datos en la tabla 'merma_seleccion' modelo 'Lista de Merma'
    * Para OpenERP [button]
    * Argumentos OpenERP: [cr, uid, ids, context]			
    @return dict
    """
    #objeto
    datos=self.pool.get( self._name ).browse( cr, uid, ids[0] )
    cantidad_mover=datos.cantidad_mover
    valida=cantidad_mover
    if valida > 0 :
      producto=datos.producto
      clave=datos.clave_ide
      cod_ean13=datos.cod_ean13
      id_producto=datos.producto_m2o_id.id
      tienda=datos.almacen_m2o_id.id
      destino_id=datos.destino_mov_m2o_id.id
      localizacion_id=datos.localizacion_m2o_id.id
      cantidad_mover=datos.cantidad_mover
      cantidad_prod=datos.cantidad_prod
      unidad_med=datos.unidad_med
      unidad_med_id=datos.medida_m2o_id.id
      precio=datos.precio
      empleado_autor=datos.empleado_autor
      autor_uid=uid
      nombre_destino=datos.destino_mov_m2o_id.name
      name_move=producto+" "+ nombre_destino
      clave_sep = nombre_destino.split()
      nombre_destino = clave_sep[1].lower()
      estado="espera"
      #se guarda id de wizard
      ide_wizard = ids[0]
      #creo fechas
      fecha_x = datetime.datetime.now()
      fecha_mov_stock = time.strftime("%y%m%d")
      resul=cantidad_prod - cantidad_mover

      if resul >= 0:
        #Valores a insertar
        valores = (
                    autor_uid, fecha_x, ide_wizard, clave, fecha_mov_stock, empleado_autor, name_move, cod_ean13, producto, cantidad_mover, 
                    unidad_med, unidad_med_id, precio, autor_uid, localizacion_id, destino_id, id_producto, tienda, nombre_destino, estado,
                    cantidad_prod,
                  )
        # print valores
        this = self.browse(cr, uid, ids)[0]
        self.write(cr, uid, ids, {
                'cod_ean13':'',
                'cod_ubicacion':'',
                'state': 'producto',
                
            }, context=context)
        #se insertan los nuevos datos a la tabla listado_codigo
        cr.execute(
          """
          INSERT INTO merma_seleccion
          (create_uid, create_date, ide_wizard, clave_ide, fecha_creacion, name_login, name_move, ean13, producto, cantidad, unidad_med,  
          product_m2o_med_id, precio_prod, usuario_m2o_id, location_id, destino_id, producto_s_m2o_id, almacen_m2o_id, nombre_destino,
          estado, cantidad_ubica )
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
          """, valores )
        
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
    else :
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

 #---------------------------------------------------------------------------------------------------------------------------------------------------
  def obtenerProducto(self, cr, uid, ids, cod_ean13, cod_ubicacion='0' ):
    """
    Función del Botón objeto objeto "obtenerProducto" con etiqueta "Buscar" y y Evento onchange de los campos "cod_ean13" y "cod_ubicacion"
    para obtener y actualizar los datos del producto
    * Para OpenERP [button]
    * Para OpenERP [onchange]
    * Argumentos OpenERP: [cr, uid, ids, cod_ean13, cod_ubicacion]			
    @param cod_ean13: (char) Codigo del producto
    @param cod_ubicacion: (char) Codigo de la ubicacion de la tienda
    @return dict
    """
    context =''

    datos=self.pool.get( self._name ).browse( cr, uid, ids[0] )
    if cod_ean13 != False and cod_ubicacion != False:
      #declaro id de localizacion
      id_locali=0
      #valida codigos no sean False
      if cod_ean13 :
        cod_ean13 = cod_ean13
      else:
        cod_ean13 = datos.cod_ean13
      if cod_ubicacion:
        cod_ubicacion = cod_ubicacion
      else:
        cod_ubicacion = datos.cod_ubicacion
      #obtener valores 
      tienda=datos.almacen_m2o_id.id
      destino=datos.destino_mov_m2o_id.id
      muestra_dest=datos.destino_mov_m2o_id.complete_name
      ide_wizard = ids[0]
      existe = False
      #valida codigo no sea  vacio
      if len(cod_ean13) >= 10:
          #valida que el codigo sea digitos y sean 13
          if len(cod_ean13) == 13 and cod_ean13.isdigit() == True:
            fecha = time.strftime("%y%m%d")
            cr.execute(
                """
                  SELECT
                  ean13
                  FROM merma_seleccion
                  WHERE fecha_creacion = %s
                  AND ean13 =%s
                  AND create_uid =%s
                """,(fecha, cod_ean13, uid ))
            registro_consultado = cr.fetchall()
            # print registro_consultado
            existe = (False) if (registro_consultado == [] or registro_consultado == None ) else ( ( True ) )
            # print existe
            if existe == False:
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
                  """,(cod_ean13,))
              producto = cr.fetchall()
              # valida producto exista
              if producto != None and type( producto ) in ( list, tuple, dict ) and producto != [] :
                producto = producto[0]
                id_producto=producto[2]
                #valida que el codigo sea digitos y sean 13
                if len(cod_ubicacion) == 13 and cod_ubicacion.isdigit() == True:
                        #consulta para obtener id de la ubicacion apartir del codigo
                        cr.execute(
                        """
                          SELECT id
                          FROM stock_location
                          WHERE active=True and
                          x_ean13_location_correct = %s
                        """,(cod_ubicacion,))
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
                                      'producto': producto[0],
                                      'imagen': producto[1],
                                      'producto_m2o_id': id_producto,
                                      'precio' : producto[3],
                                      'unidad_med' : producto[4],
                                      'medida_m2o_id' :producto[5],
                                      'cantidad_prod' : cantidad_en_ubicacion,
                                      'cantidad_mover' : '',
                                      'cod_ean13': cod_ean13,
                                      'cod_ubicacion': cod_ubicacion,
                                      'localizacion_m2o_id': id_locali,
                                      'almacen_m2o_id': tienda,
                                      'destino_mov_m2o_id': destino,
                                      'muestra_destino': muestra_dest,
                                      'muestra_localizacion': muestra_local,
                                      'clave_ide': clave,
                                      'state': 'guardar',
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
    
              else:
                  return {
                    'warning' : {
                      'title' : '¡El Producto No Existe!',
                      'message' : 'El codigo ean13 no pertenece a ningun '+
                      'producto ¡Intente con otro codigo!',
                    }  
                  }
              
            else:
                return {
                  'warning' : {
                    'title' : '¡El Producto ya se Registro!',
                    'message' : 'Ingrese el siguiente codigo de '+
                    'producto, este ya fue registrado',
                  }  
                }
            
              
          else:
            return {
                'warning' : {
                  'title' : '¡Corriga Codigo Producto!',
                  'message' : 'El codigo debe contener 13 digitos, sin espacios ni letras' ,
                }  
              }   
      else:
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
    
    else :
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
    destino=datos.destino_mov_m2o_id.id
    codigo=datos.cod_ean13
    muestra=datos.destino_mov_m2o_id.complete_name
    #se rescriben los datos
    self.write(cr, uid, ids, {
            'almacen_m2o_id': tienda,
            'destino_mov_m2o_id': destino,
            'cod_ean13': '',
            'muestra_destino': muestra,
            'state': 'producto',
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
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def onchange_filtro_almacen( self, cr, uid, ids, almacen_m2o_id) :
    """
    Evento OnChange del campo "almacen_m2o_id" con etiqueta "Tienda" para obtener el filtro de ubicaciones de esa tienda en el campo
    destino_mov_m2o_id con etiqueta "Ubicacion Destino".
    * Para OpenERP [onchange]
    * Argumentos OpenERP: [cr, uid, ids]			
    @param almacen_m2o_id: (int) Manda el valor de la tienda o almacen seleccionado
    @return dict
    """
    context =''
    #toma el datos seleccionado
    try:
       id_almacen =str(almacen_m2o_id)
    except :
      return {
        'value' : {
          'localizacion_m2o_id' : False,
          'destino_mov_m2o_id' : False,
        },
        'domain' : {
          'localizacion_m2o_id' : [( 'id', '=', '0' )],
          'destino_mov_m2o_id' : [( 'id', '=', '0' )],  
        },				
      }
    #consulta para obtener el id de la localidad en almacen y el nomnre de la tienda seleccionada
    cr.execute(
            """
            SELECT
            s.name
            from stock_warehouse s 
            INNER JOIN stock_location se
            ON s.lot_stock_id = se.id
            WHERE s.id= %s
            """,(id_almacen,))
    almacenes=cr.fetchall()
    
    if almacenes != None and type( almacenes ) in ( list, tuple, dict ):
        d_almacen=almacenes[0]
        ubicacion_seleccionada=d_almacen[0]
    #obtiene el nombre de las tiendas o de almacenes para hacer una comparaciones y obtener la variable con el numero de sucursales
    cr.execute(
            """
            SELECT
            s.name
            from stock_warehouse s 
            INNER JOIN stock_location se
            ON s.lot_stock_id = se.id
            order by s.id
            """,)
    lista_tienda=cr.fetchall()

    #Se obtiene el numero de tiendas
    rango=len(lista_tienda)
    suma=0
    sucursal=0

    for i in range(rango):
      suma=suma + 1
      if ubicacion_seleccionada.find(str(suma)) >= 0:
        sucursal=suma  

    list_loc_tienda = []
    cr.execute(
      """
      SELECT id
      FROM stock_location ls
      WHERE scrap_location = true and
      ls.name like 'Scrapped'
      """
    )
    scrapped = cr.fetchone()
    id_scrapped = scrapped[0]
    #Se obtiene el id de las localizaciones virtuales de cada tienda
    cr.execute(
      """
      SELECT
      id
      from stock_location ls
      WHERE 
      location_id=%s
      and
      scrap_location = true
      order by id
      """,(id_scrapped,))
    #recorre las lista de localidades
    for id_tienda in cr.fetchall():
       lista=id_tienda[0]
       list_loc_tienda.append(lista)   

    location_ids = []
    i=5
    #objeto de ubicaciones de almacen
    location_pool = self.pool.get('stock.location')
    for id_tienda in list_loc_tienda:
      id_tienda=int(id_tienda)
      ubicacion_t = location_pool.browse(cr, uid, id_tienda)
      nombre = ubicacion_t.name
      if sucursal>0:
        if nombre.find("SM1 Scrap Parent") >= 0 and sucursal==1 :
          location_ids = location_pool.search(cr, uid, [('location_id', 'child_of', [id_tienda])], context=context)
          # print location_ids
        if nombre.find("SM2 Scrap Parent") >= 0 and sucursal==2 :
          location_ids = location_pool.search(cr, uid, [('location_id', 'child_of', [id_tienda])], context=context)
        if nombre.find("SM3 Scrap Parent") >= 0 and sucursal==3 :
          location_ids = location_pool.search(cr, uid, [('location_id', 'child_of', [id_tienda])], context=context)
        if nombre.find("SM4 Scrap Parent") >= 0 and sucursal==4 :
          location_ids = location_pool.search(cr, uid, [('location_id', 'child_of', [id_tienda])], context=context)
        if nombre.find("SM5 Scrap Parent") >= 0 and sucursal==5 :
          location_ids = location_pool.search(cr, uid, [('location_id', 'child_of', [id_tienda])], context=context)
      if sucursal>5:
        for i in range(rango):
          i=i+1
          if nombre.find(str(i)) >= 0 and sucursal==i:
            location_ids = location_pool.search(cr, uid, [('location_id', 'child_of', [id_tienda])], context=context)
          
          else:
            return {
            'value' : {
              'localizacion_m2o_id' : False,
              'destino_mov_m2o_id' : False,
            },
            'domain' : {
              'localizacion_m2o_id' : [( 'id', '=', '0' )],
              'destino_mov_m2o_id' : [( 'id', '=', '0' )],  
            },
            'warning' : {
              'title' : '¡Aviso! Seleccione otra tienda',
              'message' : 'La tienda selecciona no tiene asocida ' +
                          'una localidad virtual de merma, caducado o desperdicio ' +
                          '¡Deben crearse primero!',
            }  
          }      
    
    if location_ids != []:
      #se borra el primer valor de tupla que es el padre de las ubicaciones
      del location_ids[0]
      #Validando el retorno de datos encontrados para el filtrado de datos en destino_mov_m2o_id con etiqueta ubicacion destino
      cadena_retorno = ( str ( "('id','=','0')" if ( location_ids == [] ) else ( "('id','in'," + str( location_ids ) + ")" ) ) )

      #se escribe el id del almacen
      self.write(cr, uid, ids, {'almacen_m2o_id': id_almacen, },)
      #filtrar ubicaciones de tienda seleccionada 
      #Retornando domain
      return {
        'value' : {
          'localizacion_m2o_id' : False,
          'destino_mov_m2o_id' : False,
          # 'filtro_ubicaciones' : cadena_retorno,
        },
          
        'domain' : {
          'localizacion_m2o_id' : [
            '&',
            eval( cadena_retorno )
          ],
          'destino_mov_m2o_id' : [
            '&',
            eval( cadena_retorno )
          ], 
        },			
      }
    else:
      return {
              'value' : {
                'localizacion_m2o_id' : False,
                'destino_mov_m2o_id' : False,
              },
              'domain' : {
                'localizacion_m2o_id' : [( 'id', '=', '0' )],
                'destino_mov_m2o_id' : [( 'id', '=', '0' )],  
              },
              'warning' : {
              'title' : '¡Aviso! Seleccione otra tienda',
              'message' : 'Por favor seleccione solo las tiendas existentes ',
              }   
            }
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def botonAceptar(self, cr, uid, ids,context = { }):
    """
    Metodo del botón "aceptar" para obtener el almacen de la tienda
    """
    datos=self.pool.get( self._name ).browse( cr, uid, ids[0] )
    tienda=datos.almacen_m2o_id.id
    destino=datos.destino_mov_m2o_id.id
    self.write(cr, uid, ids, {
            'almacen_m2o_id': tienda,
            'destino_mov_m2o_id': destino,
            'state': 'producto',
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
  #--------------------------------------------------------------------------------------------------------------------------------------------------- 
  def _obtenerIdLogueado( self, cr, uid, ids = None, field_name = None, arg = None, context = None ) :
    """
    Función para el campo "Autor"
    * Para OpenERP [field.function( empleado_autor )]
    * Argumentos OpenERP: [cr, uid, ids, field_name, arg, context]
    @return dict
    """
    result = {}
    for record in self.browse( cr, uid, ids, context ) :
      obj_user = self.pool.get( 'res.users' ).browse( cr, uid, uid )
      nombre_empleado=obj_user.partner_id.name
      result[record.id] = nombre_empleado
    #Retornando los resultados evaluados
    return result
 
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
    almacen=vals['almacen_m2o_id']
    destino=vals['destino_mov_m2o_id']
    nuevo_id = super( merma_wizard_productos, self ).create( cr, uid, vals, context = context )
    return nuevo_id  
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def _obtener_ubicaciones_subquery( self, cr, uid, ids = None, field_name = None, arg = None, context = None ) :
    """
    Función para obtener los id's de los almacenes para poder obtener sus ubicaciones
    * Para OpenERP [field.function( ubicaciones_subquery )]
    * Argumentos OpenERP: [cr, uid, context]
    @return dict
    """
    almacenes=[]
    #Se realiza una consulta para filtrar los id de todos los stock de entrada de cada tienda,
    cr.execute(
      """
      SELECT
        location_id AS id_local
        from stock_location se
        INNER JOIN stock_warehouse s
        ON s.lot_input_id = se.id
        ORDER BY location_id
      """
    )
    for registro in cr.fetchall() :
      almacenes.append( registro[0] )
  
    #Validando el retorno de datos encontrados
    cadena_retorno = (
      str ( "('id','=','0')" if ( almacenes == [] ) else ( "('id','in'," + str( almacenes ) + ")" ) )
    )
    #Retornando los id's en caso de ser un "Registro Nuevo"
    if ( ( field_name == None ) and ( arg == None ) and ( context == None ) ):
      result = cadena_retorno
    #Retornando los id's en caso de "Edicion de Registro"
    else :
      result = {}
      for record in self.browse( cr, uid, ids, context ) :		
        result[record.id] = cadena_retorno
    return result 
  #---------------------------------------------------------------------------------------------------------------------------------------------------  

	### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
	###                                                                                                                 ###
	###                                       Atributos Básicos del Modelo OpenERP                                      ###
	###                                                                                                                 ###
	### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###

  #Nombre del Modelo
  _name = 'merma_wizard_productos'
  #Descripcion
  _description = 'merma_wizard_productos'

  _columns = {
    
  # ==========================  Campos OpenERP Básicos (integer, char, text, float, etc...)  ======================== #
   'cont':fields.char("Contador", size=10, required=False),
   'clave_ide' : fields.char( 'Clave de Lista' ),
   'cod_ean13':fields.char("Código Producto", size=13, required=False),
   'cod_ubicacion':fields.char("Código Ubicación", size=13, required=False),
   'muestra_destino':fields.char("Destino", required=False),
   'muestra_localizacion':fields.char("Localizacion", required=False),
   'producto': fields.char('Nombre', size=80, readonly=True),
   'imagen': fields.binary( 'Imagen', readonly=True, help='photo'),
   'state': fields.selection([
                              ('tienda', '  Tienda'),
                              ('producto', 'Producto'),
                              ('guardar', 'Guardar')
                            ]),
   # 'filtro_ubicaciones':fields.text("Lista", required=False),
   'cantidad_prod':fields.float('Cantidad de Producto', required=False),
   'cantidad_mover':fields.float('Cantidad a Mover', required=False),
   'unidad_med':fields.char("Unidad de Medida", required=False),
   'precio':fields.float('Precio', required=False),
  # ======================================  Relaciones OpenERP [one2many](o2m) ====================================== #

   'almacen_m2o_id': fields.many2one(
      'stock.warehouse',
      'Tienda'
    ),

   'destino_mov_m2o_id': fields.many2one(
      'stock.location',
      'Ubicacion Destino'
    ),
   
   'localizacion_m2o_id': fields.many2one(
      'stock.location',
      'Localización'
    ),
   
   'producto_m2o_id': fields.many2one(
      'product.product',
      'Id Producto'
    ),
   
   'medida_m2o_id': fields.many2one('product.uom', 'Unidad de Medida'),
   
  # ======================================  Function ====================================== # 
    'empleado_autor' : fields.function(
      _obtenerIdLogueado,
      type = 'text',
      method = True,
      string = 'Autor',
      change_default = True,
      store = False,
      readonly = True,
      required = False
    ),
    #Campos function para definir el domain del campo almacen_id (no se almacena)
    'ubicaciones_subquery' : fields.function(
      _obtener_ubicaciones_subquery,
      type = 'text',
      method = True,
      string = 'SubqueryUbicaciones',
      change_default = True,
      store = False,
      readonly = True,
      required = False
    ),
  
  }

  #Valores por defecto de los elementos del arreglo [_columns]
  _defaults = {
    'state': 'tienda',
  }
   
  #Reestricciones desde código
  _constraints = [ ]

  #Reestricciones desde BD
  _sql_constraints = [ ]

merma_wizard_productos()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
