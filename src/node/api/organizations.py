# -*- coding: utf-8 -*-
from bson import ObjectId
import node.settings.errors as ERR
import node.settings.constants as constants
from flask import Blueprint, request, jsonify
from data.reviewer_model import *
from node.api.auth import required_auth
from node.api.base_functions import delete_resource, list_resources

bp = Blueprint('organizations', __name__)


@bp.route("/organizations", methods = ['POST'])
@required_auth("admin")
def add_organization():
    req = request.get_json()
    try:
        name = req['name']
    except:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        organization = Organization(name)
        organization.save()
        result = {"result":ERR.OK,
                  "id": str(organization.pk)}
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/organizations/<string:id>", methods = ['DELETE'])
@required_auth("admin")
def delete_organization(id):
    return delete_resource(Organization, id)


@bp.route("/organizations", methods = ['GET'])
def list_organizations():
    return list_resources(Organization,
                          {"id": "_id", "name": "name"})
