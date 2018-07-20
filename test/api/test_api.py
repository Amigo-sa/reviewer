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
        pass
        requests.post(cls.api_URL + "/shutdown")

    def t_not_referencing_normal(self, access_url, *args, **kwargs):
        # read from empty DB
        resp = requests.get(self.api_URL + access_url)
        self.assertEqual(200, resp.status_code, "get response status code must be 200")
        resp_json = resp.json()
        self.assertEqual(resp_json["result"], ERR.OK, "result must be ERR.OK")
        read_list = resp_json["list"]
        self.assertListEqual([],read_list, "initial DB must be empty")
        # write items to DB
        add_list = []
        items_to_write = 3
        for item_ctr in range(items_to_write):
            cur_item = dict()
            for key, value in kwargs.items():
                if value == "string":
                    cur_item.update({
                        key: "sample_" + key + "_" + str(item_ctr + 1)
                    })
                elif value == "date":
                    #TODO уточнить, подойдёт ли ISO во всех случаях
                    cur_date = datetime.date(random.randrange(1900, 2000),
                                           random.randrange(1, 12),
                                           random.randrange(1, 28))
                    date_iso = cur_date.isoformat()
                    cur_item.update({
                        key: date_iso
                    })
                elif value == "number_string":
                    cur_item.update({
                        key: "3223223" + str(item_ctr)
                    })
                else:
                    raise ValueError("unsupported field type")
            resp = requests.post(url=self.api_URL + access_url, json=cur_item)
            self.assertEqual(200, resp.status_code, "post response status code must be 200")
            resp_json = resp.json()
            self.assertEqual(resp_json["result"], ERR.OK, "post result must be ERR.OK")
            self.assertTrue(resp_json["id"], "returned id must be not None")
            cur_item.update({"id" : resp_json["id"]})
            add_list.append(cur_item)
        print("sample data for " + access_url + ":\n" + str(add_list))
        # verify written items
        resp_json = requests.get(self.api_URL + access_url).json()
        read_list = resp_json["list"]
        total_match = 0
        for added_item in add_list:
            item_match = 0
            for read_item in read_list:
                if added_item == read_item:
                    item_match += 1
                    total_match += 1
            self.assertEqual(item_match, 1, "must be exactly one match for each item")
        self.assertEqual(total_match, items_to_write, "all added items must be in GET list")
        # delete items
        for item in add_list:
            resp = requests.delete(url=self.api_URL + access_url + "/" + item["id"])
            self.assertEqual(200, resp.status_code, "delete response status code must be 200")
            resp_json = resp.json()
            self.assertEqual(resp_json["result"], ERR.OK, "result must be ERR.OK")
        # verify deletion
        resp_json = requests.get(self.api_URL + access_url).json()
        read_list = resp_json["list"]
        self.assertListEqual([], read_list, "docs must be erased from DB")


    def test_organization_normal(self):
        self.t_not_referencing_normal("/organizations", name = "string")

    def test_person_normal(self):
        self.t_not_referencing_normal("/persons",
                                      first_name="string",
                                      middle_name="string",
                                      surname="string",
                                      birth_date="date",
                                      phone_no = "number_string"
                                      )

    def test_soft_skill_normal(self):
        self.t_not_referencing_normal("/soft_skills", name="string")

    def test_hard_skill_normal(self):
        self.t_not_referencing_normal("/hard_skills", name="string")


if __name__ == "__main__":
    unittest.main(verbosity=1)
