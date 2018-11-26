# -*- coding: utf-8 -*-
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

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


def add_resource(cls, res_fields, parent_cls=None, parend_id=None, parent_name=None,
                 optional_fields=None):
    req = request.get_json()
    try:
        d = dict((field, req[field]) for field in res_fields)
        if optional_fields:
            d2 = dict((field, req[field]) for field in optional_fields
                      if field in req)
            d.update(d2)
        obj = cls()
        if parent_cls:
            if parent_cls.objects.raw({"_id": ObjectId(parend_id)}).count():
                setattr(obj, parent_name, parent_cls(_id=parend_id))
            else:
                return jsonify({"result": ERR.NO_DATA}), 200
        for key, value in d.items():
            setattr(obj, key, value)
        obj.save()
        result = {"result": ERR.OK,
                  "id": str(obj.pk)}

    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except DuplicateKeyError:
        return jsonify({"result": ERR.DB_DUPLICATE}), 200
    except Exception as e:
        result = {"result": ERR.DB,
                  "error_message": str(e)}

    return jsonify(result), 200