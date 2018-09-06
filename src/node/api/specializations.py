# -*- coding: utf-8 -*-
from bson import ObjectId
import node.settings.errors as ERR
import node.settings.constants as constants
from flask import Blueprint, request, jsonify
from data.reviewer_model import *
from node.api.auth import required_auth
from node.api.base_functions import delete_resource, list_resources, add_resource

bp = Blueprint('specializations', __name__)


@bp.route("/specializations", methods=['POST'])
@required_auth("admin")
def add_specializations():
    return add_resource(Specialization,
                        ["type"],
                        optional_fields=["detail"])


@bp.route("/specializations/<string:_id>", methods=['DELETE'])
@required_auth("admin")
def delete_specialization(_id):
    return delete_resource(Specialization, _id)


@bp.route("/specializations", methods=['GET'])
def list_specializations():
    return list_resources(Specialization,
                          {"id": "_id",
                           "type": "type",
                           "detail": "detail"})


@bp.route("/persons/<string:id>/specializations", methods=['POST'])
@required_auth("admin")
def add_person_specialization(id):
    req = request.get_json()
    try:
        person_id = id
        department_id = req['department_id']
        spec_id = req['specialization_id']
        level = req['level'] if "level" in req else None
        if not Person.objects.raw({"_id": ObjectId(person_id)}).count()\
                or not Department.objects.raw({"_id": ObjectId(department_id)}).count()\
                or not Specialization.objects.raw({"_id": ObjectId(spec_id)}).count():
            result = {"result": ERR.NO_DATA}
        else:
            person_spec = PersonSpecialization(
                Person(_id=person_id),
                Department(_id=department_id),
                Specialization(_id=spec_id),
                level
            )
            person_spec.save()
            result = {"result": ERR.OK,
                      "id": str(person_spec.pk)}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/persons/specializations/<string:_id>", methods=['DELETE'])
@required_auth("admin")
def delete_person_specialization(_id):
    return delete_resource(PersonSpecialization, _id)


@bp.route("/persons/<string:id>/specializations", methods=['GET'])
def get_person_specializations(id):
    lst = []
    try:
        if Person.objects.raw({"_id": ObjectId(id)}).count():
            for p_spec in PersonSpecialization.objects.raw({"person_id": ObjectId(id)}):
                d = {"id": str(p_spec.pk),
                     "department_id": str(p_spec.department_id.pk),
                     "level": p_spec.level,
                     "specialization_type": p_spec.specialization_id.type,
                     "is_active": str(p_spec.is_active)
                     }
                if p_spec.specialization_id.detail: d.update({"specialization_detail": p_spec.specialization_id.detail})
                if p_spec.details: d.update({"additional_details": p_spec.details})
                lst.append(d)

            result = {"result": ERR.OK, "list":lst}
        else:
            result = {"result": ERR.NO_DATA}
    except Exception as e:
        result = {"result": ERR.DB,
                  "error_message": str(e)}
    return jsonify(result), 200


@bp.route("/persons/specializations/<string:_id>", methods=['PATCH'])
@required_auth("admin")
def set_person_specialization_additions(_id):
    content_header = request.headers.get('Content-Type')
    is_active = None
    details = None
    if 'is_active' in request.args:
        string = request.args['is_active']
        if string == "true":
            is_active = True
        elif string == "false":
            is_active = False
        else:
            return jsonify({"result": ERR.INPUT}), 200
    elif content_header:
        details = request.get_json()
    else:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        if PersonSpecialization(_id=_id) in PersonSpecialization.objects.raw({"_id": ObjectId(_id)}):
            p_spec = PersonSpecialization(_id=_id)
            p_spec.refresh_from_db()
            if is_active is not None: p_spec.is_active = is_active
            if details: p_spec.details = details
            p_spec.save()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except Exception as ex:
        print(ex)
        result = {"result": ERR.DB, "error_message": str(ex)}

    return jsonify(result), 200