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

HOST=''
PORT=8069
DB=''
USER=''
PASS=''


cone1 = oerplib.OERP(
            server=HOST,
            database=DB,
            port=PORT,
            )  

cone1.login(USER,PASS)

invoice_line_ids = cone1.search('account.invoice.line', [('product_id.name', 'like', 'FSV 1.56 HMC 72 NEG'),('product_id.standard_price','=',0),('invoice_id.type','=','in_invoice')])
invoice_ids = set([i.get('invoice_id')[0] for i in cone1.read('account.invoice.line',invoice_line_ids,['invoice_id']) ])
for i in list(invoice_ids):
    print 'El id de la factura es ',i
    cone1.execute('account.invoice','action_cancel',[i])
    cone1.execute('account.invoice','action_cancel_draft',[i])
    cone1.exec_workflow('account.invoice','invoice_open',i)
            
            

invoice_line_ids = cone1.search('account.invoice.line', [('product_id.name', 'like', 'FSV 1.56 HMC 72 NEG'),('invoice_id.type','=','out_invoice')])
invoice_ids = set([i.get('invoice_id')[0] for i in cone1.read('account.invoice.line',invoice_line_ids,['invoice_id']) ])
for i in list(invoice_ids):
    print 'El id de la factura es ',i
    cone1.execute('account.invoice','action_cancel',[i])
    cone1.execute('account.invoice','action_cancel_draft',[i])
    cone1.exec_workflow('account.invoice','invoice_open',i)
            
            






