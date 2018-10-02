# -*- coding: utf-8 -*-

import context
import node.settings.errors as ERR
import data.reviewer_model as model

import time

g_qs = model.Group.objects.all()
g_list = list(g_qs.values())
print("Number of groups: %d, now finding persons in each"%len(g_list))

def eval_find_persons_in_groups(route_name):
    t_start = time.time()
    print("%s method: started at %f" % (route_name,t_start))
    for group in g_list:
        person_list = model.Person.find({route_name : group["_id"]
                                        ,"query_skip" : 500
                                        ,"query_limit" : 100})
    print("last returned list had %d elements" % len(person_list["list"]))
    t_finish = time.time()
    print("finished at %f" % t_finish)
    dt = t_finish - t_start
    print("elapsed %f" % dt)

eval_find_persons_in_groups("group_id")
eval_find_persons_in_groups("group_id_mod")
