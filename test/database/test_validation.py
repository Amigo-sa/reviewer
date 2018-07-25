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


class TestValidation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_URL = constants.core_server_url
        cls.gen_doc_ctr = 0
        cls.clear_collection(Person)
        cls.clear_collection(Organization)
        cls.clear_collection(GroupPermission)
        cls.clear_collection(GroupRole)
        cls.clear_collection(HardSkill)
        cls.clear_collection(SoftSkill)

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
        group_permission = GroupPermission("read_info")
        group_permission.save()
        group = Group(department, "А-4-03", [member_role])
        group.save()
        group_member = GroupMember()
        group_member.group_id = group
        group_member.person_id = person
        group_member.save()

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
    
            