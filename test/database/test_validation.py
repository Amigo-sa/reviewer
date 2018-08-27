# -*- coding: utf-8 -*-
import context
import unittest
import requests
import os, sys
from pymodm.connection import _get_db
parentPath = os.path.abspath("..//..//test")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
import api.api_helper_methods as hm

from node.settings import constants
import node.settings.errors as ERR
from node.node_server import start_server
from threading import Thread
import random
import datetime
from time import sleep
import re
from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError


from data.reviewer_model import (Department,
                                 Group,
                                 GroupPermission,
                                 GroupReview,
                                 GroupRole,
                                 GroupTest,
                                 GroupTestReview,
                                 HSReview,
                                 HardSkill,
                                 Organization,
                                 Person,
                                 PersonHS,
                                 PersonSS,
                                 GroupMember,
                                 GroupMemberReview,
                                 Specialization,
                                 SSReview,
                                 Service,
                                 SoftSkill,
                                 PersonSpecialization,
                                 Survey,
                                 SurveyResponse,
                                 SpecializationReview,
                                 TestResult,
                                 get_dependent_list,
                                 init_model)

test_version = "0.4"


class TestValidation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        hm.wipe_db(constants.db_name)

    @classmethod
    def clear_collection(cls, collection_class):
        for doc in collection_class.objects.all():
            doc.delete()

    def test_group_member_validation(self):
        person = Person(
                        "Леонид",
                        "Александрович",
                        "Дунаев",
                        datetime.date(1986, 5, 1),
                        "88005553535")
        person.save()
        organization = Organization("МЭИ")
        organization.save()
        department = Department("Кафедра ИИТ", organization)
        department.save()
        member_role = GroupRole("member")
        member_role.save()
        read_permission = GroupPermission("read_info")
        read_permission.save()
        group = Group(department, "А-4-03", [member_role])
        group.save()
        # add person to group without group role and permissions
        group_member = GroupMember()
        group_member.group_id = group
        group_member.person_id = person
        group_member.role_id = None
        group_member.permissions = []
        gm_id = group_member.save()
        # verify group member added
        group_member.refresh_from_db()
        gm_data = group_member.__dict__["_data"]
        ref_gm_data = {
            "_id": group_member.pk,
            "person_id": person.pk,
            "group_id": group.pk,
            "role_id": None,
            "permissions": [],
            "is_active": True}
        self.assertDictEqual(ref_gm_data, gm_data)
        # add permission to group member
        group_member.permissions.append(read_permission)
        group_member.save()
        # verify added permission
        group_member.refresh_from_db()
        gm_data = group_member.__dict__["_data"]
        ref_gm_data.update({"permissions" : [read_permission.pk]})
        self.assertDictEqual(ref_gm_data, gm_data)
        # setting None role must fail
        with self.assertRaises(ValidationError):
            group_member.set_role(None)
        # add group role
        group_member.set_role(member_role)
        # verify added role
        group_member.refresh_from_db()
        gm_data = group_member.__dict__["_data"]
        ref_gm_data.update({"role_id": member_role.pk})
        self.assertDictEqual(ref_gm_data, gm_data)
        # setting role when already set must fail
        with self.assertRaises(ValidationError):
            group_member.set_role(member_role)
        # set member as inactive
        group_member.is_active = False
        group_member.save()
        # verify
        group_member.refresh_from_db()
        gm_data = group_member.__dict__["_data"]
        ref_gm_data.update({"is_active": False})
        self.assertDictEqual(ref_gm_data, gm_data)
        # try add duplicate group member
        with self.assertRaises(DuplicateKeyError):
            dup_group_member = GroupMember()
            dup_group_member.group_id = group
            dup_group_member.person_id = person
            dup_group_member.set_role(member_role)
            dup_group_member.save()
        # add second permission
        write_permission = GroupPermission("write_info")
        write_permission.save()
        group_member.refresh_from_db()
        group_member.permissions.append(write_permission)
        group_member.save()
        # verify
        group_member.refresh_from_db()
        gm_data = group_member.__dict__["_data"]
        ref_gm_data.update({"permissions" : [read_permission.pk, write_permission.pk]})
        self.assertDictEqual(ref_gm_data, gm_data)
        # try add invalid role

        inv_role = GroupRole("god-emperor")
        inv_role.save()
        inv_group_member = GroupMember(person, group, None, [])
        with self.assertRaises(ValidationError):
            inv_group_member.set_role(inv_role)
            inv_group_member.save()
        # try add duplicate permissions
        with self.assertRaises(ValidationError):
            group_member.permissions.append(read_permission)
            group_member.save()

    def test_survey_response_validation(self):
        struct = hm.prepare_org_structure()
        survey = Survey()
        survey.group_id = struct["group_1"]["id"]
        survey.description = "some descr"
        survey.survey_options = {"1": "opt1",
                                 "2": "opt2"}
        survey.survey_result = {"1": 6,
                                "2": 4}
        survey.save()
        response = SurveyResponse()
        response.person_id = struct["person_1"]["id"]
        response.chosen_option = "7"
        with self.assertRaises(ValidationError):
            response.save()

if __name__ == "__main__":
    unittest.main(verbosity = 1)
