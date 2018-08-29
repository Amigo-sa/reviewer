# -*- coding: utf-8 -*-
from bson import ObjectId
import node.settings.errors as ERR
import node.settings.constants as constants
from flask import Blueprint, request, jsonify
from data.reviewer_model import *
from node.api.auth import required_auth
from node.api.base_functions import delete_resource, list_resources

bp = Blueprint('routes', __name__)


@bp.route("/persons", methods = ['POST'])
@required_auth("admin")
def add_person():
    req = request.get_json()
    try:
        first_name = req['first_name']
        middle_name = req['middle_name']
        surname = req['surname']
        birth_date = req['birth_date']
        phone_no = req['phone_no']
    except:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        person = Person(first_name,
                        middle_name,
                        surname,
                        birth_date,
                        phone_no)
        person.save()
        result = {"result":ERR.OK,
                  "id": str(person.pk)}
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/persons/<string:person_id>", methods = ['DELETE'])
@required_auth("user")
def delete_person(person_id):
    return delete_resource(Person, person_id)


@bp.route("/persons", methods=['GET'])
def find_persons():
    if 'query_limit' in request.args:
        limit = int(request.args['query_limit'])
    else:
        limit = 100
    if 'query_start' in request.args:
        skip = int(request.args['query_start'])
    else:
        skip = 0
    pipeline = ({"$lookup":
                     {"from": "person_specialization",
                      "localField": "_id",
                      "foreignField": "person_id",
                      "as": "person_specialization"}},)
    err = ERR.OK
    if "specialization" in request.args:
        spec_type = request.args["specialization"]
        if Specialization.objects.raw({"type": spec_type}).count():
            specializations = []
            for specialization in Specialization.objects.raw({"type": spec_type}):
                specializations.append(specialization.pk)
            pipeline += ({"$match":
                              {"person_specialization.specialization_id": {"$in": specializations}}},
                         {"$project":
                              {"first_name": 1,
                               "middle_name": 1,
                               "surname": 1,
                                  "person_specialization":
                                   {"$filter": {"input": "$person_specialization",
                                                "as": "spec",
                                                "cond": {"$in": ["$$spec.specialization_id",specializations]}
                                                }
                                    }
                               }
                          }
                         )
        else:
            return jsonify({"result": ERR.INPUT}), 200

    if 'group_id' in request.args:
        group_id = request.args['group_id']
        if Group.objects.raw({"_id": ObjectId(group_id)}).count():
            pipeline += ({"$lookup":
                            {"from": "group_member",
                             "localField": "_id",
                             "foreignField": "person_id",
                             "as": "role"}},
                         {"$match":
                             {"role.group_id": ObjectId(group_id)}},
                         )
        else:
            err = ERR.NO_DATA
    elif 'department_id' in request.args:
        department_id = request.args['department_id']
        if Department.objects.raw({"_id": ObjectId(department_id)}).count():
            pipeline += ({"$match":
                              {"person_specialization.department_id": ObjectId(department_id)}},
                        )
        else:
            err = ERR.NO_DATA
    elif 'organization_id' in request.args:
        organization_id = request.args['organization_id']
        if Organization.objects.raw({"_id": ObjectId(organization_id)}).count():
            departments = []
            for department in Department.objects.raw({"organization_id": ObjectId(organization_id)}):
                departments.append(department.pk)
            pipeline += ({"$match":
                              {"person_specialization.department_id": {"$in": departments}}},
                        )
        else:
            err = ERR.NO_DATA
    """ #оставим этот код на случай если понадобится отфильтровать пользователей без специализации
    else:
        pipeline += ({"$match":
                            {"$or": [{"tutor.department_id": {"$exists": True}},
                                    {"student.department_id": {"$exists": True}}]}},
                    )"""
    if "surname" in request.args:
        pipeline += ({"$match":
                             {"surname": {"$regex": request.args['surname'], "$options": "i"}}},
                     )
    if "first_name" in request.args:
        pipeline += ({"$match":
                          {"first_name": {"$regex": request.args['first_name'], "$options": "i"}}},
                     )
    if "middle_name" in request.args:
        pipeline += ({"$match":
                          {"middle_name": {"$regex": request.args['middle_name'], "$options": "i"}}},
                     )
    pipeline += ({"$skip": skip},
                 {"$limit": limit})
    if err == ERR.NO_DATA:
        return jsonify({"result": ERR.NO_DATA}), 200
    try:
        list = []
        for person in Person.objects.aggregate(*pipeline):
            if person["person_specialization"]:
                department_id = person["person_specialization"][0]["department_id"]
                spec_id = person["person_specialization"][0]["specialization_id"]
                specialization = Specialization(_id=spec_id)
                specialization.refresh_from_db()
                specialization = specialization.type
            else:
                department_id = None
                specialization = None
            if department_id:
                department = Department(_id=department_id)
                department.refresh_from_db()
                organization = Organization(_id=department.organization_id.pk)
                organization.refresh_from_db()
                org_name = organization.name
            else:
                org_name = "None"
            list.append({"id": str(person["_id"]),
                         "first_name": person["first_name"],
                         "middle_name": person["middle_name"],
                         "surname": person["surname"],
                         "specialization": specialization,
                         "organization_name": org_name})

        result = {"result": ERR.OK, "list": list}
    except Exception as ex:
        print(ex)
        result = {"result": ERR.DB}
    return jsonify(result), 200

