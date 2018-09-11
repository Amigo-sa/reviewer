from node.settings import constants
import os, sys, inspect, re
db_name = constants.db_name
if len(sys.argv) > 1:
    if '--test' in str(sys.argv):
        db_name = constants.db_name_test
    if '--load_test' in str(sys.argv):
        db_name = constants.db_name_load_test

from pymongo import MongoClient
uri="mongodb://localhost:27017"
client = MongoClient(uri)
db = client[db_name]

colList = db.list_collection_names()
for col in colList:
    db.drop_collection(col)
    #db[col].delete_many({})
    print("dropped collection " + col)
print("done")

import context
import data.reviewer_model as model
from node.api.auth import hash_password, gen_session_id

from bson import ObjectId, son

import datetime
import random


def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def int_to_obj_id(num):
    return ObjectId('{:024x}'.format(num))

field_aliases = {
        "fields.CharField" : "string",
        "fields.DateTimeField" : "date",
        "fields.FloatField" : "double",
        "fields.IntegerField" : "int",
        "fields.BooleanField" : "bool",
        "fields.TimestampField" : "timestamp",
        "fields.ReferenceField" : "objectId",
        "reviewer_model.ValidatedReferenceField" : "objectId",
        "reviewer_model.ValidatedReferenceList" : "ref_list",
        "fields.ListField" : "list",
        "fields.DictField" : "dict",
        "fields.BinaryField" : "binData"
    }

ignore_list = [
        "ValidatedReferenceField",
        "ValidatedReferenceList",
        "Service",
        "AuthInfo"
    ]

to_fill = {
    "person" : 20000,
    "group" : 10,
    "person_ss" : 100000,
    "person_hs" : 100000,
    "ss_review" : 100000,
    "hs_review" : 100000,
    "specialization_review" : 100000,
}
filled={}
starting_ids = {}
doc_fields = {}
doc_u_indexes = {}

members = inspect.getmembers(model, inspect.isclass)
doc_class_list = []
for name, desc in members:
    if "reviewer_model." in str(desc):
        doc_class_list.append(desc)

for doc_class in doc_class_list:
    cur_class = str(doc_class.__name__)
    if cur_class in ignore_list:
        continue
    member_list = inspect.getmembers(doc_class, None)
    fields = {}
    col_name = convert(cur_class)
    for name, cls in member_list:
        if "__dict__" not in str(name):
            for py_name, bson_name in field_aliases.items():
                if py_name in str(cls):
                    if py_name == "pymodm.fields.ReferenceField" or\
                        py_name == "reviewer_model.ValidatedReferenceField":
                        rel_model = convert(cls.related_model.__name__)
                    elif py_name == "reviewer_model.ValidatedReferenceList":
                        member_list = inspect.getmembers(cls, None)
                        rel_model = convert(cls._field.related_model.__name__)
                    else:
                        rel_model = None
                    fields.update({ name : {
                                   "type" : bson_name,
                                   "ref"  : rel_model}})

    doc_fields.update({col_name : fields})
    # This is all about indexes on reference fields (not lists of references)
    # Indexes that are combined with string fields are not considered,
    # because uniqueness of the pair is guaranteed by string field
    unique_indexes = []
    if hasattr(doc_class.Meta, "indexes"):
        for index in doc_class.Meta.indexes:
            if index.document["unique"] == True:
                ind_dict = index.document["key"].to_dict()
                has_string = False
                for field, order in ind_dict.items():
                    if fields[field]["type"] == "string":
                        has_string = True
                    if fields[field]["type"] == "objectId":
                        unique_indexes.append(field)
                if has_string:
                    unique_indexes = []
    if len(unique_indexes) > 0:
        doc_u_indexes.update({col_name: unique_indexes})

doc_ctr = 1

def gen_ref(num : int, refs : list):
    n = num
    #TODO dividers must be calculated once per collection
    dividers = [1] * len(refs)
    for i in range(len(refs)):
        dividers[i] = refs[i]
        for j in range(0,i):
            if (i != j):
                dividers[i] *= dividers[j]
    dividers.pop(len(refs)-1)
    out_list = []
    for div in dividers:
        (q,r) = divmod(n, div)
        out_list.append(q)
        n = r
    out_list.append(n)
    return out_list

remaining_fields = doc_fields.copy()
one_pass_for_everyone = hash_password("12345")

