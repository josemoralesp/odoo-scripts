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

HOST=
PORT=
DB=
USER=
PASS=

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

        value = sheet.row_values(ind)

        if value[0] == 'NUEVO':
            cost_id = conec.create('cost.structure',{'type':'v','description':value[4],'cost_ult':value[7]})
            print 'creanto producto',value[4]
            product = {

                'name':value[4],
                'ean13':len(str(int(value[3])).strip()) == 13 and str(int(value[3])) ,
                'upc': len(str(int(value[3])).strip()) == 12 and str(int(value[3])) ,
                'default_code': value[1],
                'type': 'product',
                #'cost_method': 'standar',
                'supply_method':'buy',
                'procure_method':'make_to_order',
                'categ_id':get_category(conec,value[5]) or 1,
                'property_cost_structure':cost_id,

            }

            conec.create('product.product',product)


        elif value[0] == 'ACTUALIZAR':
            product_id = conec.search('product.product',[('default_code','=',value[1])])
            print 'actualizando producto' ,value[4]
            product  = product_id and  {

                'name':value[4],
                'ean13':len(str(int(value[3])).strip()) == 13 and str(int(value[3])) ,
                'upc': len(str(int(value[3])).strip()) == 12 and str(int(value[3])) ,
                'type': 'product',
                #'cost_method': 'standar',
                'supply_method':'buy',
                'procure_method':'make_to_order',
                'categ_id':get_category(conec,value[5]) or 1,

            }
            product_id and conec.write('product.product',product_id,product)





create_or_update_product('file.xls')