@bp.route("/persons/<string:id>/group_members", methods=['GET'])
def list_group_members_by_person_id(id):
    return list_resources(GroupMember,
                          {"id": "_id"},
                          Person,
                          id,
                          "person_id")


@bp.route("/persons/<string:person_id>", methods=['GET'])
@required_auth("user")
def get_person_info(person_id):
    try:
        if Person(_id=person_id) in Person.objects.raw({"_id": ObjectId(person_id)}):
            person = Person(_id=person_id)
            person.refresh_from_db()
            birth_date_str = person.birth_date.strftime("%Y-%m-%d")
            data = {"id": str(person.pk),
                    "first_name": person.first_name,
                    "middle_name": person.middle_name,
                    "surname": person.surname,
                    "birth_date": birth_date_str,
                    "phone_no": person.phone_no}
            result = {"result": ERR.OK, "data": data}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


def add_skill(skill_cls):
    req = request.get_json()
    try:
        name = req['name']
        skill = skill_cls(name)
        skill.save()
        result = {"result":ERR.OK,
                  "id": str(skill.pk)}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/soft_skills", methods = ['POST'])
@required_auth("admin")
def add_soft_skill():
    return add_skill(SoftSkill)


@bp.route("/soft_skills/<string:id>", methods = ['DELETE'])
@required_auth("admin")
def delete_soft_skill(id):
    return delete_resource(SoftSkill, id)


@bp.route("/soft_skills", methods = ['GET'])
def list_soft_skills():
    return list_resources(SoftSkill,
                          {"id": "_id",
                           "name": "name"})


@bp.route("/hard_skills", methods = ['POST'])
@required_auth("admin")
def add_hard_skill():
    return add_skill(HardSkill)


@bp.route("/hard_skills/<string:id>", methods = ['DELETE'])
@required_auth("admin")
def delete_hard_skill(id):
    return delete_resource(HardSkill, id)


@bp.route("/hard_skills", methods = ['GET'])
def list_hard_skills():
    return list_resources(HardSkill,
                          {"id": "_id",
                           "name": "name"})


