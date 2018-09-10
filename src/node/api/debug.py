# -*- coding: utf-8 -*-
from random import randint

from bson import ObjectId
import node.settings.errors as ERR
import node.settings.constants as constants
from flask import Blueprint, request, jsonify, current_app
from data.reviewer_model import *
from datetime import datetime, timezone, timedelta, date
from node.api.auth import hash_password, gen_session_id

bp = Blueprint('routes_debug', __name__)

api_v2 = Blueprint('routes_debug_v2', __name__)

if __debug__:
    import node.settings.constants as constants
    import pymongo
    rev_client = pymongo.MongoClient(constants.mongo_db)
    rev_db = rev_client[db_name]

    @bp.route('/')
    @bp.route('/index')
    def index():
        from node.node_server import app_mode
        result_string = "Application in {0} mode<br>".format(app_mode)
        collection_names = rev_db.list_collection_names()
        result_string += "Db content: <br>"
        for name in collection_names:
            result_string += "Column: {0}<br>".format(name)
            collection = rev_db[name]
            cursor = collection.find({})
            for document in cursor:
                if "photo" in document:
                    document["photo"] = "binnary data (edited)"
                result_string += "document: {0}<br>".format(document)
        return result_string

    @bp.route("/shutdown", methods = ['POST'])
    def shutdown():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        result = {"result": ERR.OK}
        return jsonify(result), 200

    @api_v2.route('/')
    @api_v2.route('/index')
    def index_v2():
        from node.node_server import app_mode
        result_string = "Application in {0} mode<br>".format(app_mode)
        result_string += "This is absolutely new version"
        return result_string

