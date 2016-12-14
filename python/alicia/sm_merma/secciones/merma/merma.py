# -*- coding: utf-8 -*-

######################################################################################################################################################
#  @version     : 1.0                                                                                                                                #
#  @autor       : Alicia Romero                                                                                                                      #
#  @creacion    : 2015-10-20 (aaaa/mm/dd)                                                                                                            #
#  @linea       : Maximo 150 chars                                                                                                                   #
######################################################################################################################################################

#OpenERP imports
from osv import fields, osv
import time
import datetime

#Modulo :: 
class merma( osv.osv ) :
  #--------------------------------------------------------Variables Privadas y Publicas--------------------------------------------------------------
  loc_desechos= [
    ('merma', 'Merma'),
    ('caducado', 'Caducado'),
    ('desperdicio', 'Desperdicio'),
  ]
  #---------------------------------------------------------------------------------------------------------------------------------------------------  
  def accion_confirmar(self, cr, uid, ids, context=None):
    """
    Confirma la lista de productos y escribe su fecha final
    @return: True
    """
    if context is None:
        context = {}
    id_merma = ids[0]
    self.write(cr, uid, ids, { 'state': 'confirm'}, context=context)
    return True
  #---------------------------------------------------------------------------------------------------------------------------------------------------  
  def accion_ejecutar(self, cr, uid, ids, context=None):
    """
    Realiza el movimiento automatico en movimientos de almacen
    @return: True
    """
    if context is None:
        context = {}
    id_merma = ids[0]
    datos=self.pool.get( self._name ).browse( cr, uid, ids[0] )
    seleccion=datos.selecc_merma_m2m
    for id_selec in seleccion :
      selec_id=id_selec.id
      cr.execute(
      """
      SELECT 
        s.destino_id,
        s.location_id,
        s.producto_s_m2o_id,
        s.cantidad,
        s.product_m2o_med_id, 
        s.precio_prod,
        s.name_move
        FROM merma m
        INNER JOIN merma_m2m_selec_merma r
        ON r.merma_m2o_id=m.id
        INNER JOIN merma_seleccion s
        ON r.select_merma_m2o_id=s.id
        WHERE s.id = %s
        AND m.id = %s
        AND s.estado ='espera'
        order by s.id DESC
        limit 1
      """,(selec_id,id_merma,) )
      resultado = cr.fetchall()
      if resultado != None and type( resultado ) in ( list, dict) and resultado != []:
        resultado=resultado[0]
        valores =    {
          'company_id': 1,
          'location_dest_id': resultado[0],
          'location_id':resultado[1],
          'product_id':resultado[2],
          'product_qty':resultado[3],
          'product_uom':resultado[4],
          'product_uos':resultado[4],
          'product_uos_qty':resultado[3],
          'name':resultado[6],
          'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
          'date_expected': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          'auto_validate': 0,
          'priority': '1',
          'partner_id':1,
          'price_unit':resultado[5],
          'state':'done',
          #"type","out"
          'origin':'AUTOMATIC'
        }
        self.write(cr, uid, ids, { 'state': 'done'}, context=context)
        self.pool.get('stock.move').create(cr, uid, valores)

    return True
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def accion_cancelar_borrador(self, cr, uid, ids, context=None):
    """ Cancela el stock de movimiento y el estado de modificación de listado para redactar.
    @return: True
    """
    if context is None:
      context = {}
    self.write(cr, uid, ids, {'consultado': False, 'state':'draft'}, context=context)
    
    return True
