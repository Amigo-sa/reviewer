import context
import requests
import node.settings.errors as ERR
import unittest
import datetime


def post_item(instance: unittest.TestCase, url, data):
    if not isinstance(instance, unittest.TestCase):
        raise TypeError
    resp = requests.post(url=url, json=data)
    instance.assertEqual(200, resp.status_code, "post response status code must be 200")
    resp_json = resp.json()
    instance.assertEqual(ERR.OK, resp_json["result"],  "post result must be ERR.OK")
    if "error_message" in resp_json: print(resp_json["error_message"])
    instance.assertTrue(resp_json["id"], "returned id must be not None")
    return resp_json["id"]


def prepare_two_persons(instance: unittest.TestCase, api_url):
    person_data = dict(
        first_name="Владимир",
        middle_name="Ильич",
        surname="Ленин",
        birth_date=datetime.date(1870, 4, 22).isoformat(),
        phone_no="+78007773737")
    p_id = post_item(instance, api_url + "/persons", person_data)
    person_data.update({"id": p_id})
    person2_data = dict(
        first_name="Фанни",
        middle_name="Ефимовна",
        surname="Каплан",
        birth_date=datetime.date(1890, 2, 10).isoformat(),
        phone_no="+78007773838")
    p2_id = post_item(instance, api_url + "/persons", person2_data)
    person2_data.update({"id": p2_id})
    return [person_data, person2_data]