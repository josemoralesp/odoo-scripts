#!/usr/bin/env python
#-*- coding:utf- -*-
# -*- coding: iso-8859-1 -*-
import xmlrpclib
import re
import os
import re
import time
import datetime
import oerplib
import xlrd
from xlrd import open_workbook
import xlwt
##############################################################################
# constants declaration
##############################################################################

HOST=''
PORT=
DB=''
USER=''
PASS='---'

conec = oerplib.OERP(
            server=HOST,
            database=DB,
            port=PORT,
            )  

conec.login(USER,PASS)


def xlrd_to_date(cv):
    if not str(cv).isalpha() and len(str(cv)) > 1:
        from1900to1970 = datetime(1970,1,1) - datetime(1900,1,1) + timedelta(days=2)
        print cv
        value = date.fromtimestamp( int(cv) * 86400) - from1900to1970
        print value
        return value

def get_category(conec,name):
    
    categ_id = conec.search('product.category',[('name','=',name)])
    print categ_id 
    return categ_id and categ_id[0]
    
    
def create_or_update_product(xls):

    company_id = conec and conec.user and conec.user.company_id and conec.user.company_id.id
    file = open_workbook(xls)
   
    sheet = file.sheet_by_index(0)
    for ind in range(sheet.nrows):
        
        value = sheet.row_values(ind+1)
        
        product_id = conec.search('product.product',[('default_code','=',value[4])])
        print 'code',value[4]
        print 'actualizando producto',value[7]
        product_brw = product_id and conec.browse('product.product',product_id[0])
        print 'product_brw',product_brw 
        cost_id = product_brw and product_brw.property_cost_structure and product_brw.property_cost_structure.id  or conec.create('cost.structure',{'type':'v','description':value[7],'cost_ult':value[11]})
        print 'cargado el cost',cost_id
        product  = product_id and  {
       
            'name':value[7],
            'ean13':value[6] and len(str(int(value[6])).strip()) == 13 and str(int(value[6])) or product_brw.ean13 ,
            'upc': value[6] and value[7].find('ACCENTS') < 0 and len(str(int(value[6])).strip()) == 12 and str(int(value[6])) or product_brw.upc, 
            'type': 'product',
            'company_id':False,
            #'cost_method': 'standar',
            'supply_method':'buy',
            'procure_method':'make_to_order',
            '%s'%(product_brw.property_cost_structure and 'cost_ult' or 'property_cost_structure'): product_brw.property_cost_structure and value[11]  or cost_id,
        
        }
        print 'listo diccionario'
        print 'product_id',product_id 
        product_id and conec.write('product.product',product_id,product)
        print 'guarde'
            
            
            
            
create_or_update_product('/home/openerp/Descargas/inventario_inicial Max Tovar (1).xls')

