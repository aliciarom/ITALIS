# -*- coding: utf-8 -*-

######################################################################################################################################################
#  @version     : 1.0                                                                                                                                #
#  @autor       : SUPERMAS-ARC                                                                                                                       #
#  @creación    : 2015-05-21                                                                                                                         #
#  @linea       : Maximo 150 chars                                                                                                                   #
######################################################################################################################################################

#OpenERP Imports
from osv import fields, osv
from datetime import datetime, date
import time

#Modulo ::
class listado_codigo(osv.osv):
  #--------------------------------------------------------Variables Privadas y Publicas--------------------------------------------------------------
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS                                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###


  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                  Atributos basicos de un modelo OPENERP                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  
  #Nombre del modelo
  _name = 'listado_codigo'
  #Nombre de la tabla
  _table = 'listado_codigo'
 
  _columns = {
    'cod_barras' : fields.char("Codigo de Barras", required=False),
    'descripcion':fields.char("Descripción", required=False),
    'precio':fields.float('Precio', required=False),
    'ruta_codigo' : fields.char("Ruta", required=False),
    'fecha':fields.date("Fecha", required=False),
    'precio_str' : fields.char("Precio cadena", required=False),
    'fecha_str':fields.char("Fecha", required=False),
    'referencia':fields.char("Referencia interna", required=False),
  }
    
  #Valores por defecto de los campos del diccionario [_columns]
  _defaults = {
  }

#se cierra la clase
listado_codigo() 


