# -*- coding: utf-8 -*-
import context
import datetime
import random
from pymodm.connection import _get_db

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
                                 RoleInGroup,
                                 RoleInGroupReview,
                                 SRReview,
                                 SSReview,
                                 Service,
                                 SoftSkill,
                                 StudentRole,
                                 Survey,
                                 TRReview,
                                 TestResult,
                                 TutorRole,
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
            RoleInGroup(persons["Shatokhin"],
                        groups["Arduino"],
                        group_roles["admin"],
                        [group_permissions["read_info"],
                         group_permissions["modify_info"],
                         group_permissions["create_test"],
                         group_permissions["schedule_event"]]),
        "Leni4_member_arduino":
            RoleInGroup(persons["Leni4"],
                        groups["Arduino"],
                        group_roles["member"],
                        [group_permissions["read_info"],
                         group_permissions["participate_test"]]),
        "Bogi_member_arduino":
            RoleInGroup(persons["Bogi"],
                        groups["Arduino"],
                        group_roles["member"],
                        [group_permissions["read_info"],
                         group_permissions["participate_test"]]),
        "Leni4_monitor_a403":
            RoleInGroup(persons["Leni4"],
                        groups["A403"],
                        group_roles["monitor"],
                        [group_permissions["read_info"],
                         group_permissions["create_survey"],
                         group_permissions["participate_survey"]]),
        "Pashka_student_a403":
            RoleInGroup(persons["Pashka"],
                        groups["A403"],
                        group_roles["student"],
                        [group_permissions["read_info"],
                         group_permissions["participate_survey"]]),
        "Bogi_student_a403":
            RoleInGroup(persons["Bogi"],
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
    print("done")


if __name__ == "__main__":
    clear_db()
    fill_db()
