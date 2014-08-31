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
##############################################################################
# constants declaration
##############################################################################

HOST='localhost'
PORT=5252
DB='ilt'
USER='admin'
PASS='admin'

HOST_dest='wise.iltlatam.com'
PORT_dest=8069
DB_dest='ilt'
USER_dest='admin'
PASS_dest='1'



cone1 = oerplib.OERP(
            server=HOST,
            database=DB,
            port=PORT,
            )  

cone1.login(USER,PASS)

cone2 = oerplib.OERP(
            server=HOST_dest,
            database=DB_dest,
            port=PORT_dest,
            )  

cone2.login(USER_dest,PASS_dest)



account_ids = cone1.search('account.account',[('company_id','=',2)])

def type_field(model,field):

    field = cone1.execute(model,'fields_get',field)
    
    return field or {}


for account in cone1.browse('account.account',account_ids):
    
    field = type_field('account.account','user_type')
    field_relation = field.get('user_type',{}).get('relation',False)
    
    user_type = account.user_type and field_relation and  cone2.search(field_relation,[('name','=',account.user_type.name)]) 
    
    if not user_type:
        data = account.user_type and cone1.execute(field_relation,'copy_data',account.user_type.id)
        user_type = cone2.create(field_relation,data) 
        user_type = user_type and [user_type]
    company_id = account.company_id and cone2.search('res.company',[('name','=',account.company_id.name)]) 
    currency_id = account.currency_id and cone2.search('res.company',[('name','=',account.currency_id.name)]) 
    name = cone2.search('account.account',[('code','=',account.code)]) 
    
    if not account.parent_id and not name and company_id:
        print 'crear parect'
        dict_account = {
        'name':account.name,
        'code': account.code,
        'reconcile': account.reconcile,
        'user_type': user_type and user_type[0],
        'company_id': company_id and company_id[0],
        'shortcut': account.shortcut,
        'note': account.note,
        'parent_id': account.parent_id,
        'type': account.type,
        'active': account.active,
        'currency_id': currency_id,
        'level': account.level,
        'currency_mode': account.currency_mode,
        }
        cone2.create('account.account',dict_account) 
    
    else:
        if company_id  and not name :
            parent_id = account.parent_id and cone2.search('account.account',[('code','=',account.parent_id.code)])  
            parent_id = parent_id and parent_id[0]
            dict_account = parent_id and {
                        'name':account.name,
                        'code': account.code,
                        'reconcile': account.reconcile,
                        'user_type': user_type and user_type[0],
                        'company_id': company_id and company_id[0],
                        'shortcut': account.shortcut,
                        'note': account.note,
                        'parent_id': parent_id,
                        'type': account.type,
                        'active': account.active,
                        'currency_id': currency_id,
                        'level': account.level,
                        'currency_mode': account.currency_mode,
                        } or []
            
            print 'dict_account',dict_account
            dict_account and cone2.create('account.account',dict_account) 

if __name__ == '__main__':
   
    print "hola"
   
    print 'Hemos terminado con exito'
