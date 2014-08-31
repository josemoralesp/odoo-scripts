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
USER='admin'
PASS='admin'

HOST_dest=''
PORT_dest=8069
DB_dest=''
USER_dest='admin'
PASS_dest='cruca'



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



def get_journal(cone2,name):
    journal = []
    if name:
        journal = cone2.search('account.journal',[('name','=',name)])
        journal = journal and journal[0]
        
    return journal



def get_product(cone2,name):
    
    product_id = cone2.search('product.product',[('name','=',name)])
    
    product_id = product_id and product_id[0]
    
    return product_id

def search_account(cone2,code,cone1=False,id=False):
    
    company_id = cone2.user and cone2.user.company_id and cone2.user.company_id.id
    account_ids = company_id and cone2.search('account.account',[('code','=',code),('company_id','=',company_id)])
        
    return account_ids and account_ids[0] or [] 


def create_invoice_line_p(cone2,line,partner):

    lis_tup = [0,0]
    if line.product_id:
        product_id = get_product(cone2,line.product_id.name)
        value = cone2.execute('account.invoice.line','product_id_change','',product_id,
                                                                    1, 0, '', 
                                                                    line.invoice_id.type,
                                                                    partner,
                                                                    False,
                                                                    False,
                                                                    False,
                                                                        False,{})
        print 'value',value
        lines = value.get('value',False)
        lines and lines.update({'price_unit':line.price_unit,'quantity':line.quantity,'product_id':product_id})
        
        
        lis_tup.append(lines)
    else:
        lis_tup.append({'name':line.name,'price_unit':line.price_unit,
                        'account_id':line.account_id and search_account(cone2,line.account_id.code),
                        'quantity':line.quantity })
        
    return tuple(lis_tup)


def get_currency(cone2,name):
    
    currency = cone2.search('res.currency',[('name','=',name)])
    currency = currency and currency[0] 

    return currency






def search_partner(cone2,name):
    
    partner_id = cone2.search('res.partner',[('name','=',name)])
    
    partner_id = partner_id and partner_id[0]
    
    return partner_id





def load_in_invoice(cone2,cone1):
    
    invoice_ids = cone1.search('account.invoice',[('name','=','ND')])
    for invoice in cone1.browse('account.invoice',invoice_ids):
        
        
        values =  invoice.partner_id and cone2.execute('account.invoice','onchange_partner_id','', 'in_invoice', invoice.partner_id and search_partner(cone2,invoice.partner_id.name))
            
        values and values.get('value').update({'partner_id':invoice.partner_id and search_partner(cone2,invoice.partner_id.name),
                                                'company_id':cone2.user.company_id and cone2.user.company_id.id ,
                                                'currency_id':invoice.currency_id and invoice.currency_id.id ,
                                                'type':'in_invoice','date_invoice':invoice.date_invoice and str(invoice.date_invoice),
                                                'name':invoice.name,
                                                'journal_id':invoice.journal_id and get_journal(cone2,invoice.journal_id.name),
                                                })
        
        invoice_id = values and values.get('value')
        print 'invoice_id',invoice_id 
        
        invoice_id and \
        invoice_id.update({'invoice_line':[create_invoice_line_p(cone2,line,search_partner(cone2,invoice.partner_id.name) and invoice.partner_id.id) for line in invoice.invoice_line ]}) 
            
        
        invoice_ids = cone2.create('account.invoice',invoice_id)
        invoice_ids and cone2.exec_workflow('account.invoice','invoice_open',invoice_ids) 

       
            
    
    
load_in_invoice(cone2,cone1)
