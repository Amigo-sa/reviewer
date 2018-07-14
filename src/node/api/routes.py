from bson import ObjectId
import node.settings.errors as ERR
from flask import Blueprint, request, jsonify
from data.reviewer_model import *


bp = Blueprint('routes', __name__)

if __debug__:
    import node.settings.constants as constants
    import pymongo
    rev_client = pymongo.MongoClient(constants.mongo_db)
    rev_db = rev_client["reviewer"]

    @bp.route('/')
    @bp.route('/index')
    def index():
        collection_names = rev_db.list_collection_names()
        result_string = "Db content: <br>"
        for name in collection_names:
            result_string += "Column: {0}<br>".format(name)
            collection = rev_db[name]
            cursor = collection.find({})
            for document in cursor:
                  result_string += "document: {0}<br>".format(document)
        return result_string


@bp.route("/add_organization", methods = ['POST'])
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


@bp.route("/delete_organization/<string:id>", methods = ['DELETE'])
def delete_organization(id):
    try:
        if Organization(_id=id) in Organization.objects.raw({"_id":ObjectId(id)}):
            Organization(_id=id).delete()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


@bp.route("/list_organizations", methods = ['GET'])
def list_organizations():
    list = []
    try:
        for organization in  Organization.objects.all():
            list.append({"id":str(organization.pk),
                         "name":organization.name}
                        )
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/add_department", methods = ['POST'])
def add_department():
    req = request.get_json()
    try:
        organization_id = req['organization_id']
        name = req['name']
    except:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        department = Department(name, Organization(_id=organization_id))
        department.save()
        result = {"result":ERR.OK,
                  "id": str(department.pk)}
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/delete_department/<string:id>", methods = ['DELETE'])
def delete_department(id):
    try:
        if Department(_id=id) in Department.objects.raw({"_id":ObjectId(id)}):
            Department(_id=id).delete()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


@bp.route("/list_departments/<string:id>", methods = ['GET'])
def list_departments(id):
    list = []
    try:
        for department in  Department.objects.raw({"organization_id":ObjectId(id)}):
            list.append({"id":str(department.pk),
                         "name":department.name}
                        )
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/add_group", methods = ['POST'])
def add_group():
    req = request.get_json()
    try:
        department_id = req['department_id']
        name = req['name']
    except:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        group = Group(Department(_id=department_id), name)
        group.save()
        result = {"result":ERR.OK,
                  "id": str(group.pk)}
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/delete_group/<string:id>", methods = ['DELETE'])
def delete_group(id):
    try:
        if Group(_id=id) in Group.objects.raw({"_id":ObjectId(id)}):
            Group(_id=id).delete()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


@bp.route("/list_groups/<string:id>", methods = ['GET'])
def list_groups(id):
    list = []
    try:
        for group in  Group.objects.raw({"department_id":ObjectId(id)}):
            list.append({"id":str(group.pk),
                         "name":group.name}
                        )
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/add_group_role", methods = ['POST'])
def add_group_role():
    req = request.get_json()
    try:
        name = req['name']
    except:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        group_role = GroupRole(name)
        group_role.save()
        result = {"result":ERR.OK,
                  "id": str(group_role.pk)}
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/delete_group_role/<string:id>", methods = ['DELETE'])
def delete_group_role(id):
    try:
        if GroupRole(_id=id) in GroupRole.objects.raw({"_id":ObjectId(id)}):
            GroupRole(_id=id).delete()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


@bp.route("/list_group_roles", methods = ['GET'])
def list_group_roles():
    list = []
    try:
        for group_role in  GroupRole.objects.all():
            list.append({"id":str(group_role.pk),
                         "name":group_role.name}
                        )
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200