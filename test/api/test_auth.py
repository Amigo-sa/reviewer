# -*- coding: utf-8 -*-
import context
import unittest
from threading import Thread
from time import sleep
from flask import request, jsonify
import node.settings.errors as ERR
import api_helper_methods as hm
import requests
from flask import Flask, Blueprint
import datetime

from node.node_server import start_server
from node.settings import constants

mock_bp = Blueprint("mock_routes", __name__)
mock_port = 5010
mock_url = "http://127.0.0.1:" + str(mock_port)

class Session():
    def __init__(self):
        self.id = None
        self.received_code = None

cur_session = Session()

@mock_bp.route("/send_sms", methods= ["POST"])
def mock_send_sms():
    req = request.get_json()
    try:
        auth_code = req["auth_code"]
        phone_no = req["phone_no"]
        print("sending sms to " + phone_no)
        cur_session.received_code = auth_code
        #result = {"result": resp.json()["result"]}
        result = {"result" : ERR.OK}
    except KeyError:
        result = {"result" : ERR.INPUT}
    return jsonify(result), 200

@mock_bp.route("/status", methods= ["GET"])
def mock_get_status():
    result = {"result": ERR.OK}
    return jsonify(result), 200

@mock_bp.route("/shutdown", methods = ['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    result = {"result": ERR.OK}
    return jsonify(result), 200

def start_mock_server():
    app = Flask(__name__)
    app.register_blueprint(mock_bp)
    app.run(port=mock_port)

class NodeServer(Thread):
    def run(self):
        start_server()

class SmsMockServer(Thread):
    def run(self):
        start_mock_server()

node_server_thread = NodeServer()
mock_server_thread = SmsMockServer()

class TestAuth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Загрузка адреса сервера
        cls.api_URL = constants.core_server_url
        cls.gen_doc_ctr = 0
        print("Servers starting...")
        node_server_thread.start()
        mock_server_thread.start()
        attempts = 0
        connected = False
        print("Waiting for node server...")
        while not connected:
            try:
                requests.get(cls.api_URL + "/organizations")
                connected = True
            except Exception as e:
                attempts += 1
                sleep(0.5)
                print("Connection attempt %s failed" %str(attempts))
                if attempts > 20: raise ConnectionError("could not connect to node server")
        print("Connected to node server\r\n")
        attempts = 0
        connected = False
        print("Waiting for mock server...")
        while not connected:
            try:
                requests.get(mock_url + "/status")
                connected = True
            except Exception as e:
                attempts += 1
                sleep(0.5)
                print("Connection attempt %s failed" % str(attempts))
                if attempts > 20: raise ConnectionError("could not connect to mock server")
        print("Connected to mock server\r\n")


    @classmethod
    def tearDownClass(cls):
        requests.post(cls.api_URL + "/shutdown")
        requests.post(mock_url + "/shutdown")

    def tearDown(self):
        pass

    def setUp(self):
        requests.post(self.api_URL + "/wipe")
        cur_session.id = None
        cur_session.received_code = None

    def test_registration_invalid_person_phone(self):
        persons = hm.prepare_two_persons(self, self.api_URL)

        resp = requests.post(self.api_URL + "/register", json={
            "phone_no" : persons[0]["phone_no"],
            "person_id": persons[1]["id"]
        })
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.DB, resp.json()["result"])

    def test_registration_normal(self):
        # prepare persons
        persons = hm.prepare_two_persons(self, self.api_URL)
        # register previously unregistered person
        resp = requests.post(self.api_URL + "/register", json={
            "phone_no": persons[0]["phone_no"],
            "person_id": persons[0]["id"]
        })
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.OK, resp.json()["result"])
        cur_session.id = resp.json()["session"]
        # we get session id as a response for our /register request
        print("Session ID is " + cur_session.id)
        print("Waiting for SMS...")
        # the send_sms route imitates:
        # 1. sms sending by smsc;
        # 2. sms reception by user and input the code in a form.
        # when that route is requested, it stores auth_code in
        # cur_session.received_code
        while not (cur_session.id and cur_session.received_code):
            pass
        print("Got SMS with code " + cur_session.received_code)
        resp = requests.post(constants.core_server_url + "/confirm_registration",
                             json={"auth_code": cur_session.received_code,
                                   "session_id": cur_session.id})
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.OK, resp.json()["result"])


        # test invalid person and/or phone
        # test timeout did not expire
        # test normal

if __name__ == "__main__":
    unittest.main(verbosity = 1)
