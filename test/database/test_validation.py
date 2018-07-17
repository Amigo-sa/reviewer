import unittest
import settings.mongo
import context 
import datetime
from pymodm import MongoModel
from pymodm.connection import connect, _get_db
from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError

connect(settings.mongo.conn_string + "/" + settings.mongo.db_name,
            alias = "reviewer")

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
        #TODO: найти способ очищения только данных, либо создания заново
        #индексов путём инициализации классов модели
        if current_version != test_version:
            print("versions differ, refilling DB")
            colList = revDb.list_collection_names()
            for col in colList:
                revDb.drop_collection(col)
                print ("dropped collection " + col)
            import sample_data
            sample_data.fill_db()
            #FIXME: здесь должны заново создаваться индексы
        else: print("same version, skipping DB refill")
        init_model()
    except Exception as ex:
        print(ex)
        
class TestValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        
        prepare_db()
        
    #Role in group tests    
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
            