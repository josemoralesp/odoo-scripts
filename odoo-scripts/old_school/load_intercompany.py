# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY, without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import xmlrpclib
import socket
import ConfigParser
import optparse
import sys
import thread
import threading
import os
import time
import pickle
import base64
import socket


'''
CAMBIAR EL ADMINISTRADOR 
'''
HOST=''
PORT=
DB=''
USER=''
PASS=''
url ='http://%s:%d/xmlrpc/' % (HOST,PORT)
common_proxy = xmlrpclib.ServerProxy(url+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')
wizard_proxy = xmlrpclib.ServerProxy(url+'wizard')
#### MODULE LIST TO BE INSTALLED


#### LOGIN IN
uid = common_proxy.login(DB,USER,PASS)


### INSTALL MODULES
from time import sleep 

def get_location_id(name,company_id):
    '''
    This function locate location's id
    '''
    ids = object_proxy.execute(DB,uid,PASS,'stock.location', 'search', [('name','=',name), ('company_id','=',company_id)]) 
    if ids:
        return ids


group_ids = object_proxy.execute(DB,uid,PASS,'res.groups','search',[])
company_ids = object_proxy.execute(DB,uid,PASS,'res.company','search',[])
rule_ids = object_proxy.execute(DB,uid,PASS,'ir.rule','search',[('name','=','company rule')])
object_proxy.execute(DB,uid,PASS,'ir.rule','write',rule_ids,{'domain_force':"['|',('id','child_of',[user.company_id.id]),('id','in',[i.id for i in user.company_id.company_in_ids])]"})

rule_ids = object_proxy.execute(DB,uid,PASS,'ir.rule','search',[('name','=','Lotes')])
object_proxy.execute(DB,uid,PASS,'ir.rule','write',rule_ids,{'domain_force':"['|',('company_id','=',[user.company_id.id]),('company_id','in',[i.id for i in user.company_id.company_in_ids])]"})


import re
rule_ids = object_proxy.execute(DB,uid,PASS,'ir.rule','search',[('name','=','Location multi-company')])
object_proxy.execute(DB,uid,PASS,'ir.rule','write',rule_ids,{'domain_force':"['|','|',('company_id','=',False),('company_id','child_of',[user.company_id.id]),('company_id','in',[i.id for i in user.company_id.company_in_ids])]"})


rule_ids = object_proxy.execute(DB,uid,PASS,'ir.rule','search',[('name','=','stock_move multi-company')])
object_proxy.execute(DB,uid,PASS,'ir.rule','write',rule_ids,{'domain_force':"['|','|',('company_id','=',False),('company_id','child_of',[user.company_id.id]),('company_id','in',[i.id for i in user.company_id.company_in_ids])]"})



rule_ids = object_proxy.execute(DB,uid,PASS,'ir.rule','search',[('name','=','Warehouse multi-company')])
object_proxy.execute(DB,uid,PASS,'ir.rule','write',rule_ids,{'domain_force':"['|','|',('company_id','=',False),('company_id','child_of',[user.company_id.id]),('company_id','in',[i.id for i in user.company_id.company_in_ids])]"})






rule_ids = object_proxy.execute(DB,uid,PASS,'ir.rule','search',[('name','=','stock_picking multi-company')])
object_proxy.execute(DB,uid,PASS,'ir.rule','write',rule_ids,{'domain_force':"['|','|',('company_id','=',False),('company_id','child_of',[user.company_id.id]),('company_id','in',[i.id for i in user.company_id.company_in_ids])]"})



rule_ids = object_proxy.execute(DB,uid,PASS,'ir.rule','search',[('name','=','Sale Order Line multi-company')])
object_proxy.execute(DB,uid,PASS,'ir.rule','write',rule_ids,{'domain_force':"['|','|',('company_id','=',False),('company_id','child_of',[user.company_id.id]),('company_id','in',[i.id for i in user.company_id.company_in_ids])]"})

rule_ids = object_proxy.execute(DB,uid,PASS,'ir.rule','search',[('name','=','Sale Order multi-company')])
object_proxy.execute(DB,uid,PASS,'ir.rule','write',rule_ids,{'domain_force':"['|','|',('company_id','=',False),('company_id','child_of',[user.company_id.id]),('company_id','in',[i.id for i in user.company_id.company_in_ids])]"})






rule_ids = object_proxy.execute(DB,uid,PASS,'ir.rule','search',[('name','=','Account Entry')])
object_proxy.execute(DB,uid,PASS,'ir.rule','write',rule_ids,{'domain_force':"['|',('company_id','=',False),('company_id','in',[i.id for i in user.company_id.company_in_ids])]"})





rule_ids = object_proxy.execute(DB,uid,PASS,'ir.rule','search',[])
leer = object_proxy.execute(DB,uid,PASS,'ir.rule','read',rule_ids,['name','id','domain'])
for i in leer:
    if re.search('Company|company|comp',str(i.get('domain'))) and not re.search('Company|company|comp',str(i.get('name'))):
        print "siiii"
        object_proxy.execute(DB,uid,PASS,'ir.rule','write',i.get('id'),{'domain_force':"['|','|',('company_id','=',False),('company_id','child_of',[user.company_id.id]),('company_id','in',[i.id for i in user.company_id.company_in_ids])]"})
    
rule_ids = object_proxy.execute(DB,uid,PASS,'ir.model','search',[('model','=','stock.production.lot')])
rules = {'model_id':rule_ids[0],
    'domain_force':"[('company_id','=',[user.company_id.id])]",
    'name':'Lotes',     
    'global':True,
    'perm_read':True,
    'perm_create':True,
    'perm_write':True,
    'perm_unlink':True,
    }
object_proxy.execute(DB,uid,PASS,'ir.rule','create',rules)
companies = {
'DISTRIBUIDORA ACROPOLIS BARQUISIMETO, C.A.':'BRQ',
'DISTRIBUIDORA ACROPOLIS, C.A.':'BAR',
'DISTRIBUIDORA ACROPOLIS FALCON,C.A.':'FAL',
'DISTRIBUIDORA ACROPOLIS GUAYANA, C.A.':'GUA',
'DISTRIBUIDORA ACROPOLIS MARACAY, C.A.':'MAR',
'DISTRIBUIDORA ACROPOLIS MONAGAS, C.A.':'MON',
'REVESTIMIENTO DACROPOLIS C.A.':'VAL',
'TECVEMAR, C.A.':'TCV',

}


#~ for5
