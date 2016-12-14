# -*- coding: utf-8 -*-

######################################################################################################################################################
#  @version     : 1.0                                                                                                                                #
#  @autor       : SUPERMAS-ARC                                                                                                                       #
#  @creacion    : 2015-05-15 (aaaa/mm/dd)                                                                                                            #
#  @linea       : Maximo 150 chars                                                                                                                   #
######################################################################################################################################################

#OpenERP imports
from osv import fields, osv

#Modulo :: 
class sucursal( osv.osv ) :
	
	
	### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
	###                                                                                                                                              ###
	###                                                  Atributos basicos de un modelo OPENERP                                                      ###
	###                                                                                                                                              ###
	### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
	
	#Nombre del modelo
	_name = 'sucursal'
	
	#Nombre de la tabla
	_table = 'sucursal'
	
	#Nombre de la descripcion al usuario en las relaciones m2o hacia este módulo
	_rec_name = 'codigo'
	
	#Cláusula SQL "ORDER BY"
	_order = 'codigo'


	_columns = {
		
	# =========================================  OpenERP Campos Basicos (integer, char, text, float, etc...)  ====================================== #
	
	'clave':fields.integer("Clave", required=False),
	'sucursal' : fields.char( 'Sucursal', size = 80, required = True ),
	'direccion' : fields.char( 'Dirección', size = 100, required = False  ),
	'telefono':fields.integer("Telefono", size = 10, required=False),
	'municipio' : fields.char( 'Municipio', size = 100, required = False  ),
	'estado_pais' : fields.char( 'Estado', size = 50, required = False  ),
	'codigo' : fields.char( 'Código', size = 4, required = True  ),
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
	

sucursal()
