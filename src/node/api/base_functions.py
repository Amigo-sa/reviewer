# -*- coding: utf-8 -*-
from bson import ObjectId
import node.settings.errors as ERR
import node.settings.constants as constants
from flask import Blueprint, request, jsonify
from data.reviewer_model import *


def delete_resource(cls, _id):
    try:
        if cls(_id=_id) in cls.objects.raw({"_id":ObjectId(_id)}):
            cls(_id=_id).delete()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


def list_resources(cls, res_fields, parent_cls=None, parent_id=None, parent_name=None):
    list = []
    try:
        if not parent_cls or parent_cls.objects.raw({"_id": ObjectId(parent_id)}).count():
            q = {} if not parent_cls else {parent_name:ObjectId(parent_id)}
            for obj in cls.objects.raw(q).values():
                d = dict((key, str(obj[value])) for key, value in res_fields.items()
                         if value in obj.keys())
                list.append(d)
            result = {"result": ERR.OK, "list":list}
        else:
            result = {"result": ERR.NO_DATA}
    except Exception as e:
        result = {"result": ERR.DB,
                  "error_message": str(e)}
    return jsonify(result), 200
