# -*- coding: utf-8 -*-

{
  'name': 'SM Reports',
  'version': '1.0',
  'category': 'SUPERMAS',
  'author': 'SUPERMAS',
  'maintainer': 'SUPERMAS',
  'website': 'http://www.supermas.mx',
  'installable': True,
  'active': False,
  'description': 'Módulo SM Reports - Modulo para mostrar reportes',
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
    'move_stock_user/wizard/wizard_move_stock_user.xml',
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