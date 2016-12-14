# -*- coding: utf-8 -*-

{
  'name': 'SM Merma',
  'version': '1.1',
  'category': 'SUPERMAS',
  'author': 'SUPERMAS',
  'maintainer': 'SUPERMAS',
  'website': 'http://www.supermas.mx',
  'installable': True, 
  'active': False,
  'description': 'Módulo Merma - Modulo para el control de Mermas',
  #This model depends of BASE OpenERP model...
  'depends': [
    'base',
    'stock',
    'hr',
    'stock_location',
    
  ],
  #XML imports
  'data': [
    
    #------------------------------------------------------------------------------------------------------------------------------------------------#
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::: XML PARA MODELOS DEL SISTEMA ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
    #------------------------------------------------------------------------------------------------------------------------------------------------#
    
    #Archivo principal de menús
    'menus.xml',
    'secciones/merma_seleccion/merma_seleccion.xml',
    'secciones/wizard_productos/merma_wizard_productos.xml',
    'secciones/merma/merma.xml',
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