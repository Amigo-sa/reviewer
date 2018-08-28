# -*- coding: utf-8 -*-
from bson import ObjectId
import node.settings.errors as ERR
import node.settings.constants as constants
from flask import Blueprint, request, jsonify
from data.reviewer_model import *
from node.api.auth import required_auth
from node.api.base_functions import delete_resource, list_resources

bp = Blueprint('departments', __name__)


@bp.route("/organizations/<string:id>/departments", methods = ['POST'])
@required_auth("admin")
def add_department(id):
    req = request.get_json()
    try:
        name = req['name']
        if Organization(_id=id) in Organization.objects.raw({"_id": ObjectId(id)}):
            department = Department(name, Organization(_id=id))
            department.save()
            result = {"result":ERR.OK,
                      "id": str(department.pk)}
        else:
            result = {"result": ERR.NO_DATA}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/departments/<string:id>", methods = ['DELETE'])
@required_auth("admin")
def delete_department(id):
    return delete_resource(Department, id)


@bp.route("/organizations/<string:id>/departments", methods = ['GET'])
def list_departments(id):
    return list_resources(Department,
                          {"id": "_id", "name": "name"},
                          Organization,
                          id,
                          "organization_id")
