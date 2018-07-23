import context
import unittest
import requests
from node.settings import constants
import node.settings.errors as ERR
from node.node_server import start_server
from threading import Thread
import random
import datetime
import re
#from src.data.reviewer_model import *

class NodeServer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        start_server()

node_server_thread = NodeServer()

class TestApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Загрузка адреса сервера
        cls.api_URL = constants.core_server_url
        cls.gen_doc_ctr = 0
        # Запуск сервера, (проверка на запущенность не проводится!)
        # TODO добавить проверку на запущенность сервера
        # TODO добавить очищение базы с сохранинем индексов
        node_server_thread.start()
        cls.clear_collection("/persons", "/persons")
        cls.clear_collection("/organizations", "/organizations")
        cls.clear_collection("/group_permissions", "/group_permissions")
        cls.clear_collection("/group_roles", "/group_roles")
        cls.clear_collection("/hard_skills", "/hard_skills")
        cls.clear_collection("/soft_skills", "/soft_skills")

    @classmethod
    def clear_collection(cls, url_list, url_delete):
        resp_json = requests.get(cls.api_URL + url_list).json()
        if resp_json["list"]:
            print("Warning: collection %s was not cleared after tests"%url_delete)
            for doc in resp_json["list"]:
                resp_json = requests.delete(url=cls.api_URL + url_delete+ "/" + doc["id"]).json()

    @classmethod
    def tearDownClass(cls):
        requests.post(cls.api_URL + "/shutdown")

    def tearDown(self):
        pass

    def setUp(self):

        pass

    def t_simple_normal(self, url_get, url_post, url_delete, *args, **kwargs):
        # read from empty DB
        resp = requests.get(self.api_URL + url_get)
        self.assertEqual(200, resp.status_code, "get response status code must be 200")
        resp_json = resp.json()
        self.assertEqual(resp_json["result"], ERR.OK, "result must be ERR.OK")
        read_list = resp_json["list"]
        self.assertListEqual([],read_list, "initial DB must not contain any " + url_delete)
        # write items to DB
        add_list = []
        items_to_write = 2
        for item_ctr in range(items_to_write):
            cur_item = self.generate_doc(kwargs.items())
            resp = requests.post(url=self.api_URL + url_post, json=cur_item)
            self.assertEqual(200, resp.status_code, "post response status code must be 200")
            resp_json = resp.json()
            self.assertEqual(resp_json["result"], ERR.OK, "post result must be ERR.OK")
            self.assertTrue(resp_json["id"], "returned id must be not None")
            cur_item.update({"id" : resp_json["id"]})
            add_list.append(cur_item)
        print("sample data for " + url_post + ":\n" + str(add_list))
        # verify written items
        resp_json = requests.get(self.api_URL + url_get).json()
        read_list = resp_json["list"]
        total_match = 0
        for added_item in add_list:
            item_match = 0
            for read_item in read_list:
                if added_item["id"] == read_item["id"]: # сравниваем только id, так как формат выдачи будет меняться
                    item_match += 1
                    total_match += 1
            self.assertEqual(item_match, 1, "must be exactly one match for each item")
        self.assertEqual(total_match, items_to_write, "all added items must be in GET list")
        # specific tests
        if url_delete == "/tests":
            parent_id = re.findall("\w+", url_post)[1]
            for added_item in add_list:
                resp_json = requests.get(self.api_URL + "/tests/" + added_item["id"]).json()
                self.assertEqual(resp_json["result"], ERR.OK, "the get test info result must be ERR.OK")
                self.assertEqual(resp_json["data"]["info"], added_item["info"], "test info must match")
                self.assertEqual(resp_json["data"]["name"], added_item["name"], "test name must match")
                self.assertEqual(resp_json["data"]["group_id"], parent_id, "group_ids must match")
        # delete items
        for item in add_list:
            resp = requests.delete(url=self.api_URL + url_delete + "/" + item["id"])
            self.assertEqual(200, resp.status_code, "delete response status code must be 200")
            resp_json = resp.json()
            self.assertEqual(resp_json["result"], ERR.OK, "result must be ERR.OK")
        # verify deletion
        resp_json = requests.get(self.api_URL + url_get).json()
        read_list = resp_json["list"]
        self.assertListEqual([], read_list, "docs must be erased from DB")
    @classmethod
    def generate_doc(cls, type_list, *args, **kwargs):
        cls.gen_doc_ctr += 1
        cur_item = dict()
        for key, value in type_list:
            if value == "string":
                cur_item.update({
                    key: "sample_" + key + "_" + str(cls.gen_doc_ctr + 1)
                })
            elif value == "date":
                # TODO уточнить, подойдёт ли ISO во всех случаях
                cur_date = datetime.date(random.randrange(1900, 2000),
                                         random.randrange(1, 12),
                                         random.randrange(1, 28))
                date_iso = cur_date.isoformat()
                cur_item.update({
                    key: date_iso
                })
            elif value == "number_string":
                cur_item.update({
                    key: "3223223" + str(cls.gen_doc_ctr)
                })
            elif value == "skill_level":
                cur_item.update({
                    key: random.random() * 100.0
                })
            else:
                cur_item.update({
                    key: value
                })
        for key, value in kwargs.items():
            cur_item.update({key: value})
        return cur_item

    def prepare_organization(self):
        post_data = self.generate_doc(dict(name="string").items())
        resp_json = requests.post(url=self.api_URL + '/organizations', json=post_data).json()
        self.assertEqual(resp_json["result"],ERR.OK, "aux organization must be created")
        return resp_json["id"]

    def prepare_department(self):
        aux_org_id = self.prepare_organization()
        self.assertTrue(aux_org_id, "auxiliary organization must be created")
        post_data = self.generate_doc(dict(name="string").items())
        resp_json = requests.post(url=self.api_URL + '/organizations/' + aux_org_id + "/departments", json=post_data).json()
        self.assertEqual(resp_json["result"], ERR.OK, "aux department must be created")
        return {"dep_id" : resp_json["id"],
                "org_id" : aux_org_id}

    def prepare_group(self):
        aux_items_ids = self.prepare_department()
        self.assertTrue(aux_items_ids["dep_id"], "aux department must be created")
        post_data = self.generate_doc(dict(name="string").items())
        resp_json = requests.post(url=self.api_URL + '/departments/' + aux_items_ids["dep_id"] + "/groups",
                                  json=post_data).json()
        self.assertEqual(resp_json["result"], ERR.OK, "aux group must be created")
        aux_items_ids.update({"group_id": resp_json["id"]})
        return aux_items_ids

    def prepare_persons(self, person_count):
        person_type_list = dict(first_name="string",
                             middle_name="string",
                             surname="string",
                             birth_date="date",
                             phone_no="number_string")
        id_list = []
        for person_ctr in range(person_count):
            cur_person = self.generate_doc(person_type_list.items())
            resp_json = requests.post(url=self.api_URL + "/persons", json=cur_person).json()
            self.assertEqual(resp_json["result"], ERR.OK, "aux person must be added")
            id_list.append(resp_json["id"])
        return id_list

    def prepare_hs(self):
        post_data = self.generate_doc(dict(name="string").items())
        resp_json = requests.post(url=self.api_URL + '/hard_skills', json=post_data).json()
        self.assertEqual(resp_json["result"], ERR.OK, "aux hard skill must be created")

    def delete_doc(self, url):
        resp_json = requests.delete(url=self.api_URL + url).json()
        self.assertEqual(resp_json["result"], ERR.OK, "the document must be deleted")

    def test_organization_normal(self):
        self.t_simple_normal(         "/organizations",
                                      "/organizations",
                                      "/organizations",
                                        name = "string")

    def test_person_normal(self):
        self.t_simple_normal("/persons",
                            "/persons",
                            "/persons",
                             first_name="string",
                             middle_name="string",
                             surname="string",
                             birth_date="date",
                             phone_no="number_string"
                             )
        pass

    def test_soft_skill_normal(self):
        self.t_simple_normal("/soft_skills",
                            "/soft_skills",
                            "/soft_skills",
                             name="string")

    def test_hard_skill_normal(self):
        self.t_simple_normal("/hard_skills",
                            "/hard_skills",
                            "/hard_skills",
                             name="string")

    def test_group_roles_normal(self):
        self.t_simple_normal("/group_roles",
                            "/group_roles",
                            "/group_roles",
                             name="string")

    def test_group_permissions_normal(self):
        self.t_simple_normal("/group_permissions",
                             "/group_permissions",
                             "/group_permissions",
                             name="string")

    def test_department_normal(self):
        aux_org_id = self.prepare_organization()
        self.t_simple_normal(         "/organizations/" + aux_org_id + "/departments",
                                      "/organizations/" + aux_org_id + "/departments",
                                      "/departments",
                                        name="string")
        self.delete_doc("/organizations/" + aux_org_id)

    def test_group_normal(self):
        aux_item_ids = self.prepare_department()
        self.t_simple_normal("/departments/" + aux_item_ids["dep_id"] + "/groups",
                             "/departments/" + aux_item_ids["dep_id"] + "/groups",
                             "/groups",
                             name="string")
        self.delete_doc("/departments/" + aux_item_ids["dep_id"])
        self.delete_doc("/organizations/" + aux_item_ids["org_id"])

    def test_group_test_normal(self):
        aux_doc_ids = self.prepare_group()
        self.assertTrue(aux_doc_ids["group_id"], "aux group must be created")
        self.t_simple_normal("/groups/" + aux_doc_ids["group_id"] + "/tests",
                             "/groups/" + aux_doc_ids["group_id"] + "/tests",
                             "/tests",
                             name="string",
                             info="string")
        self.delete_doc("/groups/" + aux_doc_ids["group_id"])
        self.delete_doc("/departments/" + aux_doc_ids["dep_id"])
        self.delete_doc("/organizations/" + aux_doc_ids["org_id"])

    def test_tutor_role_normal(self):
        #self.t_role("Tutor")
        pass

    def test_student_role_normal(self):
        #self.t_role("Student")
        pass

    @staticmethod
    def assertDictListEqual(a, b):
        a = list(a)
        try:
            for item in b:
                a.remove(item)
        except AssertionError("dict lists are not equal"):
            return False
        return not a

    def test_general_role_person(self):
        person_count = 2
        persons = self.prepare_persons(person_count)
        facilities = self.prepare_department()
        roles = {}
        # person 0 is student
        temp_role = {
                "person_id": persons[0],
                "department_id": facilities["dep_id"],
                "role_type": "Student",
                "description": "sample_description"
            }
        temp_role.update({"id": self.post_item("/general_roles", temp_role)})
        roles["person0_Student"] = temp_role
        # person 1 is tutor and student
        temp_role = {
            "person_id": persons[1],
            "department_id": facilities["dep_id"],
            "role_type": "Tutor",
            "description": "sample_description"
        }
        temp_role.update({"id": self.post_item("/general_roles", temp_role)})
        roles["person1_Tutor"] = temp_role
        temp_role = {
            "person_id": persons[1],
            "department_id": facilities["dep_id"],
            "role_type": "Student",
            "description": "sample_description"
        }
        temp_role.update({"id": self.post_item("/general_roles", temp_role)})
        roles["person1_Student"] = temp_role
        print(roles)
        # testing that roles were added properly
        for key, value in roles.items():
            role_wo_id = value.copy()
            del role_wo_id["id"]
            role_data = self.get_item_data("/general_roles/" + value["id"])
            self.assertEqual(role_wo_id, role_data, "returned general role data must match inserted data")
        person0_rolelist = self.get_item_list("/persons/%s/general_roles" % persons[0])
        person1_rolelist = self.get_item_list("/persons/%s/general_roles" % persons[1])
        self.assertEqual(person0_rolelist,
                         [{"id": roles["person0_Student"]["id"]}])
        self.assertDictListEqual(person1_rolelist,
                         [{"id": roles["person1_Tutor"]["id"]},
                          {"id": roles["person1_Student"]["id"]}])


        
        for key, role in roles.items():
            self.delete_item("/general_roles/" + role["id"])
        for person_id in persons:
            role_list = self.get_item_list("/persons/%s/general_roles" % person_id)
            self.assertEqual([], role_list, "all roles must be deleted")
        self.delete_doc("/departments/" + facilities["dep_id"])
        self.delete_doc("/organizations/" + facilities["org_id"])
        for person_id in persons:
            self.delete_doc("/persons/" + person_id)


    def get_item_list(self, url):
        resp = requests.get(self.api_URL + url)
        self.assertEqual(200, resp.status_code, "get response status code must be 200")
        resp_json = resp.json()
        self.assertEqual(resp_json["result"], ERR.OK, "result must be ERR.OK")
        return resp_json["list"]

    def get_item_data(self, url):
        resp = requests.get(self.api_URL + url)
        self.assertEqual(200, resp.status_code, "get response status code must be 200")
        resp_json = resp.json()
        self.assertEqual(resp_json["result"], ERR.OK, "result must be ERR.OK")
        return resp_json["data"]

    def post_item(self, url, data):
        resp = requests.post(url=self.api_URL + url, json=data)
        self.assertEqual(200, resp.status_code, "post response status code must be 200")
        resp_json = resp.json()
        self.assertEqual(resp_json["result"], ERR.OK, "post result must be ERR.OK")
        self.assertTrue(resp_json["id"], "returned id must be not None")
        return resp_json["id"]

    def delete_item(self, url):
        resp = requests.delete(url=self.api_URL + url)
        self.assertEqual(200, resp.status_code, "delete response status code must be 200")
        resp_json = resp.json()
        self.assertEqual(resp_json["result"], ERR.OK, "result must be ERR.OK")

if __name__ == "__main__":
    unittest.main(verbosity=1)
