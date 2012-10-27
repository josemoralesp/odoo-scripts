import os
import csv
from xlrd import open_workbook

files = '/home/openerp/Documentos/Herrera/CSV Files/'

names = os.listdir(files)
field_help = open_workbook('/home/openerp/Documentos/Herrera/descripcion campos txt.xls')
sheet = field_help.sheet_by_index(0)
os.popen('mkdir /home/openerp/auto/herrera_madi_data')
openerp = open('/home/openerp/auto/herrera_madi_data/__openerp__.py','w')
os.popen('echo import model >> /home/openerp/auto/herrera_madi_data/__init__.py')
os.popen('mkdir /home/openerp/auto/herrera_madi_data/model /home/openerp/auto/herrera_madi_data/view /home/openerp/auto/herrera_madi_data/wizard')
init = open('/home/openerp/auto/herrera_madi_data/model/__init__.py','w')
menu = False
openerp.write('''#!/usr/bin/python
# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) Vauxoo (<http://vauxoo.com>).
#    All Rights Reserved
###############Credits######################################################
#    Coded by: Vauxoo C.A.           
#    Planified by: Nhomar Hernandez
#    Audited by: Vauxoo C.A.
#############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################''')
openerp.write('\n{\n')
openerp.write('"name" : "Herrera madi Data Imported",\n')
openerp.write('"version" : "0.1",\n')
openerp.write('"depends" : ["base"],\n')
openerp.write('"author" : "Vauxoo",\n')
openerp.write('"description" : "Create modules by file used to import data from cobol " ,\n')
openerp.write('"website" : "http://vauxoo.com",\n')
openerp.write('"category" : "Generic Modules",\n')
openerp.write('"init_xml" : [],\n')
openerp.write('"demo_xml" : [],\n')
openerp.write('"test" : [],\n')
openerp.write('"update_xml" : [\n')


for name_file in names:
    name_file and name_file[:-4].find('~') <0 and init.write('import %s\n'%name_file[:-4])
    fields = csv.DictReader(open('%s/%s'%(files,name_file)))
    clase = open('/home/openerp/auto/herrera_madi_data/model/%s.py'%name_file[:-4],'w')
    view = open('/home/openerp/auto/herrera_madi_data/view/%s_view.xml'%name_file[:-4],'w')


    view.write('<openerp>\n   <data>\n')
    view.write("   <record model='ir.ui.view' id='%s_form'>\n"%str(name_file[:-4]).lower())
    view.write("      <field name='name'>%s</field>\n"%str(name_file[:-4]).lower())
    view.write("      <field name='model'>maestro.%s</field>\n"%str(name_file[:-4]).lower())
    view.write("      <field name='type'>form</field>\n")
    view.write("      <field name='arch' type='xml'>\n")
    view.write("          <form string='%s'>\n"%str(name_file[:-4]))
    clase.write('from osv import osv\n')
    clase.write('from osv import fields')
    clase.write('\n\nclass %s(osv.osv):'%name_file[:-4])
    clase.write("\n\n    _name = 'maestro.%s'"%str(name_file[:-4]).lower())
    clase.write("\n    _columns =  { \n")
    
    for field in fields:
        tree_name = []
        clase.write("        'name' : fields.integer('N Line',help='Line number in the original file'),\n") 
        clase.write("        'used' : fields.boolean('Used',help='If line has been used to import data'),\n") 
        for key in field.keys(): 
            d = 0
            for value in range(sheet.nrows):
                ind = sheet.row_values(value)
                if str(ind[1]).strip() == str(key).strip():
                    help = ind[3].encode('ascii','ignore')
                    clase.write("        '%s' : fields.char('%s',%d,help='%s'),\n"%(str(key).replace("'",'').strip(),str(key).replace("'",'').strip(),(len(key)+3),help ))
                    
                    d+=1
            if d == 0:
                clase.write("        '%s' : fields.char('%s',%d),\n"%(str(key).replace("'",'').strip(),str(key).replace("'",'').strip(),(len(key)+3)))
                
            view.write("           <field name='%s' />\n"%str(key).replace("'",'').strip().replace("''","'"))
            tree_name.append(str(key).replace("'",'').strip().replace("''","'"))
        view.write("        </form>\n")
        view.write("     </field>\n")
        view.write("    </record>\n")
        view.write('\n\n\n')
        view.write("   <record model='ir.ui.view' id='%s_tree'>\n"%str(name_file[:-4]).lower())
        view.write("      <field name='name'>%s</field>\n"%str(name_file[:-4]).lower())
        view.write("      <field name='model'>maestro.%s</field>\n"%str(name_file[:-4]).lower())
        view.write("      <field name='type'>tree</field>\n")
        view.write("      <field name='arch' type='xml'>\n")
        view.write("          <tree string='%s'>\n"%str(name_file[:-4]))
        for tree in tree_name:
            view.write("           <field name='%s' />\n"%tree)
        view.write("        </tree>\n")
        view.write("     </field>\n")
        view.write("    </record>\n")
        view.write('\n\n\n')
        view.write("  <record model='ir.actions.act_window' id='%s_action'>\n"%str(name_file[:-4]).lower())
        view.write("    <field name='name'>maestro.%s</field>\n"%str(name_file[:-4]).lower())
        view.write("    <field name='res_model'>maestro.%s</field>\n"%str(name_file[:-4]).lower())
        view.write("    <field name='view_type'>form</field>\n")
        view.write("    <field name='view_type'>form</field>\n")
        view.write("    <field name='vies_mode'>tree,form</field>\n")
        view.write("  </record>\n")
        view.write('\n\n\n')
        if not menu:
            view.write("<menuitem name = 'Herrera files' id='herrera_principal_menu' /> \n")
            view.write("<menuitem name = 'Models' parent='herrera_principal_men' id='herrera_menu_files' /> \n")
        
        view.write("<menuitem name = '%s' id='herrera_%s'  parent='herrera_menu_files' action='%s_action' />\n"%(str(name_file[:-4]),str(name_file[:-4]).lower(),str(name_file[:-4]).lower()))
        menu = True
        view.write("  </data>\n")
        view.write("</openerp>\n")
        openerp.write("'view/%s_view.xml',\n"%name_file[:-4])
        break


    clase.write("\n }")
    clase.write('\n%s()'%name_file[:-4])
openerp.write('],\n')
openerp.write('"active": False,\n')
openerp.write('"installable": True,\n')
openerp.write('}')



