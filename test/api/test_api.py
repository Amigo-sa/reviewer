# -- coding: utf-8 --
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
        if url_delete == "/persons":
            for person in add_list:
                person_info = self.get_item_data("/persons/"+person["id"])
                self.assertEqual(person["surname"], person_info["surname"])
                self.assertEqual(person["first_name"], person_info["first_name"])
                self.assertEqual(person["middle_name"], person_info["middle_name"])
                self.assertEqual(person["phone_no"], person_info["phone_no"])
                self.assertEqual(person["birth_date"], person_info["birth_date"])
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
        return [resp_json["id"], post_data]

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

    def test_find_person_limits(self):
        person_ids = self.prepare_persons(10)
        list_0_3 = self.get_item_list("/persons?query_limit=4")
        self.assertEqual(len(list_0_3), 4, "must return requested number of items")
        for index, item in enumerate(list_0_3):
            self.assertEqual(item["id"], person_ids[index])
        list_4_7 =  self.get_item_list("/persons?query_start=4&query_limit=4")
        self.assertEqual(len(list_4_7), 4, "must return requested number of items")
        for index, item in enumerate(list_4_7):
            self.assertEqual(item["id"], person_ids[index + 4])
        list_8_9 = self.get_item_list("/persons?query_start=8")
        self.assertEqual(len(list_8_9), 2, "must return requested number of items")
        for index, item in enumerate(list_8_9):
            self.assertEqual(item["id"], person_ids[index + 8])
        for person_id in person_ids:
            self.delete_doc("/persons/" + person_id)

    @staticmethod
    def assertDictListEqual(list1, list2):
        list1_c = list(list1)
        try:
            for item in list2:
                list1_c.remove(item)
        except Exception as e:
            print(list1)
            print(list2)
            raise AssertionError("dict lists must be equal")
        return not list1_c

    def test_general_role_person(self):
        person_count = 4
        person_ids = self.prepare_persons(person_count)
        self.prepare_department()
        self.prepare_department()
        org_1 = self.get_item_list("/organizations")[0]
        org_2 = self.get_item_list("/organizations")[1]
        dep_1 = self.get_item_list("/organizations/%s/departments"%org_1["id"])[0]
        dep_2 = self.get_item_list("/organizations/%s/departments"%org_2["id"])[0]
        person_ref_data = []
        for person_id in person_ids:
            person_ref_data.append(self.get_item_data("/persons/" + person_id))
        roles = {}
        # person 0 is student
        temp_role = {
                "person_id": person_ids[0],
                "department_id": dep_1["id"],
                "role_type": "Student",
                "description": "sample_description"
            }
        temp_role.update({"id": self.post_item("/general_roles", temp_role)})
        roles["person0_Student"] = temp_role
        # person 1 is tutor and student
        temp_role = {
            "person_id": person_ids[1],
            "department_id":  dep_1["id"],
            "role_type": "Tutor",
            "description": "sample_description"
        }
        temp_role.update({"id": self.post_item("/general_roles", temp_role)})
        roles["person1_Tutor"] = temp_role
        temp_role = {
            "person_id": person_ids[1],
            "department_id":  dep_1["id"],
            "role_type": "Student",
            "description": "sample_description"
        }
        temp_role.update({"id": self.post_item("/general_roles", temp_role)})
        roles["person1_Student"] = temp_role
        # person 2 is tutor at 2-nd department of 2-nd organization
        temp_role = {
            "person_id": person_ids[2],
            "department_id": dep_2["id"],
            "role_type": "Tutor",
            "description": "sample_description"
        }
        temp_role.update({"id": self.post_item("/general_roles", temp_role)})
        roles["person2_Tutor"] = temp_role
        # person 3 has no general role
        # testing that roles were added properly
        for key, value in roles.items():
            role_wo_id = value.copy()
            del role_wo_id["id"]
            role_data = self.get_item_data("/general_roles/" + value["id"])
            self.assertEqual(role_wo_id, role_data, "returned general role data must match inserted data")
        person0_rolelist = self.get_item_list("/persons/%s/general_roles" % person_ids[0])
        person1_rolelist = self.get_item_list("/persons/%s/general_roles" % person_ids[1])
        self.assertEqual(person0_rolelist,
                         [{"id": roles["person0_Student"]["id"]}])
        self.assertDictListEqual(person1_rolelist,
                         [{"id": roles["person1_Tutor"]["id"]},
                          {"id": roles["person1_Student"]["id"]}])
        # testing find_persons without request params
        person_list = self.get_item_list("/persons")
        for person in person_list:
            ref_data = next((p for p in person_ref_data if p["id"] == person["id"]), None)
            self.assertEqual(ref_data["first_name"], person["first_name"])
            self.assertEqual(ref_data["middle_name"], person["middle_name"])
            self.assertEqual(ref_data["surname"], person["surname"])
            if person["id"] == person_ids[0]:
                self.assertEqual(person["role"], "Student")
                self.assertEqual(person["organization_name"], org_1["name"])
            if person["id"] == person_ids[1]:
                self.assertEqual(person["role"], "Tutor")
                self.assertEqual(person["organization_name"], org_1["name"])
            if person["id"] == person_ids[2]:
                self.assertEqual(person["role"], "Tutor")
                self.assertEqual(person["organization_name"], org_2["name"])
            if person["id"] == person_ids[3]:
                self.assertEqual(person["role"], "None")
                self.assertEqual(person["organization_name"], "None")
        # testing find_persons with department_id param
        person_list = self.get_item_list("/persons?department_id=" + dep_1["id"])
        for person in person_list:
            self.assertNotIn(person["id"], [person_ids[2], person_ids[3]])
            self.assertIn(person["id"], [person_ids[0], person_ids[1]])
        # testing find_persons with organization_id param
        person_list = self.get_item_list("/persons?organization_id=" + org_1["id"])
        for person in person_list:
            self.assertNotIn(person["id"], [person_ids[2], person_ids[3]])
            self.assertIn(person["id"], [person_ids[0], person_ids[1]])
        # clearing collections
        for key, role in roles.items():
            self.delete_item("/general_roles/" + role["id"])
        for person_id in person_ids:
            role_list = self.get_item_list("/persons/%s/general_roles" % person_id)
            self.assertEqual([], role_list, "all roles must be deleted")
        self.delete_doc("/departments/" + dep_1["id"])
        self.delete_doc("/departments/" + dep_2["id"])
        self.delete_doc("/organizations/" + org_1["id"])
        self.delete_doc("/organizations/" + org_2["id"])
        for person_id in person_ids:
            self.delete_doc("/persons/" + person_id)

    def test_person_hs(self):
        hs0_id, hs0_data = self.prepare_hs()
        hs1_id, hs1_data = self.prepare_hs()
        hs2_id, hs2_data = self.prepare_hs()
        person_ids = self.prepare_persons(2)
        p0_hs0_id = self.post_item("/persons/%s/hard_skills" % person_ids[0], {"hs_id" : hs0_id})
        p0_hs1_id = self.post_item("/persons/%s/hard_skills" % person_ids[0], {"hs_id" : hs1_id})
        p1_hs1_id = self.post_item("/persons/%s/hard_skills" % person_ids[1], {"hs_id" : hs1_id})
        p1_hs2_id = self.post_item("/persons/%s/hard_skills" % person_ids[1], {"hs_id": hs2_id})
        p1_hs_list = self.get_item_list("/persons/hard_skills?person_id="+person_ids[0])
        ref_p1_hs_list = [{"id": p0_hs0_id}, {"id": p0_hs1_id}]
        self.assertDictListEqual(p1_hs_list, ref_p1_hs_list)

        hs1_phs_list = self.get_item_list("/persons/hard_skills?hs_id="+hs1_id)
        ref_hs1_phs_list = [{"id": p0_hs1_id}, {"id": p1_hs1_id}]
        self.assertDictListEqual(hs1_phs_list, ref_hs1_phs_list)

        all_phs_list = self.get_item_list("/persons/hard_skills")
        ref_all_phs_list = [{"id": p0_hs0_id}, {"id": p0_hs1_id},
                            {"id": p1_hs1_id}, {"id": p1_hs2_id}]
        self.assertDictListEqual(ref_all_phs_list, all_phs_list)

        for p_hs_id in [p0_hs0_id, p0_hs1_id, p1_hs1_id, p1_hs2_id]:
            self.delete_item("/persons/hard_skills/"+p_hs_id)

        all_phs_list = self.get_item_list("/persons/hard_skills")
        self.assertDictListEqual([], all_phs_list)

        for person_id in person_ids:
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
