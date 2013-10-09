#!/usr/bin/env python
#-*- coding:utf- -*-
# -*- encoding: utf-8 -*-
import csv
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

cone1.login(USER, PASS)
fields = csv.DictReader(open('/home/openerp/Downloads/res_partner_ILT2 (2).csv' ))
for field in fields:
    country_id = cone1.search('res.country', [('name', '=', field.get('country/id'))])
    country_id = country_id and country_id[0]
    partner_id = cone1.search('res.partner', [('name', 'ilike', field.get('name'))])
    if partner_id and country_id:
        cone1.write('res.partner', partner_id, {'country_id':country_id})

if __name__ == '__main__':
   
    print "hola"
    print 'Hemos terminado con exito'
