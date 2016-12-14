# -*- coding: utf-8 -*-

{
  'name': 'SM Maintenance',
  'version': '1.1',
  'category': 'SUPERMAS',
  'author': 'SUPERMAS',
  'maintainer': 'SUPERMAS',
  'website': 'http://www.supermas.mx',
  'installable': True, 
  'active': False,
  'description': 'Módulo SM Maintenance - Modulo para el Mantenimiento y Inventario de Equipo',
  #This model depends of BASE OpenERP model...
  'depends': [
    'base',
    'board',
    'hr',
    'account',
  ],
  #XML imports
  'data': [
    
    #------------------------------------------------------------------------------------------------------------------------------------------------#
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::: XML PARA MODELOS DEL SISTEMA ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
    #------------------------------------------------------------------------------------------------------------------------------------------------#
    
    #Archivo principal de menús
    'menus.xml',
     'secciones/administracion/catalogos/cat_tipo_equipo/cat_equipo.xml',
     'secciones/inventory_equip/equipo_views.xml',
     'secciones/maintenance_equip/maintenance_equip.xml',
     # 'secciones/administracion/adjuntos_maintenance/adjuntos_maintenance.xml',

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