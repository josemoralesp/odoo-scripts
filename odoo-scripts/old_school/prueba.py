#!/usr/bin/env python
#-*- coding:utf-8 -*-
# -*- coding: iso-8859-1 -*-
import xmlrpclib
import csv
import re
import _mssql
import os
import re


##############################################################################
# constants declaration
##############################################################################

#~ HOST=''
HOST=''
#~ PORT=1
PORT=
DB=''
USER=''
PASS=''
#~ PASS=''
url ='http://%s:%d/xmlrpc/' % (HOST,PORT)
print "url",url
common_proxy = xmlrpclib.ServerProxy(url+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')
os.popen('touch error_de_partner_customer.txt')
os.popen('touch error_de_partner_customer.csv')
os.popen('touch error_de_partner_suppliers.txt')
os.popen('touch error_de_partner_suppliers.csv')
os.popen('touch product_error.csv')
### login to server
uid = common_proxy.login(DB,USER,PASS)

address_id = object_proxy.execute(DB, uid, PASS,'fiscal.requirements.config','create',{ 'vat':'123456789',
        'name':'Casa',
        'add':'cosa',
        'vat_subjected': 'True' })

print "address_id",address_id

partner = object_proxy.execute(DB, uid, PASS,'fiscal.requirements.config','read', 1,[])

print "partner",partner

if __name__ == '__main__':

    print "hola"

    print 'Hemos terminado con exito'


#~ product_obj.write(cr,uid,[product_id],{'seller_ids':[(6,0,[record_id])]})
