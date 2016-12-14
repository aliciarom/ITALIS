# coding: utf-8

#########################################################################################################################
#  @version  : 1.0                                                                                                     #
#  @autor    : Alicia Romero                                                                                            #
#  @creacion : 2015-09-09 (aaaa/mm/dd)                                                                                  #
#  @linea    : Máximo, 121 caracteres                                                                                   #
#  @descripcion: Se genera un reporte con los datos de los usuarios que realizaron movimientos en almacen               #
#########################################################################################################################

#Importando las clases necesarias
import time
from datetime import datetime
from osv import fields, osv
from openerp.tools.translate import _

#Modelo
class wizard_move_stock_user(osv.osv_memory):
 
  #Descripcion tipo consulta
  _description = 'Wizard stock move'
  
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS                                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// 
  ### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                 ###
  ###                 Definicion de Funciones para "Imprimir Reporte"                                                 ###
  ###                                                                                                                 ###
  ### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  
  #----------------------------------------------------------------------------------------------------------------------
  def obtenerReporte(self, cr, uid, ids,context = { } ) :
    """
    Metodo para imprimir el reporte en formato PDF
    * Argumentos OpenERP: [cr, uid, ids, context]
    @return dict 
    """
    res = {}
    if context is None:
        context = {}
    data = {}
    data['ids'] = context.get( 'active_ids', [] )
    data['model'] = context.get( 'active_model', 'ir.ui.menu' )
    data['form'] = self.read( cr, uid, ids, ['ean13', 'month', 'year_previous', 'date_now','select_option'] )[0]
    
    data['form'].update( self.read( cr, uid, ids, ['ean13', 'month','year_previous', 'date_now','select_option'], context = context )[0])
    
    #Inicializando la variable datas, con el modelo del catalogo
    datas = {
        'ids': [],
        'model': 'stock.move',
        'form': data,
    }
    #Return el nombre del reporte que aparece en el service.name y el tipo de datos report.xml
    return {
        'type': 'ir.actions.report.xml',
        'report_name': 'move_stock_user',
        'datas': datas,
        'nodestroy': True,
    }

	### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
	###                                                                                                                 ###
	###                                       Atributos Básicos del Modelo OpenERP                                      ###
	###                                                                                                                 ###
	### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###

  #Nombre del Modelo
  _name = 'wizard_move_stock_user'
  
  _columns = {
    
  # ==========================  Campos OpenERP Básicos (integer, char, text, float, etc...)  ======================== #
   'date_now':fields.date("Day", required=False),
   'ean13': fields.char('Ean13', size=13, required=True),
   'select_option' : fields.selection(
      (
        ('x_month','Month'),
        ( 'x_day', 'Day' ),
      ),
      'Search for', required=True
    ),
   'month':fields.selection([('01','January'), ('02','February'), ('03','March'), ('04','April'),
            ('05','May'), ('06','June'), ('07','July'), ('08','August'), ('09','September'),
            ('10','October'), ('11','November'), ('12','December')], 'Month'),
   'year_previous': fields.boolean("last year?"),

  }

  #Valores por defecto de los elementos del arreglo [_columns]
  _defaults = {
   # 'date_now': lambda *a: time.strftime('%Y-%m-%d'),
   # 'select_option':lambda *a: 'x_month'
  }
   
  #Reestricciones desde código
  _constraints = [ ]

  #Reestricciones desde BD
  _sql_constraints = [ ]

wizard_move_stock_user()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
