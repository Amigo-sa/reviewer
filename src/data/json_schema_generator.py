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
    "fields.ListField" : "list"


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
    #print("--------------------------------------------------")
    #print(cur_class + ":")
    val = {
        "$jsonSchema": {
            "bsonType": "object",
            "properties": {}
        }
    }
    col_name = convert(cur_class)
    #print("Collection " + col_name)
    member_list = inspect.getmembers(doc_class, None)
    properties = {}
    # TODO required
    # TODO allow blank
    # TODO custom filters
    # TODO filter blank
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
                                        "bsonType": "array",
                                        "items": {
                                            "bsonType": [ref_bson_name, "null"]
                                        }
                                    }
                                })
                        pass
                    elif bson_name == "ref_list":
                        properties.update({
                            name: {
                                "bsonType" : "array",
                                "items":{
                                    "bsonType" : ["objectId", "null"]
                                }
                            }
                        })
                        pass
                    elif bson_name == "dict":
                        pass
                    else:
                        properties.update({name: {
                            "bsonType": [bson_name, "null"]
                        }})

            """
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
    val["$jsonSchema"]["properties"].update(properties)
    #print(val)
    print(db.command("collMod", col_name, validator=val))

