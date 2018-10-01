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
    result = Person.find(request.args)
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