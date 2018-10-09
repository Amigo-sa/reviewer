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

import data.reviewer_model as model

test_version = "0.4"


class TestValidation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        hm.wipe_db()

    @classmethod
    def clear_collection(cls, collection_class):
        for doc in collection_class.objects.all():
            doc.delete()

    def test_person_rating_calculation(self):
        # prepare
        reviewer_1 = model.Person(phone_no="79001223234")
        reviewer_1.save()
        reviewer_2 = model.Person(phone_no="79001223235")
        reviewer_2.save()
        person = model.Person(
            "Иван",
            "Иванович",
            "Ленин",
            datetime.date(1984, 2, 6),
            "79001002030")
        person.save()
        org = model.Organization("МЭИ")
        org.save()
        dep = model.Department("ИИТ", org.pk)
        dep.save()
        skill_type = model.SkillType("skill_type_1")
        skill_type.save()
        hs = model.HardSkill("hard_skill_1", skill_type.pk)
        hs.save()
        ss = model.SoftSkill("soft_skill_1", skill_type.pk)
        ss.save()
        spec = model.Specialization("Tutor", "TOE")
        spec.save()
        person_spec = model.PersonSpecialization(person.pk, dep.pk, spec.pk, None)
        person_spec.save()
        person_hs = model.PersonHS(person.pk, hs.pk, None)
        person_hs.save()
        person_ss = model.PersonSS(person.pk, ss.pk, None)
        person_ss.save()
        # verify initial values
        person.refresh_from_db()
        self.assertEqual((None,None,None),(person.ss_rating, person.hs_rating, person.spec_rating))
        # post first review on hs
        review = model.HSReview(reviewer_1.pk, person_hs.pk, 30, "some descr")
        review.save()
        person.refresh_from_db()
        self.assertEqual((None, 30, None), (person.ss_rating, person.hs_rating, person.spec_rating))
        # post second review on hs
        review = model.HSReview(reviewer_2.pk, person_hs.pk, 40, "some descr")
        review.save()
        person.refresh_from_db()
        self.assertEqual((None, 35, None), (person.ss_rating, person.hs_rating, person.spec_rating))
        # post first review on ss
        review = model.SSReview(reviewer_1.pk, person_ss.pk, 60, "some descr")
        review.save()
        person.refresh_from_db()
        self.assertEqual((60, 35, None), (person.ss_rating, person.hs_rating, person.spec_rating))
        # post second review on hs
        review = model.SSReview(reviewer_2.pk, person_ss.pk, 90, "some descr")
        review.save()
        person.refresh_from_db()
        self.assertEqual((75, 35, None), (person.ss_rating, person.hs_rating, person.spec_rating))
        # post first review on spec
        review = model.SpecializationReview(reviewer_1.pk, person_spec.pk, 10, "some descr")
        review.save()
        person.refresh_from_db()
        self.assertEqual((75, 35, 10), (person.ss_rating, person.hs_rating, person.spec_rating))
        # post first review on spec
        review = model.SpecializationReview(reviewer_2.pk, person_spec.pk, 0, "some descr")
        review.save()
        person.refresh_from_db()
        self.assertEqual((75, 35, 5), (person.ss_rating, person.hs_rating, person.spec_rating))

    def test_group_member_validation(self):
        person = model.Person(
            "Леонид",
            "Александрович",
            "Дунаев",
            datetime.date(1986, 5, 1),
            "88005553535")
        person.save()
        organization = model.Organization("МЭИ")
        organization.save()
        department = model.Department("Кафедра ИИТ", organization)
        department.save()
        member_role = model.GroupRole("member")
        member_role.save()
        read_permission = model.GroupPermission("read_info")
        read_permission.save()
        group = model.Group(department, "А-4-03", [member_role])
        group.save()
        # add person to group without group role and permissions
        group_member = model.GroupMember()
        group_member.group_id = group
        group_member.person_id = person
        group_member.role_id = None
        group_member.permissions = []
        gm_id = group_member.save()
        # verify group member added
        group_member.refresh_from_db()
        gm_data = get_gm_dict(group_member)
        ref_gm_data = {
            "_id": gm_id.pk,
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
        gm_data = get_gm_dict(group_member)
        ref_gm_data.update({"permissions": [read_permission.pk]})
        self.assertDictEqual(ref_gm_data, gm_data)
        # setting None role must fail
        with self.assertRaises(ValidationError):
            group_member.set_role(None)
        # add group role
        group_member.set_role(member_role)
        # verify added role
        group_member.refresh_from_db()
        gm_data = get_gm_dict(group_member)
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
        gm_data = get_gm_dict(group_member)
        ref_gm_data.update({"is_active": False})
        self.assertDictEqual(ref_gm_data, gm_data)
        # try add duplicate group member
        with self.assertRaises(DuplicateKeyError):
            dup_group_member = model.GroupMember()
            dup_group_member.group_id = group
            dup_group_member.person_id = person
            dup_group_member.set_role(member_role)
            dup_group_member.save()
        # add second permission
        write_permission = model.GroupPermission("write_info")
        write_permission.save()
        group_member.refresh_from_db()
        group_member.permissions.append(write_permission)
        group_member.save()
        # verify
        group_member.refresh_from_db()
        gm_data = get_gm_dict(group_member)
        ref_gm_data.update({"permissions": [read_permission.pk, write_permission.pk]})
        self.assertDictEqual(ref_gm_data, gm_data)
        # try add invalid role

        inv_role = model.GroupRole("god-emperor")
        inv_role.save()
        inv_group_member = model.GroupMember(person, group, None, [])
        with self.assertRaises(ValidationError):
            inv_group_member.set_role(inv_role)
            inv_group_member.save()
        # try add duplicate permissions
        with self.assertRaises(ValidationError):
            group_member.permissions.append(read_permission)
            group_member.save()


def get_gm_dict(group_member):
    gm_data = {
        "_id": group_member.pk,
        "person_id": group_member.person_id.pk,
        "group_id": group_member.group_id.pk,
        "role_id": group_member.role_id.pk if group_member.role_id else None,
        "permissions": [perm.pk for perm in group_member.permissions],
        "is_active": group_member.is_active
    }
    return gm_data

if __name__ == "__main__":
    if __name__ == "__main__":
        print("test_auth argv: " + str(sys.argv))
        if "--test" in sys.argv:
            sys.argv.remove("--test")
    unittest.main(verbosity=1)
