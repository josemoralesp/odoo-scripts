#!/usr/bin/env python
#-*- coding:utf- -*-
# -*- coding: iso-8859-1 -*-
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

HOST='openerp.la'
#~ HOST='localhost'
HOST2='localhost'
#~ PORT=18069
PORT=8069
DB='ilt_test'
USER='humberto.arocha'
PASS='$4rocha!'


PORT2=8069
DB2='GRUPO_AMD'
USER2='gquilarque'
PASS2='123'


cone1 = oerplib.OERP(
            server=HOST,
            database=DB,
            port=PORT,
            )  

cone1.login(USER,PASS)

cone2 = oerplib.OERP(
            server=HOST2,
            database=DB2,
            port=PORT2,
            )  

cone2.login(USER2,PASS2)

account_ids = cone1.search('account.account',[('company_id','=',<company_id to export>)])

def type_field(model,field):

    field = cone1.execute(model,'fields_get',field)
    
    return field or {}


for account in cone1.browse('account.account',account_ids):
    
    field = type_field('account.account','user_type')
    field_relation = field.get('user_type',{}).get('relation',False)
    
    user_type = account.user_type and field_relation and  cone2.search(field_relation,[('name','=',account.user_type.name)]) 
    print 'account',account
    
    if not user_type:
        data = account.user_type and cone1.execute(field_relation,'copy_data',account.user_type.id)
        print 'data',data
        user_type = cone2.create(field_relation,data) 
    
    company_id = account.company_id and cone2.search('res.company',[('name','=',account.company_id.name)]) 
    currency_id = account.currency_id and cone2.search('res.company',[('name','=',account.currency_id.name)]) 
    name = cone2.search('account.account',[('code','=',account.code)]) 
    
    if not account.parent_id and not name and company_id and currency_id :
        dict_account = {
        'name':account.name,
        'code': account.code,
        'reconcile': account.reconcile,
        'user_type': user_type,
        'company_id': company_id,
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
        if company_id and currency_id and not name :
            parent_id = account.parent_id and cone2.search('account.account',[('code','=',account.parent_id.code)])  
            parent_id = parent_id and parent_id[0]
            dict_account = parent_id and {
                        'name':account.name,
                        'code': account.code,
                        'reconcile': account.reconcile,
                        'user_type': user_type,
                        'company_id': company_id,
                        'shortcut': account.shortcut,
                        'note': account.note,
                        'parent_id': parent_id,
                        'type': account.type,
                        'active': account.active,
                        'currency_id': currency_id,
                        'level': account.level,
                        'currency_mode': account.currency_mode,
                        } or []
            dict_account and cone2.create('account.account',dict_account) 

if __name__ == '__main__':
   
    print "hola"
   
    print 'Hemos terminado con exito'


#~ product_obj.write(cr,uid,[product_id],{'seller_ids':[(6,0,[record_id])]})

#~ 
#~ def find_partner(self, cr, uid, ids, context=None):
   #~ obj_partner = self.pool.get("res.partner")
   #~ data_brw = self.browse(cr, uid, ids)
   #~ res = {'value':{}}
   #~ for n in data_brw:
       #~ obj_partner_ids = obj_partner.search(cr, uid, [('vat', '=', n.rif)])
   #~ if obj_partner_ids:
       #~ obj_datos_brw = obj_partner.browse(cr, uid, obj_partner_ids[0])
       #~ res['value'].update({'name': obj_datos_brw.name, 'address': 'csm', 'phone': 'csm'})
   #~ else:
       #~ print 'exception'
