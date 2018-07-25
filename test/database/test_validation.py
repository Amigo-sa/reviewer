# -*- coding: utf-8 -*-
import context
import unittest
import requests
from pymodm.connection import _get_db

from node.settings import constants
import node.settings.errors as ERR
from node.node_server import start_server
from threading import Thread
import random
import datetime
from time import sleep
import re
from pymodm.errors import ValidationError


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
                                 SRReview,
                                 SSReview,
                                 Service,
                                 SoftSkill,
                                 StudentRole,
                                 Survey,
                                 TRReview,
                                 TestResult,
                                 TutorRole,
                                 get_dependent_list,
                                 init_model)

test_version = "0.3"

def clear_db():
    print("clearing db...")
    revDb = _get_db("reviewer")
    colList = revDb.list_collection_names()
    for col in colList:
        revDb[col].delete_many({})
    print("done")

class TestValidation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        clear_db()

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

"""
    # Role in group tests

    def test_vaild_role_in_group(self):
        valid_role = RoleInGroup(
                    Person.objects.get({"surname" : "Дунаев"}),
                    Group.objects.get({"name" : "Клуб анонимных ардуинщиков"}),
                    GroupRole.objects.get({"name" : "admin"}),
                    [GroupPermission.objects.get({"name" : "read_info"})])
        valid_role.save()
        self.assertIsNotNone(RoleInGroup.objects.get({"_id" : valid_role.pk}))
        valid_role.delete()
        
    def test_invaild_role_in_group(self):
        with self.assertRaises(ValidationError):
            invalid_role = RoleInGroup(
                        Person.objects.get({"surname" : "Дунаев"}),
                        Group.objects.get({"name" : "Клуб анонимных ардуинщиков"}),
                        GroupRole.objects.get({"name" : "monitor"}),
                        [GroupPermission.objects.get({"name" : "read_info"})])
            invalid_role.save()
            if invalid_role.pk is not None:
                invalid_role.delete()
    
    def test_duplicate_role_in_group(self):
        with self.assertRaises(DuplicateKeyError):
            duplicate_role = RoleInGroup(
                        Person.objects.get({"surname" : "Дунаев"}),
                        Group.objects.get({"name" : "Клуб анонимных ардуинщиков"}),
                        GroupRole.objects.get({"name" : "member"}),
                        [GroupPermission.objects.get({"name" : "read_info"})])
            duplicate_role.save()
            if duplicate_role.pk is not None:
                duplicate_role.delete()
    
    def test_role_with_no_permissions(self):
        with self.assertRaises(ValidationError):
            role_without_permissions = RoleInGroup(
                        Person.objects.get({"surname" : "Дунаев"}),
                        Group.objects.get({"name" : "Клуб анонимных ардуинщиков"}),
                        GroupRole.objects.get({"name" : "admin"}),
                        [])
            role_without_permissions.save()
            if role_without_permissions.pk is not None:
                role_without_permissions.delete()
    
    def test_duplicate_permissions(self):
        
        role_in_group = RoleInGroup.objects.get(
                {
                        "person_id" : Person.objects.get({"surname" : "Дунаев"}).pk,
                        "group_id" : Group.objects.get({"name" : "А-4-03"}).pk
                 })
        duplicate_permission = GroupPermission.objects.get({"name" : "read_info"})
        role_in_group.permissions.append(duplicate_permission)
        role_in_group.refresh_from_db()
        resulting_permissions = role_in_group.permissions
        perm_count = 0
        for item in resulting_permissions:
            if item.name == "read_info": 
                perm_count+=1
        self.assertEqual(perm_count, 1)
    
    def tearDown(self):
        pass
"""

if __name__ == "__main__":
    unittest.main(verbosity = 1)
    
            