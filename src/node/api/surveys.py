# -*- coding: utf-8 -*-
from bson import ObjectId
import node.settings.errors as ERR
import node.settings.constants as constants
from flask import Blueprint, request, jsonify
from data.reviewer_model import *
from node.api.auth import required_auth
from node.api.base_functions import delete_resource, list_resources

bp = Blueprint('surveys', __name__)


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