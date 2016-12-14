## -*- coding: utf-8 -*-
#########################################################################################################################
#  @version  : 1.0                                                                                                      #
#  @autor    : Supermas ::Alicia Romero                                                                                 #
#  @creacion : 2013-05-31 (aaaa/mm/dd)                                                                                  #
#  @linea    : Maximo, 121 caracteres                                                                                   #
#########################################################################################################################
#Importando las clases
import time
from openerp.report import report_sxw
from openerp.osv import osv
from openerp import pooler

class report_conta_asientoo(report_sxw.rml_parse):
    #variable que define al reporte
    _description = "Reporte que obtiene el asiento contable en facturas de proveedor"
    #---------------------------------------------------------------------------------------------------------------------- 
    def __init__(self, cr, uid, name, context = None):
        super(report_conta_asientoo, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_sumas':self.get_sumas,
        })
    #----------------------------------------------------------------------------------------------------------------------  
    def get_sumas( self, object, ):
      cr = self.cr
      self.cr.execute(
        """
        SELECT sum(debit) AS sum_debito,
        sum(credit) AS sum_credito
        FROM account_move_line
        WHERE move_id = %s
        """,(object,)
      )
      resultado = cr.dictfetchall()
      return resultado
    
############################################################################################################################
report_sxw.report_sxw('report.report_conta_asientoo',
                      'account.move',
                      'addons/account/report/report_conta_asientoo.rml',
                      parser=report_conta_asientoo,
                      header=False )