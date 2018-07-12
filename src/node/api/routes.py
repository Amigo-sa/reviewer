import settings.constants as constants
import settings.errors as ERR
import pymongo
from flask import Blueprint, request, jsonify

rev_client = pymongo.MongoClient(constants.mongo_db)
rev_db = rev_client["reviewer"]

bp = Blueprint('routes', __name__)

if __debug__:
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
        cursor = rev_db['organization']
        item = {"name": req['name']}
        id = cursor.insert(item)
        result = {"result":ERR.OK,
                  "id": str(id)}
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200

