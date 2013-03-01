#!/usr/bin/env python
#-*- coding:utf- -*-
# -*- coding: iso-8859-1 -*-
import os
import oerplib
import commands 
##############################################################################
# constants declaration
##############################################################################

paths = raw_input('Insert path with .py file: ')
rgrep = commands.getoutput(''' find %s -name '*.py' -type f ''' % (paths) )
rgrep = rgrep.split('\n')
for files in rgrep:
    open_f = open(files,'rw')
    os.popen('touch /tmp/clean')
    copy_f = open('/tmp/clean','w')
    for line in open_f.readlines():

        if line.find('from osv',0,8) >= 0:

            if 'fields' in line and line.find('osv',8) < 0 :
                copy_f.write('from openerp.osv import fields\n')

            elif line.find('osv',8) > 0 and not 'fields' in line:
                copy_f.write('from openerp.osv import osv\n')

            elif 'fields' in line and line.find('osv',8) > 0 and 'orm' \
                  not in line:
                copy_f.write('from openerp.osv import osv, fields\n')

            elif 'fields' in line and line.find('osv',8) > 0 and 'orm' in line:
                copy_f.write('from openerp.osv import osv, fields, orm\n')

        elif line.find('import netsvc',0,13) >= 0:
            copy_f.write('import openerp.netsvc as netsvc\n')

            
        elif line.find('from tools.',0,13) >= 0:
            copy_f.write('from openerp.tools%s\n' % line[10:])

        elif line.find('import tools',0,13) >= 0:
            copy_f.write('import openerp.tools as tools\n')

        else:
            copy_f.write(line)

    os.popen('mv /tmp/clean %s ' % files)
    open_f.close()
