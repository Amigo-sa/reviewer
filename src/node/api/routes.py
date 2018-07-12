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
    if 'name' not in req:
        return jsonify({"result":ERR.INPUT}), 200
    try:
        organization = Organization(req['name'])
        organization.save()
        result = {"result":ERR.OK,
                  "id": str(organization.pk)}
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/delete_organization/<string:id>", methods = ['DELETE'])
def delete_organization(id):
    try:
        organization = Organization(_id=id)
        organization.delete()
        result = {"result": ERR.OK}
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