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
    organization_id = fields.ReferenceField(Organization, on_delete = ReferenceField.CASCADE)
    
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
    person_id = fields.ReferenceField(Person, on_delete = ReferenceField.CASCADE)
    hs_id = fields.ReferenceField(HardSkill, on_delete = ReferenceField.CASCADE)
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
    person_id = fields.ReferenceField(Person, on_delete = ReferenceField.CASCADE)
    ss_id = fields.ReferenceField(SoftSkill, on_delete = ReferenceField.CASCADE)
    level = fields.FloatField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class TutorRole(MongoModel):
    person_id = fields.ReferenceField(Person, on_delete = ReferenceField.CASCADE)
    department_id = fields.ReferenceField(Department, on_delete = ReferenceField.CASCADE)
    discipline = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True    
        
class StudentRole(MongoModel):
    person_id = fields.ReferenceField(Person, on_delete = ReferenceField.CASCADE)
    department_id = fields.ReferenceField(Department, on_delete = ReferenceField.CASCADE)
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
        
class GroupPermission(MongoModel):
    name = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
       
class Group(MongoModel):
    department_id = fields.ReferenceField(Department, on_delete = ReferenceField.CASCADE)
    name = fields.CharField()
    role_list = fields.ListField(field = 
                fields.ReferenceField(GroupRole, on_delete = ReferenceField.CASCADE))
        
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class RoleInGroup(MongoModel):
    person_id = fields.ReferenceField(Person, on_delete = ReferenceField.CASCADE)
    group_id = fields.ReferenceField(Group, on_delete = ReferenceField.CASCADE)
    role_id = fields.ReferenceField(GroupRole, on_delete = ReferenceField.CASCADE)
    permissions = fields.ListField(field = 
                fields.ReferenceField(GroupPermission, on_delete = ReferenceField.CASCADE))
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class GroupTest(MongoModel):
    group_id = fields.ReferenceField(Group, on_delete = ReferenceField.CASCADE)
    name = fields.CharField()
    info = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class TestResult(MongoModel):
    test_id = fields.ReferenceField(GroupTest, on_delete = ReferenceField.CASCADE)
    person_id = fields.ReferenceField(Person, on_delete = ReferenceField.CASCADE)
    result_data = fields.ListField(field = fields.CharField())
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class SSReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete = ReferenceField.CASCADE)
    subject_id = fields.ReferenceField(PersonSS, on_delete = ReferenceField.CASCADE)
    value = fields.FloatField()
    description = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class HSReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete = ReferenceField.CASCADE)
    subject_id = fields.ReferenceField(PersonHS, on_delete = ReferenceField.CASCADE)
    value = fields.FloatField()
    description = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class SRReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete = ReferenceField.CASCADE)
    subject_id = fields.ReferenceField(StudentRole, on_delete = ReferenceField.CASCADE)
    value = fields.FloatField()
    description = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class TRReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete = ReferenceField.CASCADE)
    subject_id = fields.ReferenceField(TutorRole, on_delete = ReferenceField.CASCADE)
    value = fields.FloatField()
    description = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
    
class GroupReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete = ReferenceField.CASCADE)
    subject_id = fields.ReferenceField(Group, on_delete = ReferenceField.CASCADE)
    value = fields.FloatField()
    description = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
class RoleInGroupReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete = ReferenceField.CASCADE)
    subject_id = fields.ReferenceField(RoleInGroup, on_delete = ReferenceField.CASCADE)
    value = fields.FloatField()
    description = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True

class GroupTestReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete = ReferenceField.CASCADE)
    subject_id = fields.ReferenceField(GroupTest, on_delete = ReferenceField.CASCADE)
    value = fields.FloatField()
    description = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True

class Survey(MongoModel):
    group_id = fields.ReferenceField(Group, on_delete = ReferenceField.CASCADE)
    description = fields.CharField()
    survey_data = fields.DictField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        
def get_dependent_list(doc, dep_id_list):
    current_del_rules = doc._mongometa.delete_rules
    dep_id_list.append(doc)
    for item, rule in current_del_rules.items():
        #if rule == ReferenceField.DENY:
            related_model, related_field = item
            dependent_docs = related_model.objects.raw({related_field : doc.pk})
            for dep in dependent_docs:
                if dep not in dep_id_list:
                    get_dependent_list(dep, dep_id_list)

        