# -*- coding: utf-8 -*-

{
  'name': 'SM Hardware',
  'version': '1.0',
  'category': 'SUPERMAS',
  'author': 'SUPERMAS',
  'maintainer': 'SUPERMAS',
  'website': 'http://www.supermas.mx',
  'installable': True, 
  'active': False,
  'description': 'Módulo Hardware - Modulo para el inventario de hardware',
  #This model depends of BASE OpenERP model...
  'depends': [
    'base',
    'board',
  ],
  #XML imports
  'data': [
    
    #------------------------------------------------------------------------------------------------------------------------------------------------#
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::: XML PARA MODELOS DEL SISTEMA ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
    #------------------------------------------------------------------------------------------------------------------------------------------------#
    
    #Archivo principal de menús
    'menus.xml',
     'secciones/hardware/hardware_views.xml',
     'secciones/administracion/catalogos/cat_dispositivos/cat_dispositivos.xml',
     'secciones/administracion/sucursal/sucursal.xml',
  ],
  'demo_xml': [
               ],
  'update_xml': [
                  ],
  'active': False,
  'application': True,
  'installable': True,
  'auto_install': False,
}