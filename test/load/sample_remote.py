# -*- coding: utf-8 -*-
import context
import requests
import node.settings.errors as ERR
import sys
import random

server_url = "http://151.248.120.88/develop/v1"
admin_login = "79032233223"
admin_pass = "SomeSecurePass"
departments_num = 10
groups_num = 100
specializations_num = 5
persons_num = 1000


def random_name(type):
    VOWELS = "аеиоуэюя"
    CONSONANTS = "бвгджзклмнпрстфхцч"
    ALPHABET = VOWELS + CONSONANTS

    name = ""
    if type == "department":
        name += "Кафедра "
        for i in range(random.randrange(3, 5)):
            name += random.choice(ALPHABET).upper()
    if type == "group":
        name += random.choice(ALPHABET).upper() + "-" + \
                str(random.randrange(0, 99)) + "-" + str(random.randrange(0, 99))
    if type == "specialization":
        if random.choice([0, 1]):
            name += "Student"
        else:
            name += "Tutor"

    def person_name():
        name = ""
        for i in range(random.randrange(3, 8)):
            if random.choice([0, 1]):
                name += random.choice(CONSONANTS)
            else:
                name += random.choice(VOWELS)
        name = name[0].upper() + name[1:]
        return name

    if type == "first_name":
        name = person_name()
    if type == "middle_name":
        name = person_name() + "вич"
    if type == "surname":
        name = person_name() + "ов"

    return name


def fill_db():

    # login as admin
    data = {"phone_no": admin_login, "password": admin_pass}
    json_header = {'Content-Type': 'application/json'}
    resp = requests.post(url=server_url+"/user_login", json=data, headers=json_header)
    if resp.json()["result"] != 0:
        raise Exception("Fail to login")
    admin_header = {"Authorization": "Bearer " + resp.json()["session_id"]}
    print(admin_header)

    # add departments
    resp = requests.get(url=server_url + "/organizations")
    org_id = resp.json()["list"][0]["id"]

    for i in range(departments_num):
        data = {"name": random_name("department")}
        resp = requests.post(url=server_url + "/organizations/%s/departments" % org_id,
                             json=data,
                             headers={**json_header, **admin_header})
        if resp.json()["result"] != 0:
            raise Exception("Fail to add department")

    # add groups
    resp = requests.get(url=server_url + "/organizations/%s/departments" % org_id)
    dep_ids = list (dep["id"] for dep in resp.json()["list"])
    group_ids = []

    for i in range(groups_num):
        data = {"name": random_name("group")}
        dep_id = random.choice(dep_ids)
        resp = requests.post(url=server_url + "/departments/%s/groups" % dep_id,
                             json=data,
                             headers={**json_header, **admin_header})
        if resp.json()["result"] != 0:
            raise Exception("Fail to add group")
        group_ids.append(resp.json()["id"])

    # add specializations
    spec_ids = []
    for i in range(specializations_num):
        data = {"type": random_name("specialization") + str(i)}
        resp = requests.post(url=server_url + "/specializations",
                             json=data,
                             headers={**json_header, **admin_header})
        if resp.json()["result"] != 0:
            raise Exception("Fail to add specialization")
        spec_ids.append(resp.json()["id"])

    # add persons
    for i in range(persons_num):
        data = {
            "first_name": random_name("first_name"),
            "middle_name": random_name("middle_name"),
            "surname": random_name("surname"),
            "birth_date": "2000-10-10",
            "phone_no": "8901"+ "%07d"%(i+1)
        }
        resp = requests.post(url=server_url + "/persons",
                             json=data,
                             headers={**json_header, **admin_header})
        if resp.json()["result"] != 0:
            raise Exception("Fail to add person")
        p_id = resp.json()["id"]

        data = {
            "specialization_id": random.choice(spec_ids),
            "department_id": random.choice(dep_ids),
            "level": random.uniform(0,100)
        }
        resp = requests.post(url=server_url + "/persons/%s/specializations" % p_id,
                             json=data,
                             headers={**json_header, **admin_header})
        if resp.json()["result"] != 0:
            raise Exception("Fail to add person specialization")

        random.shuffle(group_ids)
        for j in range(random.randrange(1,4)):
            data = {"person_id": p_id}
            resp = requests.post(url=server_url + "/groups/%s/group_members" % group_ids[j],
                                 json=data,
                                 headers={**json_header, **admin_header})
            if resp.json()["result"] != 0:
                raise Exception("Fail to add group member")

if __name__ == "__main__":
    if "--local" in sys.argv:
        server_url = "http://127.0.0.1:5000"
        from node.node_server import start_server
        from threading import Thread

        class NodeServer(Thread):
            def run(self):
                start_server(5000, "http", False)

        node_server_thread = NodeServer()
        node_server_thread.start()
    fill_db()