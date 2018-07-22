import context
import unittest
import requests
from node.settings import constants
import node.settings.errors as ERR
from node.node_server import start_server
from threading import Thread
import random
import datetime
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
        # Запуск сервера, (проверка на запущенность не проводится!)
        # TODO добавить проверку на запущенность сервера
        # TODO добавить очищение базы с сохранинем индексов
        node_server_thread.start()

    @classmethod
    def tearDownClass(cls):
        requests.post(cls.api_URL + "/shutdown")

    def t_simple_normal(self, url_get, url_post, url_delete, *args, **kwargs):
        # read from empty DB
        resp = requests.get(self.api_URL + url_get)
        self.assertEqual(200, resp.status_code, "get response status code must be 200")
        resp_json = resp.json()
        self.assertEqual(resp_json["result"], ERR.OK, "result must be ERR.OK")
        read_list = resp_json["list"]
        self.assertListEqual([],read_list, "initial DB must be empty")
        # write items to DB
        add_list = []
        items_to_write = 3
        for item_ctr in range(items_to_write):
            cur_item = self.generate_doc(item_ctr, kwargs.items())
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
            if "info" in added_item.keys(): del added_item["info"] # Подразумевает, что мы не ожидаем получение "info" при получении списка, т.к. инфо может быть длинное
            for read_item in read_list:
                if added_item == read_item:
                    item_match += 1
                    total_match += 1
            self.assertEqual(item_match, 1, "must be exactly one match for each item")
        self.assertEqual(total_match, items_to_write, "all added items must be in GET list")
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

    @staticmethod
    def generate_doc(doc_no, type_list, *args, **kwargs):
        cur_item = dict()
        for key, value in type_list:
            if value == "string":
                cur_item.update({
                    key: "sample_" + key + "_" + str(doc_no + 1)
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
                    key: "3223223" + str(doc_no)
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
        post_data = {"name": "aux_org"}
        resp_json = requests.post(url=self.api_URL + '/organizations', json=post_data).json()
        self.assertEqual(resp_json["result"],ERR.OK, "aux organization must be created")
        return resp_json["id"]

    def prepare_department(self):
        aux_org_id = self.prepare_organization()
        self.assertTrue(aux_org_id, "auxiliary organization must be created")
        post_data = {"name": "aux_dep"}
        resp_json = requests.post(url=self.api_URL + '/organizations/' + aux_org_id + "/departments", json=post_data).json()
        self.assertEqual(resp_json["result"], ERR.OK, "aux department must be created")
        return {"dep_id" : resp_json["id"],
                "org_id" : aux_org_id}

    def prepare_group(self):
        aux_items_ids = self.prepare_department()
        self.assertTrue(aux_items_ids["dep_id"], "aux department must be created")
        post_data = {"name": "aux_group"}
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
            cur_person = self.generate_doc(person_ctr, person_type_list.items())
            resp_json = requests.post(url=self.api_URL + "/persons", json=cur_person).json()
            self.assertEqual(resp_json["result"], ERR.OK, "aux person must be added")
            id_list.append(resp_json["id"])
        return id_list

    def prepare_hs(self):
        post_data = {"name": "aux_hard_skill"}
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

    """
    #TODO проверить также второй вариант поиска
    def test_person_HS(self):
        aux_person_list = self.prepare_persons(1)
        aux_hs_id = self.prepare_hs()
        self.assertTrue(aux_person_list[0], "aux person must be created")
        self.assertTrue(aux_hs_id, "aux hard skill must be created")
        self.t_simple_normal("/persons/hard_skills/" +  + "/hard_skills",
                             "/persons/" + aux_person_list[0]+ "/hard_skills",
                             "/persons/hard_skills/",
                             hs_id=aux_hs_id)
        self.delete_doc("/hard_skills/" + aux_hs_id)
        for person_id in aux_person_list:
            self.delete_doc("/persons/" + person_id)
    """

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
        self.t_role("Tutor")
        pass

    def test_student_role_normal(self):
        self.t_role("Student")
        pass

    def t_role(self, role_type):
        person_count = 2
        aux_persons_ids = self.prepare_persons(person_count)
        aux_facilities_ids = self.prepare_department()
        roles = []
        for person_id in aux_persons_ids:
            role_list = self.get_item_list("/persons/%s/general_roles" % person_id)
            self.assertEqual([], role_list)
            cur_role = {
                "person_id": person_id,
                "department_id": aux_facilities_ids["dep_id"],
                "role_type": role_type,
                "description": "sample_description"
            }
            cur_role.update({"id": self.post_item("/general_roles", cur_role)})
            roles.append(cur_role)
        for role in roles:
            role_no_id = role.copy()
            del role_no_id["id"]
            role_data = self.get_item_data("/general_roles/" + role["id"])
            self.assertEqual(role_no_id, role_data, "returned general role data must match inserted data")
        for person_num, person_id in enumerate(aux_persons_ids):
            role_list = self.get_item_list("/persons/%s/general_roles" % person_id)
            self.assertEqual([{"id": roles[person_num]["id"]}],
                             role_list, "role list by person id must return correct data")
        for role in roles:
            self.delete_item("/general_roles/" + role["id"])
        self.delete_doc("/departments/" + aux_facilities_ids["dep_id"])
        self.delete_doc("/organizations/" + aux_facilities_ids["org_id"])
        for person_id in aux_persons_ids:
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
