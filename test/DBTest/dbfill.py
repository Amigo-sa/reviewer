# -*- coding: utf-8 -*-

import pymongo
import datetime
#import data.sample as dataSample
import settings.mongo as mongosettings

revClient = pymongo.MongoClient(mongosettings.connString)
revDb = revClient["reviewer"]

colList = revDb.list_collection_names()
for col in colList:
    revDb.drop_collection(col)


colPerson = revDb["Person"]
persons = [
        {"Name" : "Гарри"     , "BirthDate" : datetime.datetime(2000,8,8)},
        {"Name" : "Рон"       , "BirthDate" : datetime.datetime(2006,4,2)},
        {"Name" : "Гермиона"  , "BirthDate" : datetime.datetime(2001,8,25)},
        {"Name" : "Гораций"   , "BirthDate" : datetime.datetime(1920,5,1)},
        {"Name" : "Снейп"     , "BirthDate" : datetime.datetime(1943,6,1)},
        {"Name" : "Дамблдор"  , "BirthDate" : datetime.datetime(1932,9,7)}
        ]
personIds = colPerson.insert_many(persons).inserted_ids

colFeature = revDb["Feature"]
features = [
        {"Name" : "Скрытность"     , "Rate" : 7, "PersonId" : personIds[0] },
        {"Name" : "Жадность"       , "Rate" : 4, "PersonId" : personIds[1] },
        {"Name" : "Рыжесть"        , "Rate" : 10,"PersonId" : personIds[1] },
        {"Name" : "Хитрость"       , "Rate" : 9, "PersonId" : personIds[4] },
        {"Name" : "Бородатость"    , "Rate" : 11,"PersonId" : personIds[5] },
        {"Name" : "Мудрость"       , "Rate" : 7, "PersonId" : personIds[5] },
        {"Name" : "Виежливость"    , "Rate" : 8, "PersonId" : personIds[2] }
         ]
featureIds = colFeature.insert_many(features).inserted_ids

colOrganization = revDb["Organization"]
organization = {"Name" : "Хогвартс"}
orgId = colOrganization.insert_one(organization).inserted_id

colUniversity = revDb["University"]
university = {"Name" : "Хогвартс", "OrganizationId" : orgId}
uniId = colUniversity.insert_one(university).inserted_id

colDepartment = revDb["Department"]
departments = [
        {"Name" : "Cлизерин"   , "UniversityId" : uniId },
        {"Name" : "Гриффиндор" , "UniversityId" : uniId },
        {"Name" : "Когтевран"  , "UniversityId" : uniId },
        {"Name" : "Хаффлпафф"  , "UniversityId" : uniId },
         ]
depIds = colDepartment.insert_many(departments).inserted_ids

colStudent = revDb["StudentRole"]
students = [
        {"PersonId" : personIds[0], "DepartmentId" : depIds[1], "Specialization" : "Колдовство"},
        {"PersonId" : personIds[1], "DepartmentId" : depIds[2], "Specialization" : "Алхимия"},
        {"PersonId" : personIds[2], "DepartmentId" : depIds[3], "Specialization" : "История магии"}
           ]
studIds = colStudent.insert_many(students).inserted_ids

colTutor = revDb["TutorRole"]
tutors = [
        {"PersonId" : personIds[3], "DepartmentId" : depIds[0], "Disciplines" : ["Травоведение", "Оккультизм", "Сопромат"]},
        {"PersonId" : personIds[4], "DepartmentId" : depIds[1], "Disciplines" : ["Светлая магия", "Спортивное ориентирование"]},
        {"PersonId" : personIds[5], "DepartmentId" : depIds[3], "Disciplines" : ["Литература"]},
        {"PersonId" : personIds[0], "DepartmentId" : depIds[2], "Disciplines" : ["Защита от темных искусств"]}
           ]
tutIds = colTutor.insert_many(tutors).inserted_ids

colGroup = revDb["Group"] 
groups = [
        {"Name" : "Клуб анонимных алкоголиков", "RoleList" : [studIds[0], studIds[2], tutIds[0], tutIds[1]]},
        {"Name" : "Кружок кройки и шитья", "RoleList" : [studIds[1], studIds[2], tutIds[2]]}
        ]
groupIds = colGroup.insert_many(groups).inserted_ids

colReview = revDb["Review"]
reviews = [
        {"RoleId" : tutIds[1],  "SubjectId" : studIds[0],  "GroupId" : groupIds[0], "Details" : "Сожрал мои печеньки!", "Rate" : 2},
        {"RoleId" : studIds[1], "SubjectId" : tutIds[2],   "GroupId" : groupIds[1], "Details" : "Учит шить как бог"   , "Rate" : 8},
        {"RoleId" : studIds[1], "SubjectId" : groupIds[1], "GroupId" : groupIds[1], "Details" : "Прекрасный кружок"   , "Rate" : 9},
        {"RoleId" : studIds[2], "SubjectId" : studIds[0],  "GroupId" : groupIds[0], "Details" : "Хамоват"             , "Rate" : 4}
        ]
reviewIds = colReview.insert_many(reviews).inserted_ids





