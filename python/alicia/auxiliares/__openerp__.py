# -*- coding: utf-8 -*-

{
  'name': 'SM Auxiliar',
  'version': '0.5.0',
  'category': 'SUPERMAS',
  'author': 'SUPERMAS',
  'maintainer': 'SUPERMAS',
  'website': 'http://www.supermas.mx',
  'installable': True, 
  'active': False,
  'description': 'Módulo: SM Auxiliar - Auxiliar de contabilidad, Genera un archivo xls, con lo datos de una cuenta especifica, ya sea por periodo o rango de fechas. Requiere de la libreria https://pypi.python.org/pypi/xlwt' ,
  #This model depends of BASE OpenERP model...
  'depends': [
    'base',
    'board',
    'account',
  ],
  #XML imports
  'data': [
    
    #------------------------------------------------------------------------------------------------------------------------------------------------#
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::: XML PARA MODELOS DEL SISTEMA ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
    #------------------------------------------------------------------------------------------------------------------------------------------------#
    
    #Archivo principal de menús
    'menus.xml',
     'wizard/auxiliar_contable.xml',
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