#---------------------------------------------------------------------------------------------------------------------------------------------------
  def accion_enviar_a(self, cr, uid, ids, context=None):
    """ Envia el producto a Merma que es cuando se entrega al Banco o almacen .
    @return: True
    """
    if context is None:
      context = {}
    id_merma = ids[0]
    id_ubica_scrap=0
    nombre_movimiento=''
    datos=self.pool.get( self._name ).browse( cr, uid, ids[0] )
    
    seleccion=datos.selecc_merma_m2m
    obj_local = self.pool.get('stock.location')
    for id_selec in seleccion :
      selec_id=id_selec.id
      cr.execute(
      """
      SELECT 
        s.destino_id,
        s.producto_s_m2o_id,
        s.cantidad_banco,
        s.product_m2o_med_id, 
        s.precio_prod,
        s.name_move,
        s.se_llevo,
        s.producto,
        s.id
        FROM merma m
        INNER JOIN merma_m2m_selec_merma r
        ON r.merma_m2o_id=m.id
        INNER JOIN merma_seleccion s
        ON r.select_merma_m2o_id=s.id
        WHERE s.id = %s
        AND m.id = %s
        AND s.estado ='espera'
        order by s.id DESC
        limit 1
      """,(selec_id,id_merma,) )
      resultado = cr.fetchall()
      if resultado != None and type( resultado ) in ( list, dict) and resultado != [] :
        resultado=resultado[0]
        ubicar=resultado[6]
        produc=resultado[7]
        qty_bank=resultado[2]
        estado="realizado"
        if ubicar:
            nombre_movimiento= produc.upper() + "MOV. DE MERMA " + produc.upper()
            localiza_id=resultado[0]
            ubicate = obj_local.browse(cr, uid, localiza_id)
            id_ubica_scrap=ubicate.location_id.id  
            locations_scrap = obj_local.search(cr, uid, [('location_id', 'child_of', [id_ubica_scrap])], context=context)
            for id_scrap in locations_scrap:
                scrap = obj_local.browse(cr, uid, id_scrap)
                nombre=scrap.name
                nombre=nombre.lower()
                if nombre.find("merma") >= 0 :
                  ubicacion_final=id_scrap
                  fecha_mov_merma = time.strftime("%y%m%d")
                  self.pool.get('merma_seleccion').write(cr, uid, [selec_id], {'ubicacion_final_id': ubicacion_final, 'estado': estado, 'fecha_realizo': fecha_mov_merma }, context=context)
            if ubicacion_final != localiza_id and qty_bank > 0:
              valores = {
                  'company_id': 1,
                  'location_dest_id': ubicacion_final,
                  'location_id':localiza_id,
                  'product_id':resultado[1],
                  'product_qty':resultado[2],
                  'product_uom':resultado[3],
                  'product_uos':resultado[3],
                  'product_uos_qty':resultado[2],
                  'name': nombre_movimiento,
                  'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                  'date_expected': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                  'auto_validate': 0,
                  'priority': '1',
                  'partner_id':1,
                  'price_unit':resultado[4],
                  'state':'done',
                  #"type","out"
                  'origin':'AUTOMATIC'
                }
    
              self.write(cr, uid, ids, {'state':'banco-alma'}, context=context)
              self.pool.get('stock.move').create(cr, uid, valores)
            else:
              self.write(cr, uid, ids, {'state':'banco-alma'}, context=context)
             
      else:
        self.write(cr, uid, ids, {'state':'banco-alma'}, context=context)
              
    return True  

  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS                                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###

  #---------------------------------------------------------------------------------------------------------------------------------------------------  
  def obtenerProductos( self, cr, uid, ids, context = None ):
    """
    Funcion que obtiene el desecho ingresado en el registro de productos
    * Argumentos OpenERP: [ cr, uid, ids, context ]
    @param : (cr, uid, ids, context) 
    @return dic
    """
    obj_merma = self.pool.get( self._name ).browse( cr, uid, ids[0] )
    fecha_mov = obj_merma.fecha_mov
    tienda_alm = obj_merma.almacen_m2o_id.id
    destino = obj_merma.loc_final_dic
    id_merma = ids[0] 
    autor_uid = uid
    if obj_merma :
      cr.execute(
      """
      SELECT
      id
      FROM merma_seleccion
      WHERE almacen_m2o_id=%s
      AND
      TO_CHAR(create_date,'YYYY-MM-DD')= %s
      AND
      nombre_destino like %s
      AND
      estado ='espera'
      """,(tienda_alm, fecha_mov, destino,) )
      resultado = cr.fetchall()
      if resultado != None and type( resultado ) in ( list, dict) :

        if resultado:
          self.write(cr, uid, ids, {
                  'consultado': True,   
          }, context=context)
        for id_selec in resultado:
          id_select = id_selec[0]
          cr.execute(
              """
              INSERT INTO merma_m2m_selec_merma
              (merma_m2o_id, select_merma_m2o_id)
              VALUES (%s, %s)
              """, (id_merma, id_select) )
       
    else :
      return { 'value' : {} }
  #--------------------------------------------------------------------------------------------------------------------------------------------------- 
  def _obtenerIdLogueado( self, cr, uid ) :
    """
    Metodo para obtener el nombre del usuario que realizo el control de merma
    * Argumentos OpenERP: [cr, uid]
    @return string
    """
    result = {}
    obj_user = self.pool.get( 'res.users' ).browse( cr, uid, uid )
    nombre_empleado=obj_user.partner_id.name
    #Retornando
    return nombre_empleado  
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def obtenerNumero(self, cr, uid, almacen, destino ) :
    """
    Metodo que obtiene el numero siguiente
    * Para OpenERP [field.function]
    * Argumentos OpenERP: [cr, tabla,nombre_campo]
    :return dict
    """
    #Consultando cuál sería el nuevo numero
    cr.execute( """
               SELECT ( MAX( c_numero ) + 1 ) AS next_number
               FROM merma
               WHERE almacen_m2o_id = %s and loc_final_dic = %s
               """ ,(almacen, destino,) )
    registro_consultado = cr.fetchone()
    numero = (1) if (registro_consultado is None) else ( 1 if ( registro_consultado[0] is None ) else ( int( registro_consultado[0] ) ))	 
    #Retornando el nuevo folio
    return numero
  #----------------------------------------------------------------------------------------------------------------------
  def obtenerClave(self, cr, uid, almacen, destino, numero ) :
    """
    Metodo que obtiene la clave siguiente
    * Para OpenERP [field.function]
    * Argumentos OpenERP: [cr, tabla,nombre_campo]
    :return dict
    """
    #Se crea clave
    fecha_realizo = time.strftime("%y%m%d")
    obj_almacen = self.pool.get('stock.warehouse')
    tienda_nombre=obj_almacen.browse(cr, uid, almacen).name
    nombre_sep = tienda_nombre.split()
    n_tienda = nombre_sep[2] 
    clave = 'SM'+ n_tienda + destino[:3].upper()+str(numero)+'/'+fecha_realizo
    #Retornando el nuevo folio
    return clave
  #----------------------------------------------------------------------------------------------------------------------
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                             METODOS ORM                                                                      ###
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
    vals['se_creo'] =time.strftime("%y%m%d")
    almacen=vals['almacen_m2o_id']
    destino=vals['loc_final_dic']
    vals['c_numero'] = self.obtenerNumero( cr, uid, almacen, destino )
    numero=vals['c_numero']
    vals['clave_numer'] = self.obtenerClave( cr, uid, almacen, destino, numero )
    vals['n_usuario'] = self._obtenerIdLogueado( cr, uid)
  
    nuevo_id = super( merma, self ).create( cr, uid, vals, context = context )
    return nuevo_id
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def write( self, cr, uid, ids, vals, context = None) :
    """
    Método "write" se ejecuta antes de modificar el registro..
    * Argumentos OpenERP: [cr, uid, ids, vals, context]
    @return bool
    """
    datos=self.pool.get( self._name ).browse( cr, uid, ids[0] )
    almacen=datos.almacen_m2o_id.id
    destino=datos.loc_final_dic
    numero=self.obtenerNumero( cr, uid, almacen, destino )
    clave = self.obtenerClave( cr, uid, almacen, destino, numero )
    vals.update({'clave_numer': clave})
    proceso = super( merma, self ).write( cr, uid, ids, vals, context = context )
    #Retornando proceso,
    return proceso
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                  Atributos basicos de un modelo OPENERP                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  
  #Nombre del modelo
  _name = 'merma'
  
  #Nombre de la tabla
  _table = 'merma'
  
  #Nombre de la descripcion al usuario en las relaciones m2o hacia este módulo
  _rec_name = 'clave_numer'
  
  #Cláusula SQL "ORDER BY"
  _order = 'id DESC'

  #Columnas y/o campos Tree & Form
  _columns = {
    
    # =========================================  OpenERP Campos Basicos (integer, char, text, float, etc...)  ====================================== #
    'c_numero' : fields.integer( 'Clave Numero' ),
    'consultado':fields.boolean('Consultado'),
    'clave_numer' : fields.char( 'Clave' ),
    'loc_final_dic':fields.selection(loc_desechos, 'Ubicación Destino', required=True),
    'fecha_mov':fields.date("Fecha de Movimiento", required=True),
    'se_creo':fields.date("Fecha de creacion", required=False),
    
    'n_usuario': fields.char("Realizó", required=False),
    'state': fields.selection(  ( ('draft', 'Borrador'),
                                  ('cancel','Cancelado'),
                                  ('confirm','Confirmado'),
                                  ('done', 'Por Entregar'),
                                  ('banco-alma', 'Realizado'),
                                  ('fin', 'Finalizar'),
                                ),
                              'Estado', readonly=True,
                              select=True
                              ),
    # ========================================================  Relaciones [many2many](m2m) ======================================================== #
    'almacen_m2o_id': fields.many2one('stock.warehouse', 'Tienda', required=True),

    'location_id': fields.many2one('stock.location', 'Ubicacion de almacen', select=True),
    
    'selecc_merma_m2m': fields.many2many(
      #Nombre del modelo a relacionar
      'merma_seleccion',
      #Nombre de la tabla a generar
      'merma_m2m_selec_merma',
      #Primero se coloca el campo que contendra el ID del modelo local en la relacion 
      'merma_m2o_id',
      #Luego se coloca el campo que contendra el ID del modelo foraneo en la relacion
      'select_merma_m2o_id',
      #Etiqueta a mostrar al usuario
      'Selector Merma',
    ),

  }
  
  #Valores por defecto de los campos del diccionario [_columns]
  _defaults = {
    'state': 'draft',
  }
  
  #Restricciones de BD (constraints)
  _sql_constraints = []
  
  
  #Restricciones desde codigo
  _constraints = []


	### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
	###                                                                                                                 ###
	###                 Definicion de Funcion para "Imprimir Reporte"                                                   ###
	###                                                                                                                 ###
	### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###

  def imprimir_reporte_banco(self, cr, uid, ids ,context={}):
    """
    Metodo para imprimir el reporte en formato PDF
    * Argumentos OpenERP: [ cr, uid, ids, context ]
    @return dict 
    """
    
    #imprimir reporte
    if context is None:
      context = {}
    data = {}
    data['ids'] = context.get('active_ids', [])
    data['model'] = context.get('active_model', 'ir.ui.menu')
    data['form'] = self.read(cr, uid, ids,[ 'id','n_usuario','fecha_mov', 'se_creo','loc_final_dic','clave_numer','selecc_merma_m2m',], )[0]
    #Inicializando la variable datas, con el modelo
    datas = {
      'ids': [],
      'model': 'merma',
      'form': data,
    }

    #Return el nombre del reporte que aparece en el service.name y el tipo de datos report.xml	
    return {
        'type': 'ir.actions.report.xml',
        'report_name': 'reporte_bancoo',
        'datas': datas,
        'nodestroy': True,
    }  
  
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###

merma()
