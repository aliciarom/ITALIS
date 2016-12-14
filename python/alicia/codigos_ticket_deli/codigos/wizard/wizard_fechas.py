# coding: utf-8

#########################################################################################################################
#  @version  : 1.0                                                                                                      #
#  @autor    : Alicia Romero                                                                                            #
#  @creacion : 2015-06-05 (aaaa/mm/dd)                                                                                  #
#  @linea    : Máximo, 121 caracteres                                                                                   #
#  @descripcion: Realiza la busqueda de los productos que se han modificado en determinada fecha y genera las etiquetas #
#########################################################################################################################

#Importando las clases necesarias
import time
from datetime import datetime
from osv import fields, osv
import pooler
from openerp.tools.translate import _
import barcode

#Modelo
class wizard_fechas(osv.osv_memory):
 
  #Descripcion tipo consulta
  _description = 'obtiene los precios en determinada fecha'
  
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS                                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###

  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def onchange_buscarEan( self, cr, uid, ids, fecha_inicial, context = None ) :
    """
    Evento OnChange del campo "fecha_inicial" con etiqueta "fecha de cambio", obtiene los codigos ean13 de los productos que cambiaron su precio.
    * Para OpenERP [onchange]
    * Argumentos OpenERP: [cr, uid, ids]
    @param fecha_inicial: (string) fecha de cambio
    @return dict
    """
    lista_ean = ' '
    if fecha_inicial :
      #Se buscan los productos que se han modificado apartir de la fecha de escritura
      cr.execute(
        """
        SELECT p.ean13
        FROM product_template t
        INNER JOIN product_product p
        ON t.id = p.product_tmpl_id
        WHERE  to_char(t.write_date, 'YYYY-MM-DD') = %s
         """,(fecha_inicial,) )
      resp = cr.fetchall()
      #Se convierte en cadena y se le da formato de lista
      muestra= str(resp)
      salto=muestra.replace('),', '\n')
      remove=["(u",",)","'","[", "]", ","]
      lista_ean=salto.translate(None,' '.join(remove))
    #muestra los datos en el area de texto Codigos
    return { 'value' : { 'listado' : lista_ean } }
  #---------------------------------------------------------------------------------------------------------------------------------------------------  
  def obtenerCodigos( self, cr, uid, ids, context = None ):
    """
    Funcion que dependiendo de lo que obtenga el metodo _obtener_codigos genera el archivo para imprimir las etiquetas
    * Argumentos OpenERP: [ cr, uid, ids, context ]
    @param : (cr, uid, ids, context) 
    @return dict
    """
    #obtengo el valor de agregar
    agregado = self.pool.get( self._name ).browse( cr, uid, ids[0] ).agregar
    #Obtengo nuevamente los datos desde la consulta si no se agregado codigos
    if agregado == False :
      listar = self.buscar_Ean( cr, uid, ids, context = context )
      print('Agregar/False \n' + listar) 
    #Si se han agregado codigos se leen desde el campo de texto  
    else:
      leer_codigoss = self.pool.get(self._name).read(cr, uid, ids, { 'listado'}, context = context)
      listar = leer_codigoss[0]['listado']
      print('Agregar/True \n' + listar)
    #Escribe en el campo "listado" la lista de codigos obtenida en listar y cambia el valor a True 
    add_codigos = self.pool.get(self._name).write(cr, uid, ids, { 'listado': listar }, context = context)
    # Obtego la lista de codigos de mi tabla del campo listado
    lista = self.pool.get( self._name ).browse( cr, uid, ids[0] ).listado
    if lista == None or lista == '\n' or lista == ' ' or lista == False:
      if len(lista) < 13 :
        raise osv.except_osv(_( 'Avisoo' ),_( 'Debe ingresar una lista de códigos' ) )
    buscar = self._obtener_codigos( cr, uid, lista)
    if buscar == True :
        #imprimir reporte
       if context is None:
         context = {}
       data = {}
       data['ids'] = context.get('active_ids', [])
       data['model'] = context.get('active_model', 'ir.ui.menu')
       data['form'] = self.read(cr, uid, ids, ['fecha_inicial'], context=context)[0]
       #Inicializando la variable datas, con el modelo
       datas = {
         'ids': [],
         'model': 'listado_codigo',
         'form': data,
       }
       #Return el nombre del reporte que aparece en el service.name y el tipo de datos report.xml	
       return {
           'type': 'ir.actions.report.xml',
           'report_name': 'sm_etiquetas',
           'datas': datas,
           'nodestroy': True,
       }  
    else :
      return { 'value' : {} }
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def buscar_Ean( self, cr, uid, ids, context = None ) :
    """
    Función usada para obtener la lista de codigos en forma de cadena
    * Argumentos OpenERP: [cr, uid, ids]
    @return str
    """
    fecha_inicial = self.pool.get( self._name ).browse( cr, uid, ids[0] ).fecha_inicial
    lista_ean = ' '
    if fecha_inicial :
      #Se buscan los productos que se han modificado apartir de la fecha de escritura
      cr.execute(
        """
        SELECT p.ean13
        FROM product_template t
        INNER JOIN product_product p
        ON t.id = p.product_tmpl_id
        WHERE  to_char(t.write_date, 'YYYY-MM-DD') = %s
         """,(fecha_inicial,) )
      resp = cr.fetchall()
      #Se convierte en cadena y se le da formato de lista
      muestra= str(resp)
      salto=muestra.replace('),', '\n')
      remove=["(u",",)","'","[", "]", ","]
      lista_ean=salto.translate(None,' '.join(remove))
    return lista_ean  
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def _obtener_codigos( self, cr, uid, lista ) :
    """
    Metodo que obtiene la informacion del producto y el codigo de barras apartir del codigo del producto e inserta los datos en la tabla listado.
    * Argumentos OpenERP: [cr]
    @param lista: lista de codigos
    @return bool
    """
    listado = lista.split()
    valores = ' '
    fecha = time.strftime("%y%m%d")
    fecha_imp = time.strftime('%d/%m/%y')
    if ( type( listado ) in ( list, tuple ) ):
      #se eliminan los datos de la tabla listado antes de insertar
      cr.execute(
        """
        DELETE FROM listado_codigo WHERE create_uid=%s
        """,(uid,)
      )
      #se recorre el listado
      for codigo in listado:
        if codigo.isdigit() == True:
          if len(codigo) != 13:
            nombre_produc ='NO ES EAN-13'
            raise osv.except_osv(_( 'Aviso' ),_( 'El código debe contener 13 números sin espacios entre cada dígito' ) )
          else :
            nombre_produc = 'NO ENCONTRADO'
        else :
          raise osv.except_osv(_( 'Aviso!' ),_( 'El código sólo debe contener números' ) )
        #Crea el codigo de Barras
        ean = barcode.get('ean13', codigo, writer=barcode.writer.ImageWriter())
        # Genera el archivo
        ruta = '/tmp/ean_'+ str(codigo)
        f = open(ruta , 'wb')
        #se crea la imagen y se guarda en la ruta especifica
        almacena = ean.write(f)
        #si no encuentra el producto insertar
        no_encontrado = (nombre_produc, codigo, 0.0, ruta, fecha, '0.00', str(fecha_imp), uid, 'No' )
        #se ejecuta la consulta en la tabla productos
        cr.execute(
        """
          SELECT upper(name), ean13, list_price, default_code  
          FROM product_template t
          INNER JOIN product_product p
          ON t.id = p.product_tmpl_id
          WHERE p.active = true and
          ean13 = %s
          order by p.id desc
          limit 1
        """,(codigo,)
        )
        resultado = cr.fetchone()
        #se valida que el precio tenga decimales
        num = 0
        decimales =''
        precio=[]
        if resultado != None and type( resultado ) in ( list, tuple ) and resultado[2] != 0 :
          p = str(resultado[2])
          precio=p.split(".")
          decimales = str(precio[1])
          num = len(decimales)
        valores = (
                    ( resultado[0], resultado[1], (resultado[2]), ruta, fecha,
                     (
                      ( resultado[2] ) if num == 2 and precio[1] > 9  else (str(resultado[2])+'0')), str(fecha_imp),uid, resultado[3]
                     )
                    if type( resultado ) in ( list, tuple ) and resultado != None else no_encontrado
                  )
        #se insertan los nuevos datos a la tabla listado_codigo
        cr.execute(
          """
          INSERT INTO listado_codigo
          (descripcion, cod_barras, precio, ruta_codigo, fecha, precio_str, fecha_str, create_uid, referencia )
          VALUES (%s::varchar(24), %s, %s, %s, %s, %s, %s, %s, %s)
          """, valores )
      return True
    else :
      return False

	### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
	###                                                                                                                 ###
	###                                       Atributos Básicos del Modelo OpenERP                                      ###
	###                                                                                                                 ###
	### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###

  #Nombre del Modelo
  _name = 'wizard_fechas'
  
  _columns = {
    
  # ==========================  Campos OpenERP Básicos (integer, char, text, float, etc...)  ======================== #
    'fecha_inicial':fields.date("Fecha del cambio", required=False),
    'agregar':fields.boolean("Añadir mas códigos", required=False),
    'listado':fields.text("Lista de codigos", store = False, required=False),

  # ======================================  Relaciones OpenERP [one2many](o2m) ====================================== #
  
  }

  #Valores por defecto de los elementos del arreglo [_columns]
  _defaults = {

  }
   
  #Reestricciones desde código
  _constraints = [ ]

  #Reestricciones desde BD
  _sql_constraints = [ ]

wizard_fechas()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
