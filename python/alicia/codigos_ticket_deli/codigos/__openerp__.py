# -*- coding: utf-8 -*-

{
  'name': 'SM Etiquetas',
  'version': '0.6.1',
  'category': 'SUPERMAS',
  'author': 'SUPERMAS',
  'maintainer': 'SUPERMAS',
  'website': 'http://www.supermas.mx',
  'installable': True, 
  'active': False,
  'description': 'Módulo: SM Etiquetas - Generador de Etiquetas- El módulo requiere de la instalación especial de la libreria pyBarcode enlace: https://pypi.python.org/pypi/pyBarcode',
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
     'listado_codigo/listado_codigo_view.xml',
     'wizard/wizard_codigo_view.xml',
     'wizard/wizard_fechas_view.xml',
     'wizard/wizard_deli_view.xml',
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
