# -*- coding: utf-8 -*-

######################################################################################################################################################
#  @version     : 1.0                                                                                                                                #
#  @autor       : SUPERMAS-ARC                                                                                                                       #
#  @creacion    : 2015-05-12 (aaaa/mm/dd)                                                                                                            #
#  @linea       : Maximo 150 chars                                                                                                                   #
######################################################################################################################################################

#OpenERP imports
from osv import fields, osv



#Modulo :: 
class cat_dispositivos( osv.osv ) :
	
	
	### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
	###                                                                                                                                              ###
	###                                                  Atributos basicos de un modelo OPENERP                                                      ###
	###                                                                                                                                              ###
	### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
	
	#Nombre del modelo
	_name = 'cat_dispositivos'
	
	#Nombre de la tabla
	_table = 'cat_dispositivos'
	
	#Nombre de la descripcion al usuario en las relaciones m2o hacia este módulo
	_rec_name = 'descripcion'
	
	#Cláusula SQL "ORDER BY"
	_order = 'descripcion'


	_columns = {
		
		# =========================================  OpenERP Campos Basicos (integer, char, text, float, etc...)  ====================================== #
		
		'clave':fields.integer("Clave", required=False),
		'descripcion' : fields.char( 'Nombre', size = 255, required = True ),
		'codigo' : fields.char( 'Código', size = 3, required = True  ),
		'activo' : fields.boolean( 'Activo(a)' ),
	}
	
	#Valores por defecto de los campos del diccionario [_columns]
	_defaults = {
		'activo' : True,
	}
	
	#Restricciones de BD (constraints)
	_sql_constraints = []
	
	
	#Restricciones desde codigo
	_constraints = []
	

cat_dispositivos()
