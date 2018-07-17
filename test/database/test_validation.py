import unittest
import settings.mongo
import context 
import pymongo
import datetime
import random
import importlib
from pymodm import MongoModel
from pymodm.connection import connect, _get_db
from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError
import sys

connect(settings.mongo.conn_string + "/" + settings.mongo.db_name,
            alias = "reviewer")

import sample_data as sd
from src.data.reviewer_model import (Department,
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
                                     RoleInGroup,
                                     RoleInGroupReview,
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

test_version = "test_0.3"

def prepare_db():
    try:
        connect(settings.mongo.conn_string + "/" + settings.mongo.db_name,
            alias = "reviewer")
        revDb = _get_db("reviewer")
        service = revDb["service"].find_one()
        if service is None:
            current_version = None
        else:
            current_version = service["version"]
        #TODO найти способ очищения только данных, либо создания заново
        #индексов путём инициализации классов модели
        if current_version != test_version:
            print("versions differ, refilling DB")
            colList = revDb.list_collection_names()
            for col in colList:
                revDb.drop_collection(col)
                print ("dropped collection " + col)
        if current_version != test_version: fill_db()
        else: print("same version, skipping DB refill")
        init_model()
    except Exception as ex:
        print(ex)
        
def fill_db():
    #Версия используется для ускорения тестирования:
    #Данные в БД перезаписываются только при несовпадении версии 
    service = Service("test_0.3")
    service.save()
    for key, item in sd.persons.items():
        item.save()
    for key, item in sd.organizations.items():
        item.save()    
    for key, item in sd.departments.items():
        item.save()
    for key, item in sd.hard_skills.items():
        item.save()
    for key, item in sd.person_hs.items():
        item.save()
    for key, item in sd.soft_skills.items():
        item.save()
    for key, item in sd.person_ss.items():
        item.save()
    for key, item in sd.tutor_roles.items():
        item.save()
    for key, item in sd.student_roles.items():
        item.save()
    for key, item in sd.group_roles.items():
        item.save()
    for key, item in sd.group_permissions.items():
        item.save()
    for key, item in sd.groups.items():
        item.save()
    for key, item in sd.roles_in_groups.items():
        item.save()   
    for key, item in sd.group_tests.items():
        item.save()    
    for key, item in sd.test_results.items():
        item.save()
    for key, item in sd.ss_reviews.items():
        item.save()
    for key, item in sd.hs_reviews.items():
        item.save()
    for key, item in sd.sr_reviews.items():
        item.save()
    for key, item in sd.tr_reviews.items():
        item.save()
    for key, item in sd.group_reviews.items():
        item.save()
    for key, item in sd.role_in_group_reviews.items():
        item.save()
    for key, item in sd.group_test_reviews.items():
        item.save()
    for key, item in sd.surveys.items():
        item.save()

class TestValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        
        prepare_db()
        
        
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
    
        
    def tearDown(self):
        pass
        #clear_db()
        

if __name__ == "__main__":
    
    unittest.main(verbosity = 1)
            