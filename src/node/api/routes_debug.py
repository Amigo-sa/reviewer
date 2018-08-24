# -*- coding: utf-8 -*-
from random import randint

from bson import ObjectId
import node.settings.errors as ERR
import node.settings.constants as constants
from flask import Blueprint, request, jsonify
from data.reviewer_model import *
from datetime import datetime, timezone, timedelta, date
from node.api.routes_auth import hash_password, gen_session_id

bp = Blueprint('routes_debug', __name__)

if __debug__:
    import node.settings.constants as constants
    import pymongo
    rev_client = pymongo.MongoClient(constants.mongo_db)
    rev_db = rev_client[constants.db_name]

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

    @bp.route("/shutdown", methods = ['POST'])
    def shutdown():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        result = {"result": ERR.OK}
        return jsonify(result), 200


    @bp.route("/session_aging", methods=['POST'])
    def age_sessions():
        req = request.get_json()
        try:
            phone_no = req["phone_no"]
            minutes = req["minutes"]
            auth_info = AuthInfo.objects.get({"phone_no" : phone_no})
            ts = auth_info.last_send_time
            dt = ts.as_datetime()
            print("old dt %s" % (dt))
            dt -= timedelta(minutes=int(minutes))
            print("new dt %s" % (dt))
            auth_info.last_send_time = dt
            auth_info.save()
            result = {"result": ERR.OK}
        except:
            result = {"result": ERR.DB}
        return jsonify(result), 200
