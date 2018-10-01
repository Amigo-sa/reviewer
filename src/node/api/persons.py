# -*- coding: utf-8 -*-
from bson import ObjectId
import node.settings.errors as ERR
import node.settings.constants as constants
from flask import Blueprint, request, jsonify, make_response
from data.reviewer_model import *
from node.api.auth import required_auth
from node.api.base_functions import delete_resource, list_resources, add_resource

bp = Blueprint('persons', __name__)


@bp.route("/persons", methods = ['POST'])
@required_auth("admin")
def add_person():
    return add_resource(Person,
                        ["first_name",
                         "middle_name",
                         "surname",
                         "birth_date",
                         "phone_no"])


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
    pipeline =()
    person_spec_project_filter = 1
    err = ERR.OK

    group_debug = False
    if "group_id_mod" in request.args:
        group_debug = True
        group_id = request.args['group_id_mod']
        group_qs = Group.objects.raw({"_id": ObjectId(group_id)})
        if group_qs.count():
            print(group_qs.count())
            pipeline += ({"$match": {"group_id": ObjectId(group_id)}},)
            pipeline += ({"$lookup":
                              {"from": "person"
                              ,"localField": "person_id"
                              ,"foreignField": "_id"
                              ,"as": "person_member"}
                          },)

            pipeline += ({"$project":
                              {
                                  # TODO это вообще нормально, что приходится брать 1-й элемент массива?
                                  # по идее, должно возвращаться просто значение, а не как массив
                                  "first_name": {"$arrayElemAt":["$person_member.first_name", 0]},
                                  "middle_name": {"$arrayElemAt":["$person_member.middle_name",0]},
                                  "surname": {"$arrayElemAt":["$person_member.surname",0]},
                                  "_id" : {"$arrayElemAt":["$person_member._id",0]}
                              }},)
        else:
            err = ERR.NO_DATA

    if "specialization" in request.args:
        spec_type = request.args["specialization"]
        spec_qs = Specialization.objects.raw({"type": spec_type});
        if spec_qs.count():
            # Find specializations by specialization type
            specializations = list(key["_id"] for key in spec_qs.values())
            # Find persons match specialization type
            person_spec_qs = PersonSpecialization.objects.raw({"specialization_id": {"$in": specializations}})
            specialists = list(key["person_id"] for key in person_spec_qs.values())
            # Prepare query
            pipeline += ({"$match": {"_id": {"$in": specialists}}},)
            person_spec_project_filter = \
                {"$filter": {"input": "$person_specialization",
                             "as": "spec",
                             "cond": {"$in": ["$$spec.specialization_id", specializations]}}}
        else:
            return jsonify({"result": ERR.INPUT}), 200

    if 'group_id' in request.args:
        group_id = request.args['group_id']
        # Find group
        group_qs = Group.objects.raw({"_id": ObjectId(group_id)})
        if group_qs.count():
            # Find group members persons by group id
            group_members_qs = GroupMember.objects.raw({"group_id": ObjectId(group_id)});
            group_members = list(key["person_id"] for key in group_members_qs.values())
            # Find department_id
            department_id = str(group_qs.first().department_id.pk)
            # Prepare query
            pipeline += ({"$match": {"_id": {"$in": group_members}}},)
            # person_spec_project_filter = \
            #     {"$filter": {"input": "$person_specialization",
            #                  "as": "spec",
            #                  "cond": {"$in": ["$$spec.department_id", [ObjectId(department_id)]]}}}
        else:
            err = ERR.NO_DATA
    elif 'department_id' in request.args:
        department_id = request.args['department_id']
        dep_qs = Department.objects.raw({"_id": ObjectId(department_id)})
        if dep_qs.count():
            # Find persons match department
            person_spec_qs = PersonSpecialization.objects.raw({"department_id": ObjectId(department_id)})
            specialists = list(key["person_id"] for key in person_spec_qs.values())
            # Prepare query
            pipeline += ({"$match": {"_id": {"$in": specialists}}},)
            person_spec_project_filter = \
                {"$filter": {"input": "$person_specialization",
                             "as": "spec",
                             "cond": {"$in": ["$$spec.department_id", [ObjectId(department_id)]]}}}
        else:
            err = ERR.NO_DATA
    elif 'organization_id' in request.args:
        organization_id = request.args['organization_id']
        if Organization.objects.raw({"_id": ObjectId(organization_id)}).count():
            # Find departments in organization
            dep_qs = Department.objects.raw({"organization_id": ObjectId(organization_id)})
            departments = list(key["_id"] for key in dep_qs.values())
            # Find persons match departments
            person_spec_qs = PersonSpecialization.objects.raw({"department_id": {"$in": departments}})
            specialists = list(key["person_id"] for key in person_spec_qs.values())
            # Prepare query
            pipeline += ({"$match": {"_id": {"$in": specialists}}},)
            person_spec_project_filter = \
                {"$filter": {"input": "$person_specialization",
                             "as": "spec",
                             "cond": {"$in": ["$$spec.department_id", departments]}}}
        else:
            err = ERR.NO_DATA
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
    pipeline += ({"$lookup":
                      {"from": "person_specialization",
                       "localField": "_id",
                       "foreignField": "person_id",
                       "as": "person_specialization"}},
                 {"$project":
                      {"first_name": 1,
                       "middle_name": 1,
                       "surname": 1,
                       "person_specialization": person_spec_project_filter}},
                 {"$project":
                      {"first_name": 1,
                       "middle_name": 1,
                       "surname": 1,
                       "person_specialization": { "$arrayElemAt":["$person_specialization", 0]}}},
                 {"$lookup":
                      {"from": "specialization",
                       "localField": "person_specialization.specialization_id",
                       "foreignField": "_id",
                       "as": "specialization"}},
                 {"$lookup":
                      {"from": "department",
                       "localField": "person_specialization.department_id",
                       "foreignField": "_id",
                       "as": "department"}},
                 {"$lookup":
                      {"from": "organization",
                       "localField": "department.organization_id",
                       "foreignField": "_id",
                       "as": "organization"}},
                 )
    if err == ERR.NO_DATA:
        return jsonify({"result": ERR.NO_DATA}), 200
    try:
        lst = []
        target_cls = Person if not group_debug else GroupMember
        for person in target_cls.objects.aggregate(*pipeline):
            if "person_specialization" in person and person["person_specialization"]:
                specialization = person["specialization"][0]["type"]
                org_name = person["organization"][0]["name"]
            else:
                specialization = None
                org_name = "None"
            lst.append({"id": str(person["_id"]),
                        "first_name": person["first_name"],
                        "middle_name": person["middle_name"],
                        "surname": person["surname"],
                        "specialization": specialization,
                        "organization_name": org_name})

        result = {"result": ERR.OK, "list": lst}
    except Exception as e:
        result = {"result": ERR.DB,
                  "error_message": str(e)}
    return jsonify(result), 200


