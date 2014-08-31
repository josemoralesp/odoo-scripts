#!/usr/bin/env python
#-*- coding:utf- -*-
# -*- coding: iso-8859-1 -*-
import xmlrpclib
import csv
import re
import os
import re
import time
import datetime

##############################################################################
# constants declaration
##############################################################################

HOST=
#~ HOST='localhost'
HOST2=
#~ PORT=18069
PORT=8069
DB=
USER=
PASS=


PORT2=8069
DB2=
USER2=
PASS2=



#~ PASS='1'
url ='http://%s:%d/xmlrpc/' % (HOST,PORT)
url2 ='http://%s:%d/xmlrpc/' % (HOST2,PORT2)
print "url",url
common_proxy = xmlrpclib.ServerProxy(url+'common')
common_proxy2 = xmlrpclib.ServerProxy(url2+'common')

object_proxy = xmlrpclib.ServerProxy(url+'object')
object_proxy2 = xmlrpclib.ServerProxy(url2+'object')
### login to server
uid = common_proxy.login(DB,USER,PASS)
uid2 = common_proxy2.login(DB2,USER2,PASS2)
print "uid",uid 
print "object_proxy",object_proxy 
print "antes"
account_ids = object_proxy.execute(DB, uid, PASS,'account.account','search',[])
print "despues"
print "account_ids",account_ids

def type_field(model,field):

    field = object_proxy.execute(DB, uid, PASS,model,'fields_get',field)
    
    return field or {}


for account in object_proxy.execute(DB, uid, PASS,'account.account','read',account_ids,[]):
    
    field = type_field('account.account','user_type')
    field_relation = field.get('user_type',{}).get('relation',False)
    
    user_type = account.get('user_type',False) and field_relation and  object_proxy.execute(DB2, uid2, PASS2,field_relation,'search',[('name','=',account.get('user_type',False)[1])]) 
    print 'account',account
    if not user_type:
        data = account.get('user_type',False) and object_proxy.execute(DB, uid, PASS,field_relation,'copy_data',account.get('user_type',False)[0])
        user_type = object_proxy.execute(DB2, uid2, PASS2,field_relation,'create',data) 
    
    company_id = account.get('company_id',False) and object_proxy.execute(DB2, uid2, PASS2,'res.company','search',[('name','=',account.get('company_id',False)[1])]) 
    currency_id = account.get('company_id',False) and object_proxy.execute(DB2, uid2, PASS2,'res.company','search',[('name','=',account.get('currency_id',False)[1])]) 
    name = account.get('name',False) and object_proxy.execute(DB2, uid2, PASS2,'account.account','search',[('name','=',account.get('name',False)[1])]) 
    
    if not account.get('parent_id',True) and not name and company_id and currency_id :
        dict_account = {
        'name':account.get('name'),
        'code': account.get('code'),
        'reconcile': account.get('reconcile'),
        'user_type': user_type,
        'company_id': company_id,
        'shortcut': account.get('shortcut'),
        'note': account.get('note'),
        'parent_id': account.get('parent_id'),
        'type': account.get('type'),
        'active': account.get('active'),
        'currency_id': currency_id,
        'level': account.get('level'),
        'currency_mode': account.get('currency_mode'),
        }
        object_proxy.execute(DB2, uid2, PASS2,'account.account','create',dict_account) 
    
    else:
        if company_id and currency_id and not name :
            parent_id = account.get('parent_id',False) and object_proxy.execute(DB2, uid2, PASS2,'account.account','search',[('name','=',account.get('parent_id',False)[1])])  
            dict_account = parent_id and {
                        'name':account.get('name'),
                        'code': account.get('code'),
                        'reconcile': account.get('reconcile'),
                        'user_type': object_proxyuser_type,
                        'company_id': company_id,
                        'shortcut': account.get('shortcut'),
                        'note': account.get('note'),
                        'parent_id': parent_id,
                        'type': account.get('type'),
                        'active': account.get('active'),
                        'currency_id': currency_id,
                        'level': account.get('level'),
                        'currency_mode': account.get('currency_mode'),
                        } or []
            dict_account and object_proxy.execute(DB2, uid2, PASS2,'account.account','create',dict_account) 

if __name__ == '__main__':
   
    print "hola"
   
    print 'Hemos terminado con exito'
