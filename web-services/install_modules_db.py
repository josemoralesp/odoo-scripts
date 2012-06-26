#!/usr/bin/env python
#-*- coding:utf-8 -*-
# -*- coding: iso-8859-1 -*-
import xmlrpclib
import csv
import re
import _mssql
import os
import re
import datetime
from random import randrange
##############################################################################
# constants declaration
##############################################################################


HOST=''
HOST2=''
PORT=
PORT2=
DB=''
DB1=''
USER=''
USER1=''
PASS=''
PASS2=''

def install_module(HOST,HOST2,PORT,PORT2,DB,DB1,USER,USER1,PASS,PASS2):
    '''
    Modules is installed in a database and begins to install them one by one in another data base to determine which module can be causing problems

    @param HOST IP address of where is located the first database with modules to install
    @param HOST2 IP address of where is located the second database to install modules
    @param PORT XML-RPC of first instance
    @param PORT2 XML-RPC of first instance
    @param DB Name of first data base with modules to install
    @param DB1 Name of second data base to modules install
    @param USER User of first data base
    @param USER User of second data base
    @param PASS Password of first data base
    @param PASS Password of second data base
    
    
    '''

    url ='http://%s:%d/xmlrpc/' % (HOST,PORT)
    url2 ='http://%s:%d/xmlrpc/' % (HOST2,PORT2)

    common_proxy = xmlrpclib.ServerProxy(url+'common')
    common_proxy2 = xmlrpclib.ServerProxy(url2+'common')

    object_proxy = xmlrpclib.ServerProxy(url+'object')
    object_proxy2 = xmlrpclib.ServerProxy(url2+'object')

    ### login to server
    uid = common_proxy.login(DB,USER,PASS)
    uid2 = common_proxy2.login(DB1,USER1,PASS2)



    mod_id = object_proxy.execute(DB,uid,PASS,'ir.module.module','search',[('state','=','installed')])
    modules = object_proxy.execute(DB,uid,PASS,'ir.module.module','read',mod_id,['name'])
    for module in modules:
        
        mod_id = object_proxy2.execute(DB1,uid2,PASS2,'ir.module.module','search',[('name','=',module.get('name')),('state','=','uninstalled')])
        sure = mod_id and raw_input('Esta seguro que desea instalar el siguiente modulo %s  (si - no)'%module.get('name')) or False
        da = "^(S|s|y|Y)(i|I|s|S)$"
        if re.match(da,sure or 'no'):
            cha_sta = object_proxy2.execute(DB1, uid, PASS2,'ir.module.module','button_install', mod_id)
            inst_mod = object_proxy2.execute(DB1,uid,PASS2, 'base.module.upgrade', 'upgrade_module', mod_id)
        else:
            print 'El modulo %s no fue instalado, ya sea porque no fue encontrado, ya esta instalado o no selecciono una opcion valida'%module.get('name')
        
install_module(HOST,HOST2,PORT,PORT2,DB,DB1,USER,USER1,PASS,PASS2)
if __name__ == '__main__':
   
    print 'Hemos terminado con exito'