def find_person_skills(skill_cls):
    lst = []
    query = {}
    err = ERR.OK
    if skill_cls == SoftSkill:
        tag = "ss_id"
        person_skill_cls = PersonSS
    elif skill_cls == HardSkill:
        tag = "hs_id"
        person_skill_cls = PersonHS
    else:
        raise Exception("bad func usage")

    if 'person_id' in request.args:
        person_id = request.args['person_id']
        if not Person.objects.raw({"_id":ObjectId(person_id)}).count():
            err = ERR.NO_DATA
        else:
            query.update({"person_id": ObjectId(person_id)})
    if tag in request.args:
        s_id = request.args[tag]
        if not skill_cls.objects.raw({"_id":ObjectId(s_id)}).count():
            err = ERR.NO_DATA
        else:
            query.update({tag: ObjectId(s_id)})
    try:
        if err == ERR.OK:
            for person_s in person_skill_cls.objects.raw(query):
                lst.append({"id": str(person_s.pk)})
            result = {"result": ERR.OK, "list": lst}
        else:
            result = {"result": ERR.NO_DATA}
    except Exception as ex:
        print(ex)
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/persons/soft_skills", methods=['GET'])
def find_person_soft_skills():
    return find_person_skills(SoftSkill)


@bp.route("/persons/hard_skills", methods=['GET'])
def find_person_hard_skills():
    return find_person_skills(HardSkill)


def get_person_skill_info(skill_cls, id):
    if skill_cls == SoftSkill:
        tag = "ss_id"
        person_skill_cls = PersonSS
    elif skill_cls == HardSkill:
        tag = "hs_id"
        person_skill_cls = PersonHS
    else:
        raise Exception("bad func usage")
    try:
        if person_skill_cls(_id=id) in person_skill_cls.objects.raw({"_id": ObjectId(id)}):
            person_s = person_skill_cls(_id=id)
            person_s.refresh_from_db()
            if skill_cls == SoftSkill:
                person_skill_id = person_s.ss_id
            elif skill_cls == HardSkill:
                person_skill_id = person_s.hs_id
            else:
                raise Exception("bad func usage")
            data = {"person_id": str(person_s.person_id.pk),
                    tag: str(person_skill_id.pk),
                    "level": str(person_s.level)}
            result = {"result": ERR.OK, "data": data}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/persons/soft_skills/<string:id>", methods=['GET'])
def get_person_soft_skill_info(id):
    return get_person_skill_info(SoftSkill, id)


@bp.route("/persons/hard_skills/<string:id>", methods=['GET'])
def get_person_hard_skill_info(id):
    return get_person_skill_info(HardSkill, id)


@bp.route("/groups/<string:id>/tests", methods = ['POST'])
@required_auth("admin")
def add_group_test(id):
    req = request.get_json()
    try:
        name = req['name']
        info = req['info']
        if Group.objects.raw({"_id": ObjectId(id)}).count():
            group_test = GroupTest(Group(_id=id), name, info)
            group_test.save()
            result = {"result":ERR.OK,
                      "id": str(group_test.pk)}
        else:
            result = {"result": ERR.NO_DATA}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


@bp.route("/tests/<string:id>", methods = ['DELETE'])
@required_auth("admin")
def delete_group_test(id):
    return delete_resource(GroupTest, id)


@bp.route("/tests/<string:id>", methods=['GET'])
def get_group_test_info(id):
    try:
        if GroupTest(_id=id) in GroupTest.objects.raw({"_id": ObjectId(id)}):
            group_test = GroupTest(_id=id)
            group_test.refresh_from_db()
            data = {"group_id": str(group_test.group_id.pk),
                    "name": str(group_test.name),
                    "info": str(group_test.info)}
            result = {"result": ERR.OK, "data": data}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/groups/<string:id>/tests", methods=['GET'])
def list_group_tests(id):
    return list_resources(GroupTest,
                          {"id": "_id",
                          "name": "name"},
                          Group,
                          id,
                          "group_id")


@bp.route("/tests/<string:id>/results", methods = ['POST'])
@required_auth("admin")
def add_test_result(id):
    req = request.get_json()
    try:
        person_id = req['person_id']
        result_data = req['result_data']
        if GroupTest.objects.raw({"_id": ObjectId(id)}).count() and \
                Person.objects.raw({"_id": ObjectId(person_id)}).count():
            test_result = TestResult(GroupTest(_id=id), Person(_id=person_id), result_data)
            test_result.save()
            result = {"result":ERR.OK,
                      "id": str(test_result.pk)}
        else:
            result = {"result": ERR.NO_DATA}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


