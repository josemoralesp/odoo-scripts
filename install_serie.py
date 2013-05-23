#!/usr/bin/python
import oerplib
import os
import sys

HOST='localhost'
PORT=28069
DB='ovl_prueba'
USER='admin'
PASS='admin'

con = oerplib.OERP(
server=HOST, 
database=DB, 
port=PORT, 
)  

con.login(USER, PASS)
ids = []
modules = os.listdir(len(sys.argv) > 1 and sys.argv[1] or '.')
for name in modules:
    ids=con.search('ir.module.module', [('name', '=', name),
                                        ('state', '=', 'uninstalled')])

    for id in ids:
        try:
            print 'Instalando el modulo', name
            con.execute('ir.module.module', 'button_immediate_install', [id])

        except:
            print 'No se pudo instalar el modulo', name
            st_ids = con.search('ir.module.module', [('state', '=', 'to install')])
            con.write('ir.module.module', st_ids, {'state':'uninstalled'})
