# -*- coding: utf-8 -*-

import pymongo
import datetime
#import data.sample as dataSample
import settings.mongo as mongosettings

revClient = pymongo.MongoClient(mongosettings.connString)
revDb = revClient["reviewer"]

#colList = revDb.list_collection_names()
#for col in colList:
#    revDb.drop_collection(col)

colPersons = revDb["Persons"]
persons = [
        {"Name" : "Гарри"     , "BirthDate" : datetime.datetime(2000,8,8)},
        {"Name" : "Рон"       , "BirthDate" : datetime.datetime(2006,4,2)},
        {"Name" : "Гермиона"  , "BirthDate" : datetime.datetime(2001,8,25)},
        {"Name" : "Гораций"   , "BirthDate" : datetime.datetime(1920,5,1)},
        {"Name" : "Снейп"     , "BirthDate" : datetime.datetime(1943,6,1)},
        {"Name" : "Дамблдор"  , "BirthDate" : datetime.datetime(1932,9,7)}
        ]
personIds = colPersons.insert_many(persons).inserted_ids

colFeatures = revDb["Features"]
features = [
        {"Name" : "Скрытность"     , "Rate" : 7.0, "PersonId" : personIds[0] },
        {"Name" : "Жадность"       , "Rate" : 4.0, "PersonId" : personIds[1] },
        {"Name" : "Рыжесть"        , "Rate" : 10.0,"PersonId" : personIds[1] },
        {"Name" : "Хитрость"       , "Rate" : 9.0, "PersonId" : personIds[4] },
        {"Name" : "Бородатость"    , "Rate" : 10.0,"PersonId" : personIds[5] },
        {"Name" : "Мудрость"       , "Rate" : 7.0, "PersonId" : personIds[5] },
        {"Name" : "Виежливость"    , "Rate" : 8.0, "PersonId" : personIds[2] }
         ]
featureIds = colFeatures.insert_many(features).inserted_ids

colOrganizations = revDb["Organizations"]
organization = {"Name" : "Хогвартс"}
orgId = colOrganizations.insert_one(organization).inserted_id

colUniversities = revDb["Universities"]
university = {"Name" : "Хогвартс", "OrganizationId" : orgId}
uniId = colUniversities.insert_one(university).inserted_id

colSchools = revDb["Schools"]
school = {"Name" : "Хогвартс lite", "OrganizationId" : orgId}
schoolId = colSchools.insert_one(school).inserted_id

colDepartments = revDb["Departments"]
departments = [
        {"Name" : "Cлизерин"   , "UniversityId" : uniId },
        {"Name" : "Гриффиндор" , "UniversityId" : uniId },
        {"Name" : "Когтевран"  , "UniversityId" : uniId },
        {"Name" : "Хаффлпафф"  , "UniversityId" : uniId },
         ]
depIds = colDepartments.insert_many(departments).inserted_ids

colStudents = revDb["StudentRoles"]
students = [
        {"PersonId" : personIds[0], "DepartmentId" : depIds[1], "Specialization" : "Колдовство"},
        {"PersonId" : personIds[1], "DepartmentId" : depIds[2], "Specialization" : "Алхимия"},
        {"PersonId" : personIds[2], "DepartmentId" : depIds[3], "Specialization" : "История магии"}
           ]
studIds = colStudents.insert_many(students).inserted_ids

colTutors = revDb["TutorRoles"]
tutors = [
        {"PersonId" : personIds[3], "DepartmentId" : depIds[0], "Disciplines" : ["Травоведение", "Оккультизм", "Сопромат"]},
        {"PersonId" : personIds[4], "DepartmentId" : depIds[1], "Disciplines" : ["Светлая магия", "Спортивное ориентирование"]},
        {"PersonId" : personIds[5], "DepartmentId" : depIds[3], "Disciplines" : ["Литература"]},
        {"PersonId" : personIds[0], "DepartmentId" : depIds[2], "Disciplines" : ["Защита от темных искусств"]}
           ]
tutIds = colTutors.insert_many(tutors).inserted_ids

colGroups = revDb["Groups"] 
groups = [
        {"Name" : "Клуб анонимных алкоголиков", "RoleList" : [studIds[0], studIds[2], tutIds[0], tutIds[1]]},
        {"Name" : "Кружок кройки и шитья", "RoleList" : [studIds[1], studIds[2], tutIds[2]]}
        ]
groupIds = colGroups.insert_many(groups).inserted_ids

colReviews = revDb["Reviews"]
reviews = [
        {"RoleId" : tutIds[1],  "SubjectId" : studIds[0],  "GroupId" : groupIds[0], "Details" : "Сожрал мои печеньки!", "Rate" : 2.0},
        {"RoleId" : studIds[1], "SubjectId" : tutIds[2],   "GroupId" : groupIds[1], "Details" : "Учит шить как бог"   , "Rate" : 8.0},
        {"RoleId" : studIds[1], "SubjectId" : groupIds[1], "GroupId" : groupIds[1], "Details" : "Прекрасный кружок"   , "Rate" : 9.0},
        {"RoleId" : studIds[2], "SubjectId" : studIds[0],  "GroupId" : groupIds[0], "Details" : "Хамоват"             , "Rate" : 4.0}
        ]
reviewIds = colReviews.insert_many(reviews).inserted_ids

colTests = revDb["Tests"]
test = {"Name" : "Тест на вменяемость", 
        "GroupId" : groupIds[0], 
        "Description" : "При проведении теста ни одного кролика не пострадало",
        "Results":[
                {"ParticipantId": studIds[2], "Result": 88.0},
                {"ParticipantId": studIds[0], "Result": 23.0},
                {"ParticipantId": tutIds[0], "Result": 3.62},
                {"ParticipantId": tutIds[1], "Result": 0.33},
                ]
            }
testIds = colTests.insert_one(test)

colSurveys = revDb["Surveys"]
survey = {"Name" : "Любимый цвет ножниц", 
        "GroupId" : groupIds[1], 
        "Results":[
                {"Parameter": "Жёлтый", "Quantity": 4.0},
                {"Parameter": "Синий", "Quantity": 7.0},
                {"Parameter": "Прозрачный", "Quantity": 15.0},
                {"Parameter": "Чёрный", "Quantity": 1.0},
                {"Parameter": "Металлический", "Quantity": 6.0},
                {"Parameter": "Полосатый", "Quantity": 9.0}
                ]
            }
survIds = colSurveys.insert_one(survey)





