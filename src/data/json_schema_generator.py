# -*- coding: utf-8 -*-
import os, sys, inspect, re
import data.reviewer_model
from pymongo import MongoClient
from node.settings import constants


def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def create_validators(uri="mongodb://localhost:27017", db_name='reviewer'):

    members = inspect.getmembers(data.reviewer_model, inspect.isclass)
    doc_class_list = []
    for name, desc in members:
        if "reviewer_model." in str(desc):
            doc_class_list.append(desc)
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
        "ValidatedReferenceList"
    ]
    special_rules = {
        "person" : {
            "phone_no" :
                {
                    "pattern": "^[0-9]+$"
                }
        }
    }

    client = MongoClient(uri)
    db = client[db_name]
    col_list = db.collection_names()

    for doc_class in doc_class_list:
        cur_class = str(doc_class.__name__)
        if cur_class in ignore_list:
            continue
        print("--------------------------------------------------")
        print(cur_class + ":")
        val = {
            "$jsonSchema": {
                "bsonType": "object",
                "additionalProperties": False,
                "properties": {}
            }
        }
        col_name = convert(cur_class)
        print("Collection " + col_name)
        member_list = inspect.getmembers(doc_class, None)
        properties = {"_id": {}}
        required_fields = []
        for name, cls in member_list:
            if "__dict__" not in str(name):
                for py_name, bson_name in field_aliases.items():
                    if py_name in str(cls):
                        if bson_name == "list":
                            item_type = cls._field
                            for ref_py_name, ref_bson_name in field_aliases.items():
                                if ref_py_name in str(item_type):
                                    if ref_bson_name == "list" or\
                                    ref_bson_name == "ref_list" or\
                                    ref_bson_name == "dict":
                                        raise TypeError("nested lists and dicts are not supported")
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
                            properties[name]["bsonType"].append("null")
                        if col_name in special_rules:
                            if name in special_rules[col_name]:
                                properties[name].update(special_rules[col_name][name])
        val["$jsonSchema"]["properties"].update(properties)
        if required_fields:
            val["$jsonSchema"].update({"required" : required_fields})
        print(val)
        if col_name in col_list:
            print(db.command("collMod", col_name, validator=val))
        else:
            pass
            print(db.command("create", col_name, validator=val))

if __name__ == "__main__":
    db_name = constants.db_name
    print("DB initialized with argv: " + str(sys.argv))
    if len(sys.argv) > 1:
        if '--test' in str(sys.argv):
            db_name = constants.db_name_test
    print("Working with DB '%s' \n" % db_name)
    create_validators(constants.mongo_db, db_name)