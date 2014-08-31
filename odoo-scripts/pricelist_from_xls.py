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
PORT=8069
DB=''
USER='soporte'
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
    file_log = xlwt.Workbook()
    sheet_log = file_log.add_sheet('Log')
    sheet_error = file_log.add_sheet('Error')
    
    file = open_workbook(xls)
   
    sheet = file.sheet_by_index(0)
    
    price1 = False
    price2 = False
    price3 = False
    price4 = False
    price5 = False
    
    item1 = []
    item2 = []
    item3 = []
    item4 = []
    item5 = []
    
    
    for ind in range(sheet.nrows):
        
        
        
        
        try:
            
            value = sheet.row_values(ind)
            if not price1 and not price2 and not price3 and not price4 and not price5:
                print 'value1',value[1]
                price1 = conec.search('product.pricelist',[('name','=',value[1])])
                print 'orice1',price1
                price2 = conec.search('product.pricelist',[('name','=',value[2])])
                price3 = conec.search('product.pricelist',[('name','=',value[3])])
                price4 = conec.search('product.pricelist',[('name','=',value[4])])
                price5 = conec.search('product.pricelist',[('name','=',value[5])])
                
                
                price1 = price1 and conec.browse('product.pricelist',price1[0])
                price2 = price2 and conec.browse('product.pricelist',price2[0])
                price3 = price3 and conec.browse('product.pricelist',price3[0])
                price4 = price4 and conec.browse('product.pricelist',price4[0])
                price5 = price5 and conec.browse('product.pricelist',price5[0])
    
            #version_id.items_id      price_discoun  sequence    name    product_id
            
            product_id = conec.search('product.product',[('default_code','=',value[0])])
        
            if product_id:
                for i in range(1,6):
                    eval('item%s'%i).append((0,0,{
                                        'sequence':2,
                                        'product_id': product_id and product_id[0],
                                        'price_discount':value[i]
                                                }))
        except Exception, e:
            print 'error',e

    
    e = 0
    for i in [price1,price2,price3,price4,price5]:
        e+=1
        [conec.write('product.pricelist.version',[d.id],{'items_id':eval('item%s'%e)}) for d in i.version_id ]
                
    
create_or_update_product('/home/openerp/Descargas/tarifas_versiones.xls')

