#!/usr/bin/env python
#-*- coding:utf- -*-
# -*- coding: iso-8859-1 -*-
import re
import time
import oerplib
import xlrd
from xlrd import open_workbook
import xlwt
import warnings
import datetime
from datetime import date, datetime, timedelta
import base64
import os
##############################################################################
# constants declaration
##############################################################################

HOST=''
PORT=8069
DB=''
USER=''
PASS=''

HOST_dest=''
PORT_dest=
DB_dest=''
USER_dest='admin'
PASS_dest='admin'



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

bank_ids = [12,8,11],
res = {}




for i in bank_ids:
   
    try:
        cone2.execute('account.bank.statement','read_file',i)
        cone2.execute('account.bank.statement','create_aml_tmp',i)
    except Exception,e:
        print 'ERRORRR',e
    for bank in cone1.browse('account.bank.statement',i):
        
        for line in bank.bs_line_ids:
            ids = []
            for invoice in line.invoice_ids:
                invoice_ids = cone2.search('account.invoice',[('period_id.code','=',invoice.period_id.code),
                                                              ('partner_id.name','=',invoice.partner_id and invoice.partner_id.name),
                                                              ('amount_total','=',invoice.amount_total),
                                                              ])
                
                len(invoice_ids) == 1 and ids.append(invoice_ids[0])
            
            print 'line.numdocument',line.numdocument
            print 'ids',ids
            res.update({line.numdocument:list(set(ids))}) 
    
    
    
    for bank in cone2.browse('account.bank.statement',i):
        
        for line in bank.bs_line_ids:
            if res.get(line.numdocument,False):
                cone2.write('bank.statement.imported.lines',[line.id],{'invoice_ids':[(6,0,res.get(line.numdocument,False))]})
            
            
            res.update({line.numdocument:ids}) 
    
    
    
        print "res",res
            
    
    
    #create_aml_tmp

#xtrac_ids = cone1.search('account.bank.statement',[('date','>','1/6/2012'),('date','<','31/6/2012')])
#print 'xtrac_ids',xtrac_ids 
