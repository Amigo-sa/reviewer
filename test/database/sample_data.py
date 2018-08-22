# -*- coding: utf-8 -*-
import sys
import context
import datetime
import random
from pymodm.connection import connect, _get_db
from node.settings import constants

fill_script_version = "0.3"

from data.reviewer_model import (Department,
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
                                 GroupMember,
                                 GroupMemberReview,
                                 SRReview,
                                 SSReview,
                                 Service,
                                 SoftSkill,
                                 Student,
                                 Survey,
                                 TRReview,
                                 TestResult,
                                 Tutor,
                                 AuthInfo,
                                 get_dependent_list,
                                 init_model)


def clear_db():
    print("clearing db...")
    revDb = _get_db("reviewer")
    colList = revDb.list_collection_names()
    for col in colList:
        revDb.drop_collection(col)
        print("dropped collection " + col)
    print("done")

def fill_db():
    persons = {
        "Leni4":
            Person(
                "Леонид",
                "Александрович",
                "Дунаев",
                datetime.date(1986, 5, 1),
                "88005553535"),
        "Maniac":
            Person(
                "Кирилл",
                "Владимирович",
                "Ярин",
                datetime.date(1986, 1, 2),
                "79033223232"),
        "Pashka":
            Person(
                "Павел",
                "Борисович",
                "Ерин",
                datetime.date(1986, 12, 30),
                "78392122221"),
        "Vovka":
            Person(
                "Владимир",
                "Владимирович",
                "Панкин",
                datetime.date(1987, 7, 6),
                "78398889991"),
        "Bogi":
            Person(
                "Владимир",
                "Андреевич",
                "Богословских",
                datetime.date(1986, 4, 9),
                "79055533342"),
        "Shatokhin":
            Person(
                "Александр",
                "Алексеевич",
                "Шатохин",
                datetime.date(1900, 3, 4),
                "79052231123"),
        "Anisimov":
            Person(
                "Анатолий",
                "Степанович",
                "Анисимов",
                datetime.date(1812, 6, 24),
                "79050100001")
    }

    organizations = {
        "MPEI":
            Organization(
                "МЭИ")
    }

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

    person_ss = {}
    for pers_key, person in persons.items():
        for ss_key, soft_skill in soft_skills.items():
            ss = PersonSS(
                person,
                soft_skill,
                random.random() * 100.0
            )
            person_ss.update({person.surname + "_" + soft_skill.name: ss})

    tutor_roles = {
        "Shatokhin_MCU":
            Tutor(
                persons["Shatokhin"],
                departments["IIT"],
                "Отжигание на микроконтроллерах семейства 8051"
            ),
        "Anisimov_TOE":
            Tutor(
                persons["Anisimov"],
                departments["EFIS"],
                "ТОЭ"
            ),
        "Anisimov_rel":
            Tutor(
                persons["Anisimov"],
                departments["EFIS"],
                "Религиоведенье"
            ),
        "Shatokhin_debug":
            Tutor(
                persons["Shatokhin"],
                departments["IIT"],
                "Отладка кода, написанного за 20 лет до вашего рождения"
            ),
    }

    student_roles = {
        "Leni4":
            Student(
                persons["Leni4"],
                departments["IIT"],
                "Студент очной формы обучения"
            ),
        "Pashka":
            Student(
                persons["Pashka"],
                departments["IIT"],
                "Студент очной формы обучения"
            ),
        "Vovka":
            Student(
                persons["Vovka"],
                departments["IIT"],
                "Студент очной формы обучения"
            ),
        "Bogi":
            Student(
                persons["Bogi"],
                departments["IIT"],
                "Студент очной формы обучения"
            ),
        "Maniac":
            Student(
                persons["Maniac"],
                departments["IIT"],
                "Отчислен"
            ),
    }

    group_roles = {
        "admin":
            GroupRole(
                "admin"
            ),
        "guest":
            GroupRole(
                "guest"
            ),
        "member":
            GroupRole(
                "member"
            ),
        "student":
            GroupRole(
                "student"
            ),
        "monitor":
            GroupRole(
                "monitor"
            )
    }

    group_permissions = {
        "read_info":
            GroupPermission(
                "read_info"
            ),
        "modify_info":
            GroupPermission(
                "modify_info"
            ),
        "create_test":
            GroupPermission(
                "create_test"
            ),
        "participate_test":
            GroupPermission(
                "participate_test"
            ),
        "schedule_event":
            GroupPermission(
                "schedule_event"
            ),
        "create_survey":
            GroupPermission(
                "create_survey"),
        "participate_survey":
            GroupPermission(
                "participate_survey"
            )
    }

    groups = {
        "Arduino":
            Group(departments["IIT"],
                  "Клуб анонимных ардуинщиков",
                  [group_roles["admin"], group_roles["member"]]
                  ),
        "A403":
            Group(departments["IIT"],
                  "А-4-03",
                  [group_roles["monitor"], group_roles["student"]]
                  )
    }

    roles_in_groups = {
        "Shatokhin_admin_arduino":
            GroupMember(persons["Shatokhin"],
                        groups["Arduino"],
                        group_roles["admin"],
                        [group_permissions["read_info"],
                         group_permissions["modify_info"],
                         group_permissions["create_test"],
                         group_permissions["schedule_event"]]),
        "Leni4_member_arduino":
            GroupMember(persons["Leni4"],
                        groups["Arduino"],
                        group_roles["member"],
                        [group_permissions["read_info"],
                         group_permissions["participate_test"]]),
        "Bogi_member_arduino":
            GroupMember(persons["Bogi"],
                        groups["Arduino"],
                        group_roles["member"],
                        [group_permissions["read_info"],
                         group_permissions["participate_test"]]),
        "Leni4_monitor_a403":
            GroupMember(persons["Leni4"],
                        groups["A403"],
                        group_roles["monitor"],
                        [group_permissions["read_info"],
                         group_permissions["create_survey"],
                         group_permissions["participate_survey"]]),
        "Pashka_student_a403":
            GroupMember(persons["Pashka"],
                        groups["A403"],
                        group_roles["student"],
                        [group_permissions["read_info"],
                         group_permissions["participate_survey"]]),
        "Bogi_student_a403":
            GroupMember(persons["Bogi"],
                        groups["A403"],
                        group_roles["student"],
                        [group_permissions["read_info"],
                         group_permissions["participate_survey"]]),
    }

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

    ss_reviews = {
        "bogi_anisimov_posAtt":
            SSReview(
                persons["Bogi"],
                person_ss["Анисимов_Positive attitude"],
                1.0,
                "Очень негативный человек!!!1"
            ),
        "Leni4_Maniac_posAtt":
            SSReview(
                persons["Leni4"],
                person_ss["Ярин_Communication"],
                40.0,
                "Картавит"
            )
    }

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

    role_in_group_reviews = {
        "Bogi_Shatokhin_Arduino":
            GroupMemberReview(
                persons["Bogi"],
                roles_in_groups["Shatokhin_admin_arduino"],
                80.0,
                "Хороший админ, и конкурсы интересные"
            ),
        "Anisimov_arduino":
            GroupMemberReview(
                persons["Anisimov"],
                roles_in_groups["Leni4_monitor_a403"],
                70.0,
                "Умён, но ленив"
            )
    }

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

    surveys = {
        "A403_foodcourt":
            Survey(
                groups["A403"],
                "Опрос про любимую столовую",
                {"в корпусе В": 55.0,
                 "в корпусе М": 40.0,
                 "в корпусе К": 5.0, }
            ),
        "A403_timetable":
            Survey(
                groups["A403"],
                "Опрос по смещению расписания занятий",
                {"начинать в 8:40": 35.0,
                 "начинать в 9:00": 40.0,
                 "начинать в 9:20": 25.0, }
            )
    }

    auth_users = {
        "admin":
            AuthInfo(
                phone_no = "88001112233",
                last_send_time = datetime.datetime.now(datetime.timezone.utc),
                is_approved = True,
                password = "0ffe1abd1a08215353c233d6e009613e95eec4253832a761af28ff37ac5a150c",
                session_id = "12345",
                permissions = 1
            ),
        "generic_user":
            AuthInfo(
                phone_no="88005553535",
                last_send_time=datetime.datetime.now(datetime.timezone.utc),
                is_approved=True,
                password="0ffe1abd1a08215353c233d6e009613e95eec4253832a761af28ff37ac5a150c",
                session_id="55555",
                permissions=0,
                person_id = persons["Leni4"]
            ),
    }
    print("Filling db...")
    print("Fill script version is " + fill_script_version)
    service = Service(fill_script_version)
    service.save()
    for key, item in persons.items():
        item.save()
    for key, item in organizations.items():
        item.save()
    for key, item in departments.items():
        item.save()
    for key, item in hard_skills.items():
        item.save()
    for key, item in person_hs.items():
        item.save()
    for key, item in soft_skills.items():
        item.save()
    for key, item in person_ss.items():
        item.save()
    for key, item in tutor_roles.items():
        item.save()
    for key, item in student_roles.items():
        item.save()
    for key, item in group_roles.items():
        item.save()
    for key, item in group_permissions.items():
        item.save()
    for key, item in groups.items():
        item.save()
    for key, item in roles_in_groups.items():
        item.save()
    for key, item in group_tests.items():
        item.save()
    for key, item in test_results.items():
        item.save()
    for key, item in ss_reviews.items():
        item.save()
    for key, item in hs_reviews.items():
        item.save()
    for key, item in sr_reviews.items():
        item.save()
    for key, item in tr_reviews.items():
        item.save()
    for key, item in group_reviews.items():
        item.save()
    for key, item in role_in_group_reviews.items():
        item.save()
    for key, item in group_test_reviews.items():
        item.save()
    for key, item in surveys.items():
        item.save()
    for key, item in auth_users.items():
        item.save()
    print("done")


