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
from bson import ObjectId
import sys
# from src.data.reviewer_model import *
import api_helper_methods as hm
import data.reviewer_model as model
from pymodm.errors import DoesNotExist
from bson.binary import Binary, BINARY_SUBTYPE

node_port = 5002


class NodeServer(Thread):
    def run(self):
        start_server(node_port, log=False)


node_server_thread = NodeServer()


# TODO с учётом прямого общения с базой тесты неплохо бы оптимизировать
class TestApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Загрузка адреса сервера
        cls.api_URL = "http://127.0.0.1:" + str(node_port)
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
                print("Connection attempt %s failed" % str(attempts))
                if attempts > 20: raise ConnectionError("could not connect to server")
        print("Connected")

    @classmethod
    def tearDownClass(cls):
        # TODO в окончательной версии лучше вайпнуть ДБ тут тоже
        requests.post(cls.api_URL + "/shutdown")

    def tearDown(self):
        pass

    def setUp(self):
        # requests.post(self.api_URL + "/wipe")
        hm.wipe_db()
        self.admin_header = {"Cookie":
                                 "session_id=" + hm.prepare_first_admin()}

    def setup_reviewer(self):
        reviewer = hm.prepare_logged_in_person("78001112233")
        self.reviewer_header = {"Cookie":
                                    "session_id=" + reviewer["session_id"]}
        self.reviewer_id = reviewer["person_id"]

    def setup_reviewer2(self):
        reviewer = hm.prepare_logged_in_person("78001112234")
        self.reviewer_header2 = {"Cookie":
                                     "session_id=" + reviewer["session_id"]}
        self.reviewer_id2 = reviewer["person_id"]

    def t_simple_normal(self, url_get, url_post, url_delete, *args, **kwargs):
        # read from empty DB
        read_list = self.get_item_list(url_get)
        self.assertListEqual([], read_list, "initial DB must not contain any " + url_delete)
        # write items to DB
        add_list = []
        items_to_write = 2
        for item_ctr in range(items_to_write):
            cur_item = self.generate_doc(kwargs.items())
            cur_id = self.post_item(url_post, cur_item)
            cur_item.update({"id": cur_id})
            add_list.append(cur_item)
        print("sample data for " + url_post + ":\n" + str(add_list))
        # verify written items
        read_list = self.get_item_list(url_get)
        total_match = 0
        for added_item in add_list:
            item_match = 0
            for read_item in read_list:
                if added_item["id"] == read_item["id"]:  # сравниваем только id, так как формат выдачи будет меняться
                    item_match += 1
                    total_match += 1
            self.assertEqual(item_match, 1, "must be exactly one match for each item")
        self.assertEqual(total_match, items_to_write, "all added items must be in GET list")
        # specific tests
        if url_delete == "/tests":
            parent_id = re.findall("\w+", url_post)[1]
            for added_item in add_list:
                item_data = self.get_item_data("/tests/" + added_item["id"])
                self.assertEqual(item_data["info"], added_item["info"], "test info must match")
                self.assertEqual(item_data["name"], added_item["name"], "test name must match")
                self.assertEqual(item_data["group_id"], parent_id, "group_ids must match")
        if url_delete == "/persons":
            for person in add_list:
                person_info = self.get_item_data("/persons/" + person["id"])
                self.assertEqual(person["surname"], person_info["surname"])
                self.assertEqual(person["first_name"], person_info["first_name"])
                self.assertEqual(person["middle_name"], person_info["middle_name"])
                self.assertEqual(person["phone_no"], person_info["phone_no"])
                self.assertEqual(person["birth_date"], person_info["birth_date"])
        # delete items
        for item in add_list:
            self.delete_item(url_delete + "/" + item["id"])
        # verify deletion
        read_list = self.get_item_list(url_get)
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
        org_id = self.post_item('/organizations', post_data)
        return org_id

    def prepare_department(self) -> dict:
        aux_org_id = self.prepare_organization()
        self.assertTrue(aux_org_id, "auxiliary organization must be created")
        post_data = self.generate_doc(dict(name="string").items())
        dep_id = self.post_item('/organizations/' + aux_org_id + "/departments", post_data)
        return {"dep_id": dep_id,
                "org_id": aux_org_id}

    def prepare_group(self) -> dict:
        aux_items_ids = self.prepare_department()
        self.assertTrue(aux_items_ids["dep_id"], "aux department must be created")
        post_data = self.generate_doc(dict(name="string").items())
        group_id = self.post_item('/departments/' + aux_items_ids["dep_id"] + "/groups",
                                  post_data)
        aux_items_ids.update({"group_id": group_id})
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
            p_id = self.post_item("/persons", cur_person)
            id_list.append(p_id)
        return id_list

    def prepare_hs(self):
        skill_type = model.SkillType()
        skill_type.name = "hard_skill_type"
        skill_type.save()
        hard_skill = model.HardSkill()
        hard_skill.name = "hs_name"
        hard_skill.skill_type_id = skill_type.pk
        hard_skill.save()
        return [str(hard_skill.pk), {
            "name" : "hs_name",
            "skill_type_id": str(skill_type.pk)
        }]

    def prepare_ss(self):
        skill_type = model.SkillType()
        skill_type.name = "soft_skill_type"
        skill_type.save()
        soft_skill = model.SoftSkill()
        soft_skill.name = "ss_name"
        soft_skill.skill_type_id = skill_type.pk
        soft_skill.save()
        return [str(soft_skill.pk), {
            "name": "ss_name",
            "skill_type_id": str(skill_type.pk)
        }]

    def test_organization_normal(self):
        self.t_simple_normal("/organizations",
                             "/organizations",
                             "/organizations",
                             name="string")

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


    def test_add_skill_type(self):
        post_data = {"name": "some_name"}
        st_id = self.post_item("/skill_types", post_data)
        skill_type = model.SkillType(_id=st_id)
        skill_type.refresh_from_db()
        self.assertEqual("some_name", skill_type.name, "must save correct name")
        with self.assertRaises(AssertionError):
            self.post_item("/skill_types", post_data)

    def test_delete_skill_type(self):
        skill_type = model.SkillType()
        skill_type.name = "sample_name"
        skill_type.save()
        skill_type.refresh_from_db()
        self.delete_item("/skill_types/%s" % skill_type.pk)
        with self.assertRaises(DoesNotExist):
            skill_type.refresh_from_db()
        with self.assertRaises(AssertionError):
            self.delete_item("/skill_types/%s" % skill_type.pk)

    def test_list_skill_types(self):
        pks = []
        for i in range(2):
            skill_type = model.SkillType()
            skill_type.name = "name%s"%i
            skill_type.save()
            pks.append(str(skill_type.pk))
        list = self.get_item_list("/skill_types")
        self.assertEqual(2, len(list), "must return all items")
        for i in range(2):
            self.assertIn({"id" : pks[i],
                       "name" : "name%s"%i},
                      list, "must return correct list")

    def test_add_soft_skill(self):
        skill_type = model.SkillType()
        skill_type.name = "sample_skill_type"
        skill_type.save()
        post_data = {"name": "some_name"}
        ss_id = self.post_item("/skill_types/%s/soft_skills" % skill_type.pk, post_data)
        soft_skill = model.SoftSkill(_id=ss_id)
        soft_skill.refresh_from_db()
        self.assertEqual("some_name", soft_skill.name, "must save correct name")
        with self.assertRaises(AssertionError):
            self.post_item("/skill_types/%s/soft_skills" % skill_type.pk, post_data)

    def test_add_hard_skill(self):
        skill_type = model.SkillType()
        skill_type.name = "sample_skill_type"
        skill_type.save()
        post_data = {"name": "some_name"}
        hs_id = self.post_item("/skill_types/%s/hard_skills" % skill_type.pk, post_data)
        hard_skill = model.HardSkill(_id=hs_id)
        hard_skill.refresh_from_db()
        self.assertEqual("some_name", hard_skill.name, "must save correct name")
        with self.assertRaises(AssertionError):
            self.post_item("/skill_types/%s/hard_skills" % skill_type.pk, post_data)

    def test_delete_soft_skill(self):
        skill_type = model.SkillType()
        skill_type.name = "sample_skill_type"
        skill_type.save()
        soft_skill = model.SoftSkill()
        soft_skill.name = "sample_name"
        soft_skill.skill_type_id=skill_type.pk
        soft_skill.save()
        soft_skill.refresh_from_db()
        self.delete_item("/soft_skills/%s" % soft_skill.pk)
        with self.assertRaises(DoesNotExist):
            soft_skill.refresh_from_db()
        with self.assertRaises(AssertionError):
            self.delete_item("/soft_skills/%s" % soft_skill.pk)

    def test_delete_hard_skill(self):
        skill_type = model.SkillType()
        skill_type.name = "sample_skill_type"
        skill_type.save()
        hard_skill = model.HardSkill()
        hard_skill.name = "sample_name"
        hard_skill.skill_type_id=skill_type.pk
        hard_skill.save()
        hard_skill.refresh_from_db()
        self.delete_item("/hard_skills/%s" % hard_skill.pk)
        with self.assertRaises(DoesNotExist):
            hard_skill.refresh_from_db()
        with self.assertRaises(AssertionError):
            self.delete_item("/hard_skills/%s" % hard_skill.pk)

    def test_list_soft_skills(self):
        skill_type = model.SkillType()
        skill_type.name = "sample_skill_type"
        skill_type.save()
        pks = []
        for i in range(2):
            soft_skill = model.SoftSkill()
            soft_skill.name = "name%s"%i
            soft_skill.skill_type_id = skill_type.pk
            soft_skill.save()
            pks.append(str(soft_skill.pk))
        list = self.get_item_list("/soft_skills")
        self.assertEqual(2, len(list), "must return all items")
        for i in range(2):
            self.assertIn({"id" : pks[i],
                       "name" : "name%s"%i,
                       "skill_type" : str(skill_type.pk)},
                      list, "must return correct list")

    def test_list_hard_skills(self):
        skill_type = model.SkillType()
        skill_type.name = "sample_skill_type"
        skill_type.save()
        pks = []
        for i in range(2):
            hard_skill = model.HardSkill()
            hard_skill.name = "name%s"%i
            hard_skill.skill_type_id = skill_type.pk
            hard_skill.save()
            pks.append(str(hard_skill.pk))
        list = self.get_item_list("/hard_skills")
        self.assertEqual(2, len(list), "must return all items")
        for i in range(2):
            self.assertIn({"id" : pks[i],
                       "name" : "name%s"%i,
                       "skill_type" : str(skill_type.pk)},
                      list, "must return correct list")


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
        self.t_simple_normal("/organizations/" + aux_org_id + "/departments",
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
        test_data = {"name": "sample_test_name",
                     "info": "sample_test_info"}
        test_id = self.post_item("/groups/%s/tests" % group_id, test_data)
        test2_id = self.post_item("/groups/%s/tests" % group_id, {"name": "test 2",
                                                                  "info": "test 2 info"})
        ref_result_data = {"person_id": person_id,
                           "result_data": ["result 1", "result 2"]}
        # post test result
        result_id = self.post_item("/tests/%s/results" % test_id, ref_result_data)
        # verify
        item_list = self.get_item_list("/tests/results")
        self.assertDictListEqual([{"id": result_id}], item_list)
        item_list = self.get_item_list("/tests/results?person_id=" + person_id)
        self.assertDictListEqual([{"id": result_id}], item_list)
        item_list = self.get_item_list("/tests/results?person_id=" + person2_id)
        self.assertDictListEqual([], item_list)
        item_list = self.get_item_list("/tests/results?test_id=" + test_id)
        self.assertDictListEqual([{"id": result_id}], item_list)
        item_list = self.get_item_list("/tests/results?test_id=" + test2_id)
        self.assertDictListEqual([], item_list)
        # verify test result info
        result_data = self.get_item_data("/tests/results/" + result_id)
        ref_result_data.update({"test_id": test_id})
        self.assertDictEqual(ref_result_data, result_data)
        # delete
        self.delete_item("/tests/results/" + result_id)
        # verify
        item_list = self.get_item_list("/tests/results")
        self.assertDictListEqual([], item_list)

    def test_find_persons_limits(self):
        person_ids = self.prepare_persons(10)
        list_0_3 = self.get_item_list("/persons?query_limit=4")
        self.assertEqual(len(list_0_3), 4, "must return requested number of items")
        for index, item in enumerate(list_0_3):
            self.assertEqual(item["id"], person_ids[index])
        list_4_7 = self.get_item_list("/persons?query_start=4&query_limit=4")
        self.assertEqual(len(list_4_7), 4, "must return requested number of items")
        for index, item in enumerate(list_4_7):
            self.assertEqual(item["id"], person_ids[index + 4])
        list_8_9 = self.get_item_list("/persons?query_start=8")
        self.assertEqual(len(list_8_9), 2, "must return requested number of items")
        for index, item in enumerate(list_8_9):
            self.assertEqual(item["id"], person_ids[index + 8])

    def test_find_persons_filters(self):
        persons = [
            {"surname": "Иванов",
             "first_name": "Петр",
             "middle_name": "Андреевич",
             "birth_date": datetime.date(2000, 1, 1).isoformat(),
             "phone_no": "79002222201",
             },
            {"surname": "Петров",
             "first_name": "Николай",
             "middle_name": "Владимирович",
             "birth_date": datetime.date(2000, 1, 1).isoformat(),
             "phone_no": "79002222202",
             },
            {"surname": "Сидоров",
             "first_name": "Петр",
             "middle_name": "Владимирович",
             "birth_date": datetime.date(2000, 1, 1).isoformat(),
             "phone_no": "79002222203",
             },
            {"surname": "Иванов",
             "first_name": "Александр",
             "middle_name": "Николаевич",
             "birth_date": datetime.date(2000, 1, 1).isoformat(),
             "phone_no": "79002222204",
             },
        ]
        person_ids = []
        for person in persons:
            person_ids.append(self.post_item("/persons", person))

        # filter by surname
        person_list = self.get_item_list("/persons?surname=Иванов")
        for person in person_list:
            self.assertIn(person["id"], [person_ids[0], person_ids[3]])
            self.assertNotIn(person["id"], [person_ids[1], person_ids[2]])

        # filter by first_name
        person_list = self.get_item_list("/persons?first_name=Петр")
        for person in person_list:
            self.assertIn(person["id"], [person_ids[0], person_ids[2]])
            self.assertNotIn(person["id"], [person_ids[1], person_ids[3]])

        # filter by middle_name
        person_list = self.get_item_list("/persons?middle_name=Николаевич")
        for person in person_list:
            self.assertIn(person["id"], [person_ids[3]])
            self.assertNotIn(person["id"], [person_ids[0], person_ids[1], person_ids[2]])

        pass

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

    def test_post_specialization(self):
        # post without detail
        # struct = hm.prepare_org_structure()
        spec_data = {"type": "Student"}
        spec_id = self.post_item("/specializations", spec_data)
        spec = model.Specialization.objects.get({"_id": ObjectId(spec_id)})
        spec.refresh_from_db()
        self.assertEqual("Student", spec.type, "spec type must be saved")
        self.assertIsNone(spec.detail, "no detail must present")
        # post with detail
        spec_data = {"type": "Tutor", "detail": "ТОЭ"}
        spec_id = self.post_item("/specializations", spec_data)
        spec = model.Specialization.objects.get({"_id": ObjectId(spec_id)})
        spec.refresh_from_db()
        self.assertEqual("Tutor", spec.type, "spec type must be saved")
        self.assertEqual("ТОЭ", spec.detail, "spec detail must be saved")

    def test_delete_specialization(self):
        spec = model.Specialization("student")
        spec.save()
        self.delete_item("/specializations/%s" % spec.pk)
        with self.assertRaises(DoesNotExist):
            spec.refresh_from_db()

    def test_list_specializations(self):
        spec_1 = model.Specialization("Tutor", "ТОЭ")
        spec_1.save()
        spec_2 = model.Specialization("Student")
        spec_2.save()
        spec_list = self.get_item_list("/specializations")
        self.assertEqual(2, len(spec_list))
        self.assertIn({"id": str(spec_1.pk),
                       "type": spec_1.type,
                       "detail": spec_1.detail}, spec_list)
        self.assertIn({"id": str(spec_2.pk),
                       "type": spec_2.type}, spec_list)

    def test_post_person_specialization(self):
        # without level
        struct = hm.prepare_org_structure()
        p_spec_data = {"department_id": struct["dep_1"]["id"],
                       "specialization_id": struct["spec_1"]["id"]}
        p_spec_id = self.post_item("/persons/%s/specializations" % struct["person_1"]["id"],
                                   p_spec_data)
        p_spec = model.PersonSpecialization.objects.get({"_id": ObjectId(p_spec_id)})
        p_spec.refresh_from_db()
        self.assertEqual(struct["dep_1"]["id"], str(p_spec.department_id.pk), "dep_id must be saved")
        self.assertEqual(struct["spec_1"]["id"], str(p_spec.specialization_id.pk), "spec_id must be saved")
        self.assertEqual(struct["person_1"]["id"], str(p_spec.person_id.pk), "person_id must be saved")
        self.assertEqual(None, p_spec.level, "no level must be saved")
        # with level
        p_spec_data = {"department_id": struct["dep_2"]["id"],
                       "specialization_id": struct["spec_2"]["id"],
                       "level": "60.0"}
        p_spec_id = self.post_item("/persons/%s/specializations" % struct["person_2"]["id"],
                                   p_spec_data)
        p_spec = model.PersonSpecialization.objects.get({"_id": ObjectId(p_spec_id)})
        p_spec.refresh_from_db()
        self.assertEqual(struct["dep_2"]["id"], str(p_spec.department_id.pk), "dep_id must be saved")
        self.assertEqual(struct["spec_2"]["id"], str(p_spec.specialization_id.pk), "spec_id must be saved")
        self.assertEqual(struct["person_2"]["id"], str(p_spec.person_id.pk), "person_id must be saved")
        self.assertEqual(60.0, p_spec.level, "level must be saved")

    def test_delete_person_specialization(self):
        struct = hm.prepare_org_structure()
        p_spec = model.PersonSpecialization(
            ObjectId(struct["person_1"]["id"]),
            ObjectId(struct["dep_1"]["id"]),
            ObjectId(struct["spec_1"]["id"]),
            50.0,
            {"detail": "text"},
            True
        )
        p_spec.save()
        self.delete_item("/persons/specializations/%s" % p_spec.pk)
        with self.assertRaises(DoesNotExist):
            p_spec.refresh_from_db()

    def test_get_person_specializations(self):
        struct = hm.prepare_org_structure()
        p_spec_1 = model.PersonSpecialization(
            ObjectId(struct["person_1"]["id"]),
            ObjectId(struct["dep_1"]["id"]),
            ObjectId(struct["spec_1"]["id"]),
            50.0,
            {"detail": "text"},
            True
        )
        p_spec_1.save()
        p_spec_2 = model.PersonSpecialization(
            ObjectId(struct["person_1"]["id"]),
            ObjectId(struct["dep_2"]["id"]),
            ObjectId(struct["spec_2"]["id"]),
            40.0,
        )
        p_spec_2.is_active = False
        p_spec_2.save()
        p_spec_3 = model.PersonSpecialization(
            ObjectId(struct["person_2"]["id"]),
            ObjectId(struct["dep_2"]["id"]),
            ObjectId(struct["spec_2"]["id"]),
            30.0,
            {"detail": "text3"},
            True
        )
        p_spec_3.save()
        person_1_spec_list = self.get_item_list("/persons/%s/specializations"
                                                % struct["person_1"]["id"])
        self.assertEqual(2, len(person_1_spec_list))
        self.assertIn({"id": str(p_spec_1.pk),
                       "department_id": struct["dep_1"]["id"],
                       "level": 50.0,
                       "specialization_type": struct["spec_1"]["type"],
                       "is_active": "True",
                       "specialization_detail": struct["spec_1"]["detail"],
                       "additional_details": {"detail": "text"}},
                      person_1_spec_list,
                      "p_spec info must present")
        self.assertIn({"id": str(p_spec_2.pk),
                       "department_id": struct["dep_2"]["id"],
                       "level": 40.0,
                       "specialization_type": struct["spec_2"]["type"],
                       "is_active": "False",
                       },
                      person_1_spec_list,
                      "p_spec info must present")

    def test_patch_person_specialization(self):
        struct = hm.prepare_org_structure()
        p_spec_1 = model.PersonSpecialization(
            ObjectId(struct["person_1"]["id"]),
            ObjectId(struct["dep_1"]["id"]),
            ObjectId(struct["spec_1"]["id"]),
            50.0,
            {"detail": "text"},
            True
        )
        p_spec_1.save()
        # test status change
        self.patch_item("/persons/specializations/%s?is_active=false" % p_spec_1.pk)
        p_spec_1.refresh_from_db()
        self.assertFalse(p_spec_1.is_active, "is_active must be set")
        self.patch_item("/persons/specializations/%s?is_active=true" % p_spec_1.pk)
        p_spec_1.refresh_from_db()
        self.assertTrue(p_spec_1.is_active, "is_active must be set")
        # test set details
        patch_data = {"detail 2": "text 2"}
        self.patch_item("/persons/specializations/%s" % p_spec_1.pk, patch_data)
        p_spec_1.refresh_from_db()
        self.assertEqual(patch_data, p_spec_1.details, "details must be patched")

    def test_find_persons_spec_filters(self):
        struct = hm.prepare_org_structure()
        p_spec_1 = model.PersonSpecialization(
            ObjectId(struct["person_1"]["id"]),
            ObjectId(struct["dep_1"]["id"]),
            ObjectId(struct["spec_1"]["id"]),
            50.0,
            {"detail": "text"},
            True
        )
        p_spec_1.save()


        # test if person_1 is in return list
        p_list = self.get_item_list("/persons")
        p_1_ref_dict = struct["person_1"]
        p_1_ref_dict.pop("phone_no")
        p_1_ref_dict.pop("birth_date")
        p_1_ref_dict.update({"specialization": struct["spec_1"]["type"]})
        p_1_ref_dict.update({"organization_name": struct["org_1"]["name"]})
        self.assertIn(p_1_ref_dict, p_list, "must return correct person info")
        # test if org and spec are not returned when absent
        p_2_ref_dict = struct["person_2"]
        p_2_ref_dict.pop("phone_no")
        p_2_ref_dict.pop("birth_date")
        # TODO внести единство в эти None и "None"
        p_2_ref_dict.update({"specialization": None})
        p_2_ref_dict.update({"organization_name": "None"})
        self.assertIn(p_2_ref_dict, p_list, "must return correct person info")

        p_spec_4 = model.PersonSpecialization(
            ObjectId(struct["person_1"]["id"]),
            ObjectId(struct["dep_1"]["id"]),
            ObjectId(struct["spec_3"]["id"]),
            50.0,
            {"detail": "text"},
            True
        )
        p_spec_4.save()

        p_list = self.get_item_list("/persons?specialization=Tutor")
        self.assertEqual(1, len(p_list), "must not contain duplicates")
        self.assertIn(p_1_ref_dict, p_list, "must return correct person info")
        self.assertNotIn(p_2_ref_dict, p_list, "must not return non-matching persons info")

        p_spec_2 = model.PersonSpecialization(
            ObjectId(struct["person_1"]["id"]),
            ObjectId(struct["dep_2"]["id"]),
            ObjectId(struct["spec_2"]["id"]),
            40.0,
        )
        p_spec_2.is_active = False
        p_spec_2.save()
        p_spec_3 = model.PersonSpecialization(
            ObjectId(struct["person_2"]["id"]),
            ObjectId(struct["dep_2"]["id"]),
            ObjectId(struct["spec_2"]["id"]),
            30.0,
            {"detail": "text3"},
            True
        )
        p_spec_3.save()
        p_list = self.get_item_list("/persons?specialization=Tutor")
        p1_id = [item for item in p_list if item["id"] == p_1_ref_dict["id"]]
        self.assertTrue(p1_id)
        p2_id = [item for item in p_list if item["id"] == p_2_ref_dict["id"]]
        self.assertFalse(p2_id)
        p_list = self.get_item_list("/persons?specialization=Student")
        p1_id = [item for item in p_list if item["id"] == p_1_ref_dict["id"]]
        self.assertTrue(p1_id)
        p2_id = [item for item in p_list if item["id"] == p_2_ref_dict["id"]]
        self.assertTrue(p2_id)
        p_list = self.get_item_list("/persons?department_id=%s" % struct["dep_1"]["id"])
        self.assertEqual(1, len(p_list), "must not contain duplicates")
        p1_id = [item for item in p_list if item["id"] == p_1_ref_dict["id"]]
        self.assertTrue(p1_id)
        p2_id = [item for item in p_list if item["id"] == p_2_ref_dict["id"]]
        self.assertFalse(p2_id)
        p_list = self.get_item_list("/persons?department_id=%s" % struct["dep_2"]["id"])
        p1_id = [item for item in p_list if item["id"] == p_1_ref_dict["id"]]
        self.assertTrue(p1_id)
        p2_id = [item for item in p_list if item["id"] == p_2_ref_dict["id"]]
        self.assertTrue(p2_id)
        p_list = self.get_item_list("/persons?organization_id=%s" % struct["org_1"]["id"])
        self.assertEqual(1, len(p_list), "must not contain duplicates")
        p1_id = [item for item in p_list if item["id"] == p_1_ref_dict["id"]]
        self.assertTrue(p1_id)
        p2_id = [item for item in p_list if item["id"] == p_2_ref_dict["id"]]
        self.assertFalse(p2_id)
        p_list = self.get_item_list("/persons?organization_id=%s" % struct["org_2"]["id"])
        p1_id = [item for item in p_list if item["id"] == p_1_ref_dict["id"]]
        self.assertTrue(p1_id)
        p2_id = [item for item in p_list if item["id"] == p_2_ref_dict["id"]]
        self.assertTrue(p2_id)

    def test_group_member_normal(self):
        person_id = self.prepare_persons(1)[0]
        facility_ids = self.prepare_group()
        group_id = facility_ids["group_id"]
        # verify that group member list is initially empty
        gm_list = self.get_item_list("/groups/%s/group_members" % group_id)
        self.assertEqual([], gm_list)
        # add group_member without role
        post_data = {"person_id": person_id}
        gm_id = self.post_item("/groups/%s/group_members" % group_id, post_data)
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
                       "is_active": "True"}
        self.assertDictEqual(ref_gm_info, gm_info)
        # verify with /persons
        self.prepare_persons(2)
        person_info = self.get_item_list("/persons?group_id=" + group_id)
        self.assertEqual(1, len(person_info))
        self.assertEqual(person_id, person_info[0]["id"])
        # add role to list of roles in group
        admin_id = self.post_item("/group_roles", {"name": "admin"})
        self.post_modify_item("/groups/%s/role_list" % group_id, {"role_list": [admin_id]})
        # verify
        role_list = self.get_item_list("/groups/%s/role_list" % group_id)
        self.assertEqual(admin_id, role_list[0]["id"])
        # set group role
        self.post_modify_item("/group_members/%s/group_roles" % gm_id, {"group_role_id": admin_id})
        # verify
        gm_info = self.get_item_data("/group_members/" + gm_id)
        ref_gm_info.update({"role_id": admin_id})
        self.assertDictEqual(ref_gm_info, gm_info)
        # add permissions
        read_permission = self.post_item("/group_permissions", {"name": "read_info"})
        self.post_modify_item("/group_members/%s/permissions" % gm_id,
                              {"group_permission_id": read_permission})
        write_permission = self.post_item("/group_permissions", {"name": "write_info"})
        self.post_modify_item("/group_members/%s/permissions" % gm_id,
                              {"group_permission_id": write_permission})
        # verify
        gm_info = self.get_item_data("/group_members/" + gm_id)
        ref_gm_info.update({"permissions": [read_permission, write_permission]})
        self.assertDictEqual(ref_gm_info, gm_info)
        # delete permission
        self.delete_item("/group_members/%s/permissions/%s" % (gm_id, write_permission))
        # verify
        gm_info = self.get_item_data("/group_members/" + gm_id)
        ref_gm_info.update({"permissions": [read_permission]})
        self.assertDictEqual(ref_gm_info, gm_info)
        # set inactive
        self.patch_item("/group_members/%s?is_active=false" % gm_id)
        # verify
        gm_info = self.get_item_data("/group_members/" + gm_id)
        ref_gm_info.update({"is_active": "False"})
        self.assertDictEqual(ref_gm_info, gm_info)
        # test for duplicates in search
        post_data = {"person_id": person_id}
        gm2_id = self.post_item("/groups/%s/group_members" % group_id, post_data)
        p_list = self.get_item_list("/persons?group_id=" + group_id)
        self.assertEqual(1, len(p_list), "must contain no duplicate persons")
        # delete
        self.delete_item("/group_members/" + gm_id)
        resp_json = requests.get(self.api_URL + "/group_members/" + gm_id, headers=self.admin_header).json()
        self.assertEqual(ERR.NO_DATA, resp_json["result"])

    def test_reviews_normal(self):
        person_id = self.prepare_persons(1)[0]
        facility_ids = self.prepare_group()
        org_id = facility_ids["org_id"]
        dep_id = facility_ids["dep_id"]
        group_id = facility_ids["group_id"]
        hs_id = self.prepare_hs()[0]
        ss_id = self.prepare_ss()[0]
        spec_id = self.post_item("/specializations",
                                 {"type": "Tutor",
                                  "detail": "TOE"})
        p_spec_id = self.post_item("/persons/%s/specializations" % person_id,
                                   {"department_id": dep_id,
                                    "specialization_id": spec_id})
        gm_id = self.post_item("/groups/%s/group_members" % group_id, {"person_id": person_id})
        g_test_id = self.post_item("/groups/%s/tests" % group_id, {"name": "sample_test_name",
                                                                   "info": "sample_test_info"})
        subject_urls = {"Specialization": "/specializations/%s/reviews" % (p_spec_id),
                        "PersonHS": "/persons/%s/hard_skills/%s/reviews" % (person_id, hs_id),
                        "PersonSS": "/persons/%s/soft_skills/%s/reviews" % (person_id, ss_id),
                        "Group": "/groups/%s/reviews" % group_id,
                        "GroupTest": "/tests/%s/reviews" % g_test_id,
                        "GroupMember": "/group_members/%s/reviews" % gm_id}
        subj_ids = {"Specialization": p_spec_id,
                    "PersonHS": None,
                    "PersonSS": None,
                    "Group": group_id,
                    "GroupTest": g_test_id,
                    "GroupMember": gm_id}

        rev_ids = {}
        # add reviews
        self.setup_reviewer()
        self.setup_reviewer2()

        for subj_type, subj_url in subject_urls.items():
            review_data = {"reviewer_id": self.reviewer_id,
                           "value": "60.0",
                           "description": "sample_descr"}
            cur_id = self.post_item(subj_url, review_data, auth="reviewer")
            rev_ids.update({subj_type: cur_id})
        p_ss_id = self.get_item_list("/persons/soft_skills")[0]["id"]
        p_hs_id = self.get_item_list("/persons/hard_skills")[0]["id"]
        subj_ids["PersonSS"] = p_ss_id
        subj_ids["PersonHS"] = p_hs_id

        # verify reviews
        review_list = self.get_item_list("/reviews")
        ref_review_list = [{"id": rev_id} for subj_id, rev_id in rev_ids.items()]
        self.assertDictListEqual(ref_review_list, review_list)
        # verify with reviewer_id
        person2_id = self.prepare_persons(1)[0]
        review_list = self.get_item_list("/reviews?reviewer_id=" + self.reviewer_id)
        self.assertDictListEqual(ref_review_list, review_list)
        review_list = self.get_item_list("/reviews?reviewer_id=" + person2_id)
        self.assertDictListEqual([], review_list)
        # verify with subject_id
        for subj_type, rev_id in rev_ids.items():
            print(subj_ids[subj_type])
            review_list = self.get_item_list("/reviews?subject_id=" + subj_ids[subj_type])
            self.assertEqual([{"id": rev_id}], review_list)
        # get review info
        for subj_type, rev_id in rev_ids.items():
            review_data = self.get_item_data("/reviews/" + rev_id)
            ref_data = {"reviewer_id": self.reviewer_id,
                        "subject_id": subj_ids[subj_type],
                        "value": 60.0,
                        "description": "sample_descr"}
            self.assertDictEqual(ref_data, review_data)
        # verify with review from person2
        review_data = {
            "reviewer_id": self.reviewer_id2,
            "subject_id": p_spec_id,
            "value": "80.0",
            "description": "sample_descr2"}
        rev2_id = self.post_item("/specializations/%s/reviews" % (p_spec_id),
                                 review_data,
                                 auth="reviewer2")
        review_list = self.get_item_list("/reviews?subject_id=" + p_spec_id)
        self.assertEqual([{"id": rev_ids["Specialization"]}, {"id": rev2_id}], review_list)
        # delete review
        self.delete_item("/reviews/" + rev_ids["Specialization"], auth="reviewer")
        rev_ids.pop("Specialization")
        # verify
        review_list = self.get_item_list("/reviews?subject_id=" + p_spec_id)
        self.assertEqual([{"id": rev2_id}], review_list)
        # delete all reviews
        self.delete_item("/reviews/" + rev2_id, auth="reviewer2")
        for subj_id, rev_id in rev_ids.items():
            self.delete_item("/reviews/" + rev_id, auth="reviewer")
        # verify for one subject
        review_list = self.get_item_list("/reviews?subject_id=" + gm_id)
        self.assertEqual([], review_list)

    def test_organization_duplicate(self):
        self.post_duplicate_item("/organizations",
                                 "/organizations",
                                 name="String")

    def test_person_duplicate(self):
        self.post_duplicate_item("/persons",
                                 "/persons",
                                 first_name="string",
                                 middle_name="string",
                                 surname="string",
                                 birth_date="date",
                                 phone_no="number_string"
                                 )

    def test_group_roles_duplicate(self):
        self.post_duplicate_item("/group_roles",
                                 "/group_roles",
                                 name="string")

    def test_group_permissions_duplicate(self):
        self.post_duplicate_item("/group_permissions",
                                 "/group_permissions",
                                 name="string")

    def test_department_duplicate(self):
        aux_org_id = self.prepare_organization()
        self.post_duplicate_item("/organizations/" + aux_org_id + "/departments",
                                 "/organizations/" + aux_org_id + "/departments",
                                 name="string")

    def test_group_duplicate(self):
        aux_item_ids = self.prepare_department()
        self.post_duplicate_item("/departments/" + aux_item_ids["dep_id"] + "/groups",
                                 "/departments/" + aux_item_ids["dep_id"] + "/groups",
                                 name="string")

    def test_specialization_duplicate(self):
        p_id = self.prepare_persons(1)[0]
        d_id = self.prepare_department()["dep_id"]
        spec_id = self.post_item("/specializations",
                                 {"type": "Tutor",
                                  "detail": "TOE"})
        self.post_duplicate_item("/persons/%s/specializations" % p_id,
                                 "/persons/%s/specializations" % p_id,
                                 specialization_id=spec_id,
                                 department_id=d_id)

    def test_group_member_duplicate(self):
        p_id = self.prepare_persons(1)[0]
        g_id = self.prepare_group()["group_id"]
        self.post_duplicate_item("/groups/%s/group_members" % g_id,
                                 "/persons/%s/group_members" % p_id,
                                 person_id=p_id)

    def test_test_result_duplicate(self):
        p_id = self.prepare_persons(1)[0]
        g_id = self.prepare_group()["group_id"]
        t_id = self.post_item("/groups/%s/tests" % g_id, {"name": "sample_test", "info": "sample_info"})
        self.post_duplicate_item("/tests/%s/results" % t_id,
                                 "/tests/results",
                                 person_id=p_id,
                                 result_data="string")

    def test_reviews_duplicate(self):
        person_id = self.prepare_persons(1)[0]
        facility_ids = self.prepare_group()
        org_id = facility_ids["org_id"]
        dep_id = facility_ids["dep_id"]
        group_id = facility_ids["group_id"]
        hs_id = self.prepare_hs()[0]
        ss_id = self.prepare_ss()[0]
        print(person_id, org_id, dep_id, group_id, hs_id, ss_id)
        spec_id = self.post_item("/specializations",
                                 {"type": "Tutor",
                                  "detail": "TOE"})
        p_spec_id = self.post_item("/persons/%s/specializations" % person_id,
                                   {"department_id": dep_id,
                                    "specialization_id": spec_id})
        gm_id = self.post_item("/groups/%s/group_members" % group_id, {"person_id": person_id})
        g_test_id = self.post_item("/groups/%s/tests" % group_id, {"name": "sample_test_name",
                                                                   "info": "sample_test_info"})
        subject_urls = {"Specialization": "/specializations/%s/reviews" % (p_spec_id),
                        "PersonHS": "/persons/%s/hard_skills/%s/reviews" % (person_id, hs_id),
                        "PersonSS": "/persons/%s/soft_skills/%s/reviews" % (person_id, ss_id),
                        "Group": "/groups/%s/reviews" % group_id,
                        "GroupTest": "/tests/%s/reviews" % g_test_id,
                        "GroupMember": "/group_members/%s/reviews" % gm_id}
        self.setup_reviewer()
        for subj_type, subj_url in subject_urls.items():
            review_data = {"reviewer_id": self.reviewer_id,
                           "value": "60.0",
                           "description": "sample_descr"}
            cur_id = self.post_item(subj_url, review_data, auth="reviewer")
            resp = requests.post(url=self.api_URL + subj_url, json=review_data,
                                 headers=self.reviewer_header)
            self.assertEqual(200, resp.status_code, "post response status code must be 200")
            resp_json = resp.json()
            self.assertEqual(ERR.DB, resp_json["result"], "duplicate post result must be ERR.OK")

    def test_invalid_post(self):
        self.setup_reviewer()
        p_id = self.prepare_persons(1)[0]
        fac_ids = self.prepare_group()
        org_id = fac_ids["org_id"]
        dep_id = fac_ids["dep_id"]
        group_id = fac_ids["group_id"]
        g_test_id = self.post_item("/groups/%s/tests" % group_id, {"name": "test_name",
                                                                   "info": "test_info"})
        gm_id = self.post_item("/groups/%s/group_members" % group_id,
                               {"person_id": p_id})
        sr_id = self.post_item("/specializations",
                               {"person_id": p_id,
                                "department_id": dep_id,
                                "type": "Student",
                                "description": "specialization_description"})
        st_id = self.post_item("/skill_types",
                               {"name" : "skill_type_name"})
        hs_id = self.post_item("/skill_types/%s/hard_skills" % st_id,
                               {"name": "hard_skill_name",
                                "skill_type_id" : st_id})
        ss_id = self.post_item("/skill_types/%s/soft_skills" % st_id,
                               {"name": "soft_skill_name",
                                "skill_type_id": st_id})
        post_routes = [
            "/organizations",
            "/organizations/%s/departments" % org_id,
            "/departments/%s/groups" % dep_id,
            "/group_roles",
            "/group_permissions",
            "/groups/%s/group_members" % group_id,
            "/group_members/%s/permissions" % gm_id,
            "/group_members/%s/group_roles" % gm_id,
            "/specializations",
            "/specializations/%s/reviews" % sr_id,
            "/groups/%s/reviews" % group_id,
            "/tests/%s/reviews" % g_test_id,
            "/group_members/%s/reviews" % gm_id,
            "/persons/%s/hard_skills/%s/reviews" % (p_id, hs_id),
            "/persons/%s/soft_skills/%s/reviews" % (p_id, ss_id),
            "/persons",
            "/skill_types",
            "/skill_types/%s/soft_skills" % st_id,
            "/skill_types/%s/hard_skills" % st_id,
            "/groups/%s/tests" % group_id,
            "/tests/%s/results" % g_test_id
        ]
        for route in post_routes:
            if "reviews" in route:
                headers = self.reviewer_header
                json_value = {"reviewer_id": self.reviewer_id, "noname": "novalue"}
            else:
                headers = self.admin_header
                json_value = {"noname": "novalue"}
            resp = requests.post(url=self.api_URL + route, json=json_value, headers=headers)
            self.assertEqual(200, resp.status_code, msg="url = " + route)
            self.assertEqual(ERR.INPUT, resp.json()["result"], msg="url = " + route)

    def test_post_invalid_reference(self):
        # setup
        persons_ids = self.prepare_persons(2)
        p_id = persons_ids[0]
        p2_id = persons_ids[1]
        fac_ids = self.prepare_group()
        org_id = fac_ids["org_id"]
        dep_id = fac_ids["dep_id"]
        group_id = fac_ids["group_id"]
        spec_id = self.post_item("/specializations",
                                 {"type": "Tutor",
                                  "detail": "TOE"})
        p_spec_id = self.post_item("/persons/%s/specializations" % p_id,
                                   {"department_id": dep_id,
                                    "specialization_id": spec_id})
        hard_skill_id = self.prepare_hs()[0]
        soft_skill_id = self.prepare_ss()[0]
        g_test_id = self.post_item("/groups/%s/tests" % group_id, {"name": "test_name",
                                                                   "info": "test_info"})

        gm_id = self.post_item("/groups/%s/group_members" % group_id,
                               {"person_id": p_id})
        g_role_id = self.post_item("/group_roles", {"name": "sample_role"})
        # tests
        # department
        self.pass_invalid_ref("/organizations/" + p_id + "/departments",
                              name="string")
        # group
        self.pass_invalid_ref("/departments/" + org_id + "/groups",
                              name="string")
        self.pass_invalid_ref("/groups/" + group_id + "/role_list",
                              role_list=[dep_id])

        # tutor_specialization
        self.pass_invalid_ref("/persons/%s/specializations" % p_id,
                              specialization_id=spec_id,
                              department_id=org_id)
        self.pass_invalid_ref("/persons/%s/specializations" % p_id,
                              specialization_id=org_id,
                              department_id=dep_id)
        self.pass_invalid_ref("/persons/%s/specializations" % hard_skill_id,
                              specialization_id=spec_id,
                              department_id=dep_id)

        # group_member
        self.pass_invalid_ref("/groups/%s/group_members" % hard_skill_id,
                              person_id=p_id)
        self.pass_invalid_ref("/groups/%s/group_members" % group_id,
                              person_id=soft_skill_id)

        self.pass_invalid_ref("/group_members/%s/group_roles" % p_id,
                              group_role_id=g_role_id)
        self.pass_invalid_ref("/group_members/%s/group_roles" % gm_id,
                              group_role_id=p_id)

        # group_test
        self.pass_invalid_ref("/groups/%s/tests" % p_id,
                              name="string",
                              info="string")

        # test_result
        self.pass_invalid_ref("/tests/%s/results" % org_id,
                              person_id=p_id,
                              result_data="string")

        self.pass_invalid_ref("/tests/%s/results" % g_test_id,
                              person_id=dep_id,
                              result_data="string")

        # reviews
        self.setup_reviewer()
        self.pass_invalid_ref("/specializations/%s/reviews" % group_id,
                              auth="reviewer",
                              reviewer_id=self.reviewer_id,
                              value="skill_level",
                              description="string"
                              )
        self.pass_invalid_ref("/groups/%s/reviews" % hard_skill_id,
                              auth="reviewer",
                              reviewer_id=self.reviewer_id,
                              value="skill_level",
                              description="string"
                              )
        self.pass_invalid_ref("/group_members/%s/reviews" % hard_skill_id,
                              auth="reviewer",
                              reviewer_id=self.reviewer_id,
                              value="skill_level",
                              description="string"
                              )
        self.pass_invalid_ref("/tests/%s/reviews" % hard_skill_id,
                              auth="reviewer",
                              reviewer_id=self.reviewer_id,
                              value="skill_level",
                              description="string"
                              )
        self.pass_invalid_ref("/persons/%s/hard_skills/%s/reviews" % (p_id, p_id),
                              auth="reviewer",
                              reviewer_id=self.reviewer_id,
                              value="skill_level",
                              description="string"
                              )
        self.pass_invalid_ref("/persons/%s/soft_skills/%s/reviews" % (p_id, p_id),
                              auth="reviewer",
                              reviewer_id=self.reviewer_id,
                              value="skill_level",
                              description="string"
                              )

    def test_post_survey(self):
        struct = hm.prepare_org_structure()
        post_data = {"description": "some_desc",
                     "options": {"1": "opt1", "2": "opt2"}}
        survey_id = self.post_item("/groups/%s/surveys" % struct["group_1"]["id"], post_data)
        survey = model.Survey(_id=survey_id)
        survey.refresh_from_db()
        self.assertEqual("some_desc", survey.description, "must save correct description")
        self.assertEqual({"1": "opt1", "2": "opt2"}, survey.survey_options, "must save correct options")
        self.assertEqual({"1": 0, "2": 0}, survey.survey_result, "must save correct initial result")

    def test_delete_survey(self):
        struct = hm.prepare_org_structure()
        survey = model.Survey()
        survey.group_id = struct["group_1"]["id"]
        survey.description = "some descr"
        survey.survey_options = {"1": "opt1"}
        survey.save()
        survey.refresh_from_db()
        self.delete_item("/surveys/%s" % survey.pk)
        with self.assertRaises(DoesNotExist):
            survey.refresh_from_db()

    def test_get_survey(self):
        struct = hm.prepare_org_structure()
        survey = model.Survey()
        survey.group_id = struct["group_1"]["id"]
        survey.description = "some descr"
        survey.survey_options = {"1": "opt1",
                                 "2": "opt2"}
        survey.survey_result = {"1": 6,
                                "2": 4}
        survey.save()
        survey_2 = model.Survey()
        survey_2.group_id = struct["group_2"]["id"]
        survey_2.description = "some descr2"
        survey_2.survey_options = {"3": "opt3",
                                   "5": "opt5"}
        survey_2.survey_result = {"3": 2,
                                  "5": 3}
        survey_2.save()
        survey_ref_data = {
            "group_id": struct["group_1"]["id"],
            "id": str(survey.pk),
            "options": {"1": "opt1",
                        "2": "opt2"},
            "results": {"1": 6, "2": 4}}
        survey_2_ref_data = {
            "group_id": struct["group_2"]["id"],
            "id": str(survey_2.pk),
            "options": {"3": "opt3",
                        "5": "opt5"},
            "results": {"3": 2, "5": 3}}
        survey_list = self.get_item_list("/surveys")
        self.assertEqual(2, len(survey_list))
        self.assertIn(survey_ref_data, survey_list, "must return correct survey data")
        self.assertIn(survey_2_ref_data, survey_list, "must return correct survey data")
        survey_list = self.get_item_list("/surveys?group_id=%s" % struct["group_2"]["id"])
        self.assertEqual(1, len(survey_list))
        self.assertIn(survey_2_ref_data, survey_list, "must return correct survey data")
        self.assertNotIn(survey_ref_data, survey_list, "must return correct survey data")

    def test_post_survey_responce(self):
        struct = hm.prepare_org_structure()
        survey = model.Survey()
        survey.group_id = struct["group_1"]["id"]
        survey.description = "some descr"
        survey.survey_options = {"1": "opt1",
                                 "2": "opt2"}
        survey.survey_result = {"1": 6,
                                "2": 4}
        survey.save()
        group_member = model.GroupMember()
        group_member.group_id = struct["group_1"]["id"]
        group_member.person_id = struct["person_1"]["id"]
        group_member.role_id = struct["group_role_1"]["id"]
        group_member.save()
        post_data = {"person_id": struct["person_1"]["id"],
                     "chosen_option": "1"}
        response_id = self.post_item("/surveys/%s" % survey.pk, post_data)
        response = model.SurveyResponse(_id=response_id)
        response.refresh_from_db()
        survey.refresh_from_db()
        self.assertEqual(struct["person_1"]["id"], str(response.person_id.pk))
        self.assertEqual("1", str(response.chosen_option))
        self.assertEqual(7, survey.survey_result["1"], "must update survey result")

    def test_post_survey_invalid_responce(self):
        struct = hm.prepare_org_structure()
        survey = model.Survey()
        survey.group_id = struct["group_1"]["id"]
        survey.description = "some descr"
        survey.survey_options = {"1": "opt1",
                                 "2": "opt2"}
        survey.survey_result = {"1": 6,
                                "2": 4}
        survey.save()
        group_member = model.GroupMember()
        group_member.group_id = struct["group_1"]["id"]
        group_member.person_id = struct["person_1"]["id"]
        group_member.role_id = struct["group_role_1"]["id"]
        group_member.save()
        post_data = {"person_id": struct["person_2"]["id"],
                     "chosen_option": "1"}
        resp = hm.try_post_item(self, self.api_URL + "/surveys/%s" % survey.pk,
                                post_data, self.admin_header)
        self.assertEqual(ERR.AUTH, resp["result"])
        post_data = {"person_id": struct["person_1"]["id"],
                     "chosen_option": "9"}
        resp = hm.try_post_item(self, self.api_URL + "/surveys/%s" % survey.pk,
                                post_data, self.admin_header)
        self.assertEqual(ERR.INPUT, resp["result"])


    def test_get_version(self):
        service = model.Service("0.2", "3")
        service.save()
        data = requests.get(self.api_URL + "/version").json()
        self.assertEqual("0.2", data["db_version"], "must return correct db version")
        self.assertEqual("3", data["api_version"], "must return correct api version")
        pass

    def test_put_photo(self):
        person = model.Person(
            "Леонид",
            "Александрович",
            "Дунаев",
            datetime.date(1986, 5, 1),
            "78005553535")
        person.save()
        with open(r"../database/img/Leni4.jpg", mode='rb') as file:
            file_content = file.read()
        headers = {"Content-Type" : "image/jpeg"}
        headers.update(self.admin_header)
        resp = requests.put(self.api_URL + "/persons/%s/photo" % str(person.pk),
                     headers= headers,
                     data= file_content)
        self.assertEqual(200, resp.status_code, "status code must be 200")
        person.refresh_from_db()
        self.assertEqual(file_content, bytes(person.photo), "file must be saved to db")
        person.delete()
        resp = requests.put(self.api_URL + "/persons/%s/photo" % str(person.pk),
                            headers=headers,
                            data=file_content)
        self.assertEqual(200, resp.status_code, "status code must be 200")
        self.assertEqual(ERR.NO_DATA, resp.json()["result"], "must return ERR.NO_DATA if no person exist")
        headers["Content-Type"] = "some other type"
        resp = requests.put(self.api_URL + "/persons/%s/photo" % str(person.pk),
                            headers=headers,
                            data=file_content)
        self.assertEqual(ERR.INPUT, resp.json()["result"], "must return ERR.INPUT for wrong content type")


    def test_get_photo(self):
        with open(r"../database/img/Leni4.jpg", mode='rb') as file:
            file_content = file.read()
        bin_data = Binary(file_content)
        person = model.Person(
                    "Леонид",
                    "Александрович",
                    "Дунаев",
                    datetime.date(1986, 5, 1),
                    "78005553535",
                    bin_data)
        person.save()
        resp = requests.get(self.api_URL + "/persons/%s/photo" % str(person.pk))
        self.assertEqual( 200, resp.status_code,"response code must be 200")
        self.assertEqual("image/jpeg",resp.headers["Content-Type"],  "must return correct Content-Type")
        self.assertEqual("attachment; filename=%s.jpg" % str(person.pk),
                         resp.headers["Content-Disposition"],
                         "must return correct Content-Disposition")
        self.assertEqual(file_content, resp.content, "must return correct image")
        person.delete()
        resp = requests.get(self.api_URL + "/persons/%s/photo" % str(person.pk))
        self.assertEqual( 200, resp.status_code,"response code must be 200")
        self.assertEqual( ERR.NO_DATA, resp.json()["result"], "must return ERR.NO_DATA when no person exists")
        person = model.Person(
            "Иван",
            "Иванович",
            "Петров",
            datetime.date(1986, 5, 1),
            "78005553565")
        person.save()
        resp = requests.get(self.api_URL + "/persons/%s/photo" % str(person.pk))
        self.assertEqual(204, resp.status_code,"response code must be 204 when no photo present")

    def pass_invalid_ref(self, url_post, auth="admin", **kwargs):
        data = self.generate_doc(kwargs.items())
        if auth == "reviewer":
            auth_header = self.reviewer_header
        else:
            auth_header = self.admin_header
        resp = requests.post(url=self.api_URL + url_post, json=data, headers=auth_header)
        self.assertEqual(200, resp.status_code, "post response status code must be 200")
        resp_json = resp.json()
        self.assertEqual(ERR.NO_DATA, resp_json["result"], "post result must be ERR.NO_DATA in " +
                         url_post + " " + str(data))

    def post_duplicate_item(self, url_post, url_get_list, **kwargs):
        data = self.generate_doc(kwargs.items())
        self.post_item(url_post, data)
        resp = requests.post(url=self.api_URL + url_post, json=data, headers=self.admin_header)
        self.assertEqual(200, resp.status_code, "post response status code must be 200")
        resp_json = resp.json()
        self.assertEqual(ERR.DB, resp_json["result"], "duplicate post result must be ERR.DB")
        self.assertNotIn("id", resp_json, "returned id must be None")
        item_list = self.get_item_list(url_get_list)
        self.assertEqual(1, len(item_list))

    def get_item_list(self, url):
        resp = requests.get(self.api_URL + url, headers=self.admin_header)
        self.assertEqual(200, resp.status_code, "get response status code must be 200")
        resp_json = resp.json()
        if "error_message" in resp_json: print(resp_json["error_message"])
        self.assertEqual(ERR.OK, resp_json["result"], "result must be ERR.OK")
        return resp_json["list"]

    def get_item_data(self, url):
        resp = requests.get(self.api_URL + url, headers=self.admin_header)
        self.assertEqual(200, resp.status_code, "get response status code must be 200")
        resp_json = resp.json()
        if "error_message" in resp_json: print(resp_json["error_message"])
        self.assertEqual(ERR.OK, resp_json["result"], "result must be ERR.OK")
        return resp_json["data"]

    def post_item(self, url, data, auth="admin"):
        if auth == "reviewer":
            auth_header = self.reviewer_header
        elif auth == "reviewer2":
            auth_header = self.reviewer_header2
        else:
            auth_header = self.admin_header
        resp = requests.post(url=self.api_URL + url, json=data, headers=auth_header)
        self.assertEqual(200, resp.status_code, "post response status code must be 200")
        resp_json = resp.json()
        self.assertEqual(ERR.OK, resp_json["result"], "post result must be ERR.OK")
        if "error_message" in resp_json: print(resp_json["error_message"])
        self.assertTrue(resp_json["id"], "returned id must be not None")
        return resp_json["id"]

    def post_modify_item(self, url, data):
        resp = requests.post(url=self.api_URL + url, json=data, headers=self.admin_header)
        self.assertEqual(200, resp.status_code, "post response status code must be 200")
        resp_json = resp.json()
        self.assertEqual(ERR.OK, resp_json["result"], "post result must be ERR.OK")
        if "error_message" in resp_json: print(resp_json["error_message"])

    def delete_item(self, url, auth="admin"):
        if auth == "reviewer":
            auth_header = self.reviewer_header
        elif auth == "reviewer2":
            auth_header = self.reviewer_header2
        else:
            auth_header = self.admin_header
        resp = requests.delete(url=self.api_URL + url, headers=auth_header)
        self.assertEqual(200, resp.status_code, "delete response status code must be 200")
        resp_json = resp.json()
        if "error_message" in resp_json: print(resp_json["error_message"])
        self.assertEqual(ERR.OK, resp_json["result"], "result must be ERR.OK")

    def patch_item(self, url, data=None):
        resp = requests.patch(url=self.api_URL + url, json=data, headers=self.admin_header)
        self.assertEqual(200, resp.status_code, "patch response status code must be 200")
        resp_json = resp.json()
        if "error_message" in resp_json: print(resp_json["error_message"])
        self.assertEqual(ERR.OK, resp_json["result"], "result must be ERR.OK")


if __name__ == "__main__":
    print("test_api argv: " + str(sys.argv))
    if "--test" in sys.argv:
        sys.argv.remove("--test")
    unittest.main(verbosity=1)
