# -*- coding: utf-8 -*-
from bson import ObjectId
import node.settings.errors as ERR
import node.settings.constants as constants
from flask import Blueprint, request, jsonify
from data.reviewer_model import *
from node.api.auth import required_auth
from node.api.base_functions import delete_resource, list_resources, add_resource

bp = Blueprint('departments', __name__)


@bp.route("/organizations/<string:id>/departments", methods = ['POST'])
@required_auth("admin")
def add_department(id):
    return add_resource(Department,
                        ["name"],
                        Organization,
                        id,
                        "organization_id")


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
