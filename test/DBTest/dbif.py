from pymodm.connection import connect
from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
import settings.mongo as mongosettings
import datetime

connect(mongosettings.connString+"/reviewer", alias = "rev")

class Person(MongoModel):
    FirstName = fields.CharField()
    MiddleName = fields.CharField()
    Surname = fields.CharField()
    BirthDate  = fields.DateTimeField()
    PhoneNo = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "rev"
        
class Feature(MongoModel):
    Name = fields.CharField()
    Rate = fields.FloatField()
    PersonId = fields.ReferenceField(Person, on_delete=fields.ReferenceField.DENY)
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "rev"
        
        
def add_person(first_name, middle_name, surname, birth_date, phone_no):
    person = Person(first_name, middle_name, surname, birth_date, phone_no)
    try:
        person.save()
    except Exception as ex:
        return None
    return person

def add_feature(name, rate, person):
    feature = Feature(name, rate, person)
    try:
        feature.save()
    except Exception as ex:
        return None
    return feature
   
person1 = add_person("Ivan", 
                     "Sergeevich", 
                     "Sidorov", 
                     datetime.datetime(2000,1,1), 
                     "322223")
feature1 = add_feature("Laziness", 10.0, person1)



