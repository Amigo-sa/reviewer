# -*- coding: utf-8 -*-
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


    from pymodm.connection import _get_db

    @bp.route("/wipe", methods=['POST'])
    def wipe():
        try:
            revDb = _get_db(constants.db_name)
            colList = revDb.list_collection_names()
            for col in colList:
                revDb[col].delete_many({})
            result = {"result": ERR.OK}
        except:
            result = {"result": ERR.DB}
        return jsonify(result), 200


    @bp.route("/first_admin", methods=['POST'])
    def prepare_first_admin():
        try:
            auth_info = AuthInfo()
            auth_info.is_approved = True
            auth_info.phone_no = "79032233223"
            auth_info.password = hash_password("boov")
            session_id = gen_session_id()
            auth_info.session_id = session_id
            auth_info.permissions = 1
            result = {"result": ERR.OK,
                      "session_id" : session_id}
            auth_info.save()
        except:
            result = {"result": ERR.DB}
        return jsonify(result), 200

    @bp.route("/logged_in_person", methods=['POST'])
    def prepare_logged_in_person():
        try:
            phone_no = "79037577575"
            person = Person(
                "Иван",
                "Иванович",
                "Кац",
                date(1980, 1, 1),
                "78398889991")
            person.save()
            auth_info = AuthInfo()
            auth_info.is_approved = True
            auth_info.phone_no = phone_no
            auth_info.password = hash_password("user")
            session_id = gen_session_id()
            auth_info.session_id = session_id
            auth_info.permissions = 0
            auth_info.person_id = person.pk
            auth_info.save()
            result = {"result": ERR.OK,
                      "session_id": session_id,
                      "person_id" : str(person.pk)}
        except Exception as e:
            result = {"result": ERR.DB}
            print(e)
        return jsonify(result), 200

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