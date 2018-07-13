# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 10:26:02 2018

@author: Stross
"""

from pymodm.connection import connect
#from pymongo.write_concern import WriteConcern
#from pymodm import MongoModel, fields, ReferenceField
import settings.mongo as mongosettings
import datetime
import pymongo
import random
import os, sys

parentPath = os.path.abspath("..//..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from src.data.reviewer_model import *#<- govnocode


connect(mongosettings.conn_string + "/" + mongosettings.db_name,
        alias = "reviewer")

#print(dir(src.data.reviewer_model))

#mod_items = dir(src.data.reviewer_model)

#for item in Department.objects.all():
#    print(item.name)

def get_dependencies(doc, dep_id_list):
    current_del_rules = doc._mongometa.delete_rules
    print (current_del_rules.__class__)
    print (current_del_rules)
    
    for item, rule in current_del_rules.items():
        if rule == ReferenceField.DENY:
            related_model, related_field = item
            print("-----------------")
            print(related_model)
            print(related_field)
            
            deps = related_model.objects.raw({related_field : doc.pk})
            
            for dep in deps:
                if dep not in dep_id_list:
                    print(dep)
                    dep_id_list.append(dep)
                    get_dependencies(dep, dep_id_list)
            
            """
            related_qs = related_model._mongometa.default_manager.raw(
                        {related_field: doc.pk}).values()
            print(related_qs.count())
            for dep in related_qs:
                print(dep)
                dep_id_list.append(dep)
                get_dependencies(dep, dep_id_list)
            """
    return dep_id_list       
        
    
    
iit = Department.objects.get({"name" : "Кафедра ИИТ"})
mpei = Organization.objects.get({"name" : "МЭИ"})
pashka = Person.objects.get(({"surname" : "Ерин"}))
#print_dependencies(iit)
dep_id_list = []

dep_list = get_dependencies(mpei, dep_id_list)
print(len(dep_list))
print("-----------------")
for item in dep_list:
    print("--")
    print(item.__class__)
    print(item.to_son().to_dict())
    

