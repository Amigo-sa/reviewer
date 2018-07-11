from pymodm.connection import connect
#from pymongo.write_concern import WriteConcern
#from pymodm import MongoModel, fields, ReferenceField
import settings.mongo as mongosettings
import datetime
import pymongo
import random
from reviewer_model import *    #<- govnocode                       

try:
    revClient = pymongo.MongoClient(mongosettings.conn_string)
    revDb = revClient["reviewer"]
    colList = revDb.list_collection_names()
    for col in colList:
        revDb.drop_collection(col)
        print ("Dropped collection " + col)
    revClient.close()
except Exception as ex:
    print("Failed to drop collections: " + ex)

connect(mongosettings.conn_string + "/" + mongosettings.db_name,
        alias = "reviewer")


print("----Persons:")
persons = {
    "Leni4":
        Person(
        "Леонид",
        "Александрович",
        "Дунаев",
        datetime.date(1986,5,1),
        "88005553535"),
    "Maniac":
        Person(
        "Кирилл",
        "Владимирович",
        "Ярин",
        datetime.date(1986,1,2),
        "79033223232"),
    "Pashka":
        Person(
        "Павел",
        "Борисович",
        "Ерин",
        datetime.date(1986,12,30),
        "78392122221"),
    "Vovka":
        Person(
        "Владимир",
        "Владимирович",
        "Панкин",
        datetime.date(1987,7,6),
        "78398889991"),
     "Bogi":
        Person(
        "Владимир",
        "Андреевич",
        "Богословских",
        datetime.date(1986,4,9),
        "79055533342"),
    "Shatokhin":
        Person(
        "Александр",
        "Алексеевич",
        "Шатохин",
        datetime.date(1900,3,4),
        "79052231123"),
    "Anisimov":
        Person(
        "Анатолий",
        "Степанович",
        "Анисимов",
        datetime.date(1812,6,24),
        "79050100001")
          
}

for key, item in persons.items():
    item.save()
for item in Person.objects.all():
    print(item.surname + " _id:" + str(item.pk))
    
print("----Organizations:")
organizations = {
    "MPEI":
        Organization(
        "МЭИ")
}
for key, item in organizations.items():
    item.save()
for item in Organization.objects.all():
    print(item.name + " _id:" + str(item.pk))
    
print("----Departments:")
departments = {
    "IIT":
        Department(
        "Кафедра ИИТ",
        organizations["MPEI"]),
    "EFIS":
        Department(
        "Кафедра ЭФИС",
        organizations["MPEI"])
}
for key, item in departments.items():
    item.save()
for item in Department.objects.all():
    print(item.name + " _id:" + str(item.pk))

print("----Hard Skills:")
hard_skills = {
    "VFP":
        HardSkill(
                "Visual Fox Pro"),
    "uC":
        HardSkill(
                "C для микроконтроллеров"),
    "digSch":
        HardSkill(
                "Цифровая схемотехника"),
    "litrbol":
        HardSkill(
                "Литрбол"),
    "phoneRepair":
        HardSkill(
                "Ремонт телефонов"),
    "psySupp":
        HardSkill(
                "Психологическое подавление")
}
for key, item in hard_skills.items():
    item.save()
for item in HardSkill.objects.all():
    print(item.name + " _id:" + str(item.pk))        

print("----Person Hard Skills:")
person_hs = {
    "Leni4_VFP":
        PersonHS(
                persons["Leni4"],
                hard_skills["VFP"],
                15.0),
    "Leni4_uC":
        PersonHS(
                persons["Leni4"],
                hard_skills["uC"],
                60.0),
    "Maniac_phoneRepair":
        PersonHS(
                persons["Maniac"],
                hard_skills["phoneRepair"],
                99.0),
    "Shatokhin_uC":
        PersonHS(
                persons["Shatokhin"],
                hard_skills["uC"],
                90.0),
    "Pashka_litrbol":
        PersonHS(
                persons["Pashka"],
                hard_skills["litrbol"],
                100.0),
    "Anisimov_psySupp":
        PersonHS(
                persons["Anisimov"],
                hard_skills["psySupp"],
                95.0),
        }
    
for key, item in person_hs.items():
    item.save()
for item in PersonHS.objects.all():
    print(item.person_id.surname + 
          ", " + 
          item.hs_id.name +
          ", lvl: "+
          str(item.level))        

print("----Soft Skills:")
soft_skills = {
    "Communication":
        SoftSkill(
                "Communication"),
    "Courtesy":
        SoftSkill(
                "Courtesy"),
    "Flexibility":
        SoftSkill(
                "Flexibility"),
    "Integrity":
        SoftSkill(
                "Integrity"),
    "Interpersonal skills":
        SoftSkill(
                "Interpersonal skills"),
    "Positive attitude":
        SoftSkill(
                "Positive attitude")
}
for key, item in soft_skills.items():
    item.save()
for item in SoftSkill.objects.all():
    print(item.name + " _id:" + str(item.pk))              

print("----Person Soft Skills:")
for pers_key, person in persons.items():
    for ss_key, soft_skill in soft_skills.items():
        person_ss = PersonSS(
                person,
                soft_skill,
                random.random() * 100.0
                )
        person_ss.save()

