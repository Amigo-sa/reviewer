from pymodm import MongoModel, fields, ReferenceField
from pymongo.write_concern import WriteConcern

class Service(MongoModel):
    version = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True

class Person(MongoModel):
    first_name = fields.CharField()
    middle_name = fields.CharField()
    surname = fields.CharField()
    birth_date  = fields.DateTimeField()
    phone_no = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class Organization(MongoModel):
    name = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
    
class Department(MongoModel):
    name = fields.CharField()
    organization_id = fields.ReferenceField(Organization, on_delete = ReferenceField.DENY)
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class HardSkill(MongoModel):
    name = fields.CharField()
        
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class PersonHS(MongoModel):
    person_id = fields.ReferenceField(Person, on_delete = ReferenceField.DENY)
    hs_id = fields.ReferenceField(HardSkill, on_delete = ReferenceField.DENY)
    level = fields.FloatField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class SoftSkill(MongoModel):
    name = fields.CharField()
        
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class PersonSS(MongoModel):
    person_id = fields.ReferenceField(Person, on_delete = ReferenceField.DENY)
    ss_id = fields.ReferenceField(SoftSkill, on_delete = ReferenceField.DENY)
    level = fields.FloatField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class TutorRole(MongoModel):
    person_id = fields.ReferenceField(Person, on_delete = ReferenceField.DENY)
    department_id = fields.ReferenceField(Department, on_delete = ReferenceField.DENY)
    discipline = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True    
        
class StudentRole(MongoModel):
    person_id = fields.ReferenceField(Person, on_delete = ReferenceField.DENY)
    department_id = fields.ReferenceField(Department, on_delete = ReferenceField.DENY)
    description = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
     
class GroupRole(MongoModel):
    name = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
    
class Group(MongoModel):
    department_id = fields.ReferenceField(Department, on_delete = ReferenceField.DENY)
    name = fields.CharField()
    #role_list = fields.ListField(field = GroupRole)
        
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class RoleInGroup(MongoModel):
    person_id = fields.ReferenceField(Person, on_delete = ReferenceField.DENY)
    group_id = fields.ReferenceField(Group, on_delete = ReferenceField.DENY)
    role_id = fields.ReferenceField(GroupRole, on_delete = ReferenceField.DENY)
    permissions = fields.ListField(field = fields.CharField())
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class GroupTest(MongoModel):
    group_id = fields.ReferenceField(Group, on_delete = ReferenceField.DENY)
    name = fields.CharField()
    info = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class TestResult(MongoModel):
    test_id = fields.ReferenceField(GroupTest, on_delete = ReferenceField.DENY)
    person_id = fields.ReferenceField(Person, on_delete = ReferenceField.DENY)
    result_data = fields.ListField(field = fields.CharField())
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class SSReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete = ReferenceField.DENY)
    subject_id = fields.ReferenceField(PersonSS, on_delete = ReferenceField.DENY)
    value = fields.FloatField()
    description = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class HSReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete = ReferenceField.DENY)
    subject_id = fields.ReferenceField(PersonHS, on_delete = ReferenceField.DENY)
    value = fields.FloatField()
    description = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class SRReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete = ReferenceField.DENY)
    subject_id = fields.ReferenceField(StudentRole, on_delete = ReferenceField.DENY)
    value = fields.FloatField()
    description = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class TRReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete = ReferenceField.DENY)
    subject_id = fields.ReferenceField(TutorRole, on_delete = ReferenceField.DENY)
    value = fields.FloatField()
    description = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
    
class GroupReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete = ReferenceField.DENY)
    subject_id = fields.ReferenceField(Group, on_delete = ReferenceField.DENY)
    value = fields.FloatField()
    description = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class RoleInGroupReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete = ReferenceField.DENY)
    subject_id = fields.ReferenceField(RoleInGroup, on_delete = ReferenceField.DENY)
    value = fields.FloatField()
    description = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True

class GroupTestReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete = ReferenceField.DENY)
    subject_id = fields.ReferenceField(GroupTest, on_delete = ReferenceField.DENY)
    value = fields.FloatField()
    description = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True

class Survey(MongoModel):
    group_id = fields.ReferenceField(Group, on_delete = ReferenceField.DENY)
    description = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        