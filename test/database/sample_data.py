# -*- coding: utf-8 -*-
import sys
import context
import datetime
import random
from pymodm.connection import connect, _get_db
from node.settings import constants
from node.api.auth import hash_password, gen_session_id
from bson.binary import Binary, BINARY_SUBTYPE

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
                                 Specialization,
                                 SSReview,
                                 Service,
                                 SkillType,
                                 SoftSkill,
                                 PersonSpecialization,
                                 Survey,
                                 SpecializationReview,
                                 TestResult,
                                 AuthInfo,
                                 SurveyResponse,
                                 get_dependent_list,
                                 init_model)

from data.initial_data import fill_initial_data

"""
def clear_db():
    print("clearing db...")
    revDb = _get_db("reviewer")
    colList = revDb.list_collection_names()
    for col in colList:
        revDb.drop_collection(col)
        print("dropped collection " + col)
    print("done")

def wipe_db(db_name):
    try:
        revDb = _get_db(db_name)
        colList = revDb.list_collection_names()
        for col in colList:
            revDb[col].delete_many({})
    except Exception as e:
        print("Failed to wipe DB")
        print(str(e))
"""

def fill_db():

    persons = {
        "Leni4":
            Person(
                "Леонид",
                "Александрович",
                "Дунаев",
                datetime.date(1986, 5, 1),
                "78005553535"),
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
                "79050100001"),
        "Ivanov":
            Person(
                "Полуэкт",
                "Степанович",
                "Иванов",
                datetime.date(1812, 6, 24)),
        "Petrov":
            Person(
                "Иван",
                "Васильевич",
                "Петров",
                datetime.date(1812, 6, 24))
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

    specializations = {
        "TOE_Tutor":
            Specialization(
                "Tutor",
                "ТОЭ"
            ),
        "MCU_Tutor":
            Specialization(
                "Tutor",
                "Микропросессорные системы"
            ),
        "Metr_Assistant":
            Specialization(
                "Lab assistant",
                "Метрология"
            ),
        "Student":
            Specialization(
                "Student",
            ),
    }

    person_specializations = {
        "Shatokhin_MCU":
            PersonSpecialization(
                persons["Shatokhin"],
                departments["IIT"],
                specializations["MCU_Tutor"],
                70.0
            ),
        "Anisimov_TOE":
            PersonSpecialization(
                persons["Anisimov"],
                departments["EFIS"],
                specializations["TOE_Tutor"],
                90.0
            ),
        "Shatokhin_TOE":
            PersonSpecialization(
                persons["Shatokhin"],
                departments["IIT"],
                specializations["TOE_Tutor"],
                45.0
            ),
        "Leni4":
            PersonSpecialization(
                persons["Leni4"],
                departments["IIT"],
                specializations["Student"],
                None,
                {"graduation": "окончил"},
                False
            ),
        "Leni4_lab":
            PersonSpecialization(
                persons["Leni4"],
                departments["IIT"],
                specializations["Metr_Assistant"],
            ),
        "Pashka":
            PersonSpecialization(
                persons["Pashka"],
                departments["IIT"],
                specializations["Student"],
                None,
                {"graduation": "окончил"},
                False
            ),
        "Vovka":
            PersonSpecialization(
                persons["Vovka"],
                departments["IIT"],
                specializations["Student"]
            ),
        "Bogi":
            PersonSpecialization(
                persons["Bogi"],
                departments["IIT"],
                specializations["Student"]
            ),
        "Maniac":
            PersonSpecialization(
                persons["Maniac"],
                departments["IIT"],
                specializations["Student"],
                20.0,
                {"graduation": "отчислен"},
                False
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

    from data.initial_data import group_permission_dict as group_permissions
    from data.initial_data import hard_skill_list, soft_skill_list

    roles_in_groups = {
        "Shatokhin_admin_arduino":
            GroupMember(persons["Shatokhin"],
                        groups["Arduino"],
                        group_roles["admin"],
                        [group_permissions["read_info"],
                         group_permissions["modify_info"],
                         group_permissions["create_survey"]]),
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

    p_spec_reviews = {
        "Shatokhin_Pashka_sr":
            SpecializationReview(
                persons["Shatokhin"],
                person_specializations["Pashka"],
                50.0,
                "Тема",
                "Часто появляется с перегаром",
                datetime.date(2001, 5, 1)
            ),
        "Anisimov_Bogi_sr":
            SpecializationReview(
                persons["Anisimov"],
                person_specializations["Bogi"],
                20.0,
                "Тема",
                "Боится ТОЭ",
                datetime.date(2001, 5, 1)
            ),
        "Pashka_Shatokhin_MCU":
            SpecializationReview(
                persons["Pashka"],
                person_specializations["Shatokhin_MCU"],
                50.0,
                "Тема",
                "Не знает современную элементную базу",
                datetime.date(2001, 5, 1)
            ),
        "Leni4_Anisimov_rel":
            SpecializationReview(
                persons["Leni4"],
                person_specializations["Anisimov_TOE"],
                100.0,
                "Тема",
                "Это просто чудо какое-то!",
                datetime.date(2001, 5, 1)
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
                {"1": "в корпусе В",
                 "2": "в корпусе М",
                 "3": "в корпусе К"}
            ),
        "A403_timetable":
            Survey(
                groups["A403"],
                "Опрос по смещению расписания занятий",
                {"1": "начинать в 8:40",
                 "2": "начинать в 9:00",
                 "3": "начинать в 9:20"}
            )
    }

    survey_responses = {
        "Leni4_food":
            SurveyResponse(
                surveys["A403_foodcourt"],
                persons["Leni4"],
                "2"
            ),
        "Pashka_food":
            SurveyResponse(
                surveys["A403_foodcourt"],
                persons["Pashka"],
                "2"
            ),
        "Shatokhin_food":
            SurveyResponse(
                surveys["A403_foodcourt"],
                persons["Shatokhin"],
                "2"
            ),
        "Bogi_food":
            SurveyResponse(
                surveys["A403_foodcourt"],
                persons["Bogi"],
                "1"
            ),
        "Vovka_food":
            SurveyResponse(
                surveys["A403_foodcourt"],
                persons["Vovka"],
                "3"
            ),
        "Anisimov_food":
            SurveyResponse(
                surveys["A403_foodcourt"],
                persons["Anisimov"],
                "3"
            ),
    }

    auth_users = {
        "generic_user":
            AuthInfo(
                phone_no=persons["Leni4"].phone_no,
                last_send_time=datetime.datetime.now(datetime.timezone.utc),
                is_approved=True,
                password=hash_password("12345678"),
                session_id=None,
                permissions=0,
                person_id=persons["Leni4"]
            ),
    }

    print("Filling db...")

    for key, item in persons.items():
        try:
            with open(r"./img/" + key + r".jpg", mode='rb') as file:
                fileContent = file.read()
            item.photo = Binary(fileContent)
        except FileNotFoundError:
            pass
        item.save()
    for key, item in organizations.items():
        item.save()
    for key, item in departments.items():
        item.save()
    # add skills
    for key,item in persons.items():
        for i in range(10):
            p_ss = PersonSS()
            p_ss.person_id = item.pk
            p_ss.level = random.random() * 10
            p_ss.ss_id = random.choice(random.choice(soft_skill_list))
            try:
                p_ss.save()
                #print("%s получил софт скилл %s -> %s"%(item.surname, p_ss.ss_id.skill_type_id.name, p_ss.ss_id.name))
            except:
                #print("Не повезло: %s пропустил софт скилл"%item.surname)
                pass
            p_hs = PersonHS()
            p_hs.person_id = item.pk
            p_hs.level = random.random() * 10
            p_hs.hs_id = random.choice(random.choice(hard_skill_list))
            try:
                p_hs.save()
                #print("%s получил хард скилл %s -> %s"%(item.surname, p_hs.hs_id.skill_type_id.name, p_hs.hs_id.name))
            except:
                #print("Не повезло: %s пропустил хард скилл"%item.surname)
                pass

    for i in range(100):
        reviewer = random.choice(list(persons.values()))
        reviewed = random.choice(list(PersonHS.objects.all()))
        hs_review = HSReview()
        hs_review.reviewer_id = reviewer.pk
        hs_review.subject_id = reviewed.pk
        hs_review.value = random.random() * 10
        hs_review.topic = "Тема отзыва"
        hs_review.description = "Описание отзыва %s на %s пользователя %s"%(reviewer.surname, reviewed.hs_id.name,
                                    reviewed.person_id.surname)
        hs_review.date = datetime.date(2000, 5, 1)
        try:
            hs_review.save()
        except:
            pass
        reviewer = random.choice(list(persons.values()))
        reviewed = random.choice(list(PersonSS.objects.all()))
        ss_review = SSReview()
        ss_review.reviewer_id = reviewer.pk
        ss_review.subject_id = reviewed.pk
        ss_review.value = random.choice([0,10])
        ss_review.topic = "Тема отзыва"
        ss_review.description = "Описание %s %s на %s пользователя %s" % (
                                ("лайка" if ss_review.value == 10 else "дизлайка"),
                                reviewer.surname, reviewed.ss_id.name,
                                reviewed.person_id.surname)
        ss_review.date = datetime.date(2000, 5, 1)
        try:
            ss_review.save()
        except:
            pass

    for key, item in specializations.items():
        if item.type == "Student":
            item_type = "Студент"
        elif item.type == "Tutor":
            item_type = "Преподаватель"
        elif item.type == "Lab assistant":
            item_type = "Лаборант"
        else:
            item_type = item.type
        display_text = item_type
        if (item.detail):
            display_text += ", " + item.detail
        item.display_text = display_text
        item.save()
    for key, item in person_specializations.items():
        item.save()
    for key, item in group_roles.items():
        item.save()
    for key, item in groups.items():
        item.save()
    for key, item in roles_in_groups.items():
        item.save()
    for key, item in group_tests.items():
        item.save()
    for key, item in test_results.items():
        item.save()

    i = 0;
    for s_key, s_item in person_specializations.items():
        for p_key, p_item in persons.items():
            if (s_item.person_id != p_item.pk):
                # print(s_item.person_id.surname + p_item.surname)
                i += 1
                review = SpecializationReview()
                review.reviewer_id = p_item.pk
                review.subject_id = s_item.pk
                review.value = random.randint(0,100)
                review.topic = "Тема отзыва " + str(i)
                review.description = "Отзыв %s на '%s' пользователя %s"%\
                                     (p_item.surname,
                                      s_item.specialization_id.display_text,
                                      s_item.person_id.surname)
                review.date = datetime.date(random.randint(1990,2018), random.randint(1,12), random.randint(1,28))
                review.save()
    # for key, item in p_spec_reviews.items():
    #     item.save()
    for key, item in group_reviews.items():
        item.save()
    for key, item in role_in_group_reviews.items():
        item.save()
    for key, item in group_test_reviews.items():
        item.save()
    for key, item in surveys.items():
        item.save()
    for key, item in survey_responses.items():
        item.save()
    # обработка опросов
    for item in Survey.objects.all():
        response_list = list(SurveyResponse.objects.raw({"survey_id": item.pk}))
        survey_dict = {}
        for response in response_list:
            option = response.chosen_option
            if option not in survey_dict:
                survey_dict.update({option: 1})
            else:
                survey_dict.update({option: survey_dict[option] + 1})
        if survey_dict:
            item.survey_result = survey_dict
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
        print("%s %s -> %s: %3.1f" %
              (item.person_id.surname,
               item.hs_id.skill_type_id.name,
               item.hs_id.name,
               item.level))

    print("----Soft Skills:")
    for item in SoftSkill.objects.all():
        print(item.name + " _id:" + str(item.pk))

    print("----Person Soft Skills:")
    for item in PersonSS.objects.all():
        print("%s %s -> %s: %3.1f" %
              (item.person_id.surname,
               item.ss_id.skill_type_id.name,
               item.ss_id.name,
               item.level))

    print("----Specializations")
    for item in Specialization.objects.all():
        print("{0} {1}".format(item.type,
                               item.detail))

    print("----Person Specializations:")
    for item in PersonSpecialization.objects.all():
        print("{0} - {1} {2}, {3}, рейтинг - {4}".format(item.person_id.surname,
                                                         item.specialization_id.type,
                                                         item.specialization_id.detail,
                                                         item.department_id.name,
                                                         item.level))
        if not item.is_active:
            print("Неактивен")
        print(item.details)

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
        print("{0} оставил отзыв с оценкой {1:3.1f} на {2} пользователя {3} с комментарием: {4}".format(
            item.reviewer_id.surname,
            item.value,
            item.subject_id.ss_id.name,
            item.subject_id.person_id.surname,
            item.description))

    print("----Hard Skill Reviews:")
    for item in HSReview.objects.all():
        print("{0} оставил отзыв с оценкой {1:3.1f} на {2} пользователя {3} с комментарием: {4}".format(
            item.reviewer_id.surname,
            item.value,
            item.subject_id.hs_id.name,
            item.subject_id.person_id.surname,
            item.description))

    print("----Person Specialization Reviews:")
    for item in SpecializationReview.objects.all():
        print(
            "{0} оставил отзыв с оценкой {1} на пользователя {2} в качестве {3} {4} "
            "подразделения {5} с комментарием: {6}".format(
                item.reviewer_id.surname,
                item.value,
                item.subject_id.person_id.surname,
                item.subject_id.specialization_id.type,
                item.subject_id.specialization_id.detail,
                item.subject_id.department_id.name,
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
        print("В группе {0} Проведен {1} ".format(
            item.group_id.name,
            item.description))
        print("Варианты ответов:")
        for key, value in item.survey_options.items():
            print("%s: %s" % (key, value))

    print("----Survey Responses:")
    for item in SurveyResponse.objects.all():
        print("{0} выбрал вариант '{1}' в опросе {2}".format(
            item.person_id.surname,
            item.survey_id.survey_options[item.chosen_option],
            item.survey_id.description
        ))

    print("----Survey Results:")
    for item in Survey.objects.all():
        print("Результаты опроса " + item.description)
        if item.survey_result:
            for key, value in item.survey_result.items():
                print("{0}: {1} ответов".format(
                    item.survey_options[key],
                    value
                ))
        else:
            print("Опрос не завершён")


if __name__ == "__main__":
    """
    db_name = constants.db_name
    if len(sys.argv) > 1:
        if '--help' in str(sys.argv):
            print("usage: sample_data.py [--test] fill test database otherwise fill main database")
            exit()
        if '--test' in str(sys.argv):
            db_name = constants.db_name_test
        if '--load_test' in str(sys.argv):
            db_name = constants.db_name_load_test
        if '--develop' in str(sys.argv):
            db_name = constants.db_name_develop
    print("Filling DB '%s' \n" % db_name)
    """
    #connect(constants.mongo_db + "/" + db_name, alias="reviewer")
    #wipe_db("reviewer")
    fill_initial_data("..//..//src//data//hard_skills",
                      "..//..//src//data//soft_skills")
    fill_db()
    #display_data()
