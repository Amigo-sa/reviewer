# -*- coding: utf-8 -*-
import os, sys, inspect, re
import data.reviewer_model
from pymongo import MongoClient

members = inspect.getmembers(data.reviewer_model, inspect.isclass)

doc_class_list = []
class_names = []
for name, desc in members:
    if "reviewer_model." in str(desc):
        doc_class_list.append(desc)
        class_names.append(name)

links = {}
fields = {}
for doc_class in doc_class_list:
    print("--------------------------------------------------")
    cur_class = str(doc_class.__name__)
    print(cur_class + " references:")
    links.update({cur_class: []})
    fields.update({cur_class: []})
    member_list = inspect.getmembers(doc_class, None)
    for name, cls in member_list:
        if "__dict__" not in str(name):
            field = {"name": name}
            if "fields.CharField" in str(cls):
                field.update({"type": "string"})
                fields[cur_class].append(field)
            if "fields.DateTimeField" in str(cls):
                field.update({"type": "date"})
                fields[cur_class].append(field)
            if "fields.FloatField" in str(cls):
                field.update({"type": "double"})
                fields[cur_class].append(field)
            if "fields.IntegerField" in str(cls):
                field.update({"type": "int"})
                fields[cur_class].append(field)
            if "fields.BooleanField" in str(cls):
                field.update({"type": "bool"})
                fields[cur_class].append(field)
            if "fields.TimestampField" in str(cls):
                field.update({"type": "timestamp"})
                fields[cur_class].append(field)
            """
            if "pymodm.fields.ReferenceField" in str(cls) \
                    or "reviewer_model.ValidatedReferenceField" in str(cls):
                rel_model = cls.related_model.__name__
                print(rel_model)
                links[cur_class].append(rel_model)
                # TODO implement
            if "reviewer_model.ValidatedReferenceList" in str(cls):
                member_list = inspect.getmembers(cls, None)
                rel_model = cls._field.related_model.__name__
                print(rel_model)
                links[cur_class].append(rel_model)
                # TODO implement
            
            
            if "fields.DictField" in str(cls):
                field = name# + ': "dict"'
                fields[cur_class].append(field)
            if "fields.ListField" in str(cls):
                field = name# + ': "list"'
                fields[cur_class].append(field)
            """

ignore_list = [
    "Service",
    "ValidatedReferenceField",
    "ValidatedReferenceList"
]
for item in ignore_list:
    links.pop(item)
    class_names.remove(item)
    fields.pop(item)

def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


print(fields)

client = MongoClient('localhost', 27017)
db = client.reviewer

for key, values in fields.items():
    col_name = convert(key)
    print(col_name)
    # TODO required
    val = {
        "$jsonSchema": {
            "bsonType": "object",
            "properties": {}
        }
    }
    props = {}
    for item in values:
        props.update({item["name"] : {
            "bsonType": [item["type"], "null"]
        }})
    val["$jsonSchema"]["properties"].update(props)
    print(val)
    print(db.command("collMod", col_name, validator=val))


"""
val = {
  "$jsonSchema": {
     "bsonType": "object",
     "required": ["first_name"],
     "properties": {
        "first_name": {
           "bsonType": "string",
           "description": "must be a string and is required"
        },
     }
  }
}
"""







