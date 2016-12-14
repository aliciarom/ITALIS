# coding: utf-8

#########################################################################################################################
#  @version  : 1.0                                                                                                      #
#  @autor    : Alicia Romero                                                                                            #
#  @creacion : 2015-06-24 (aaaa/mm/dd)                                                                                  #
#  @linea    : Máximo, 121 caracteres                                                                                   #
#  @descripcion: auxiliar de contabilidad                                                                               #
#########################################################################################################################

#Importando las clases necesarias
import time
from datetime import date
from osv import fields, osv
from openerp.tools.translate import _
#para crear la hoja de calculo
import xlwt

import base64
import tempfile

#Modelo
class auxiliar_contable(osv.osv_memory):
 
  #Descripcion tipo consulta
  _description = 'auxiliar de contabilidad'
  
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS                                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  
  def _obtener_periodo( self, cr, uid, ids, context = None ):
    """
    Metodo para obtener por defecto el id del periodo anterior dependiendo de la fecha actual
    * Argumentos OpenERP: [cr, uid, ids, context]
    @return int
    """   
    self.query = ""
    per_id=''
    carry=0
    current_date=date.today()
    new_month=current_date.month-1
    if new_month == 0 :
      new_month=12
      carry=1
    current_date=current_date.replace(year=current_date.year-carry, month=new_month, day=1)
    self.query = str(current_date)
    cr.execute(
      """
      SELECT id
      FROM account_period
      WHERE date_start = '"""+ self.query +"""'
      """)
    registro = cr.fetchone()
    if registro != None and type( registro ) in ( list, tuple ):
      if (len( registro ) > 0 ):
      #Obteniendo el ID del periodo
        per_id = registro[0]
    else:
      cr.execute(
      """
      SELECT id
      FROM account_period
      ORDER BY id DESC
      """)
      registro = cr.fetchone()
      per_id = registro[0]
    return per_id
  #--------------------------------------------------------------------------------------------------------------------------------------------------- 
  def _creaworksheet(self, cr, uid, ids, worksheet):

    style_title = xlwt.easyxf('pattern: pattern solid, fore_colour red; '
                              'font: colour white, bold True; align: vert centre;')
    

    if worksheet :
      #Se crean los nombres de las columnas
      worksheet.write(0,0,'FECHA', style_title)
      worksheet.write(0,1,'CREACION', style_title)
      worksheet.write(0,2,'DEBITO', style_title)
      worksheet.write(0,3,'CREDITO', style_title)
      worksheet.write(0,4,'NOMBRE', style_title)
      worksheet.write(0,5,'DESCRIPCION', style_title)
      worksheet.col(1).width = 30 * 256
      worksheet.col(4).width = 40 * 256
      worksheet.col(5).width = 50 * 256
      return True
    
    return False
  
  #---------------------------------------------------------------------------------------------------------------------------------------------------     
  def obtenerXlwt( self, cr, uid, ids, context = None ):
    """
    Metodo para imprimir el reporte en formato .xlsx hojas de cálculo
    * Argumentos OpenERP: [cr, uid, ids, context]
    @return dict 
    """
    #objeto del modelo
    obj=self.pool.get( self._name )
    datos=obj.browse( cr, uid, ids[0] )
    self.query = ""
    cuenta=''
    namee=''
    tipo_name=''
    bandera=False
    path='Auxiliar.xls'
    if datos.account_id != 0:
      cuenta=str(datos.account_id.id)
      self.query = "AND aml.account_id = " + cuenta
      
      if datos.por_periodo == True :
        periodo_id_init=datos.period_id.id
        tipo_name='el periodo seleccionado'
        periodo_fin_id = datos.period_fin_id.id
        if periodo_id_init <= periodo_fin_id :
          periodo_id_init=str(periodo_id_init)
          periodo_fin_id=str(periodo_fin_id)
          self.query = self.query + " AND aml.period_id BETWEEN " + periodo_id_init + " AND " + periodo_fin_id
          print self.query
        else:
          periodo_id_init=str(periodo_id_init)
          periodo_fin_id=str(periodo_fin_id)
          self.query = self.query + " AND aml.period_id BETWEEN " + periodo_fin_id + " AND " + periodo_id_init
        bandera=True
      else:  
        if datos.rango_fechas == True :
          inicio = datos.fecha_inicio
          tipo_name = 'las fechas seleccionadas'
          fin = datos.fecha_fin
          self.query = self.query + " AND aml.create_date BETWEEN " + "'" + inicio + " 06:00:01"+ "'" + " AND " + "'" + fin + " 05:59:59"+ "'"
          bandera=True
        
      if bandera == True:
        cr.execute(
            """
              SELECT 
              aml.date AS date,
              aml.create_date AS create_d,
              aml.debit AS debit,
              aml.credit AS credit,
              aml.name AS name,
              acc.name AS nombre
              FROM account_move_line aml
              INNER JOIN account_account acc
              ON aml.account_id = acc.id
              WHERE  aml.state = 'valid'
              """+ self.query +"""
              ORDER BY aml.date ASC
            """)
        aux = cr.fetchall()
        if type( aux ) in ( list, dict) :
          #objeto que crea el libro de trabajo con el constructor Workbook()
          workbook = xlwt.Workbook()
          #El objeto de libro llama al método add_sheet() para agregar una nueva hoja de cálculo
          worksheet = workbook.add_sheet('Cuenta por Periodo')
          style0 = xlwt.easyxf('font: name Arial, color-index black', num_format_str='#,##0.00')
          style1 = xlwt.easyxf(num_format_str='DD-MM-YY')
          styleNo = xlwt.easyxf('font: name Arial, color-index red', num_format_str='#,##0.00')
    
          if ( len( aux ) > 0 ) :
            row = 1
            col = 0
            num=0
            n=1
            fecha =aux[0][0]
            num_mess=fecha.split("-")
            siguiente = int(num_mess[1]) + 1 
            creado=self._creaworksheet(cr, uid, ids, worksheet)
            titul=''
            for date, create_d, debit, credit, name, nombre in (aux):
              num_mes=date.split("-")
              mes = int(num_mes[1])
              anio = int(num_mes[0])
              
              if mes == siguiente :

                n+=1
                siguiente = mes + 1
                period= str(num_mes[1]) +'-'+str(num_mes[0])
                worksheet = workbook.add_sheet('Cuenta por Periodo ' + str(period))
                creado=self._creaworksheet(cr, uid, ids, worksheet)
                if creado == True :
                  row = 1
                  col = 0
                else:
                  break  

              worksheet.write(row, col, date, style0)
              worksheet.write(row, col + 1, create_d, style1)
              worksheet.write(row, col + 2, debit, style0)
              worksheet.write(row, col + 3, credit, style0)
              worksheet.write(row, col + 4, name, style0)
              worksheet.write(row, col + 5, nombre.title(), style0)
              row += 1
              num += 1    
              titul=nombre
              
            titul=titul.split()
            namee='Auxiliar_'+str(titul[0]).capitalize()+'.xls'
          else:
              raise osv.except_osv(_( '¡Aviso!' ),_( 'No se encontraron datos en ' + tipo_name) )
              # worksheet.write(1, 0, '* No se encontraron datos en la busqueda *', styleNo)
      else:
        raise osv.except_osv(_( 'Aviso' ),_( 'Por favor de seleccionar una de las opciones de búsqueda: Por Periodo ó Por Rango de Fechas' ) )

    print namee
    # guarda el archivo en la ruta especificada      
    with tempfile.NamedTemporaryFile(delete=False) as fcsv:
        workbook.save(fcsv.name)
    with open(fcsv.name, 'r') as fname:
        data1 = fname.read()
    
    self.write(cr, uid, ids, {
              'state': 'get',
              'report_name': namee,
              'report_xls': base64.encodestring(data1),
          }, context=context)
      
    this = self.browse(cr, uid, ids)[0]
    return {
              'type': 'ir.actions.act_window',
              'view_type': 'form',
              'view_mode': 'form',
              'res_id': this.id,
              'views': [(False, 'form')],
              'res_model': 'auxiliar_contable',
              'target': 'new',
          }
  
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def onchange_periodo( self, cr, uid, ids, por_periodo) :
    """
    Evento OnChange del campo "por_periodo" con etiqueta "Por periodo" 
    que regresa False al campo rango_fechas
    * Para OpenERP [onchange]
    * Argumentos OpenERP: [cr, uid, ids, por_periodo, rango_fechas ]
    @param key: (string) por_periodo
    @return dict
    """
    if por_periodo == True:
      return {
        'value' : {
          'rango_fechas' : False,
        }
      }
    return { 'value' : {} }
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def onchange_rango( self, cr, uid, ids, rango_fechas) :
    """
    Evento OnChange del campo 'rango_fechas' con etiqueta 'Por Rango de fechas'
    que regresa False al campo por_periodo
    * Para OpenERP [onchange]
    * Argumentos OpenERP: [cr, uid, ids, por_periodo, rango_fechas ]
    @param key: (string) rango_fechas
    @return dict
    """
    if rango_fechas == True:
      return {
        'value' : {
          'por_periodo' : False ,
        }
      }
    return { 'value' : {} }
  ### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                 ###
  ###                                       Atributos Básicos del Modelo OpenERP                                      ###
  ###                                                                                                                 ###
  ### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###

  #Nombre del Modelo
  _name = 'auxiliar_contable'
  
  _columns = {
    
  # ==========================  Campos OpenERP Básicos (integer, char, text, float, etc...)  ======================== #
    'rango_fechas': fields.boolean("Por Rango de Fechas"),
    'por_periodo': fields.boolean("Por Periodo"),
    'fecha_inicio':fields.date("Fecha inicio", required=True),
    'fecha_fin':fields.date("Fecha fin", required=True),
    
    # ======================================  Dowload ====================================== #
    'state': fields.selection([ ('choose', 'Choose'),
                                ('get', 'Get')]),
    'report_name': fields.char('File name', size=128,
                                readonly=True, help='This is File name'),
    'report_xls': fields.binary( 'File', readonly=True, help='You can export file'),

  # ======================================  Relaciones OpenERP [one2many](o2m) ====================================== #
    'period_id': fields.many2one('account.period', 'Periodo inicial', required=True),
    'period_fin_id': fields.many2one('account.period', 'Periodo final', required=True),
    'account_id': fields.many2one('account.account', 'Cuenta', required=True),
  }

  #Valores por defecto de los elementos del arreglo [_columns]
  _defaults = {
    'state': 'choose',
    'period_id': _obtener_periodo,
    'period_fin_id': _obtener_periodo,
    'fecha_inicio': lambda *a: time.strftime('%Y-01-%m'),
    'fecha_fin': lambda *a: time.strftime('%Y-01-%m'),
  }
auxiliar_contable()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: