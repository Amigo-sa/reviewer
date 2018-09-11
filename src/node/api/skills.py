# -*- coding: utf-8 -*-
from bson import ObjectId
import node.settings.errors as ERR
import node.settings.constants as constants
from flask import Blueprint, request, jsonify
from data.reviewer_model import *
from node.api.auth import required_auth
from node.api.base_functions import delete_resource, list_resources, add_resource

bp = Blueprint('skills', __name__)


@bp.route("/skill_types", methods = ['POST'])
@required_auth("admin")
def add_skill_type():
    return add_resource(SkillType,
                        ["name"])


@bp.route("/skill_types/<string:id>", methods = ['DELETE'])
@required_auth("admin")
def delete_skill_type(id):
    return delete_resource(SkillType, id)


@bp.route("/skill_types", methods = ['GET'])
def list_skill_types():
    return list_resources(SkillType,
                          {"id": "_id",
                           "name": "name"})


@bp.route("/skill_types/<string:id>/soft_skills", methods = ['POST'])
@required_auth("admin")
def add_soft_skill(id):
    return add_resource(SoftSkill,
                        ["name"],
                        SkillType,
                        id,
                        "skill_type_id")


@bp.route("/soft_skills/<string:id>", methods = ['DELETE'])
@required_auth("admin")
def delete_soft_skill(id):
    return delete_resource(SoftSkill, id)


@bp.route("/soft_skills", methods = ['GET'])
def list_soft_skills():
    return list_resources(SoftSkill,
                          {"id": "_id",
                           "name": "name",
                           "skill_type": "skill_type_id"})


@bp.route("/skill_types/<string:id>/hard_skills", methods = ['POST'])
@required_auth("admin")
def add_hard_skill(id):
    return add_resource(HardSkill,
                        ["name"],
                        SkillType,
                        id,
                        "skill_type_id")


@bp.route("/hard_skills/<string:id>", methods = ['DELETE'])
@required_auth("admin")
def delete_hard_skill(id):
    return delete_resource(HardSkill, id)


@bp.route("/hard_skills", methods = ['GET'])
def list_hard_skills():
    return list_resources(HardSkill,
                          {"id": "_id",
                           "name": "name",
                           "skill_type": "skill_type_id"})
