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
import generate_account_move
##############################################################################
# constants declaration
##############################################################################
base = raw_input('Ingresa el nombre de la base de datos a crear: ')

HOST=''
PORT=
DB=''
USER=''
PASS='!'

HOST_dest=''
PORT_dest=
DB_dest=base
USER_dest=
PASS_dest=

HOST_ext=''
PORT_ext=
user_id =

cone1 = oerplib.OERP(
            server=HOST,
            database=DB,
            port=PORT,
            )

cone1.login(USER,PASS)


cone3 = oerplib.OERP(
            server=HOST_ext,
            port=PORT_ext,
            )



cone3.db.create_and_wait(
            super_admin_passwd='admin',
            database=base,
            demo_data=False, lang='es_CR',
            admin_passwd='admin')


cone2 = oerplib.OERP(
            server=HOST_dest,
            database=DB_dest,
            port=PORT_dest,
            )

cone2.login(USER_dest,PASS_dest)

def load_in_invoice(cone2,cone1):

    invoice_ids = cone1.search('account.invoice',[('type','=','in_invoice')])

    for invoice in cone1.browse('account.invoice',invoice_ids):

        try:
            values =  invoice.partner_id and cone2.execute('account.invoice','onchange_partner_id','', 'in_invoice', invoice.partner_id and search_partner(cone2,invoice.partner_id.name))

            values and values.get('value').update({'partner_id':invoice.partner_id and search_partner(cone2,invoice.partner_id.name),
                                                    'company_id':cone2.user.company_id and cone2.user.company_id.id ,
                                                    'currency_id':invoice.currency_id and invoice.currency_id.id,
                                                    'type':'in_invoice','date_invoice':invoice.date_invoice and str(invoice.date_invoice),
                                                    'name':invoice.number,
                                                    'journal_id':get_journal(cone2,'Compra de Producto'),
                                                    })

            invoice_id = values and values.get('value')
            print 'invoice_id',invoice_id

            invoice_id and \
            invoice_id.update({'invoice_line':[create_invoice_line_p(cone2,line,search_partner(cone2,invoice.partner_id.name) and invoice.partner_id.id) for line in invoice.invoice_line ]})


            invoice_ids = cone2.create('account.invoice',invoice_id)
            invoice_ids and cone2.exec_workflow('account.invoice','invoice_open',invoice_ids)

        except Exception,e:

            print 'Error with invoice ',e


load_in_invoice(cone2,cone1)













] FX SUNACTIVES GREY XTREME STEEL RX Producto

buscar facturas id buscar y crear parent_id

conciliar nota credito con el asiento ya generado



for i in invoice.move_id.move_line
    invoice.account_id.id == i.account_id.id:


    reconsail_partial account_move_line(lineas de asientos) 734 account_move_line




wise 18 facturas gasto en version 6



