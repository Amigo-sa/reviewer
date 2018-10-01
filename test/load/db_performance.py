# -*- coding: utf-8 -*-

import context
import node.settings.errors as ERR
import data.reviewer_model as model

import time

g_qs = model.Group.objects.all()
g_list = list(g_qs.values())
print("Number of groups: %d, now finding persons in each"%len(g_list))

t_start = time.time()
print("list method: started at %f"%t_start)

for group in g_list:
    person_list = model.Person.find({"group_id" : str(group["_id"])})
    #print(len(person_list["list"]))

t_finish = time.time()
print("finished at %f"%t_finish)
dt = t_finish - t_start
print("elapsed %f"%dt)

t_start = time.time()
print("lookup method: started at %f"%t_start)

for group in g_list:
    person_list = model.Person.find({"group_id_mod" : str(group["_id"])})
    #print(len(person_list["list"]))

t_finish = time.time()
print("finished at %f"%t_finish)
dt = t_finish - t_start
print("elapsed %f"%dt)