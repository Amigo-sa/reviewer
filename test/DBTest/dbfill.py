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

service = Service("0.3")
service.save()


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
                "Студент очной формы обучения"
                ),
    "Pashka":
        StudentRole(
                persons["Pashka"],
                departments["IIT"],
                "Студент очной формы обучения"
                ),
    "Vovka":
        StudentRole(
                persons["Vovka"],
                departments["IIT"],
                "Студент очной формы обучения"
                ),
    "Bogi":
        StudentRole(
                persons["Bogi"],
                departments["IIT"],
                "Студент очной формы обучения"
                ),
    "Maniac":
        StudentRole(
                persons["Maniac"],
                departments["IIT"],
                "Отчислен"
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
                ),
    "Student":
        GroupRole(
                "Студент"
                ),
    "Monitor":
        GroupRole(
                "Староста"
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
                ),
    "A403":
        Group(departments["IIT"],
              "А-4-03"
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
                    ["read", "modify", "initiate tests"]),
        "Leni4_member_arduino":
        RoleInGroup(persons["Leni4"],
                    groups["Arduino"],
                    group_roles["Member"],
                    ["read"]),
        "Bogi_member_arduino":
        RoleInGroup(persons["Bogi"],
                    groups["Arduino"],
                    group_roles["Member"],
                    ["read"]),
        "Leni4_monitor_a403":
        RoleInGroup(persons["Leni4"],
                    groups["A403"],
                    group_roles["Monitor"],
                    ["read", "modify"]),
        "Pashka_student_a403":
        RoleInGroup(persons["Pashka"],
                    groups["A403"],
                    group_roles["Student"],
                    ["read"]),
        "Bogi_student_a403":
        RoleInGroup(persons["Bogi"],
                    groups["A403"],
                    group_roles["Student"],
                    ["read"]),
}
    
for key, item in roles_in_groups.items():
    item.save()
for item in RoleInGroup.objects.all():
    print("{0} - {1} группы {2}, права: {3}".format(
            item.person_id.surname, 
            item.role_id.name,
            item.group_id.name,
            item.permissions))

print("----Tests:")
group_tests = {
    "TOE_exam":
        GroupTest(groups["A403"],
                    "Экзамен по ТОЭ",
                    "Итоговый экзамен по дисциплине \"Теоретические основы электротехники\" за 4 семестр"
                    ),
    "Arduino_model_test":
        GroupTest(groups["Arduino"],
                    "Тест на знание ардуино",
                    "Запись в столбик всех моделей Arduino сломанной левой рукой в темноте"
                    )
        
}
    
for key, item in group_tests.items():
    item.save()
for item in GroupTest.objects.all():
    print("В группе {0} проведен {1}".format(
            item.group_id.name, 
            item.name))
    
print("----Test Results:")
test_results = {
    "Leni4_TOE":
        TestResult(group_tests["TOE_exam"],
                   persons["Leni4"],
                   ["Оценка: 4.0", 
                    "Время: 1:20"]
                    ),
    "Bogi_TOE":
        TestResult(group_tests["TOE_exam"],
                   persons["Bogi"],
                   ["Оценка: 2.0", 
                    "Время: 1:50"]
                    ),
    "Pashka_TOE":
        TestResult(group_tests["TOE_exam"],
                   persons["Pashka"],
                   ["Оценка: 3.5", 
                    "Время: 1:00"]
                    ),
    "Leni4_Arduino":
        TestResult(group_tests["Arduino_model_test"],
                   persons["Leni4"],
                   ["Оценка: 4.0", 
                    "Время: 1:07",
                    "Уснул в процессе"]
                    ),
    "Bogi_Arduino":
        TestResult(group_tests["Arduino_model_test"],
                   persons["Bogi"],
                   ["Оценка: 5.0", 
                    "Время: 0:04"]
                    )
}
    
for key, item in test_results.items():
    item.save()
for item in TestResult.objects.all():
    print("{0} сдал {1} со следующими результатами: {2}".format(
            item.person_id.surname, 
            item.test_id.name,
            item.result_data))

print("----Soft Skill Reviews:")

ss_reviews = {
    "bogi_anisimov_posAtt":
            SSReview(
                    persons["Bogi"],
                    PersonSS.objects.get(
                            {"ss_id" : soft_skills["Positive attitude"].pk,
                            "person_id" : persons["Anisimov"].pk}),
                    1.0,
                    "Очень негативный человек!!!1"
                    ),
    "Leni4_Maniac_posAtt":
            SSReview(
                    persons["Leni4"],
                    PersonSS.objects.get(
                            {"ss_id" : soft_skills["Communication"].pk,
                            "person_id" : persons["Maniac"].pk}),
                    40.0,
                    "Картавит"
                    )
        }

for key, item in ss_reviews.items():
    item.save()

for item in SSReview.objects.all():
    print("{0} оставил отзыв с оценкой {1} на {2} пользователя {3} с комментарием: {4}".format(
            item.reviewer_id.surname,
            item.value,
            item.subject_id.ss_id.name,
            item.subject_id.person_id.surname,
            item.description))
    
