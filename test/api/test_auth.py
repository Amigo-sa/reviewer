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
import sys
import data.reviewer_model as model
from bson.binary import Binary

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


@mock_bp.route("/send_sms", methods=["POST"])
def mock_send_sms():
    req = request.get_json()
    try:
        auth_code = req["auth_code"]
        phone_no = req["phone_no"]
        print("sending sms to " + phone_no)
        cur_session.received_code = auth_code
        result = {"result": ERR.OK}
    except KeyError:
        result = {"result": ERR.INPUT}
    return jsonify(result), 200


@mock_bp.route("/status", methods=["GET"])
def mock_get_status():
    result = {"result": ERR.OK}
    return jsonify(result), 200


@mock_bp.route("/shutdown", methods=['POST'])
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
        start_server(node_port, log=False)


class SmsMockServer(Thread):
    def run(self):
        start_mock_server()


node_server_thread = NodeServer()
mock_server_thread = SmsMockServer()


class TestAuth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Загрузка адреса сервера
        cls.api_URL = "http://127.0.0.1:" + str(node_port)
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
                print("Connection attempt %s failed" % str(attempts))
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
        # requests.post(self.api_URL + "/wipe")
        hm.wipe_db(constants.db_name)
        cur_session.id = None
        cur_session.received_code = None
        self.admin_header = {"Authorization":
                                 "Bearer " + hm.prepare_first_admin()}

    def prepare_lists(self):
        # admin only routes
        self.admin_only_post = [
            "/organizations",
            "/persons",
            "/organizations/%s/departments" % self.org_id,
            "/departments/%s/groups" % self.dep_id,
            "/groups/%s/role_list" % self.group_id,
            "/group_roles",
            "/group_permissions",
            "/groups/%s/group_members" % self.group_id,
            "/group_members/%s/permissions" % self.group_member_id,
            "/group_members/%s/group_roles" % self.group_member_id,
            "/specializations",
            "/skill_types/%s/soft_skills" % self.skill_type_id,
            "/skill_types/%s/hard_skills" % self.skill_type_id,
            "/groups/%s/surveys" % self.group_id,
            "/groups/%s/tests" % self.group_id,
            "/tests/%s/results" % self.test_id,
            "/user_permissions",
            "/skill_types"
        ]
        self.admin_only_delete = [
            "/organizations/%s" % self.org_id,
            "/departments/%s" % self.dep_id,
            "/groups/%s" % self.group_id,
            "/group_roles/%s" % self.group_role_id,
            "/group_permissions/%s" % self.group_perm_id,
            "/persons/%s" % self.other_person_id,
            "/group_members/%s" % self.group_member_id,
            "/group_members/%s/permissions/%s" % (self.group_member_id, self.group_perm_id),
            "/specializations/%s" % self.spec_id,
            "/persons/specializations/%s" % self.user_spec_id,
            "/soft_skills/%s" % self.soft_skill_id,
            "/hard_skills/%s" % self.hard_skill_id,
            "/surveys/%s" % self.survey_id,
            "/tests/%s" % self.test_id,
            "/tests/results/%s" % self.test_result_id,
            "/skill_types/%s" % self.skill_type_id
        ]
        self.admin_only_patch = [
            "/group_members/%s" % self.group_member_id,
            "/persons/specializations/%s" % self.user_spec_id
        ]
        self.admin_only_get = [
            "/persons/%s" % self.other_person_id,
            "/group_members/%s" % self.other_group_member_id
        ]

        # non-admin permissions
        self.user_allowed_delete = [
            "/persons/%s" % self.user_person_id,
        ]
        self.user_allowed_get = [
            "/persons/%s" % self.user_person_id
        ]
        self.user_allowed_post = {
            "/surveys/%s" % self.group_id: {"person_id": self.user_person_id,
                                            "chosen_option": "1"}
        }

        self.user_allowed_put = [
            "/persons/%s/photo" % self.user_person_id
        ]

        self.gm_allowed_get = [
            "/group_members/%s" % self.group_member_id
        ]
        self.review_valid_post = [
            "/specializations/%s/reviews" % self.other_spec_id,
            "/groups/%s/reviews" % self.group_id,
            "/tests/%s/reviews" % self.test_id,
            "/group_members/%s/reviews" % self.other_group_member_id,
            "/persons/%s/hard_skills/%s/reviews" % (self.other_person_id, self.hard_skill_id),
            "/persons/%s/soft_skills/%s/reviews" % (self.other_person_id, self.soft_skill_id)
        ]
        # отзывы на свои качества и роли
        self.review_invalid_post = [
            "/specializations/%s/reviews" % self.user_spec_id,
            "/group_members/%s/reviews" % self.group_member_id,
            "/persons/%s/hard_skills/%s/reviews" % (self.user_person_id, self.hard_skill_id),
            "/persons/%s/soft_skills/%s/reviews" % (self.user_person_id, self.soft_skill_id)
        ]

        self.no_auth_get = [
            "/organizations",
            "/organizations/%s/departments" % self.org_id,
            "/groups/%s/role_list" % self.group_id,
            "/departments/%s/groups" % self.dep_id,
            "/group_roles",
            "/group_permissions",
            "/groups/%s/group_members" % self.group_id,
            "/persons/%s/group_members" % self.user_person_id,
            "/specializations",
            "/persons/%s/specializations" % self.user_person_id,
            "/persons",
            "/reviews",
            "/soft_skills",
            "/hard_skills",
            "/persons/soft_skills",
            "/persons/hard_skills",
            "/persons/soft_skills/%s" % self.soft_skill_id,
            "/persons/hard_skills/%s" % self.hard_skill_id,
            "/surveys",
            "/tests/%s" % self.test_id,
            "/tests/results/%s" % self.test_result_id,
            "/tests/results",
            "/version",
            "/skill_types"

        ]
        self.no_auth_data_get = [
            "/persons/%s/photo" % self.user_person_id,
        ]

    def prepare_docs(self):
        # prepare user
        self.user_phone = "78001112233"
        auth_user = hm.prepare_logged_in_person(self.user_phone)
        self.user_person_id = auth_user["person_id"]
        self.user_session_id = auth_user["session_id"]
        self.user_header = {"Authorization":
                                "Bearer " + self.user_session_id}
        # prepare data

        self.org_id = hm.post_item(self, self.api_URL + "/organizations", {"name": "sample_org"})
        self.dep_id = hm.post_item(self, self.api_URL + "/organizations/%s/departments" % self.org_id,
                                   {"name": "sample_dep"})
        self.group_id = hm.post_item(self, self.api_URL + "/departments/%s/groups" % self.dep_id,
                                     {"name": "sample_group"})
        self.group_role_id = hm.post_item(self, self.api_URL + "/group_roles",
                                          {"name": "sample_group_role"})
        self.group_perm_id = hm.post_item(self, self.api_URL + "/group_permissions",
                                          {"name": "sample_group_permission"})
        resp_json = requests.post(self.api_URL + "/groups/%s/role_list" % self.group_id,
                                  json={"role_list": [self.group_role_id]}, headers=self.admin_header).json()
        print(resp_json)
        self.group_member_id = hm.post_item(self, self.api_URL + "/groups/%s/group_members" % self.group_id,
                                            {"person_id": self.user_person_id,
                                             "role_id": self.group_role_id})

        self.spec_id = hm.post_item(self, self.api_URL + "/specializations",
                                    {"type": "Tutor",
                                     "detail": "TOE"})
        self.user_spec_id = hm.post_item(self, self.api_URL + "/persons/%s/specializations" % self.user_person_id,
                                         {"department_id": self.dep_id,
                                          "specialization_id": self.spec_id
                                          })

        skill_type = model.SkillType()
        skill_type.name = "skill_type_name"
        skill_type.save()

        self.skill_type_id = str(skill_type.pk)

        hard_skill = model.HardSkill()
        hard_skill.name = "hs_name"
        hard_skill.skill_type_id = skill_type.pk
        hard_skill.save()

        self.hard_skill_id = str(hard_skill.pk)

        soft_skill = model.SoftSkill()
        soft_skill.name = "ss_name"
        soft_skill.skill_type_id = skill_type.pk
        soft_skill.save()

        self.soft_skill_id = str(soft_skill.pk)

        survey = model.Survey()
        survey.group_id = self.group_id
        survey.description = "some descr"
        survey.survey_options = {"1": "opt1",
                                 "2": "opt2"}
        survey.survey_result = {"1": 6,
                                "2": 4}
        survey.save()
        self.survey_id = str(survey.pk)
        s_response = model.SurveyResponse()
        s_response.survey_id = survey.pk
        s_response.chosen_option = "1"
        s_response.person_id = self.user_person_id
        s_response.save()
        self.s_resp_id = str(s_response.pk)

        g_test = model.GroupTest()
        g_test.group_id = self.group_id
        g_test.name = "test_name"
        g_test.info = "test_info"
        g_test.save()
        self.test_id = str(g_test.pk)

        test_result = model.TestResult()
        test_result.test_id = self.test_id
        test_result.person_id = self.user_person_id
        test_result.result_data = ["result1"]
        test_result.save()
        self.test_result_id = str(test_result.pk)

        # prepare second person
        auth_user = hm.prepare_logged_in_person("78001112234")
        self.other_person_id = auth_user["person_id"]
        self.other_user_session_id = auth_user["session_id"]
        self.other_user_header = {"Authorization":
                                      "Bearer " + self.other_user_session_id}
        self.other_spec_id = hm.post_item(self, self.api_URL + "/persons/%s/specializations" % self.other_person_id,
                                          {"department_id": self.dep_id,
                                           "specialization_id": self.spec_id
                                           })

        self.other_group_member_id = hm.post_item(self, self.api_URL + "/groups/%s/group_members" % self.group_id,
                                                  {"person_id": self.other_person_id,
                                                   "role_id": self.group_role_id})

        self.third_person_id = hm.post_item(self, self.api_URL + "/persons",
                                            dict(first_name="Гендальф",
                                                 middle_name="Батькович",
                                                 surname="Серый",
                                                 birth_date=datetime.date(1170, 6, 12).isoformat(),
                                                 phone_no="79007745737"))

    def test_set_user_permissions(self):
        self.prepare_docs()
        post_data = {"phone_no" : self.user_phone,
                     "permissions" : "admin"}
        auth_info = model.AuthInfo.objects.get({"phone_no" : self.user_phone})
        auth_info.refresh_from_db()
        auth_info.permissions = 0x02
        auth_info.save()
        resp = requests.post(self.api_URL + "/user_permissions",
                             json=post_data,
                             headers=self.admin_header)
        self.assertEqual(200, resp.status_code, "resp status must be 200")
        self.assertEqual(ERR.OK, resp.json()["result"])
        auth_info.refresh_from_db()
        self.assertEqual(0x03, auth_info.permissions, "admin flag must be set")
        post_data = {"phone_no": self.user_phone,
                     "permissions": "user"}
        resp = requests.post(self.api_URL + "/user_permissions",
                             json=post_data,
                             headers=self.admin_header)
        self.assertEqual(200, resp.status_code, "resp status must be 200")
        self.assertEqual(ERR.OK, resp.json()["result"])
        auth_info.refresh_from_db()
        self.assertEqual(0x02, auth_info.permissions, "admin flag must be unset")

        post_data = {"phone_no": "somefakephone",
                     "permissions": "user"}
        resp = requests.post(self.api_URL + "/user_permissions",
                             json=post_data,
                             headers=self.admin_header)
        self.assertEqual(200, resp.status_code, "resp status must be 200")
        self.assertEqual(ERR.AUTH_INVALID_PHONE, resp.json()["result"],
                         "must return ERR.INVALID_PHONE on wrong phone format")

        post_data = {"phone_no": "78008989998",
                     "permissions": "user"}
        resp = requests.post(self.api_URL + "/user_permissions",
                             json=post_data,
                             headers=self.admin_header)
        self.assertEqual(200, resp.status_code, "resp status must be 200")
        self.assertEqual(ERR.NO_DATA, resp.json()["result"], "must return ERR.NO_DATA when no user exists")

        auth_info.is_approved = False
        auth_info.save()
        post_data = {"phone_no": self.user_phone,
                     "permissions": "user"}
        resp = requests.post(self.api_URL + "/user_permissions",
                             json=post_data,
                             headers=self.admin_header)
        self.assertEqual(200, resp.status_code, "resp status must be 200")
        self.assertEqual(ERR.AUTH, resp.json()["result"], "must return ERR_AUTH when user is not approved")

        auth_info.is_approved = True
        auth_info.save()
        post_data = {"phone_no": self.user_phone,
                     "permissions": "god_emperor"}
        resp = requests.post(self.api_URL + "/user_permissions",
                             json=post_data,
                             headers=self.admin_header)
        self.assertEqual(200, resp.status_code, "resp status must be 200")
        self.assertEqual(ERR.INPUT, resp.json()["result"], "must return ERR_INPUT on invalid input")


    def test_user_restricted_access(self):

        self.prepare_docs()
        self.prepare_lists()
        # trying posts and deletes
        post_data = {"sample": "data"}

        cont_header = self.user_header
        cont_header.update({"Content-Type": "image/jpeg"})

        resp = requests.put(self.api_URL + "/persons/%s/photo" % self.other_person_id,
                            headers=cont_header,
                            data=bytes(b"\x01"))
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.AUTH, resp.json()["result"])


        for url in self.admin_only_post:
            resp_json = hm.try_post_item(self, self.api_URL + url,
                                         post_data, self.user_header)
            self.assertEqual(ERR.AUTH, resp_json["result"],
                             "%s is restricted to post for user %s" % (url, self.user_person_id))
        for url in self.admin_only_delete:
            resp_json = hm.try_delete_item(self, self.api_URL + url, self.user_header)
            self.assertEqual(ERR.AUTH, resp_json["result"],
                             "%s is restricted to delete for user %s" % (url, self.user_person_id))
        for url in self.admin_only_patch:
            resp_json = hm.try_patch_item(self, self.api_URL + url,
                                          post_data, self.user_header)
            self.assertEqual(ERR.AUTH, resp_json["result"],
                             "%s is restricted to patch for user %s" % (url, self.user_person_id))
        for url in self.admin_only_get:
            resp_json = hm.try_get_item(self, self.api_URL + url,
                                        self.user_header)
            self.assertEqual(ERR.AUTH, resp_json["result"],
                             "%s is restricted to get for user %s" % (url, self.user_person_id))

    def test_user_allowed_access(self):
        self.prepare_docs()
        self.prepare_lists()
        post_data = {"sample": "data"}
        user_allowed_get_urls = []
        user_allowed_get_urls += self.user_allowed_get
        user_allowed_get_urls += self.gm_allowed_get

        for url, data in self.user_allowed_post.items():
            resp_json = hm.try_post_item(self, self.api_URL + url, data, self.user_header)
            self.assertNotEqual(ERR.AUTH, resp_json["result"],
                                "%s must not return ERR.AUTH for user %s" % (url, self.user_person_id))
        for url in user_allowed_get_urls:
            resp_json = hm.try_get_item(self, self.api_URL + url, self.user_header)
            self.assertNotEqual(ERR.AUTH, resp_json["result"],
                                "%s must not return ERR.AUTH for user %s" % (url, self.user_person_id))

        cont_header = self.user_header
        cont_header.update({"Content-Type": "image/jpeg"})
        for url in self.user_allowed_put:
            resp = requests.put(self.api_URL + url,
                                headers=cont_header,
                                data=bytes(b"\x01"))
            self.assertEqual(200, resp.status_code)
            self.assertEqual(ERR.OK, resp.json()["result"])

        for url in self.user_allowed_delete:
            resp_json = hm.try_delete_item(self, self.api_URL + url, self.user_header)
            self.assertNotEqual(ERR.AUTH, resp_json["result"],
                                "%s must not return ERR.AUTH for user %s" % (url, self.user_person_id))



    def test_review_post_normal(self):
        self.prepare_docs()
        self.prepare_lists()
        review_data = {"reviewer_id": self.user_person_id,
                       "value": "50.0",
                       "description": "string"}
        for url in self.review_valid_post:
            resp_json = hm.try_post_item(self, self.api_URL + url,
                                         review_data, self.user_header)
            self.assertNotEqual(ERR.AUTH, resp_json["result"],
                                "%s must not return ERR.AUTH for user %s" % (url, self.user_person_id))

    def test_review_wrong_reviewer_id(self):
        self.prepare_docs()
        self.prepare_lists()
        review_data = {"reviewer_id": self.other_person_id,
                       "value": "50.0",
                       "description": "string"}
        for url in self.review_valid_post:
            resp_json = hm.try_post_item(self, self.api_URL + url,
                                         review_data, self.user_header)
            self.assertEqual(ERR.AUTH, resp_json["result"],
                             "%s must return ERR.AUTH for user %s" % (url, self.user_person_id))

    def test_review_delete_normal(self):
        self.prepare_docs()
        self.prepare_lists()
        review_data = {"reviewer_id": self.user_person_id,
                       "value": "50.0",
                       "description": "string"}
        rev_ids = []
        for url in self.review_valid_post:
            resp_json = hm.try_post_item(self, self.api_URL + url,
                                         review_data, self.user_header)
            rev_ids.append(resp_json["id"])
            self.assertNotEqual(ERR.AUTH, resp_json["result"],
                                "%s must not return ERR.AUTH for user %s" % (url, self.user_person_id))
        for rev_id in rev_ids:
            resp_json = hm.try_delete_item(self, self.api_URL + "/reviews/" + rev_id,
                                           self.user_header)
            self.assertNotEqual(ERR.AUTH, resp_json["result"],
                                "DELETE %s must not return ERR.AUTH for user %s" % (url, self.user_person_id))

    def test_review_delete_unauth(self):
        self.prepare_docs()
        self.prepare_lists()
        review_data = {"reviewer_id": self.user_person_id,
                       "value": "50.0",
                       "description": "string"}
        rev_ids = []
        for url in self.review_valid_post:
            resp_json = hm.try_post_item(self, self.api_URL + url,
                                         review_data, self.user_header)
            rev_ids.append(resp_json["id"])
            self.assertNotEqual(ERR.AUTH, resp_json["result"],
                                "%s must not return ERR.AUTH for user %s" % (url, self.user_person_id))
        for rev_id in rev_ids:
            resp_json = hm.try_delete_item(self, self.api_URL + "/reviews/" + rev_id,
                                           self.other_user_header)
            self.assertEqual(ERR.AUTH, resp_json["result"],
                             "DELETE %s must return ERR.AUTH for user %s" % (url, self.user_person_id))

    def test_get_unauth(self):
        self.prepare_docs()
        self.prepare_lists()
        review_data = {"reviewer_id": self.user_person_id,
                       "value": "50.0",
                       "description": "string"}
        rev_ids = []
        person = model.Person(_id= self.user_person_id)
        person.refresh_from_db()
        person.photo = Binary(b"\x01")
        person.save()

        for url in self.no_auth_data_get:
            resp = requests.get(self.api_URL + url)
            self.assertEqual(200, resp.status_code)
            self.assertTrue(resp.content)
        for url in self.review_valid_post:
            resp_json = hm.try_post_item(self, self.api_URL + url,
                                         review_data, self.user_header)
            rev_ids.append(resp_json["id"])
            self.assertNotEqual(ERR.AUTH, resp_json["result"],
                                "%s must not return ERR.AUTH for user %s" % (url, self.user_person_id))
        for url in self.no_auth_get:
            resp_json = hm.try_get_item(self, self.api_URL + url, None)
            self.assertNotEqual(ERR.AUTH, resp_json["result"],
                                "get %s must not return ERR.AUTH without session" % url)
        for rev_id in rev_ids:
            resp_json = hm.try_get_item(self, self.api_URL + "/reviews/" + rev_id, None)
            self.assertNotEqual(ERR.AUTH, resp_json["result"],
                                "get %s must not return ERR.AUTH without session" % url)

    def test_review_post_on_self(self):
        self.prepare_docs()
        self.prepare_lists()
        review_data = {"reviewer_id": self.user_person_id,
                       "value": "50.0",
                       "description": "string"}
        for url in self.review_invalid_post:
            resp_json = hm.try_post_item(self, self.api_URL + url,
                                         review_data, self.user_header)
            self.assertEqual(ERR.AUTH, resp_json["result"],
                             "%s must return ERR.AUTH for user %s" % (url, self.user_person_id))

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
        self.assertEqual(ERR.AUTH_INVALID_PHONE, resp.json()["result"])
        phone_no = "99703322212"
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={
            "phone_no": phone_no,
        })
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.AUTH_INVALID_PHONE, resp.json()["result"])
        phone_no = "797033x2212"
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={
            "phone_no": phone_no,
        })
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.AUTH_INVALID_PHONE, resp.json()["result"])
        phone_no = "7970332"
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={
            "phone_no": phone_no,
        })
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.AUTH_INVALID_PHONE, resp.json()["result"])

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
            self.assertEqual(ERR.AUTH_CODE_INCORRECT, resp.json()["result"])
            self.assertEqual("wrong code, %s attempts remain" % (max_attempts - i - 1),
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
        hm.age_session(phone_no, 20)
        self.assertEqual(ERR.OK, resp.json()["result"])
        resp = requests.post(self.api_URL + "/finish_phone_confirmation",
                             json={"auth_code": cur_session.received_code,
                                   "session_id": cur_session.id})
        self.assertEqual(200, resp.status_code)
        self.assertEqual(ERR.AUTH_SESSION_EXPIRED, resp.json()["result"])

    def test_multiple_sms(self):
        phone_no = "79803322212"
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={"phone_no": phone_no})
        self.assertEqual(ERR.OK, resp.json()["result"])
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={"phone_no": phone_no})
        self.assertEqual(ERR.AUTH_SMS_TIMEOUT, resp.json()["result"])
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={"phone_no": phone_no})
        self.assertEqual(ERR.AUTH_SMS_TIMEOUT, resp.json()["result"])
        hm.age_session(phone_no, 1)
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={"phone_no": phone_no})
        self.assertEqual(ERR.AUTH_SMS_TIMEOUT, resp.json()["result"])
        hm.age_session(phone_no, 1)
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={"phone_no": phone_no})
        self.assertEqual(ERR.OK, resp.json()["result"])
        resp = requests.post(self.api_URL + "/confirm_phone_no", json={"phone_no": phone_no})
        self.assertEqual(ERR.AUTH_SMS_TIMEOUT, resp.json()["result"])

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
                                   "session_id": cur_session.id})
        self.assertEqual(ERR.OK, resp.json()["result"])
        return phone_no, password


if __name__ == "__main__":
    print("test_auth argv: " + str(sys.argv))
    if "--test" in sys.argv:
        sys.argv.remove("--test")
    unittest.main(verbosity=1)
