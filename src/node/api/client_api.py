import settings.constants as constants
import pymongo
from flask import Blueprint

rev_client = pymongo.MongoClient(constants.mongo_db)
rev_db = rev_client["reviewer"]

bp = Blueprint('client_api', __name__)

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