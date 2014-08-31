# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY, without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import xmlrpclib
import socket
import ConfigParser
import optparse
import sys
import thread
import threading
import os
import time
import pickle
import base64
import socket
import re


'''
CAMBIAR EL ADMINISTRADOR 
'''
HOST=''
HOST2=''
PORT=
PORT2=
DB=''
DB2='-133712--0403-12'
USER=''
PASS='



url ='http://%s:%d/xmlrpc/' % (HOST,PORT)
url2 ='http://%s:%d/xmlrpc/' % (HOST2,PORT2)
common_proxy = xmlrpclib.ServerProxy(url+'common')
common_proxy2 = xmlrpclib.ServerProxy(url2+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')
object_proxy2 = xmlrpclib.ServerProxy(url2+'object')
wizard_proxy = xmlrpclib.ServerProxy(url+'wizard')
wizard_proxy2 = xmlrpclib.ServerProxy(url2+'wizard')
#### MODULE LIST TO BE INSTALLED


#### LOGIN IN
uid = common_proxy.login(DB,USER,PASS)
uid2 = common_proxy2.login(DB2,USER,PASS)
print uid
print uid2
#~ ### INSTALL MODULES
#~ admin = object_proxy.execute(DB2,uid2,PASS,'res.users','search',[('name','=','Administrator')])
#~ admin = object_proxy.execute(DB2, uid2, PASS,'res.users','copy', admin[0],{'name':'Maria Gabriela','login':'gaby'})
#~ print "admin",admin
#~ tasks = object_proxy.execute(DB,uid,PASS,'project.task.type','search',[('name','=')])
#~ 
#~ tasks2 = object_proxy.execute(DB2,uid2,PASS,'project.task.type','search',[])
#~ 
#~ tasks2 = object_proxy.execute(DB2, uid2, PASS,'project.task.type','read', tasks2,[])
#~ print "task",tasks2
#~ tasks = object_proxy.execute(DB, uid, PASS,'project.task.type','read', tasks,[])
# Task Create
taskss = []
tarea = {}
#~ squence = tasks2[-1]['sequence']

#~ metodo para crear registros de forma dinamica y retornar el id del nuevo registro
def new_create(model,dict,DB,uid,PASS):
    
    dict.get('id') and dict.pop('id')
    new = object_proxy2.execute(DB,uid,PASS,model,'create',dict)
    return new
    
#~ Recorre el diccionario para buscar relaciones en una diccionario, de encontrarlo se agregaran los ids de las relaciones correspondientes en la base de datos nueva
def move_to_dicts(dicts,model):
    
    if type(dicts) is list:
        for dict in dicts: 
            for key in dict.keys():
                if type(dict.get(key)) is list and len(dicts.get(key)) > 1  and dict[key][1] is str:
                    if model == object_proxy.execute(DB, uid, PASS,model,'fields_get', key)[key].get('relation'):
                        pass
                    else:
                        dicts.update(many2one(model,key,dict[key]))
                elif type(dict.get(key)) is list and all([False for d in dict[key] if type(d) is str ]):
                    if model == object_proxy.execute(DB, uid, PASS,model,'fields_get', key)[key].get('relation'):
                        pass
                    else:
                        dicts.update(one2many(model,key,dict[key]))
    else:
        for key in dicts.keys():
            
            if type(dicts.get(key)) is list and len(dicts.get(key)) > 1 and dicts.get(key)[1] is str:
                if  model == object_proxy.execute(DB, uid, PASS,model,'fields_get',key)[key].get('relation'):
                    pass
                else:    
                    dicts.update(many2one(model,key,dicts[key]))
            elif type(dicts.get(key)) is list and all([False for d in dicts[key] if type(d) is str ]):
                if model == object_proxy.execute(DB, uid, PASS,model,'fields_get',key)[key].get('relation'):
                    pass
                else:
                    dicts.update(one2many(model,key,dicts[key]))
    return dicts
    

#~  Metodo para agregar relaciones many2one a un diccionario para luego crear el registro
#~ def many2one(model,key,value):
    #~ field = object_proxy.execute(DB, uid, PASS,model,'fields_get', key)
    #~ dicti = {}
    #~ field_id = object_proxy.execute(DB2,uid2,PASS,field[key]['relation'],'search',[('name','=',value[-1])])
    #~ 
    #~ 
    #~ if field_id:
        #~ dicti.update({key: field_id[0]})
    #~ 
    #~ else:
        #~ read = object_proxy.execute(DB, uid, PASS,field[key]['relation'],'read',int(value[0]),[])
        #~ dic = move_to_dicts(read,field[key]['relation'])
        #~ field_id = new_create(model,dic,DB2,uid2,PASS)
        #~ dicti.update({key: [(0,0,dic)]})
            #~ 
        #~ 
    #~ print "many2one dic",dicti
    #~ return dicti
    
def many2one(model,key,value):
    
    field = object_proxy.execute(DB, uid, PASS,model,'fields_get', key)
    dicti = {}
    
    field_id = object_proxy2.execute(DB2,uid2,PASS,field[key]['relation'],'search',[('name','=',value[-1])])
    if field_id:
        dicti.update({key:field_id[0]})
    
    else:
        if field[key]['relation'] == 'res.currency':
            pass
        else:
            read = object_proxy.execute(DB,uid,PASS,field[key]['relation'],'read',value[0],[])
            dic = move_to_dicts(read,field[key]['relation']) 
            'id' in dic and dic.pop('id')
            dicti.update({key: [(0,0,dic)]})
    print "dicti",dicti
    dicti.get('currency_id',False) and dicti.pop('currency_id')
    return dicti
    
repeat = []

def one2many(model,key,value):
    global repeat
    if len(repeat) > 2:
        repeat = []
    add = []
    add2 = []
    create = []
    field = object_proxy.execute(DB, uid, PASS,model,'fields_get', key)
    dicti = {}
    read1 = field[key].get('relation') and object_proxy.execute(DB, uid, PASS,field[key]['relation'],'read',value,[])
#~ tener bien en cuenta que solo necesito una lista de ids que seran colocadas en el key del diccionario que llega a este metodo
    #~ buscando los registros si existen se llenara una lista de ids de lo contrario se genera otra lista con ids de los registros que deberan ser creados
    if read1:
        for read in read1:
            for keys in read.keys():
                if not re.search('date|fecha|hora|time',keys):
                    field2 = object_proxy.execute(DB, uid, PASS,field[key]['relation'],'fields_get', keys)
                    if field2 and field2.get(keys) and not field2.get(keys).get('relation')  and field2.get(keys).get('required') == True and type(read[keys]) is not list and field2[keys]['type'] in ['char']:
                        field_id = object_proxy2.execute(DB2,uid2,PASS,field[key]['relation'],'search',[(keys,'=',read[keys])])
                        if field_id:
                            field_id[0] not in add2 and add2.append(field_id[0])
                        else:
                            create.append(read.get('id'))
        
        for ids in create:
            if field[key]['relation'] == 'res.currency':
                pass
            else:
                projecs = object_proxy.execute(DB, uid, PASS,field[key]['relation'],'read',ids,[])
                for keyy in projecs.keys():
                    if type(projecs.get(keyy)) is list and type(projecs.get(keyy) and projecs[keyy][-1]) is str:
                        if field[key]['relation'] in repeat:
                            pass
                        else:
                            repeat.append(field[key]['relation'])
                            projecs.update(many2one(field[key]['relation'],keyy,projecs[keyy]))
                    
                    elif type(projecs.get(keyy)) is list and len(projecs[keyy]) >= 2 and all([False for d in projecs[keyy] if type(d) is str ]):
                        if field[key]['relation'] in repeat:
                            pass
                        else:
                            repeat.append(field[key]['relation'])
                            projecs.update(one2many(field[key]['relation'],keyy,projecs[keyy]))
                'id' in projecs and projecs.pop('id') 
                add.append((0,0,projecs))
                add2 and add.append((6,0,add2))    
        
    dicti.update({key:add})
    dicti.get('currency_id',False) and dicti.pop('currency_id')
    print "dicti",dicti 
    return dicti
    
tareas = object_proxy.execute(DB,uid,PASS,'project.task','search',[])
tareas = object_proxy.execute(DB, uid, PASS,'project.task','read', tareas,[])


for i in tareas:
    for key in i.keys():
        if type(i.get(key)) is list and type(i.get(key) and i[key][1]) is str:
            i.update(many2one('project.task',key,i[key]))
        
        elif type(i.get(key)) is list and len(i[key]) >= 2 and all([False for d in i[key] if type(d) is str ]):
            i.update(one2many('project.task',key,i[key]))
    i.get('id') and i.pop('id')
    print "diccionario",i
    object_proxy2.execute(DB2,uid2,PASS,'project.task','create',i)

projec = object_proxy.execute(DB,uid,PASS,'project.project','search',[])
projec = object_proxy.execute(DB, uid, PASS,'project.project','read', projec,[])

for projecs in projec:  
    for key in projecs.keys():
        if type(projecs.get(key)) is list and type(projecs.get(key) and projecs[key][1]) is str:
            projecs.update(many2one('project.project',key,projecs[key]))
        
        elif type(projecs.get(key)) is list and len(projecs[key]) >= 2 and all([False for d in projecs[key] if type(d) is str ]):
            projecs.update(one2many('project.project',key,projecs[key]))
    projecs.get('id') and projecs.pop('id')
    print "projecs",projecs 
    object_proxy2.execute(DB2,uid2,PASS,'project.project','create',projecs)

#~ if squence in [d for i in tasks2 for d in i.values()]:
    #~ pass
    #~ print "ya"
#~ else:
    #~ for task in tasks:  
        #~ for key in task.keys():
            #~ tarea = {
                #~ 'name': key and key == 'name' and task[key] or tarea.get('name'),
                #~ 'description': key and key == 'description' and task[key] or tarea.get('description'),
                #~ 'sequence': squence,
            
            #~ }
        #~ taskss.append(tarea)
    #~ task_ids = []
    #~ for task in taskss:
        #~ task_id = object_proxy.execute(DB2,uid2,PASS,'project.task.type','write',ids,task)
        #~ task_ids.append(task_id)
    #~ print task_ids
