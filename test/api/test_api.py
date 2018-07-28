# -*- coding: utf-8 -*-
import context
import unittest
import requests
from node.settings import constants
import node.settings.errors as ERR
from node.node_server import start_server
from threading import Thread
import random
import datetime
from time import sleep
import re
#from src.data.reviewer_model import *


class NodeServer(Thread):
    def run(self):
        start_server()

node_server_thread = NodeServer()


class TestApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Загрузка адреса сервера
        cls.api_URL = constants.core_server_url
        cls.gen_doc_ctr = 0
        print("Server starting...")
        node_server_thread.start()
        attempts = 0
        connected = False
        print("Waiting for server...")
        while not connected:
            try:
                requests.get(cls.api_URL + "/organizations")
                connected = True
            except Exception as e:
                attempts += 1
                sleep(0.5)
                print("Connection attempt %s failed" %str(attempts))
                if attempts > 20: raise ConnectionError("could not connect to server")
        print("Connected")
        # Подразумевается, что в delete_rule установлено правило CASCADE, поэтому остальные коллекции удалятся цепочкой
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
        requests.post(self.api_URL + "/wipe")

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

    def prepare_organization(self) -> str:
        post_data = self.generate_doc(dict(name="string").items())
        resp_json = requests.post(url=self.api_URL + '/organizations', json=post_data).json()
        self.assertEqual(resp_json["result"],ERR.OK, "aux organization must be created")
        return resp_json["id"]

    def prepare_department(self) -> dict:
        aux_org_id = self.prepare_organization()
        self.assertTrue(aux_org_id, "auxiliary organization must be created")
        post_data = self.generate_doc(dict(name="string").items())
        resp_json = requests.post(url=self.api_URL + '/organizations/' + aux_org_id + "/departments", json=post_data).json()
        self.assertEqual(resp_json["result"], ERR.OK, "aux department must be created")
        return {"dep_id" : resp_json["id"],
                "org_id" : aux_org_id}

    def prepare_group(self) -> dict:
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

    def prepare_ss(self):
        post_data = self.generate_doc(dict(name="string").items())
        resp_json = requests.post(url=self.api_URL + '/soft_skills', json=post_data).json()
        self.assertEqual(resp_json["result"], ERR.OK, "aux soft skill must be created")
        return [resp_json["id"], post_data]

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
        self.delete_item("/organizations/" + aux_org_id)

    def test_group_normal(self):
        aux_item_ids = self.prepare_department()
        self.t_simple_normal("/departments/" + aux_item_ids["dep_id"] + "/groups",
                             "/departments/" + aux_item_ids["dep_id"] + "/groups",
                             "/groups",
                             name="string")
        self.delete_item("/departments/" + aux_item_ids["dep_id"])
        self.delete_item("/organizations/" + aux_item_ids["org_id"])

    def test_group_test_normal(self):
        aux_doc_ids = self.prepare_group()
        self.t_simple_normal("/groups/" + aux_doc_ids["group_id"] + "/tests",
                             "/groups/" + aux_doc_ids["group_id"] + "/tests",
                             "/tests",
                             name="string",
                             info="string")
        self.delete_item("/groups/" + aux_doc_ids["group_id"])
        self.delete_item("/departments/" + aux_doc_ids["dep_id"])
        self.delete_item("/organizations/" + aux_doc_ids["org_id"])

    def test_group_test_result_normal(self):
        group_id = self.prepare_group()["group_id"]
        person_id, person2_id = self.prepare_persons(2)
        test_data = {"name" : "sample_test_name",
                     "info" : "sample_test_info"}
        test_id = self.post_item("/groups/%s/tests"%group_id, test_data)
        test2_id = self.post_item("/groups/%s/tests"%group_id, {"name" : "test 2",
                                                                "info" : "test 2 info"})
        ref_result_data = {"person_id": person_id,
                       "result_data": ["result 1", "result 2"]}
        # post test result
        result_id = self.post_item("/tests/%s/results"%test_id, ref_result_data)
        # verify
        list = self.get_item_list("/tests/results")
        self.assertDictListEqual( [{"id":result_id}], list)
        list = self.get_item_list("/tests/results?person_id=" + person_id)
        self.assertDictListEqual([{"id": result_id}], list)
        list = self.get_item_list("/tests/results?person_id=" + person2_id)
        self.assertDictListEqual([], list)
        list = self.get_item_list("/tests/results?test_id=" + test_id)
        self.assertDictListEqual([{"id": result_id}], list)
        list = self.get_item_list("/tests/results?test_id=" + test2_id)
        self.assertDictListEqual([], list)
        # verify test result info
        result_data = self.get_item_data("/tests/results/" + result_id)
        ref_result_data.update({"test_id": test_id})
        self.assertDictEqual(ref_result_data, result_data)
        # delete
        self.delete_item("/tests/results/" + result_id)
        # verify
        list = self.get_item_list("/tests/results")
        self.assertDictListEqual([], list)

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
        """

        for person_id in person_ids:
            self.delete_doc("/persons/" + person_id)
        """

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
        if list1_c: raise AssertionError("dict lists must be equal")

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
        """

        self.delete_doc("/departments/" + dep_1["id"])
        self.delete_doc("/departments/" + dep_2["id"])
        self.delete_doc("/organizations/" + org_1["id"])
        self.delete_doc("/organizations/" + org_2["id"])
        for person_id in person_ids:
            self.delete_doc("/persons/" + person_id)
        """

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

        p0_hs1_data = self.get_item_data("/persons/hard_skills/" + p0_hs1_id)
        self.assertEqual(person_ids[0], p0_hs1_data["person_id"])
        self.assertEqual(hs1_id, p0_hs1_data["hs_id"])
        self.assertEqual(50.0, float(p0_hs1_data["level"]),)

        all_phs_list = self.get_item_list("/persons/hard_skills")
        ref_all_phs_list = [{"id": p0_hs0_id}, {"id": p0_hs1_id},
                            {"id": p1_hs1_id}, {"id": p1_hs2_id}]
        self.assertDictListEqual(ref_all_phs_list, all_phs_list)

        for p_hs_id in [p0_hs0_id, p0_hs1_id, p1_hs1_id, p1_hs2_id]:
            self.delete_item("/persons/hard_skills/"+p_hs_id)

        all_phs_list = self.get_item_list("/persons/hard_skills")
        self.assertDictListEqual([], all_phs_list)
        """
        for person_id in person_ids:
            self.delete_item("/persons/" + person_id)
        for hs_id in [hs0_id, hs1_id, hs2_id]:
            self.delete_item("/hard_skills/" + hs_id)
        """
            
    def test_person_ss(self):
        ss0_id, ss0_data = self.prepare_ss()
        ss1_id, ss1_data = self.prepare_ss()
        ss2_id, ss2_data = self.prepare_ss()
        person_ids = self.prepare_persons(2)
        p0_ss0_id = self.post_item("/persons/%s/soft_skills" % person_ids[0], {"ss_id": ss0_id})
        p0_ss1_id = self.post_item("/persons/%s/soft_skills" % person_ids[0], {"ss_id": ss1_id})
        p1_ss1_id = self.post_item("/persons/%s/soft_skills" % person_ids[1], {"ss_id": ss1_id})
        p1_ss2_id = self.post_item("/persons/%s/soft_skills" % person_ids[1], {"ss_id": ss2_id})

        p1_ss_list = self.get_item_list("/persons/soft_skills?person_id="+person_ids[0])
        ref_p1_ss_list = [{"id": p0_ss0_id}, {"id": p0_ss1_id}]
        self.assertDictListEqual(p1_ss_list, ref_p1_ss_list)

        ss1_pss_list = self.get_item_list("/persons/soft_skills?ss_id="+ss1_id)
        ref_ss1_pss_list = [{"id": p0_ss1_id}, {"id": p1_ss1_id}]
        self.assertDictListEqual(ss1_pss_list, ref_ss1_pss_list)

        p0_ss1_data = self.get_item_data("/persons/soft_skills/" + p0_ss1_id)
        self.assertEqual(person_ids[0], p0_ss1_data["person_id"])
        self.assertEqual(ss1_id, p0_ss1_data["ss_id"])
        self.assertEqual(50.0 ,float(p0_ss1_data["level"]))

        all_pss_list = self.get_item_list("/persons/soft_skills")
        ref_all_pss_list = [{"id": p0_ss0_id}, {"id": p0_ss1_id},
                            {"id": p1_ss1_id}, {"id": p1_ss2_id}]
        self.assertDictListEqual(ref_all_pss_list, all_pss_list)

        for p_ss_id in [p0_ss0_id, p0_ss1_id, p1_ss1_id, p1_ss2_id]:
            self.delete_item("/persons/soft_skills/"+p_ss_id)

        all_pss_list = self.get_item_list("/persons/soft_skills")
        self.assertDictListEqual([], all_pss_list)
        """

        for person_id in person_ids:
            self.delete_item("/persons/" + person_id)
        for ss_id in [ss0_id, ss1_id, ss2_id]:
            self.delete_item("/soft_skills/" + ss_id)
        """

    # TODO возможно, следует верификацию включить сюда, а не в отдельный тест
    def test_group_member_normal(self):
        person_id = self.prepare_persons(1)[0]
        facility_ids = self.prepare_group()
        group_id = facility_ids["group_id"]
        # verify that group member list is initially empty
        gm_list = self.get_item_list("/groups/%s/group_members"%group_id)
        self.assertEqual( [], gm_list)
        # add group_member without role
        post_data = {"person_id": person_id}
        gm_id = self.post_item("/groups/%s/group_members"%group_id, post_data)
        # verify
        gm_list = self.get_item_list("/groups/%s/group_members" % group_id)
        self.assertEqual(gm_id, gm_list[0]["id"])
        gm_list = self.get_item_list("/persons/%s/group_members" % person_id)
        self.assertEqual(gm_id, gm_list[0]["id"])
        # verify
        gm_info = self.get_item_data("/group_members/" + gm_id)
        ref_gm_info = {"person_id": person_id,
                       "group_id": group_id,
                       "permissions": [],
                       "is_active" : "True"}
        self.assertDictEqual(ref_gm_info, gm_info)
        # verify with /persons
        self.prepare_persons(2)
        person_info = self.get_item_list("/persons?group_id=" + group_id)
        self.assertEqual(1, len(person_info))
        self.assertEqual(person_id, person_info[0]["id"])
        # add role to list of roles in group
        admin_id = self.post_item("/group_roles", {"name": "admin"})
        self.post_modify_item("/groups/%s/role_list"%group_id, {"role_list" : [admin_id]})
        # verify
        role_list = self.get_item_list("/groups/%s/role_list" % group_id)
        self.assertEqual(admin_id, role_list[0]["id"])
        # set group role
        self.post_modify_item("/group_members/%s/group_roles"%gm_id, {"group_role_id": admin_id})
        # verify
        gm_info = self.get_item_data("/group_members/" + gm_id)
        ref_gm_info.update({"role_id" : admin_id})
        self.assertDictEqual(ref_gm_info, gm_info)
        # add permissions
        read_permission = self.post_item("/group_permissions", {"name" : "read_info"})
        self.post_modify_item("/group_members/%s/permissions"%gm_id,
                              {"group_permission_id" : read_permission})
        write_permission = self.post_item("/group_permissions", {"name": "write_info"})
        self.post_modify_item("/group_members/%s/permissions" % gm_id,
                              {"group_permission_id": write_permission})
        # verify
        gm_info = self.get_item_data("/group_members/" + gm_id)
        ref_gm_info.update({"permissions": [read_permission, write_permission]})
        self.assertDictEqual(ref_gm_info, gm_info)
        # delete permission
        self.delete_item("/group_members/%s/permissions/%s"%(gm_id,write_permission))
        # verify
        gm_info = self.get_item_data("/group_members/" + gm_id)
        ref_gm_info.update({"permissions": [read_permission]})
        self.assertDictEqual(ref_gm_info, gm_info)
        # set inactive
        self.patch_item("/group_members/%s?is_active=false"%gm_id)
        # verify
        gm_info = self.get_item_data("/group_members/" + gm_id)
        ref_gm_info.update({"is_active" : "False"})
        self.assertDictEqual(ref_gm_info, gm_info)
        # delete
        self.delete_item("/group_members/" + gm_id)
        resp_json = requests.get(self.api_URL+"/group_members/" + gm_id).json()
        self.assertEqual(ERR.NO_DATA, resp_json["result"])


        """
        self.delete_item("/group_roles/" + admin_id)
        self.delete_item("/persons/" + person_id)
        self.delete_item("/groups/" + facility_ids["group_id"])
        self.delete_item("/departments/" + facility_ids["dep_id"])
        self.delete_item("/organizations/" + facility_ids["org_id"])
        """
        pass

    def test_reviews_normal(self):
        person_id = self.prepare_persons(1)[0]
        facility_ids = self.prepare_group()
        org_id = facility_ids["org_id"]
        dep_id = facility_ids["dep_id"]
        group_id = facility_ids["group_id"]
        hs_id = self.prepare_hs()[0]
        ss_id = self.prepare_ss()[0]
        print(person_id, org_id, dep_id, group_id, hs_id, ss_id)
        student_role = {
            "person_id": person_id,
            "department_id": dep_id,
            "role_type": "Student",
            "description": "sample_description"
        }
        student_role.update({"id": self.post_item("/general_roles", student_role)})
        tutor_role = {
            "person_id": person_id,
            "department_id": dep_id,
            "role_type": "Tutor",
            "description": "sample_description"
        }
        tutor_role.update({"id": self.post_item("/general_roles", tutor_role)})
        p_hs_id = self.post_item("/persons/%s/hard_skills" % person_id, {"hs_id" : hs_id})
        p_ss_id = self.post_item("/persons/%s/soft_skills" % person_id, {"ss_id": ss_id})
        gm_id = self.post_item("/groups/%s/group_members" % group_id, {"person_id": person_id})
        g_test_id = self.post_item("/groups/%s/tests" % group_id, {"name" : "sample_test_name",
                                                                    "info" : "sample_test_info"})
        subjects = { "StudentRole" : student_role["id"],
                     "TutorRole" : tutor_role["id"],
                     "HardSkill" : p_hs_id,
                     "SoftSkill" : p_ss_id,
                     "Group" : group_id,
                     "GroupTest" : g_test_id,
                     "GroupMember": gm_id}
        rev_ids = {}
        # add reviews
        for subj_type, subj_id in subjects.items():
            review_data = {"type" : subj_type,
                           "reviewer_id" : person_id,
                           "subject_id" : subj_id,
                           "value" : "60.0",
                           "description" : "sample_descr"}
            cur_id = self.post_item("/reviews", review_data)
            rev_ids.update({subj_id : cur_id})
        # verify reviews
        review_list = self.get_item_list("/reviews")
        ref_review_list = [{"id" : rev_id} for subj_id, rev_id in rev_ids.items()]
        self.assertDictListEqual(ref_review_list, review_list)
        # verify with reviewer_id
        person2_id = self.prepare_persons(1)[0]
        review_list = self.get_item_list("/reviews?reviewer_id=" + person_id)
        self.assertDictListEqual(ref_review_list, review_list)
        review_list = self.get_item_list("/reviews?reviewer_id=" + person2_id)
        self.assertDictListEqual([], review_list)
        # verify with subject_id
        for subj_id, rev_id in rev_ids.items():
            review_list = self.get_item_list("/reviews?subject_id=" + subj_id)
            self.assertEqual([{"id" : rev_id}], review_list)
        # get review info
        for subj_id, rev_id in rev_ids.items():
            review_data = self.get_item_data("/reviews/" + rev_id)
            ref_data = {"reviewer_id": person_id,
                        "subject_id": subj_id,
                        "value": 60.0,
                        "description": "sample_descr"}
            self.assertDictEqual(ref_data, review_data)
        # verify with review from person2
        review_data = {"type": "StudentRole",
                       "reviewer_id": person2_id,
                       "subject_id": student_role["id"],
                       "value": "80.0",
                       "description": "sample_descr2"}
        rev2_id = self.post_item("/reviews", review_data)
        review_list = self.get_item_list("/reviews?subject_id=" + student_role["id"])
        self.assertEqual([{"id": rev_ids[student_role["id"]]}, {"id": rev2_id}], review_list)
        # delete review
        self.delete_item("/reviews/" + rev_ids[student_role["id"]])
        rev_ids.pop(student_role["id"])
        # verify
        review_list = self.get_item_list("/reviews?subject_id=" + student_role["id"])
        self.assertEqual([{"id": rev2_id}], review_list)
        # delete all reviews
        self.delete_item("/reviews/" + rev2_id)
        for subj_id, rev_id in rev_ids.items():
            self.delete_item("/reviews/" + rev_id)
        # verify for one subject
        review_list = self.get_item_list("/reviews?subject_id=" + gm_id)
        self.assertEqual([], review_list)

    def get_item_list(self, url):
        resp = requests.get(self.api_URL + url)
        self.assertEqual(200, resp.status_code, "get response status code must be 200")
        resp_json = resp.json()
        if "error_message" in resp_json: print(resp_json["error_message"])
        self.assertEqual(ERR.OK, resp_json["result"],"result must be ERR.OK")
        return resp_json["list"]

    def get_item_data(self, url):
        resp = requests.get(self.api_URL + url)
        self.assertEqual(200, resp.status_code, "get response status code must be 200")
        resp_json = resp.json()
        if "error_message" in resp_json: print(resp_json["error_message"])
        self.assertEqual(ERR.OK, resp_json["result"], "result must be ERR.OK")
        return resp_json["data"]

    def post_item(self, url, data):
        resp = requests.post(url=self.api_URL + url, json=data)
        self.assertEqual(200, resp.status_code, "post response status code must be 200")
        resp_json = resp.json()
        self.assertEqual(ERR.OK, resp_json["result"],  "post result must be ERR.OK")
        if "error_message" in resp_json: print(resp_json["error_message"])
        self.assertTrue(resp_json["id"], "returned id must be not None")
        return resp_json["id"]

    def post_modify_item(self, url, data):
        resp = requests.post(url=self.api_URL + url, json=data)
        self.assertEqual(200, resp.status_code, "post response status code must be 200")
        resp_json = resp.json()
        self.assertEqual(ERR.OK, resp_json["result"],"post result must be ERR.OK")
        if "error_message" in resp_json: print(resp_json["error_message"])

    def delete_item(self, url):
        resp = requests.delete(url=self.api_URL + url)
        self.assertEqual(200, resp.status_code, "delete response status code must be 200")
        resp_json = resp.json()
        if "error_message" in resp_json: print(resp_json["error_message"])
        self.assertEqual(ERR.OK, resp_json["result"], "result must be ERR.OK")

    def patch_item(self, url):
        resp = requests.patch(url=self.api_URL + url)
        self.assertEqual(200, resp.status_code, "patch response status code must be 200")
        resp_json = resp.json()
        if "error_message" in resp_json: print(resp_json["error_message"])
        self.assertEqual(ERR.OK, resp_json["result"], "result must be ERR.OK")

if __name__ == "__main__":
    unittest.main(verbosity=1)
