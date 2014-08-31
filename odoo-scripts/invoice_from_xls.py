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
import xlrd
from xlrd import open_workbook
import xlwt
##############################################################################
# constants declaration
##############################################################################

HOST=''
PORT=9069
DB=''
USER=''
PASS=''

conec = oerplib.OERP(
            server=HOST,
            database=DB,
            port=PORT,
            )

conec.login(USER,PASS)


def xlrd_to_date(cv):
    if not str(cv).isalpha() and len(str(cv)) > 1:
        from1900to1970 = datetime(1970,1,1) - datetime(1900,1,1) + timedelta(days=2)
        print cv
        value = date.fromtimestamp( int(cv) * 86400) - from1900to1970
        print value
        return value

def get_journal(cone2,name):
    journal = []
    if name:
        journal = cone2.search('account.journal',[('name','=',name)])
        journal = journal and journal[0]

    return journal

def create_account_move(xls):
    invoices_caja_ids = conec.search('account.invoice',[('partner_id','=',13)])
    cone1.execute('account.invoice','action_cancel',invoices_caja_ids)
    cone1.execute('account.invoice','action_cancel_draft',invoices_caja_ids)
    company_id = conec and conec.user and conec.user.company_id and conec.user.company_id.id
    file = open_workbook(xls)
    for name in ['53170','53211','53210','53212']:
        account_id = conec.search('account.account',[('code','=',name),('company_id','=',company_id)])
        sheet = file.sheet_by_name(name)
        move_line = []
        invoice_id = False
        date_invoice = False
        line = []
        rang = range(sheet.nrows)
        for ind in rang:

            value = sheet.row_values(ind)
            period = conec.execute('account.period','find',value[0],{'company_id':company_id})
            date = '%s-1'%value[0][:7]
            if date == date_invoice:
                line.append((0,0,{'name':value[1],'account_id': account_id and account_id[0]    }))
                invoice_id and invoice_id.update({'invoice_line':line})
                #print 'period',period
                #print '%s-1'%value[0][:7]

            elif date > date_invoice or date_invoice == False:
                if invoice_id:
                    invo = conec.create('account.invoice',invoice_id)
                    cone1.exec_workflow('account.invoice','invoice_open',invo)
                    line = []
                    invoice_id = False
                    date_invoice = False


                values = conec.execute('account.invoice','onchange_partner_id','', 'in_invoice', 13)
                values and values.get('value').update({'partner_id':13,
                                                    'company_id':company_id ,
                                                    'currency_id':41,
                                                    'date_invoice':date,
                                                    'period_id':period and period[0],
                                                    'type':'in_invoice',
                                                    'journal_id':get_journal(conec,'Compra de Producto'),
                                                    })

                invoice_id = values and values.get('value')
                date_invoice = date


            elif ind == rang[-1]:
                invo = conec.create('account.invoice',invoice_id)
                cone1.exec_workflow('account.invoice','invoice_open',invo)
                line = []
                invoice_id = False
                date_invoice = False




create_account_move('fiel.xls')
