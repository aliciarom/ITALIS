# -*- coding: utf-8 -*-

######################################################################################################################################################
#  @version     : 1.0                                                                                                                                #
#  @autor       : SUPERMAS-ARC                                                                                                                       #
#  @creación    : 2015-08-21                                                                                                                         #
#  @linea       : Maximo 150 chars                                                                                                                   #
######################################################################################################################################################

#OpenERP Imports
from osv import fields, osv
# from datetime import datetime, date
from datetime import datetime, timedelta, date
import math

from openerp import tools, SUPERUSER_ID
from openerp.tools.translate import _

from dateutil import parser
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from openerp.service import web_services

import pytz
import re
import time
from operator import itemgetter

#Modulo ::
class maintenance_equip(osv.osv):
  #----------------------------------------------------------------------------------------------------------------------
  def _obtener_fecha( self, cr, uid, ids ) :
    """
    Devuelve la fecha del sistema
    * Argumentos OpenERP: [cr, uid, ids]
    @return string
    """
    
    return str( datetime.date.today() )
  #----------------------------------------------------------------------------------------------------------------------
  @staticmethod
  def getNextModelFolio( cr, tabla, nombre_campo = 'number' ) :
    """
    Metodo que obtiene el numero de clave siguiente
    * Para OpenERP [field.function]
    * Argumentos OpenERP: [cr, tabla,nombre_campo]
    :return dict
    """ 
    #Consultando cuál sería el nuevo folio
    cr.execute( 'SELECT ( MAX( ' + nombre_campo + ' ) + 1 ) AS next_folio FROM ' + tabla, () )
    registro_consultado = cr.fetchone()
    #Retornando el nuevo folio
    return (
      1
    ) if (
      registro_consultado is None
    ) else (
      1 if ( registro_consultado[0] is None ) else ( int( registro_consultado[0] ) )
    )	

  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS                                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def _func_obtener_informe( self, cr, uid, ids, field_name, arg, context ) :
    """
    Función para el campo "Informacion"
    * Para OpenERP [field.function( ... )]
    * Argumentos OpenERP: [cr, uid, ids, field_name, arg, context]
    @return dict
    """
    result = {}
    for record in self.browse( cr, uid, ids, context ) :
      equipo = ''
      brad = ''
      model = ''
      serial = ''
      if (record.equipo_m2o_id) != 0:
        equipo = str( record.equipo_m2o_id.cat_equipo_m2o_id.descripcion)
        brad = str( record.equipo_m2o_id.brad )
        model = str( record.equipo_m2o_id.model )
        serial = str( record.equipo_m2o_id.serial_number)
        # concatenando
        if model==False:
          modelo=', \n MODEL: No'
        else :
          modelo= ', \n MODEL: '+ model 
        informe = 'Equipment:' + equipo + ', \n BRAD: ' + brad + modelo + ', \n SERIE: ' + serial
        #convirtiendo a mayúsculas
        informe = informe.upper()
        result[record.id] = informe
      #Retornando los resultados evaluados
      return result
    #Función que verifica que la fecha no puede sea porterior a la fecha actual
  #---------------------------------------------------------------------------------------------------------------------------------------------------  
  def _valida_fecha( self, cr, uid, ids, date_system, date ) :
    """
    Función que verifica que la fecha ingresada no debe ser mayor a la fecha actual
    * Argumentos OpenERP: [cr, uid, ids]
    @param fecha_systema: (date) Indica la fecha del sistema
    @param fecha_ingreso: (date) Indica la fecha ingresada
    @return boolean
    """
    
    lista_fechainicio=str( date_system ).split( '-' )
    lista_fechafinal=str( date ).split( '-' )
    #Esta bandera por default es falsa, por si el año escogido es menor al actual
    bandera = False
    
    #Verifica si el año de la fecha es menor al año de la fecha actual
    if int( lista_fechainicio[0] ) > int( lista_fechafinal[0] ) :
      bandera = True
      
    #Verifica si el año de la fecha es igual al año de la fecha actual,ahora debe verifica los meses 
    elif int( lista_fechainicio[0] ) == int( lista_fechafinal[0] ) :
      
        #Verifica si el mes de la fecha es menor al mes de la fecha actual
        if int( lista_fechainicio[1] ) > int( lista_fechafinal[1] ) :
          bandera = True
          
        #Verifica si el mes de la fecha es igual al mes de la fecha actual,ahora debe verifica los días	
        elif int( lista_fechainicio[1] ) == int( lista_fechafinal[1] ) :
            
            #Verifica si el día de la fecha es menor al día de la fecha actual
            dia_inicial=str(lista_fechainicio[2]).split(' ')
            dia_fin=str(lista_fechafinal[2]).split(' ')
            if int( dia_inicial[0] ) >= int( dia_fin[0] ) :
              bandera = True	
            else :
              bandera = False
    return bandera  

  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS ONCHANGE                                                             ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ### 

  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS ORM                                                                  ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  #---------------------------------------------------------------------------------------------------------------------------------------------------  
  def onchange_dates(self, cr, uid, ids, date, duration=False, date_deadline=False, allday=False, context=None):
    """Returns duration and/or end date based on values passed
    @param self: The object pointer
    @param cr: the current row, from the database cursor,
    @param uid: the current user's ID for security checks,
    @param ids: List of calendar event's IDs.
    @param start_date: Starting date
    @param duration: Duration between start date and end date
    @param date_deadline: Ending Datee
    @param context: A standard dictionary for contextual values
    """
    if context is None:
        context = {}

    value = {}

    #-----------------------------------------------------
    if not date:
        return value
    if not date_deadline and not duration:
        duration = 1.00
        value['duration'] = duration

    start = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    if allday: # For all day event
        duration = 24.0
        value['duration'] = duration
        # change date's time to 00:00:00 in the user's timezone
        user = self.pool.get('res.users').browse(cr, uid, uid)
        tz = pytz.timezone(user.tz) if user.tz else pytz.utc
        start = pytz.utc.localize(start).astimezone(tz)     # convert start in user's timezone
        start = start.replace(hour=0, minute=0, second=0)   # change start's time to 00:00:00
        start = start.astimezone(pytz.utc)                  # convert start back to utc
        date = start.strftime("%Y-%m-%d %H:%M:%S")
        value['date'] = date

    if date_deadline and not duration:
        end = datetime.strptime(date_deadline, "%Y-%m-%d %H:%M:%S")
        diff = end - start
        duration = float(diff.days)* 24 + (float(diff.seconds) / 3600)
        value['duration'] = round(duration, 2)
    elif not date_deadline:
        end = start + timedelta(hours=duration)
        value['date_deadline'] = end.strftime("%Y-%m-%d %H:%M:%S")
    elif date_deadline and duration and not allday:
        # we have both, keep them synchronized:
        # set duration based on date_deadline (arbitrary decision: this avoid
        # getting dates like 06:31:48 instead of 06:32:00date_deadline        end = datetime.strptime(date_deadline, "%Y-%m-%d %H:%M:%S")
        diff = end - start
        duration = float(diff.days)* 24 + (float(diff.seconds) / 3600)
        value['duration'] = round(duration, 2)

    return {'value': value}
  #-------------------------------------------------------------------------------------------------------------------------------------------------
  def onchange_fecha( self, cr, uid, ids, date_deadline ) :
    """
    Evento OnChange del campo "date" con etiqueta "Date" que valida que la fecha
    no sea mayor a la actual
    * Para OpenERP [onchange]
    * Argumentos OpenERP: [cr, uid, ids]			
    @param fecha: (date) Fecha
    @return dict
    """
    #Obtener la fecha del sistema
    date_system = self._obtener_fecha( cr, uid, ids )
    bandera = self._valida_fecha( cr, uid, ids, date_system, date_deadline )
    if bandera == False :
      return {
        'value': {
          #Limpia el campo de la fecha
          'date': None,
        },
        'warning':{
          'title': 'Error de captura',
          'message': 'La fecha no puede ser posterior a la fecha actual, favor de verificarla'
        }
      }
    
    return { 'value' : {} }
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def onchange_func(self, cr, uid, ids, equipo_m2o_id):
    if equipo_m2o_id:
      for obj in self.pool.get('equipo').browse(cr, uid, [equipo_m2o_id]):
        return {
          'value': {
            'descripcion': obj.descripcion,
            'nombre_equipo': obj.name_equip,
            'serie_equipo': obj.serial_number,
          }
        }
    return {
          'value': {
            'descripcion': '',
            'nombre_equipo': '' ,
            'descripcion':''
          }
    }
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
    vals['number'] = self.getNextModelFolio( cr, self._table, nombre_campo = 'number' )
    vals['number_order'] = str(vals['number'])
    nuevo_id = super( maintenance_equip, self ).create( cr, uid, vals, context = context )
    return nuevo_id
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                  Atributos basicos de un modelo OPENERP                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  
  #Nombre del modelo
  _name = 'maintenance_equip'
  #Nombre de la tabla
  _table = 'maintenance_equip'
  #Ordenar la vista
  _order = 'number'
 
  _columns = {
    'number' : fields.integer("Number", requiered=False),
    'number_order' : fields.char("Number order", requiered=False),
    #calendar
    'name': fields.char('Description', size=64, required=False ),
    'date': fields.datetime('Maintenance Date'),
    'date_deadline': fields.datetime('Maintenance End Date'),
    'duration': fields.float('Duration'),
    'show_as': fields.selection(
      [
       ('free', 'Free'),
       ('busy', 'Busy')
      ],
      'Show Time as',
    ),
    'allday': fields.boolean('All Day'),
    #----------------------------------------------
    'responsible': fields.char('Responsible', size=100, required=False ),
    'cost_repair': fields.float('Previsto Coste'),
    # SERVICE PERFORMED
    'type_maint' : fields.selection(
      (
        ( 'preventive', 'Preventive' ),
        ( 'corrective', 'Corrective' ),
      ),
      'Type of maintenance',
    ),

    'maintenance_date':fields.date("Maintenance Date", required=False),
    'delivery_date':fields.date("Delivery date", required=False),
    'causes':fields.text("Defects according to the user"),
    'diagnostic':fields.text("Diagnostic"),
    'solution':fields.text("Solution"),
    'piece_change':fields.text("Piece to change"),
    
  # ================================ Relaciones [related] =====================================================================================#
  
    'descripcion': fields.related('equipo_m2o_id', 'descripcion', type="char", relation='equipo', readonly=True, string="Maintenance Group"),
    'nombre_equipo': fields.related('equipo_m2o_id', 'name_equip', type="char", relation='equipo', readonly=True, string="Name"),
    'serie_equipo': fields.related('equipo_m2o_id', 'serial_number', type="char", relation='equipo', readonly=True, string="Serial"),
    'fac_costo_total': fields.related('invoice_m2o_id', 'amount_total', type="float", relation='account.invoice', readonly=True, string="Total Cost"),
    # 'provedor': fields.related('invoice_m2o_id', 'partner_id', type="many2one", relation='account.invoice', readonly=True, string="Provedor"),
    
  # ================================ Relaciones [one2many](o2m) =====================================================================================#
    'equipo_m2o_id': fields.many2one(
      'equipo',
      'Registration Key',
      required = False
    ),
    'invoice_m2o_id': fields.many2one(
      'account.invoice',
      'Invoice',
      required = False
    ),

  # ================================== Campos Function ==============================================================================================#  
    # 'equipo_info' : fields.function(
    #   _func_obtener_informe,
    #   type = 'char',
    #   size = 80,
    #   method = True,
    #   string = 'Device',
    #   store = False,
    #   readonly = True,
    # ),
  }
    
  #Valores por defecto de los campos del diccionario [_columns]
  _defaults = {
    'show_as': 'busy',
    'name' : 'Mantenimiento',
    'allday': False,
  }

#se cierra la clase
maintenance_equip() 


