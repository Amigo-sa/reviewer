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