for ss in PersonSS.objects.all():
    print(ss.person_id.surname + 
          " " +
          ss.ss_id.name +
          ": " +
          str(ss.level))


print("----Tutor Roles:")
tutor_roles = {
    "Shatokhin_MCU":
        TutorRole(
                persons["Shatokhin"],
                departments["IIT"],
                "Отжигание на микроконтроллерах семейства 8051"
                ),
    "Anisimov_TOE":
        TutorRole(
                persons["Anisimov"],
                departments["EFIS"],
                "ТОЭ"
                ),
    "Anisimov_rel":
        TutorRole(
                persons["Anisimov"],
                departments["EFIS"],
                "Религиоведенье"
                ),
    "Shatokhin_debug":
        TutorRole(
                persons["Shatokhin"],
                departments["IIT"],
                "Отладка кода, написанного за 20 лет до вашего рождения"
                ),
}
for key, item in tutor_roles.items():
    item.save()
for item in TutorRole.objects.all():
    print("{0} из {2} ведет {1}".format(item.person_id.surname,
                                     item.discipline,
                                     item.department_id.name))              

print("----Student Roles:")
student_roles = {
    "Leni4":
        StudentRole(
                persons["Leni4"],
                departments["IIT"],
                "Староста группы А-4-03"
                ),
    "Pashka":
        StudentRole(
                persons["Pashka"],
                departments["IIT"],
                "Студент группы А-4-03"
                ),
    "Vovka":
        StudentRole(
                persons["Vovka"],
                departments["IIT"],
                "Студент группы А-4-03"
                ),
    "Bogi":
        StudentRole(
                persons["Bogi"],
                departments["IIT"],
                "Студент группы А-4-03"
                ),
}
for key, item in student_roles.items():
    item.save()
for item in StudentRole.objects.all():
    print("{0} - {1}, {2}".format(item.person_id.surname,
                                     item.description,
                                     item.department_id.name))              

print("----Roles for Groups:")
group_roles = {
    "Admin":
        GroupRole(
                "Администратор"
                ),
    "Guest":
        GroupRole(
                "Бесправный"
                ),
    "Member":
        GroupRole(
                "Член"
                )
}
for key, item in group_roles.items():
    item.save()
for item in GroupRole.objects.all():
    print("{0}:_id {1}".format(item.name, str(item.pk)))
    
print("----Groups:")
groups = {
    "Arduino":
        Group(departments["IIT"],
              "Клуб анонимных ардуинщиков"
              #[group_roles["Admin"], group_roles["Member"]]
                )
}
for key, item in groups.items():
    item.save()
for item in Group.objects.all():
    print("{0} при {1}".format(item.name, item.department_id.name))

print("----Roles in Groups:")
roles_in_groups = {
    "Shatokhin_admin_arduino":
        RoleInGroup(persons["Shatokhin"],
                    groups["Arduino"],
                    group_roles["Admin"],
                    ["read", "modify"]),
        "Leni4_member_arduino":
        RoleInGroup(persons["Leni4"],
                    groups["Arduino"],
                    group_roles["Member"],
                    ["read"])
}
    
for key, item in roles_in_groups.items():
    item.save()
for item in RoleInGroup.objects.all():
    print("{0} - {1} группы {2}".format(
            item.person_id.surname, 
            item.role_id.name,
            item.group_id.name))

    
"""
person_ss = {
    "Leni4_VFP":
        PersonHS(
                persons["Leni4"],
                hard_skills["VFP"],
                15.0),
    "Leni4_uC":
        PersonHS(
                persons["Leni4"],
                hard_skills["uC"],
                60.0),
    "Maniac_phoneRepair":
        PersonHS(
                persons["Maniac"],
                hard_skills["phoneRepair"],
                99.0),
    "Shatokhin_uC":
        PersonHS(
                persons["Shatokhin"],
                hard_skills["uC"],
                90.0),
    "Pashka_litrbol":
        PersonHS(
                persons["Pashka"],
                hard_skills["litrbol"],
                100.0),
    "Anisimov_psySupp":
        PersonHS(
                persons["Anisimov"],
                hard_skills["psySupp"],
                95.0),
        }
    
for key, item in person_hs.items():
    item.save()
for key, item in person_hs.items():
    print(key + " saved with _id = " + str(item.pk))       

"""
"""
pers_maniac = Person(
        "Кирилл",
        "Владимирович",
        "Ярин",
        datetime.date(1986,1,2),
        "79033223232")

pers_pashka = Person(
        "Павел",
        "Борисович",
        "Ерин",
        datetime.date(1986,12,30),
        "89020020032")

pers_vovka = Person(
        "Владимир",
        "Владимирович",
        "Панкин",
        datetime.date(1987,7,6),
        "78392122221")

pers_ = Person(
        "Владимир",
        "Владимирович",
        "Панкин",
        datetime.date(1987,7,6),
        "78392122221")

"""
"""
org1 = add_organization("МЭИ")
person1 = add_person(
        "Иван",
        "Иванович",
        "Иванов",
        datetime.date(2000,1,1),
        "222322")

"""
"""
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

"""