# coding: utf-8

#########################################################################################################################
#  @version  : 1.1                                                                                                      #
#  @autor    : Alicia Romero                                                                                            #
#  @creacion : 2015-08-01 (aaaa/mm/dd)                                                                                  #
#  @linea    : Máximo, 121 caracteres                                                                                   #
#  @descripcion: Apartir de la inserción de un codigo Ean13 se obtienen los datos del producto y se generan             #
#                las etiquetas                                                                                          #
#########################################################################################################################

#Importando las clases necesarias
import time
from datetime import datetime
from osv import fields, osv
import pooler
from openerp.tools.translate import _
import barcode

#Modelo
class wizard_deli(osv.osv_memory):
 
  #Descripcion tipo consulta
  _description = 'Wizard Deli'
  
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS                                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  #---------------------------------------------------------------------------------------------------------------------------------------------------  
  def obtenerCodigos( self, cr, uid, ids, context = None ):
    """
    Funcion que dependiendo de lo que obtenga el metodo _obtener_codigos genera el archivo para imprimir las etiquetas
    * Argumentos OpenERP: [ cr, uid, ids, context ]
    @param : (cr, uid, ids, context) 
    @return dict
    """
    codigo_deli = str(self.pool.get( self._name ).browse( cr, uid, ids[0] ).cod_number)
    divide_etiquetas = self.pool.get( self._name ).browse( cr, uid, ids[0] ).divide_etiquetas
    codigo_deli2 = ''
    codigo_deli3 = ''
    print divide_etiquetas

    if len(codigo_deli) < 13:
      raise osv.except_osv(_( 'Avisoo' ),_( 'Debe ingresar un código EAN13' ) )
    if divide_etiquetas == True:
      codigo_deli2 = str(self.pool.get( self._name ).browse( cr, uid, ids[0] ).cod_number2)
      codigo_deli3 = str(self.pool.get( self._name ).browse( cr, uid, ids[0] ).cod_number3)
      if len(codigo_deli2) < 13 or len(codigo_deli3) < 13:
        raise osv.except_osv(_( 'Avisoo' ),_( 'Debe ingresar un código EAN13' ) )
    buscar = self._obtener_codigos( cr, uid, codigo_deli, codigo_deli2, codigo_deli3, divide_etiquetas)
    if buscar == True :
        #imprimir reporte
       if context is None:
         context = {}
       data = {}
       data['ids'] = context.get('active_ids', [])
       data['model'] = context.get('active_model', 'ir.ui.menu')
       data['form'] = self.read(cr, uid, ids )[0]
       #Inicializando la variable datas, con el modelo
       datas = {
         'ids': [],
         'model': 'listado_codigo',
         'form': data,
       }
       #Return el nombre del reporte que aparece en el service.name y el tipo de datos report.xml	
       return {
           'type': 'ir.actions.report.xml',
           'report_name': 'sm_etiquetas_deli',
           'datas': datas,
           'nodestroy': True,
       }  
    else :
      return { 'value' : {} }
    
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def _obtener_codigos( self, cr, uid, codigo_deli, codigo_deli2, codigo_deli3, divide_etiquetas ) :
    """
    Metodo que obtiene la informacion del producto y el codigo de barras apartir del codigo del producto e inserta los datos en la tabla listado.
    * Argumentos OpenERP: [cr]
    @param lista: lista de codigos
    @return bool
    """
    listado = []
    numero=1
    valores = ' '
    fecha = time.strftime("%y%m%d")
    fecha_imp = time.strftime('%d/%m/%y')

    if divide_etiquetas == False:
      while numero <= 30:
        # print numero
        listado.append(codigo_deli)
        numero += 1
    else:
      while numero <= 30:

        if numero <=10 :
          listado.append(codigo_deli)
        elif numero >10 and numero <=20 :
          listado.append(codigo_deli2)  
        elif numero >20 :
          listado.append(codigo_deli3)
        numero += 1  

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
        # Genera el archivo
        ruta = 'No se genera codigo de barras'
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
                    (
                      resultado[0], resultado[1],
                      (resultado[2]), ruta,
                      fecha, (( resultado[2] ) if num == 2 and precio[1] > 9  else (str(resultado[2])+'0')),
                      str(fecha_imp), uid, resultado[3]
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
  _name = 'wizard_deli'
  
  _columns = {
    
  # ==========================  Campos OpenERP Básicos (integer, char, text, float, etc...)  ======================== #
   'cod_number':fields.char("Código", size=13, required=True),
   'cod_number2':fields.char("Segundo Código", size=13),
   'cod_number3':fields.char("Tercer Código", size=13),
   'divide_etiquetas':fields.boolean("Añadir otros códigos en la misma hoja", required=False),
   
  # ======================================  Relaciones OpenERP [one2many](o2m) ====================================== #
  
  }

  #Valores por defecto de los elementos del arreglo [_columns]
  _defaults = {
  }
   
  #Reestricciones desde código
  _constraints = [ ]

  #Reestricciones desde BD
  _sql_constraints = [ ]

wizard_deli()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
