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

field_aliases = {
    "fields.CharField" : "string",
    "fields.DateTimeField" : "date",
    "fields.FloatField" : "double",
    "fields.IntegerField" : "int",
    "fields.BooleanField" : "bool",
    "fields.TimestampField" : "timestamp",
    "pymodm.fields.ReferenceField" : "objectId",
    "reviewer_model.ValidatedReferenceField" : "objectId",
    "reviewer_model.ValidatedReferenceList" : "ref_list",
    "fields.ListField" : "list",
    "fields.DictField" : "dict"
}
ignore_list = [
    "Service",
    "ValidatedReferenceField",
    "ValidatedReferenceList"
]

def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

client = MongoClient('localhost', 27017)
db = client.reviewer

links = {}
fields = {}
for doc_class in doc_class_list:
    cur_class = str(doc_class.__name__)
    if cur_class in ignore_list:
        continue
    print("--------------------------------------------------")
    print(cur_class + ":")
    val = {
        "$jsonSchema": {
            "bsonType": "object",
            "properties": {}
        }
    }
    col_name = convert(cur_class)
    print("Collection " + col_name)
    member_list = inspect.getmembers(doc_class, None)
    properties = {}
    required_fields = []
    for name, cls in member_list:
        if "__dict__" not in str(name):
            for py_name, bson_name in field_aliases.items():
                if py_name in str(cls):
                    if bson_name == "list":
                        item_type = cls._field
                        for ref_py_name, ref_bson_name in field_aliases.items():
                            if ref_py_name in str(item_type):
                                if ref_bson_name == "list":
                                    raise TypeError("nested lists are not supported")
                                properties.update({
                                    name: {
                                        "bsonType": ["array"],
                                        "items": {
                                            "bsonType": [ref_bson_name, "null"]
                                        }
                                    }
                                })
                    elif bson_name == "ref_list":
                        properties.update({
                            name: {
                                "bsonType" : ["array"],
                                "items":{
                                    "bsonType" : ["objectId"]
                                }
                            }
                        })
                        pass
                    elif bson_name == "dict":
                        properties.update({
                            name: {
                                "bsonType": ["object"]
                            }
                        })
                    else:
                        properties.update({name: {
                            "bsonType": [bson_name]
                        }})
                    if cls.required:
                        required_fields.append(name)
                    if cls.blank:
                        print(cls)
                        properties[name]["bsonType"].append("null")
                        print(properties)
    val["$jsonSchema"]["properties"].update(properties)
    if required_fields:
        val["$jsonSchema"].update({"required" : required_fields})
    print(val)
    print(db.command("collMod", col_name, validator=val))
