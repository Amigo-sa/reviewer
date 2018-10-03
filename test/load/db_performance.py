# -*- coding: utf-8 -*-
import gc

import context
import node.settings.errors as ERR
import data.reviewer_model as model
import sample_local as sl
import datetime

import time

def get_group_list():
    g_qs = model.Group.objects.all()
    g_list = list(g_qs.values())
    return g_list

def count_persons():
    return model.Person.objects.all().count()

def eval_find_persons_in_groups(route_name, g_list, skip):
    t_start = time.time()
    print("%s method: started at %f" % (route_name,t_start))
    for group in g_list:
        person_list = model.Person.find({route_name : group["_id"]
                                        ,"query_skip" : skip
                                        ,"query_limit" : 100})
    print("last returned list had %d elements" % len(person_list["list"]))
    t_finish = time.time()
    print("finished at %f" % t_finish)
    dt = t_finish - t_start
    print("elapsed %f" % dt)
    return dt

#eval_find_persons_in_groups("group_id")
#eval_find_persons_in_groups("group_id_mod")

fill_groups = [
    {"person" : 100
    ,"group_member" : 100
    ,"group" : 10
    ,"group_role" : 10},



    {"person" : 1000
    ,"group_member" : 1000
    ,"group" : 10
    ,"group_role" : 10},

    {"person" : 10000
    ,"group_member" : 10000
    ,"group" : 10
    ,"group_role" : 10},

    {"person" : 100000
    ,"group_member" : 1000000
    ,"group" : 10
    ,"group_role" : 10},

    {"person" : 10000
    ,"group_member" : 100000
    ,"group" : 10
    ,"group_role" : 1},

    {"person" : 20010
    ,"group_member" : 20011
    ,"group" : 1000
    ,"group_role" : 10},

    {"person" : 10000,
    "group_member" : 1000,
    "group" : 10,
    "group_role" : 10,
    "person_ss" : 10000,
    "person_hs" : 10000,
    "ss_review" : 20010,
    "hs_review" : 20010,
    "specialization_review" : 11,
    "person_specialization": 2001,},

    {"person" : 10000,
    "group_member" : 10000,
    "group" : 10,
    "group_role" : 1,
    "person_ss" : 10000,
    "person_hs" : 10000,
    "ss_review" : 20010,
    "hs_review" : 20010,
    "specialization_review" : 11,
    "person_specialization": 2001,},

    {"person" : 100
    ,"group_member" : 100
    ,"group" : 1000
    ,"group_role" : 10},

    {"person": 100000
    ,"group_member": 200000
    ,"group": 2
    ,"group_role": 1},

]
routes_to_test = [
    "group_id_mod",
    "group_id",
]

def prepare_header(fill_groups, routes_to_test):
    headers = []
    for group in fill_groups:
        print(group)
        for key,value in group.items():
            if key not in headers:
                headers.append(key)
    for route in routes_to_test:
        headers.append("%s, no skip, limit 100" % route)
        headers.append("%s, skip half, limit 100" % route)
    return headers


if __name__ == "__main__":
    filename = "out_{:%Y-%m-%d_%H%M%S}.csv".format(datetime.datetime.now())
    headers = prepare_header(fill_groups, routes_to_test)
    f = open(filename, "w")
    for header in headers:
        f.write("%s;"%header)
    f.write("\n")
    f.close()

    for group in fill_groups:

        with open(filename, "a") as f:
            sl.clear_collections(sl.db)
            sl.fill_db(sl.db,group,sl.validate_after_fill,sl.diverse)
            g_list = get_group_list()
            p_count = count_persons()
            avg_persons_per_group = p_count/len(g_list)
            print("avg persons in group: %s" % avg_persons_per_group)
            skip = 0 if avg_persons_per_group < 200 else int(avg_persons_per_group/2)
            for route in routes_to_test:
                gc.collect()
                t = eval_find_persons_in_groups(route, g_list, 0)
                group.update({"%s, no skip, limit 100" % route : int(t*1000)})
                if skip:
                    gc.collect()
                    t = eval_find_persons_in_groups(route, g_list, skip)
                    group.update({"%s, skip half, limit 100" % route: int(t * 1000)})
                else:
                    group.update({"%s, skip half, limit 100" % route: ""})
            for header in headers:
                if header in group:
                    f.write("%s;"%group[header])
                else:
                    f.write("_%s_;"%sl.DEFAULT_FILL_AMT)

            f.write("\n")

