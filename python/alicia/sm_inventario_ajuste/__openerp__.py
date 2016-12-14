# -*- coding: utf-8 -*-

{
  'name': 'SM Ajuste Inventario',
  'version': '1.0',
  'category': 'SUPERMAS',
  'author': 'SUPERMAS',
  'maintainer': 'SUPERMAS',
  'website': 'http://www.supermas.mx',
  'installable': True, 
  'active': False,
  'description': 'Módulo Ajuste Inventario - Modulo para el Ajustar Inventario por Productos',
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
    'secciones/inventario_registro/inventario_registro_view.xml',
    'secciones/inventario_ajuste/inventario_ajuste_view.xml',
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