while len(remaining_fields) > 0:
    print("--------------")
    for col_name, field_list in doc_fields.items():
        print("------")
        print(datetime.datetime.now())
        can_fill = True
        if col_name in filled:
            print(col_name + " is already filled, skipping")
            can_fill = False
        for field, info in field_list.items():
            if info["ref"] and info["ref"] not in filled:
                print("%s not filled yet, skipping %s for now" %(info["ref"],col_name))
                can_fill = False
        if can_fill:
            ref_count = {}
            print("filling " + col_name)
            if col_name in to_fill:
                insert_amount = to_fill[col_name]
            else:
                insert_amount = 10
            increment = 1
            if col_name in doc_u_indexes:
                print("Need to guarantee reference combinations uniqueness for %s"%col_name)
                max_comb = 1

                for field, info in field_list.items():
                    if field in doc_u_indexes[col_name]:
                        max_comb *= filled[info["ref"]]
                        ref_count.update({info["ref"] : filled[info["ref"]]})
                print("Maximum reference combinations: %s" % max_comb)
                print("Requested reference combinations: %s" % insert_amount)
                if max_comb < insert_amount:
                    raise ValueError("uniqueness is impossible for %s" %col_name)
                print(ref_count)
                increment = int(max_comb/insert_amount)
            doc_list = []
            cur_starting_id = doc_ctr
            starting_ids.update({col_name : cur_starting_id})
            added_cnt = 0

            r_col_names = []
            r_cnts = []
            r_field_names = []
            for r_name, r_cnt in ref_count.items():
                r_col_names.append(r_name)
                r_cnts.append(r_cnt)
                for field, info in field_list.items():
                    if info["ref"] == r_name:
                        r_field_names.append(field)

            auth_list = []
            for i in range(insert_amount):
                cur_doc = {"_id" : int_to_obj_id(doc_ctr)}
                #first we are going to fill reference fields that are in unique index
                if ref_count:

                    ref_field_vals = gen_ref(increment *(doc_ctr - cur_starting_id),
                                             r_cnts)
                    for i, r_name in enumerate(r_field_names):
                        start = starting_ids[r_col_names[i]]
                        cur_doc.update({r_field_names[i]: start + ref_field_vals[i]})
                for field, info in field_list.items():
                    if info["type"] == "string":
                        cur_doc.update({field : field + "_" + str(random.randint(0,999)) +
                                                                 "_" + str(doc_ctr)})
                    elif info["type"] == "date":
                        cur_doc.update({field: datetime.datetime(random.randrange(1900, 2000),
                                             random.randrange(1, 12),
                                             random.randrange(1, 28))})
                    elif info["type"] == "double":
                        cur_doc.update({field: random.random()*100})
                    elif info["type"] == "int":
                        cur_doc.update({field: random.randint(0,10)})
                    elif info["type"] == "bool":
                        cur_doc.update({field: True})
                    elif info["type"] == "timestamp":
                        cur_doc.update({field: None})
                    elif info["type"] == "list":
                        cur_doc.update({field: ["stub"]})
                    elif info["type"] == "dict":
                        cur_doc.update({field: {"1" : "stub"}})
                    elif info["type"] == "binData":
                        pass
                    elif info["type"] == "objectId":
                        if info["ref"] not in ref_count:
                            start = starting_ids[info["ref"]]
                            amt = filled[info["ref"]]
                            num = start + random.randint(0,amt)
                            cur_doc.update({field: int_to_obj_id(num)})
                doc_list.append(cur_doc)

                if col_name == "person":
                    auth_doc = {"_id": int_to_obj_id(doc_ctr + to_fill["person"])}
                    auth_doc.update({
                        "attempts": 0,
                        "auth_code": None,
                        "is_approved": True,
                        "last_send_time": None,
                        "password": one_pass_for_everyone,
                        "permissions": random.randint(0, 1),
                        "person_id": cur_doc["_id"],
                        "phone_no" : cur_doc["phone_no"],
                        "session_id" : None
                    })
                    auth_list.append(auth_doc)
                doc_ctr += 1

            cnt = len(db[col_name].insert_many(doc_list, ordered=False).inserted_ids)
            filled.update({col_name: cnt})
            if auth_list:
                a_cnt = len(db["auth_info"].insert_many(auth_list, ordered=False).inserted_ids)
                doc_ctr += a_cnt

            remaining_fields.pop(col_name)

db["service"].insert_one({"_id" : int_to_obj_id(doc_ctr),
                          "db_version" : "0.4",
                          "api_version" : constants.api_version})
doc_ctr+= 1
db["auth_info"].insert_one({"_id" : int_to_obj_id(doc_ctr),
                          "attempts": 0,
                        "auth_code": None,
                        "is_approved": True,
                        "last_send_time": None,
                        "password": hash_password("SomeSecurePass"),
                        "permissions": 1,
                        "person_id": None,
                        "phone_no" : "79032233223",
                        "session_id" : None})
doc_ctr+= 1

print("--------------------------")
print("total inserted:")
for key,item in filled.items():
    print("%s: %s"% (key,item))