@bp.route("/persons/<string:person_id>", methods = ['DELETE'])
@required_auth("user")
def delete_person(person_id):
    return delete_resource(Person, person_id)


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


@bp.route("/persons/<string:person_id>/photo", methods=['PUT'])
@required_auth("user")
def post_person_photo(person_id):
    try:
        header = request.headers.get('Content-Type')
        if header != "image/jpeg":
            return jsonify({"result": ERR.INPUT}), 200
        if Person(_id=person_id) in Person.objects.raw({"_id": ObjectId(person_id)}):
            person = Person(_id=person_id)
            person.photo = request.get_data()
            person.save()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except KeyError:
        result = {"result": ERR.INPUT}
    except Exception as e:
        result = {"result": ERR.DB,
                  "error_message": str(e)}
    return jsonify(result), 200


@bp.route("/persons/<string:person_id>/photo", methods=['GET'])
def get_person_photo(person_id):
    try:
        if Person(_id=person_id) in Person.objects.raw({"_id": ObjectId(person_id)}):
            person = Person(_id=person_id)
            person.refresh_from_db()
            if not person.photo:
                return "", 204
            image_binary = person.photo
            response = make_response(image_binary)
            response.headers.set('Content-Type', 'image/jpeg')
            response.headers.set(
                'Content-Disposition', 'attachment', filename='%s.jpg' % person_id)
            return response
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/persons/<string:id>/group_members", methods=['GET'])
def list_group_members_by_person_id(id):
    return list_resources(GroupMember,
                          {"id": "_id"},
                          Person,
                          id,
                          "person_id")


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