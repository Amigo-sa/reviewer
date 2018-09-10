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


from bson import ObjectId
import datetime
import random




def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

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
        "Service"
    ]

to_fill = {
    "person" : 2000,
    "group" : 100,
    "person_ss" : 1000,
    "person_hs" : 1000,
    "ss_review" : 1000,
    "hs_review" : 1000,
    "specialization_review" : 1000,
}
filled={}
starting_ids = {}
doc_fields = {}

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

doc_ctr = 1

remaining_fields = doc_fields.copy()

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
            print("filling " + col_name)
            #doc_list = []
            starting_ids.update({col_name : doc_ctr})
            added_cnt = 0
            if col_name in to_fill:
                insert_amount = to_fill[col_name]
            else:
                insert_amount = 10
            for i in range(insert_amount):
                cur_doc = {"_id" : doc_ctr}
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
                        start = starting_ids[info["ref"]]
#                        print(start)
                        amt = filled[info["ref"]]
#                        print(amt)
                        num = start + random.randint(0,amt)
                        cur_doc.update({field: num})
                #doc_list.append(cur_doc)
                #TODO handle uniqueness properly
                try:
                    db[col_name].insert_one(cur_doc)
                    added_cnt += 1
                    doc_ctr += 1
                except:
                    pass
            #cnt = len(db[col_name].insert_many(doc_list, ordered=False).inserted_ids)
            #filled.update({col_name : cnt})
            filled.update({col_name: added_cnt})
            remaining_fields.pop(col_name)

db["service"].insert_one({"db_version" : "0.4",
                          "api_version" : constants.api_version})

print("--------------------------")
print("total inserted:")
for key,item in filled.items():
    print("%s: %s"% (key,item))


