# -*- coding: utf-8 -*-

{
  #Características del modulo generales del modulo.
  'name': 'SM Hardware',
  'version': '2.0',
  'category': 'SUPERMAS',
  'author': 'SUPERMAS',
  'maintainer': 'SUPERMAS',
  'website': 'http://www.supermas.mx',
  'installable': True,
  'active': False,
  'description': 'Módulo Hardware - Modulo para el inventario de hardware y mantenimiento',
  #Módulos de los cual les depende su funcionamiento.
  'depends': [
    'base',
    'board',
    'hr',
    'web',
  ],
  #Importación de las vistas del modulo
  'data': [

    #------------------------------------------------------------------------------------------------------------------------------------------------#
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::: XML PARA MODELOS DEL SISTEMA ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
    #------------------------------------------------------------------------------------------------------------------------------------------------#

    #Archivo principal de menús
    'menus.xml',
    'secciones/hardware/hardware_views.xml',
    'secciones/administracion/catalogos/cat_dispositivos/cat_dispositivos.xml',
    'secciones/administracion/sucursal/sucursal.xml',
    'secciones/maintenance/maintenance_view.xml',
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