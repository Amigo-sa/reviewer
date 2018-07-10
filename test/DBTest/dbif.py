from pymodm.connection import connect
from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
import settings.mongo as mongosettings
import datetime

connect(mongosettings.connString+"/reviewer", alias = "rev")

class Person(MongoModel):
    first_name = fields.CharField()
    middle_name = fields.CharField()
    surname = fields.CharField()
    birth_date  = fields.DateTimeField()
    phone_no = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "rev"
        final = True
        
class Organization(MongoModel):
    name = fields.CharField()
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "rev"
        final = True
        
        
def add_person(first_name, middle_name, surname, birth_date, phone_no):
    person = Person(first_name, middle_name, surname, birth_date, phone_no)
    try:
        person.save()
    except Exception as ex:
        print(ex)
        return None
    return person

def add_organization(name):
    organization = Organization(name)
    try:
        organization.save()
    except Exception as ex:
        print(ex)
        return None
    return organization


org1 = add_organization("МЭИ")
person1 = add_person(
        "Иван",
        "Иванович",
        "Иванов",
        datetime.date(2000,1,1),
        "222322")

print(person1.is_valid())