@bp.route("/tests/results/<string:id>", methods = ['DELETE'])
@required_auth("admin")
def delete_test_result(id):
    return delete_resource(TestResult, id)


@bp.route("/tests/results/<string:id>", methods=['GET'])
def get_test_result_info(id):
    try:
        if TestResult(_id=id) in TestResult.objects.raw({"_id": ObjectId(id)}):
            test_result = TestResult(_id=id)
            test_result.refresh_from_db()
            data = {"test_id": str(test_result.test_id.pk),
                    "person_id": str(test_result.person_id.pk),
                    "result_data": test_result.result_data}
            result = {"result": ERR.OK, "data": data}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/tests/results", methods=['GET'])
def find_test_results():
    lst = []
    query = {}
    err = ERR.OK
    if 'person_id' in request.args:
        person_id = request.args['person_id']
        if Person.objects.raw({"_id": ObjectId(person_id)}).count():
            query.update({"person_id": ObjectId(person_id)})
        else:
            err = ERR.NO_DATA
    if 'test_id' in request.args:
        test_id = request.args['test_id']
        if GroupTest.objects.raw({"_id": ObjectId(test_id)}).count():
            query.update({"test_id": ObjectId(test_id)})
        else:
            err = ERR.NO_DATA
    try:
        if err == ERR.OK:
            for test_result in TestResult.objects.raw(query):
                lst.append({"id": str(test_result.pk)})
            result = {"result": ERR.OK, "list": lst}
        else:
            result = {"result": ERR.NO_DATA}
    except Exception as ex:
        print(ex)
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/groups/<string:id>/surveys", methods = ['POST'])
@required_auth("admin")
def add_survey(id):
    req = request.get_json()
    try:
        description = req['description']
        options = req['options']
        results = dict((key, 0) for key in options.keys())
        if Group.objects.raw({"_id": ObjectId(id)}).count():
            survey = Survey(Group(_id=id), description, options, results)
            survey.save()
            result = {"result":ERR.OK,
                      "id": str(survey.pk)}
        else:
            result = {"result": ERR.NO_DATA}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


@bp.route("/surveys/<string:id>", methods = ['DELETE'])
@required_auth("admin")
def delete_survey(id):
    return delete_resource(Survey, id)


@bp.route("/surveys", methods=['GET'])
def find_surveys():
    lst = []
    query = {}
    err = ERR.OK
    if 'group_id' in request.args:
        group_id = request.args['group_id']
        if Group.objects.raw({"_id": ObjectId(group_id)}).count():
            query.update({"group_id": ObjectId(group_id)})
        else:
            err = ERR.NO_DATA
    try:
        if err == ERR.OK:
            for survey in Survey.objects.raw(query):
                lst.append({"id": str(survey.pk),
                            "group_id": str(survey.group_id.pk),
                            "options": survey.survey_options,
                            "results": survey.survey_result})
            result = {"result": ERR.OK, "list": lst}
    except Exception as ex:
        print(ex)
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/surveys/<string:id>", methods = ['POST'])
@required_auth("user")
def participate_survey(id):
    req = request.get_json()
    try:
        person_id = req['person_id']
        chosen_option = req['chosen_option']
        if Survey.objects.raw({"_id": ObjectId(id)}).count():
            survey = Survey(_id=id)
            survey.refresh_from_db()
            group_id = survey.group_id.pk
            # проверка, что голосующий человек состоит в данной группе
            if GroupMember.objects.raw({"person_id": ObjectId(person_id),
                                        "group_id": ObjectId(group_id)}).count():
                survey_response = SurveyResponse(survey,
                                                 Person(_id=person_id),
                                                 chosen_option)
                survey.survey_result[chosen_option] += 1
                survey_response.save()
                survey.save()
                result = {"result": ERR.OK,
                          "id" : str(survey_response.pk)}
            else:
                result = {"result": ERR.AUTH}
        else:
            result = {"result": ERR.NO_DATA}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except Exception as e:
        result = {"result": ERR.DB,
                  "error_message": str(e)}
    return jsonify(result), 200