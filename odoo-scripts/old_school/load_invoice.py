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
import random

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
invo_ids = object_proxy.execute(DB,uid,PASS,'account.invoice','search',[('invoice_line.product_id','=', 431)])
read = object_proxy.execute(DB,uid,PASS,'account.invoice','read',invo_ids[0],[])
print "read",read
for i in range(10000):
    object_proxy.execute(DB,uid,PASS,'account.invoice','copy',random.randrange(38,43),{'date_invoice':'2012-03-%s'%random.randrange(23,30)})
    
#~ object_proxy.execute(DB,uid,PASS,'ir.rule','create',rules)
#~ 
#~ company_id = object_proxy.execute(DB,uid,PASS,'res.company','search',[('name','=',i)])
   #~ 

