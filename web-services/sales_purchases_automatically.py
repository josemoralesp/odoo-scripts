#!/usr/bin/env python
#-*- coding:utf- -*-
# -*- coding: iso-8859-1 -*-
import xmlrpclib
import csv
import re
import _mssql
import os
import re
import DateTime
from random import randrange
import datetime
from dateutil import relativedelta
##############################################################################
# constants declaration
##############################################################################



def sale_and_purchase_generator(HOST,PORT,DB,USER,PASS,limite,date_beging=False,date_end=False):
   
    '''
    Creation of purchase orders and sales automatic, 
    these will be automatically created and confirmed 
    with their invoices generated in the operation
  
    @param HOST ip address of the server
    @param PORT XML-RPC port where the server is running
    @param DB Name of the database where transactions generate
    @param USER User login which will be made to the server
    @param PASS Selected user's password
    @param limite Limit ventass to perform
    @param date_beging Starting date of the transactions month/year
    @param date_end Transaction Deadline month/year
    If not sent inition dates and termination of transactions will be made ​​to the current date
    If the date format is not sent correctly (month / year), they will be made ​​in current date
    '''
    
    line = []
    url ='http://%s:%d/xmlrpc/' % (HOST,PORT)
    common_proxy = xmlrpclib.ServerProxy(url+'common')
    object_proxy = xmlrpclib.ServerProxy(url+'object')
    uid = common_proxy.login(DB,USER,PASS)
    cont = 0
    cont2 = 0
    product_ids=[]  
    date1 = date_beging and len(date_beging.split('/')) == 2 and \
            int(date_beging.split('/')[1]) > int(date_beging.split('/')[0]) and  len(date_beging.split('/')[1]) == 4 and \
            datetime.date(int(date_beging.split('/')[1]),int(date_beging.split('/')[0]),1) or \
            datetime.date.today().strftime('%Y/%m/%d')
    
    
    date2 = date_end and len(date_end.split('/')) == 2 and  \
            int(date_end.split('/')[1]) > int(date_end.split('/')[0]) and  len(date_end.split('/')[1]) == 4 and \
            datetime.date(int(date_end.split('/')[1]),int(date_end.split('/')[0]),1) or \
            False
    
    date = date1 and date2 and (date2 - date1).days > 0 and (date2 - date1).days  or date1
    range = randrange(1,limite)
    
    
