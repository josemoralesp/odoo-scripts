#!/usr/bin/env python
#-*- coding:utf- -*-
# -*- encoding: utf-8 -*-
import xmlrpclib
import csv
import re
import _mssql
import os
import re
import time
import datetime
import oerplib
##############################################################################
# constants declaration
##############################################################################

HOST=''
PORT=
DB=''
USER='admin'
PASS='admin'


cone1 = oerplib.OERP(
            server=HOST,
            database=DB,
            port=PORT,
            )  

cone1.login(USER,PASS)
print cone1.user.company_id.name
cone1.execute('import.master','crontab_execute',5)
#cone2 = oerplib.OERP(
            #server=HOST,
            #database=DB,
            #port=PORT,
            #)  
#
#cone2.login(USER2,PASS2)
#
#
#
#partner_america_ids = cone1.search('product.category',[])
#for partner in cone1.browse('product.category',partner_america_ids):
    #if partner.property_account_expense_categ and partner.property_account_income_categ:
        #print 'partner.property_account_expense_categ.code',partner.property_account_expense_categ.code
        #print 'partner.property_account_income_categ.code',partner.property_account_income_categ.code
        #
        #property_account_expense_categ = cone2.search('account.account',[('code','=',partner.property_account_expense_categ.code),
                                                                        #('company_id','=',cone2.user.company_id.id)])
                                                                        #
        #property_account_income_categ = cone2.search('account.account',[('code','=',partner.property_account_income_categ.code),
                                                                        #('company_id','=',cone2.user.company_id.id)])
        #
        #dic = {'property_account_income_categ':property_account_income_categ and int(property_account_income_categ[0]),
                #'property_account_expense_categ':property_account_expense_categ and int(property_account_expense_categ[0])}
        #print 'dic',dic
        #break
#property_account_expense_categ and property_account_income_categ and cone2.write('product.category',partner_america_ids,dic)                                                                 
        
#['|',('company_id','child_of',[user.company_id.id]),('company_id','=',False)]




Arrancada 1.5

pagina 12 medio dia (No pasar)





if __name__ == '__main__':
   
    print "hola"
    print 'Hemos terminado con exito'


{'code': '12002', 'reconcile': False, 'user_type': False or [(0,0,{'name':'Gasto','code':'expense','close_method':'none',
                                                                                      'report_type':'expense'})],
             'currency_id': False, 'active': True, 'name': 'INVENTARIO OUT', 'company_id': 'company_id', 'shortcut': False,
             'note': False, 'parent_id': 'search_account(cone2,1000)','level': 2, 'currency_mode': 'current', 'type': 'other'}
