from pymongo import MongoClient
uri="mongodb://localhost:27017"
db_name='reviewer'
client = MongoClient(uri)
db = client[db_name]

colList = db.list_collection_names()
for col in colList:
    db.drop_collection(col)
    print("dropped collection " + col)
print("done")

import context
import data.reviewer_model as model
import os, sys, inspect, re

from bson import ObjectId
import datetime
import random
from node.settings import constants



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
    "person" : 20000,
    "group" : 1000,
    "person_ss" : 100000,
    "person_hs" : 100000,
    "ss_review" : 100000,
    "hs_review" : 100000,
    "specialization_review" : 100000,
}
filled={}
starting_ids = {}

#global_oid = 0xF00000000000000000000000

doc_dependencies = {}
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
    fields = []
    dependencies = []
    col_name = convert(cur_class)
    for name, cls in member_list:
        if "__dict__" not in str(name):
            for py_name, bson_name in field_aliases.items():
                if py_name in str(cls):
                    if py_name == "pymodm.fields.ReferenceField" or\
                        py_name == "reviewer_model.ValidatedReferenceField":
                        rel_model = cls.related_model.__name__
                        dependencies.append((name, bson_name, convert(rel_model)))
                        fields.append((name, bson_name, convert(rel_model)))
                    elif py_name == "reviewer_model.ValidatedReferenceList":
                        member_list = inspect.getmembers(cls, None)
                        rel_model = cls._field.related_model.__name__
                        dependencies.append((name, bson_name, convert(rel_model)))
                        fields.append((name, bson_name, convert(rel_model)))
                    else:
                        fields.append((name, bson_name))

    doc_dependencies.update({col_name : dependencies})
    doc_fields.update({col_name : fields})

doc_ctr = 0


#TODO implement proper condition check
for k in range(5):
    print("step %s"% (k + 1))
    for col_name, field_list in doc_fields.items():
        print("------")
        print(datetime.datetime.now())
        can_add = True
        if col_name in filled:
            print(col_name + " is filled, skipping")
            can_add = False
        for dep in doc_dependencies[col_name]:
            if dep[2] not in filled:
                print(dep[2] + " not filled yet, skipping for now")
                can_add = False
        if can_add:
            print("now filling " + col_name)
            doc_list = []
            starting_ids.update({col_name : doc_ctr + 1})
            added_cnt = 0
            if col_name in to_fill:
                insert_amount = to_fill[col_name]
            else:
                insert_amount = 10
            for i in range(insert_amount):
                doc_ctr += 1
                cur_doc = {"_id" : doc_ctr}
                #global_oid += 1
                for field in field_list:
                    if field[1] == "string":
                        cur_doc.update({field[0] : field[0] + "_" + str(doc_ctr)})
                    elif field[1] == "date":
                        cur_doc.update({field[0]: datetime.datetime(random.randrange(1900, 2000),
                                             random.randrange(1, 12),
                                             random.randrange(1, 28))})
                    elif field[1] == "double":
                        cur_doc.update({field[0]: random.random()*100})
                    elif field[1] == "int":
                        cur_doc.update({field[0]: random.randint(0,10)})
                    elif field[1] == "bool":
                        cur_doc.update({field[0]: True})
                    elif field[1] == "timestamp":
                        cur_doc.update({field[0]: None})
                    elif field[1] == "list":
                        cur_doc.update({field[0]: ["stub"]})
                    elif field[1] == "dict":
                        cur_doc.update({field[0]: {"1" : "stub"}})
                    elif field[1] == "binData":
                        pass
                    elif field[1] == "objectId":
                        start = starting_ids[field[2]]
#                        print(start)
                        amt = filled[field[2]]
#                        print(amt)
                        num = start + random.randint(0,amt)
                        cur_doc.update({field[0]: num})
                doc_list.append(cur_doc)
                #TODO handle uniqueness properly
                try:
                    db[col_name].insert_one(cur_doc)
                    added_cnt+= 1
                except:
                    doc_ctr -= 1
            #cnt = len(db[col_name].insert_many(doc_list, ordered=False).inserted_ids)
            #filled.update({col_name : cnt})
            filled.update({col_name: added_cnt})

db["service"].insert_one({"db_version" : "0.4",
                          "api_version" : constants.api_version})

print("--------------------------")
print("total inserted:")
for key,item in filled.items():
    print("%s: %s"% (key,item))


