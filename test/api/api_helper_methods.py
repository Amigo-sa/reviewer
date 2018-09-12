# -*- coding: utf-8 -*-
import context
import requests
import node.settings.errors as ERR
import unittest
import datetime
import random
from pymodm.connection import _get_db
import data.reviewer_model as model
from node.api.auth import hash_password, gen_session_id
from datetime import datetime, timezone, timedelta, date
from random import randint


def prepare_org_structure():
    org_1 = model.Organization("МЭИ")
    org_1.save()
    org_2 = model.Organization("МТУ")
    org_2.save()
    dep_1 = model.Department("ИИТ", org_1.pk)
    dep_1.save()
    dep_2 = model.Department("АС", org_2.pk)
    dep_2.save()
    person_1 = model.Person(
        "Павел",
        "Борисович",
        "Ерин",
        date(1986, 12, 30),
        "78392122221")
    person_1.save()
    person_2 = model.Person(
        "Владимир",
        "Владимирович",
        "Панкин",
        date(1987, 7, 6),
        "78398889991")
    person_2.save()
    spec_1 = model.Specialization("Tutor", "ТОЭ")
    spec_1.save()
    spec_2 = model.Specialization("Student")
    spec_2.save()
    group_role_1 = model.GroupRole("role_1")
    group_role_1.save()
    group_role_2 = model.GroupRole("role_2")
    group_role_2.save()
    group_1 = model.Group(dep_1.pk, "A-4-03", [group_role_1])
    group_1.save()
    group_2 = model.Group(dep_2.pk, "A-4-04", [group_role_2])
    group_2.save()

    structure_dict = {
        "org_1": {
            "name": org_1.name,
            "id": str(org_1.pk),
        },
        "org_2": {
            "name": org_2.name,
            "id": str(org_2.pk),
        },
        "dep_1": {
            "name": dep_1.name,
            "id": str(dep_1.pk),
        },
        "dep_2": {
            "name": dep_2.name,
            "id": str(dep_2.pk),
        },
        "person_1": {
            "first_name": person_1.first_name,
            "middle_name": person_1.middle_name,
            "surname": person_1.surname,
            "birth_date": person_1.birth_date,
            "phone_no": person_1.phone_no,
            "id": str(person_1.pk),
        },
        "person_2": {
            "first_name": person_2.first_name,
            "middle_name": person_2.middle_name,
            "surname": person_2.surname,
            "birth_date": person_2.birth_date,
            "phone_no": person_2.phone_no,
            "id": str(person_2.pk),
        },
        "spec_1": {
            "type": spec_1.type,
            "detail": spec_1.detail,
            "id": str(spec_1.pk),
        },
        "spec_2": {
            "type": spec_2.type,
            "detail": None,
            "id": str(spec_2.pk),
        },
        "group_1": {
            "name": group_1.name,
            "id": str(group_1.pk),
        },
        "group_2": {
            "name": group_2.name,
            "id": str(group_2.pk),
        },
        "group_role_1": {
            "name": group_role_1.name,
            "id": str(group_role_1.pk),
        },
        "group_role_2": {
            "name": group_role_2.name,
            "id": str(group_role_2.pk),
        },
    }
    return structure_dict


def age_session(phone_no, minutes):
    try:
        auth_info = model.AuthInfo.objects.get({"phone_no": phone_no})
        ts = auth_info.last_send_time
        dt = ts.as_datetime()
        dt -= timedelta(minutes=int(minutes))
        auth_info.last_send_time = dt
        auth_info.save()
    except Exception as e:
        print("Failed to age session")
        print(str(e))


def prepare_logged_in_person(phone_no):
    try:
        person = model.Person(
            "Клон",
            "Один Из",
            "Миллионов",
            date(1980, 1, 1),
            phone_no)
        person.save()
        auth_info = model.AuthInfo()
        auth_info.is_approved = True
        auth_info.phone_no = phone_no
        auth_info.password = hash_password("user")
        session_id = gen_session_id()
        auth_info.session_id = session_id
        auth_info.permissions = 0
        auth_info.person_id = person.pk
        auth_info.save()
        return {"session_id": session_id,
                "person_id": str(person.pk)}
    except Exception as e:
        print("Failed to prepare logged in person")
        print(str(e))


def prepare_first_admin():
    try:
        auth_info = model.AuthInfo()
        auth_info.is_approved = True
        auth_info.phone_no = "79032233223"
        auth_info.password = hash_password("boov")
        session_id = gen_session_id()
        auth_info.session_id = session_id
        auth_info.permissions = 1
        auth_info.save()
        return auth_info.session_id
    except Exception as e:
        print("Failed to prepare first admin")
        print(str(e))


def wipe_db():
    try:
        revDb = _get_db("reviewer")
        print("Deleting records from %s" %revDb)
        colList = revDb.list_collection_names()
        for col in colList:
            revDb[col].delete_many({})
    except Exception as e:
        print("Failed to wipe DB")
        print(str(e))


def post_item(instance, url, data, auth_header="admin"):
    if not isinstance(instance, unittest.TestCase):
        raise TypeError
    if auth_header == "admin":
        header = instance.admin_header
    else:
        header = auth_header
    resp = requests.post(url=url, json=data, headers=header)
    instance.assertEqual(200, resp.status_code, "post response status code must be 200")
    resp_json = resp.json()
    instance.assertEqual(ERR.OK, resp_json["result"], "post result must be ERR.OK")
    if "error_message" in resp_json: print(resp_json["error_message"])
    instance.assertTrue(resp_json["id"], "returned id must be not None")
    return resp_json["id"]


def try_post_item(instance, url, data, headers):
    if not isinstance(instance, unittest.TestCase):
        raise TypeError
    resp = requests.post(url=url,
                         json=data,
                         headers=headers)
    instance.assertEqual(200, resp.status_code, "post response status code must be 200")
    return resp.json()


def try_delete_item(instance, url, headers):
    if not isinstance(instance, unittest.TestCase):
        raise TypeError
    resp = requests.delete(url=url,
                           headers=headers)
    instance.assertEqual(200, resp.status_code, "delete response status code must be 200")
    return resp.json()


def try_get_item(instance, url, headers):
    if not isinstance(instance, unittest.TestCase):
        raise TypeError
    resp = requests.get(url=url,
                        headers=headers)
    instance.assertEqual(200, resp.status_code, "get response status code must be 200")
    return resp.json()


def try_patch_item(instance, url, data, headers):
    if not isinstance(instance, unittest.TestCase):
        raise TypeError
    resp = requests.patch(url=url,
                          json=data,
                          headers=headers)
    instance.assertEqual(200, resp.status_code, "patch response status code must be 200")
    return resp.json()


def prepare_two_persons(instance, api_url):
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


def generate_doc(instance, type_list, *args, **kwargs):
    instance.gen_doc_ctr += 1
    cur_item = dict()
    for key, value in type_list:
        if value == "string":
            cur_item.update({
                key: "sample_" + key + "_" + str(instance.gen_doc_ctr + 1)
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
                key: "3223223" + str(instance.gen_doc_ctr)
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


def prepare_persons(instance, api_url, person_count):
    person_type_list = dict(first_name="string",
                            middle_name="string",
                            surname="string",
                            birth_date="date",
                            phone_no="number_string")
    id_list = []
    for person_ctr in range(person_count):
        cur_person = generate_doc(instance, person_type_list.items())
        resp_json = requests.post(url=api_url + "/persons", json=cur_person).json()
        instance.assertEqual(resp_json["result"], ERR.OK, "aux person must be added")
        id_list.append(resp_json["id"])
    return id_list