print("----Hard Skill Reviews:")    
hs_reviews = {
    "Shatokhin_Leni4_uC":
            HSReview(
                    persons["Shatokhin"],
                    person_hs["Leni4_uC"],
                    90.0,
                    "Способен запрограммировать даже советский утюг"
                    ),
    "Pashka_Maniac_phone":
            HSReview(
                    persons["Pashka"],
                    person_hs["Maniac_phoneRepair"],
                    0.0,
                    "Ушатал мне мобилу"
                    ),
    "Bogi_Anisimov_psy":
            HSReview(
                    persons["Bogi"],
                    person_hs["Anisimov_psySupp"],
                    100.0,
                    "Подавил так подавил"
                    )
        }

for key, item in hs_reviews.items():
    item.save()
for item in HSReview.objects.all():
    print("{0} оставил отзыв с оценкой {1} на {2} пользователя {3} с комментарием: {4}".format(
            item.reviewer_id.surname,
            item.value,
            item.subject_id.hs_id.name,
            item.subject_id.person_id.surname,
            item.description))
    
print("----Student Role Reviews:")    
sr_reviews = {
    "Shatokhin_Pashka_sr":
            SRReview(
                    persons["Shatokhin"],
                    student_roles["Pashka"],
                    50.0,
                    "Часто появляется с перегаром"
                    ),
    "Anisimov_Bogi_sr":
            SRReview(
                    persons["Anisimov"],
                    student_roles["Bogi"],
                    0.0,
                    "Сам ты негативный, засранец!"
                    )
        }

for key, item in sr_reviews.items():
    item.save()
for item in SRReview.objects.all():
    print("{0} оставил отзыв с оценкой {1} на пользователя {2} в качестве {3} подразделения {4} с комментарием: {5}".format(
            item.reviewer_id.surname,
            item.value,
            item.subject_id.person_id.surname,
            item.subject_id.description,
            item.subject_id.department_id.name,
            item.description))
    
print("----Tutor Role Reviews:")    
tr_reviews = {
    "Pashka_Shatokhin_MCU":
            TRReview(
                    persons["Pashka"],
                    tutor_roles["Shatokhin_MCU"],
                    50.0,
                    "Не знает современную элементную базу"
                    ),
    "Leni4_Anisimov_rel":
            TRReview(
                    persons["Leni4"],
                    tutor_roles["Anisimov_rel"],
                    100.0,
                    "Это просто чудо какое-то!"
                    )
        }

for key, item in tr_reviews.items():
    item.save()
for item in TRReview.objects.all():
    print("{0} оставил отзыв с оценкой {1} на пользователя {2} в качестве преподавателя {3} с комментарием: {4}".format(
            item.reviewer_id.surname,
            item.value,
            item.subject_id.person_id.surname,
            item.subject_id.discipline,
            item.description))

print("----Group Reviews:")    
group_reviews = {
    "Bogi_A403":
            GroupReview(
                    persons["Bogi"],
                    groups["A403"],
                    99.0,
                    "Лучшая группа в мире!"
                    ),
    "Shatokhin_arduino":
            GroupReview(
                    persons["Shatokhin"],
                    groups["Arduino"],
                    10.0,
                    "Лучше бы я вёл историю"
                    )
        }

for key, item in group_reviews.items():
    item.save()
for item in GroupReview.objects.all():
    print("{0} оставил отзыв с оценкой {1} на группу {2} с комментарием: {3}".format(
            item.reviewer_id.surname,
            item.value,
            item.subject_id.name,
            item.description))           

print("----Role in Group Reviews:")    
role_in_group_reviews = {
    "Bogi_Shatokhin_Arduino":
            RoleInGroupReview(
                    persons["Bogi"],
                    roles_in_groups["Shatokhin_admin_arduino"],
                    80.0,
                    "Хороший админ, и конкурсы интересные"
                    ),
    "Anisimov_arduino":
            RoleInGroupReview(
                    persons["Anisimov"],
                    roles_in_groups["Leni4_monitor_a403"],
                    70.0,
                    "Умён, но ленив"
                    )
        }

for key, item in role_in_group_reviews.items():
    item.save()
for item in RoleInGroupReview.objects.all():
    print("{0} оставил отзыв с оценкой {1} на роль {2} пользователя {3} в группе {4} с комментарием: {5}".format(
            item.reviewer_id.surname,
            item.value,
            item.subject_id.role_id.name,
            item.subject_id.person_id.surname,
            item.subject_id.group_id.name,
            item.description))     

print("----Group Test Reviews:")    
group_test_reviews = {
    "Bogi_TOE_Exam":
            GroupTestReview(
                    persons["Bogi"],
                    group_tests["TOE_exam"],
                    40.0,
                    "Слишком строгие критерии"
                    ),
    "Leni4_Arduino_model_test":
            GroupTestReview(
                    persons["Leni4"],
                    group_tests["Arduino_model_test"],
                    20.0,
                    "Очень низкоквалифицированный тест"
                    )
        }

for key, item in group_test_reviews.items():
    item.save()
for item in GroupTestReview.objects.all():
    print("{0} оставил отзыв с оценкой {1} на {2} с комментарием: {3}".format(
            item.reviewer_id.surname,
            item.value,
            item.subject_id.name,
            item.description))                             
    
print("----Surveys:")    
surveys = {
    "A403_foodcourt":
            Survey(
                    groups["A403"],
                    "Опрос про любимую столовую",
                    {"в корпусе В": 55.0,
                     "в корпусе М": 40.0,
                     "в корпусе К": 5.0,}
                    )
        }
            
for key, item in surveys.items():
    item.save()
for item in Survey.objects.all():
    print("В группе {0} Проведен {1} с результатами: {2}".format(
            item.group_id.name,
            item.description,
            item.survey_data)) 