def display_data():
    print("--Displaying data")
    print("----Persons:")
    for item in Person.objects.all():
        print(item.surname + " _id:" + str(item.pk))

    print("----Organizations:")
    for item in Organization.objects.all():
        print(item.name + " _id:" + str(item.pk))

    print("----Departments:")
    for item in Department.objects.all():
        print(item.name + " _id:" + str(item.pk))

    print("----Hard Skills:")
    for item in HardSkill.objects.all():
        print(item.name + " _id:" + str(item.pk))

    print("----Person Hard Skills:")
    for item in PersonHS.objects.all():
        print(item.person_id.surname +
              ", " +
              item.hs_id.name +
              ", lvl: " +
              str(item.level))

    print("----Soft Skills:")
    for item in SoftSkill.objects.all():
        print(item.name + " _id:" + str(item.pk))

    print("----Person Soft Skills:")
    for ss in PersonSS.objects.all():
        print(ss.person_id.surname +
              " " +
              ss.ss_id.name +
              ": " +
              str(ss.level))

    print("----Tutor Roles:")
    for item in Tutor.objects.all():
        print("{0} из {2} ведет {1}".format(item.person_id.surname,
                                            item.discipline,
                                            item.department_id.name))

    print("----Student Roles:")
    for item in Student.objects.all():
        print("{0} - {1}, {2}".format(item.person_id.surname,
                                      item.description,
                                      item.department_id.name))

    print("----Roles for Groups:")
    for item in GroupRole.objects.all():
        print("{0}:_id {1}".format(item.name, str(item.pk)))

    print("----Group Permissions:")
    for item in GroupPermission.objects.all():
        print("{0}:_id {1}".format(item.name, str(item.pk)))

    print("----Groups:")
    for item in Group.objects.all():
        print("{0} при {1}. Допустимые роли:".format(item.name, item.department_id.name))
        for role_id in item.role_list:
            print(role_id.name)

    print("----Roles in Groups:")
    for item in GroupMember.objects.all():
        print("{0} - {1} группы {2}, права:".format(
            item.person_id.surname,
            item.role_id.name,
            item.group_id.name))
        for perm in item.permissions:
            print(perm.name)

    print("----Tests:")
    for item in GroupTest.objects.all():
        print("В группе {0} проведен {1}".format(
            item.group_id.name,
            item.name))

    print("----Test Results:")
    for item in TestResult.objects.all():
        print("{0} сдал {1} со следующими результатами: {2}".format(
            item.person_id.surname,
            item.test_id.name,
            item.result_data))

    print("----Soft Skill Reviews:")
    for item in SSReview.objects.all():
        print("{0} оставил отзыв с оценкой {1} на {2} пользователя {3} с комментарием: {4}".format(
            item.reviewer_id.surname,
            item.value,
            item.subject_id.ss_id.name,
            item.subject_id.person_id.surname,
            item.description))

    print("----Hard Skill Reviews:")
    for item in HSReview.objects.all():
        print("{0} оставил отзыв с оценкой {1} на {2} пользователя {3} с комментарием: {4}".format(
            item.reviewer_id.surname,
            item.value,
            item.subject_id.hs_id.name,
            item.subject_id.person_id.surname,
            item.description))

    print("----Student Role Reviews:")
    for item in SRReview.objects.all():
        print(
            "{0} оставил отзыв с оценкой {1} на пользователя {2} в качестве {3} подразделения {4} с комментарием: {5}".format(
                item.reviewer_id.surname,
                item.value,
                item.subject_id.person_id.surname,
                item.subject_id.description,
                item.subject_id.department_id.name,
                item.description))

    print("----Tutor Role Reviews:")
    for item in TRReview.objects.all():
        print(
            "{0} оставил отзыв с оценкой {1} на пользователя {2} в качестве преподавателя {3} с комментарием: {4}".format(
                item.reviewer_id.surname,
                item.value,
                item.subject_id.person_id.surname,
                item.subject_id.discipline,
                item.description))

    print("----Group Reviews:")
    for item in GroupReview.objects.all():
        print("{0} оставил отзыв с оценкой {1} на группу {2} с комментарием: {3}".format(
            item.reviewer_id.surname,
            item.value,
            item.subject_id.name,
            item.description))

    print("----Role in Group Reviews:")
    for item in GroupMemberReview.objects.all():
        print("{0} оставил отзыв с оценкой {1} на роль {2} пользователя {3} в группе {4} с комментарием: {5}".format(
            item.reviewer_id.surname,
            item.value,
            item.subject_id.role_id.name,
            item.subject_id.person_id.surname,
            item.subject_id.group_id.name,
            item.description))

    print("----Group Test Reviews:")
    for item in GroupTestReview.objects.all():
        print("{0} оставил отзыв с оценкой {1} на {2} с комментарием: {3}".format(
            item.reviewer_id.surname,
            item.value,
            item.subject_id.name,
            item.description))

    print("----Surveys:")
    for item in Survey.objects.all():
        print("В группе {0} Проведен {1} с результатами: {2}".format(
            item.group_id.name,
            item.description,
            item.survey_data))

if __name__ == "__main__":
    db_name = constants.db_name
    if len(sys.argv) > 1:
        if '--help' in str(sys.argv):
            print("usage: sample_data.py [--test] fill test database otherwise fill main database")
            exit()
        if '--test' in str(sys.argv):
            db_name = constants.db_name_test
    print("Filling DB '%s' \n" % db_name)
    connect(constants.mongo_db + "/" + db_name, alias="reviewer")
    clear_db()
    fill_db()
    display_data()
