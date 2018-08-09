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
node_port = 5002

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
        start_server(node_port)

class SmsMockServer(Thread):
    def run(self):
        start_mock_server()

node_server_thread = NodeServer()
mock_server_thread = SmsMockServer()

class TestAuth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Загрузка адреса сервера
        cls.api_URL = "http://127.0.0.1:"+str(node_port)
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

    def test_registration_normal(self):
        phone_no = "79803322212"
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={
            "phone_no": phone_no,
        })
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.OK, resp.json()["result"])
        cur_session.id = resp.json()["session_id"]
        print("Session ID is " + cur_session.id)
        print("Got SMS with code " + cur_session.received_code)
        resp = requests.post(self.api_URL + "/finish_phone_confirmation",
                             json={"auth_code": cur_session.received_code,
                                   "session_id": cur_session.id})
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.OK, resp.json()["result"])

    def test_registration_already_confirmed(self):
        phone_no, password = self.prepare_confirmed_user()
        resp = requests.post(self.api_URL + "/confirm_phone_no",
                             json={"phone_no": phone_no})
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.AUTH, resp.json()["result"])
        self.assertFalse("session_id" in resp.json(), "must not return session_id")

    def test_wrong_phone_no_format(self):
        phone_no = "797803322212"
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={
            "phone_no": phone_no,
        })
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.INPUT, resp.json()["result"])
        phone_no = "99703322212"
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={
            "phone_no": phone_no,
        })
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.INPUT, resp.json()["result"])
        phone_no = "797033x2212"
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={
            "phone_no": phone_no,
        })
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.INPUT, resp.json()["result"])
        phone_no = "7970332"
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={
            "phone_no": phone_no,
        })
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.INPUT, resp.json()["result"])


    def test_wrong_sms_code(self):
        phone_no = "79803322212"
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={
            "phone_no": phone_no,
        })
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.OK, resp.json()["result"])
        cur_session.id = resp.json()["session_id"]
        print("Session ID is " + cur_session.id)
        print("Got SMS with code " + cur_session.received_code)
        max_attempts = 3
        for i in range(max_attempts - 1):
            resp = requests.post(self.api_URL + "/finish_phone_confirmation",
                                 json={"auth_code": "some_wrong_code",
                                       "session_id": cur_session.id})
            self.assertEqual(200, resp.status_code)
            self.assertEqual(ERR.AUTH, resp.json()["result"])
            self.assertEqual("wrong code, %s attempts remain"%(max_attempts - i - 1),
                             resp.json()["error_message"])
        resp = requests.post(self.api_URL + "/finish_phone_confirmation",
                             json={"auth_code": "some_wrong_code",
                                   "session_id": cur_session.id})
        self.assertEqual("out of attempts, auth code destroyed",
                         resp.json()["error_message"])
        resp = requests.post(self.api_URL + "/finish_phone_confirmation",
                             json={"auth_code": "some_wrong_code",
                                   "session_id": cur_session.id})
        self.assertEqual(ERR.AUTH_NO_SESSION,
                         resp.json()["result"])
        self.assertEqual("no session found",
                         resp.json()["error_message"])
        print(resp.json())

    def test_sms_timeout(self):
        phone_no = "79803322212"
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={
            "phone_no": phone_no,
        })
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.OK, resp.json()["result"])
        cur_session.id = resp.json()["session_id"]
        print("Session ID is " + cur_session.id)
        print("Got SMS with code " + cur_session.received_code)
        resp = requests.post(self.api_URL + "/session_aging", json={
            "phone_no": phone_no,
            "minutes": "20",
        })
        self.assertEqual(ERR.OK, resp.json()["result"])
        resp = requests.post(self.api_URL + "/finish_phone_confirmation",
                             json={"auth_code": cur_session.received_code,
                                   "session_id": cur_session.id})
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.AUTH, resp.json()["result"])


    def test_multiple_sms(self):
        phone_no = "79803322212"
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={"phone_no": phone_no})
        self.assertEqual(ERR.OK, resp.json()["result"])
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={"phone_no": phone_no})
        self.assertEqual(ERR.AUTH, resp.json()["result"])
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={"phone_no": phone_no})
        self.assertEqual(ERR.AUTH, resp.json()["result"])
        resp = requests.post(self.api_URL + "/session_aging", json={
            "phone_no": phone_no,
            "minutes": "1"})
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={"phone_no": phone_no})
        self.assertEqual(ERR.AUTH, resp.json()["result"])
        resp = requests.post(self.api_URL + "/session_aging", json={
            "phone_no": phone_no,
            "minutes": "1"})
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={"phone_no": phone_no})
        self.assertEqual(ERR.OK, resp.json()["result"])
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={"phone_no": phone_no})
        self.assertEqual(ERR.AUTH, resp.json()["result"])

    def test_login_normal(self):
        phone_no, password = self.prepare_confirmed_user()
        resp = requests.post(self.api_URL + "/user_login", json={
            "phone_no": phone_no,
            "password": password})
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.OK, resp.json()["result"])
        self.assertTrue(resp.json()["session_id"], "must return session_id")

    def test_login_wrong_pass(self):
        phone_no, password = self.prepare_confirmed_user()
        resp = requests.post(self.api_URL + "/user_login", json={
            "phone_no": phone_no,
            "password": "blablabla"})
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.AUTH, resp.json()["result"])
        self.assertFalse("session_id" in resp.json(), "must not return session_id")

    def test_login_no_user(self):
        phone_no, password = self.prepare_confirmed_user()
        resp = requests.post(self.api_URL + "/user_login", json={
            "phone_no": "99999999999",
            "password": password})
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.AUTH, resp.json()["result"])
        self.assertFalse("session_id" in resp.json(), "must not return session_id")

    def prepare_confirmed_user(self):
        phone_no = "78007553535"
        password = "sa"
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={
            "phone_no": phone_no})
        self.assertEqual(ERR.OK, resp.json()["result"])
        cur_session.id = resp.json()["session_id"]
        resp = requests.post(self.api_URL + "/finish_phone_confirmation",
                             json={"auth_code": cur_session.received_code,
                                   "session_id": cur_session.id})
        self.assertEqual(ERR.OK, resp.json()["result"])
        resp = requests.post(self.api_URL + "/password",
                             json={"password": password,
                                   "session_id" : cur_session.id})
        self.assertEqual(ERR.OK, resp.json()["result"])
        return phone_no, password



if __name__ == "__main__":
    unittest.main(verbosity = 1)