#~ ------------------------- Generator of purchase order ---------------------------------------
    
    partner_id = object_proxy.execute(DB, uid, PASS,'res.partner','search',[('customer','=',True)])
    product_id = object_proxy.execute(DB, uid, PASS,'product.product','search',[('type','!=','service'),('id','!=',212)])
    company = object_proxy.execute(DB, uid, PASS,'res.users','read',uid )
    warehouse_id = company.get('company_id',False) and company.get('company_id',False)[0]  and object_proxy.execute(DB, uid, PASS,'stock.warehouse','search',[('company_id','=',company.get('company_id',False)[0])])
    while cont != range:
        
        dates = type(date) is int and (date1 + datetime.timedelta(days=randrange((-date/4),-1))).strftime('%Y/%m/%d') or \
                date2
        print dates
        
        partner = partner_id and partner_id[randrange(len(partner_id))]
        purchase = object_proxy.execute(DB, uid, PASS,'purchase.order','onchange_partner_id',partner,1)
        purchase.get('value',False) and purchase.get('value').update({'partner_id':partner,'invoice_method':'order','date_order':dates})
        res = warehouse_id and object_proxy.execute(DB, uid, PASS,'purchase.order','onchange_warehouse_id',warehouse_id[0],1)
        purchase.get('value',False) and  res.get('value',False) and purchase.get('value').update(res.get('value',False))
        purchase = purchase.get('value')
        
        
        range2 = randrange(60,80)
        purchase_id = object_proxy.execute(DB, uid, PASS,'purchase.order','create',purchase)
        cont2 = 0
        while cont2 != range2:
            product = product_id and product_id[randrange(len(product_id))]
            product_ids.append(product)
            qty = randrange(80,120)
            lines = object_proxy.execute(DB, uid, PASS,'purchase.order.line','product_id_change',1,
                                        purchase.get('pricelist_id',False),
                                        product,qty,False, purchase.get('partner_id',False),
                                        purchase.get('date_order',False),purchase.get('fiscal_position',False),
                                        False,False,False,False).get('value')
            
            
            
            lines.update({'product_id':product,'order_id':purchase_id,'product_qty':qty,'date_planned':dates})
            object_proxy.execute(DB, uid, PASS,'purchase.order.line','create',lines)
            cont2 = cont2 + 1 
        object_proxy.exec_workflow(DB, uid, PASS,'purchase.order', 'purchase_confirm',purchase_id)
        order = object_proxy.execute(DB, uid, PASS,'purchase.order','read',purchase_id)
        [object_proxy.execute(DB, uid, PASS,'stock.picking','action_confirm',[pick]) for pick in order.get('picking_ids',[]) ]
        [object_proxy.execute(DB, uid, PASS,'stock.picking','action_done',[pick]) for pick in order.get('picking_ids',[]) ]
        [object_proxy.exec_workflow(DB, uid, PASS,'account.invoice', 'invoice_open',pick) for pick in order.get('invoice_ids',[]) ]
        [object_proxy.execute(DB, uid, PASS,'account.invoice', 'write',[pick],{'date_invoice':dates}) for pick in order.get('invoice_ids',[]) ]
        cont = cont + 1 
        print "Generada compra N: ", cont
    
    
    
    
    #~ ------------------------------Generator of sale order ---------------------------------------------------
    partner_id = object_proxy.execute(DB, uid, PASS,'res.partner','search',[('supplier','=',True)])
    cont = 0
    while cont != range:
        
        date2 = type(date) is int and (date1 + datetime.timedelta(days=randrange(1,date))).strftime('%Y/%m/%d') or \
                date2
        
        partner = partner_id and partner_id[randrange(len(partner_id))]
        sale = object_proxy.execute(DB, uid, PASS,'sale.order','onchange_partner_id',partner,1)
        sale.get('value',False) and sale.get('value').update({'partner_id':partner,'order_policy':'manual','date_order':date2})
        sale = sale.get('value')
        
        
        range2 = randrange(60,80)
        sale_id = object_proxy.execute(DB, uid, PASS,'sale.order','create',sale)
        cont2 = 0
        while cont2 != range2:
            product = product_ids and product_ids[randrange(len(product_ids))]
            qty = randrange(20,50)
            lines = object_proxy.execute(DB, uid, PASS,'sale.order.line','product_id_change',1,
                                        sale.get('pricelist_id',False),
                                        product,qty,False, 0,False,'',
                                        sale.get('partner_id',False),False,True,
                                        sale.get('date_order',False),False,sale.get('fiscal_position',False),
                                        False).get('value')
            
            lines.update({'product_id':product,'order_id':sale_id,'product_uom_qty':qty})
            object_proxy.execute(DB, uid, PASS,'sale.order.line','create',lines)
            cont2 = cont2 + 1 
        object_proxy.exec_workflow(DB, uid, PASS,'sale.order', 'order_confirm',sale_id)
        invo_ids = object_proxy.execute(DB, uid, PASS,'sale.order','manual_invoice',[sale_id])
        #~ invo_ids and invo_ids.get('res_id',False) and object_proxy.execute(DB, uid, PASS,'account.invoice', 'write',[invo_ids.get('res_id',False)],{'date_invoice':date2})
        invo_ids and invo_ids.get('res_id',False) and object_proxy.exec_workflow(DB, uid, PASS,'account.invoice', 'invoice_open',invo_ids.get('res_id',False))
        cont = cont + 1 
        print "Generada Venta N: ",cont


if __name__ == '__main__':
    print "hola"
   
    print 'Hemos terminado con exito'

