# -*- coding: utf-8 -*-
from bson import ObjectId
import node.settings.errors as ERR
import node.settings.constants as constants
from flask import Blueprint, request, jsonify
from data.reviewer_model import *
from pymodm.errors import DoesNotExist
from node.api.auth import required_auth
from node.api.base_functions import delete_resource, list_resources

bp = Blueprint('reviews', __name__)


def post_review(review_type, subject_id, reviewer_id):
    req = request.get_json()
    try:
        subject_id = ObjectId(subject_id)
        value = req['value']
        topic = req['topic']
        description = req['description']
        obj = {
            "SpecializationReview":
                SpecializationReview(reviewer_id, subject_id, value, topic, description),
            "Group":
                GroupReview(reviewer_id, subject_id, value, topic, description),
            "GroupTest":
                GroupTestReview(reviewer_id, subject_id, value, topic, description),
            "GroupMember":
                GroupMemberReview(reviewer_id, subject_id, value, topic, description)
        }
        subj_class = {
            "SpecializationReview":
                PersonSpecialization,
            "Group":
                Group,
            "GroupTest":
                GroupTest,
            "GroupMember":
                GroupMember
        }
        if review_type not in obj:
            result = {"result": ERR.INPUT}
        else:
            if subj_class[review_type].objects.raw({"_id":ObjectId(subject_id)}).count() \
                    and Person.objects.raw({"_id":ObjectId(reviewer_id)}).count():
                subj = subj_class[review_type].objects.get({"_id":ObjectId(subject_id)})
                # проверка не является оставляет ли человек отзыв на себя
                if review_type != "GroupTest" and review_type != "Group"\
                    and str(subj.person_id.pk) == reviewer_id:
                    result = {"result": ERR.AUTH}
                else:
                    obj[review_type].save()
                    result = {"result":ERR.OK,
                              "id": str(obj[review_type].pk)}
            else:
                result = {"result": ERR.NO_DATA}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except Exception as e:
        result = {"result":ERR.DB,
                  "error_message": str(e)}

    return jsonify(result), 200


@bp.route("/specializations/<string:id>/reviews", methods = ['POST'])
@required_auth("reviewer")
def post_specialization_review(id, reviewer_id):
    return post_review("SpecializationReview", id, reviewer_id)


@bp.route("/groups/<string:id>/reviews", methods = ['POST'])
@required_auth("reviewer")
def post_group_review(id, reviewer_id):
    return post_review("Group", id, reviewer_id)


@bp.route("/tests/<string:id>/reviews", methods = ['POST'])
@required_auth("reviewer")
def post_group_test_review(id, reviewer_id):
    return post_review("GroupTest", id, reviewer_id)


@bp.route("/group_members/<string:id>/reviews", methods = ['POST'])
@required_auth("reviewer")
def post_group_member_review(id, reviewer_id):
    return post_review("GroupMember", id, reviewer_id)


def post_person_skill_review(skill_review_cls, p_id, s_id, reviewer_id):
    req = request.get_json()
    try:
        if reviewer_id == p_id:
            return jsonify({"result": ERR.AUTH}), 200
        if skill_review_cls != SSReview and skill_review_cls != HSReview:
            return jsonify({"result": ERR.INPUT}), 200
        value = req['value']
        topic = req['topic']
        description = req['description']
        review_id = add_person_skill_review(skill_review_cls,
                                             reviewer_id,
                                             p_id,
                                             s_id,
                                             value,
                                             topic,
                                             description)
        result = {"result": ERR.OK,
                  "id": review_id}
    except DoesNotExist as e:
        return jsonify({"result": ERR.NO_DATA,
                        "error_message": str(e)})
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except Exception as e:
        print(e)
        result = {"result": ERR.DB,
                  "error_message": str(e)}

    return jsonify(result), 200


@bp.route("/persons/<string:p_id>/hard_skills/<string:hs_id>/reviews", methods = ['POST'])
@required_auth("reviewer")
def post_person_hard_skill_review(p_id, hs_id, reviewer_id):
    return post_person_skill_review(HSReview, p_id, hs_id, reviewer_id)


@bp.route("/persons/<string:p_id>/soft_skills/<string:ss_id>/reviews", methods = ['POST'])
@required_auth("reviewer")
def post_person_soft_skill_review(p_id, ss_id, reviewer_id):
    return post_person_skill_review(SSReview, p_id, ss_id, reviewer_id)


@bp.route("/reviews/<string:id>", methods=['DELETE'])
@required_auth("reviewer")
def delete_review(id):
    try:
        err = ERR.NO_DATA
        review_cls = None
        if SpecializationReview(_id=id) in SpecializationReview.objects.raw({"_id":ObjectId(id)}):
            review_cls = SpecializationReview
        elif HSReview(_id=id) in HSReview.objects.raw({"_id":ObjectId(id)}):
            review_cls = HSReview
        elif SSReview(_id=id) in SSReview.objects.raw({"_id":ObjectId(id)}):
            review_cls = SSReview
        elif GroupReview(_id=id) in GroupReview.objects.raw({"_id":ObjectId(id)}):
            review_cls = GroupReview
        elif GroupTestReview(_id=id) in GroupTestReview.objects.raw({"_id":ObjectId(id)}):
            review_cls = GroupTestReview
        elif GroupMemberReview(_id=id) in GroupMemberReview.objects.raw({"_id":ObjectId(id)}):
            review_cls = GroupMemberReview

        if review_cls:
            err = ERR.OK
            review = review_cls(_id=id)
            review.refresh_from_db()
            review.delete()

        result = {"result": err}
    except Exception as e:
        result = {"result": ERR.DB,
                  "error_message": str(e)}
    return jsonify(result), 200


@bp.route("/reviews/<string:id>", methods=['GET'])
def get_review_info(id):
    try:
        if SpecializationReview(_id=id) in SpecializationReview.objects.raw({"_id":ObjectId(id)}):
            subject = SpecializationReview(_id=id)
        elif HSReview(_id=id) in HSReview.objects.raw({"_id": ObjectId(id)}):
            subject = HSReview(_id=id)
        elif SSReview(_id=id) in SSReview.objects.raw({"_id": ObjectId(id)}):
            subject = SSReview(_id=id)
        elif GroupReview(_id=id) in GroupReview.objects.raw({"_id": ObjectId(id)}):
            subject = GroupReview(_id=id)
        elif GroupTestReview(_id=id) in GroupTestReview.objects.raw({"_id": ObjectId(id)}):
            subject = GroupTestReview(_id=id)
        elif GroupMemberReview(_id=id) in GroupMemberReview.objects.raw({"_id": ObjectId(id)}):
            subject = GroupMemberReview(_id=id)
        else:
            result = {"result": ERR.NO_DATA}
            return jsonify(result), 200
        subject.refresh_from_db()
        data = {"reviewer_id" : str(subject.reviewer_id.pk),
                "subject_id" : str(subject.subject_id.pk),
                "value" : subject.value,
                "topic" : subject.topic,
                "description" : subject.description}
        result = {"result": ERR.OK, "data": data}
    except Exception as e:
        result = {"result": ERR.DB, "error_message" : str(e)}
    return jsonify(result), 200


def find_reviews(subj_cls):
    query = {}
    try:
        err = ERR.OK
        if 'query_start' in request.args:
            start = int(request.args['query_start'])
        else:
            start = 0
        if 'query_limit' in request.args:
            limit = int(request.args['query_limit'])
        else:
            limit = 20
        if 'reviewer_id' in request.args:
            reviewer_id = request.args['reviewer_id']
            if Person.objects.raw({"_id": ObjectId(reviewer_id)}).count():
                query.update({"reviewer_id": ObjectId(reviewer_id)})
            else:
                err = ERR.NO_DATA
        if 'person_id' in request.args:
            person_id = request.args['person_id']
            subjects_qs = subj_cls.objects.raw({"person_id": ObjectId(person_id)})
            subjects = list(ObjectId(key["_id"]) for key in subjects_qs.values())
            query.update({"subject_id": {"$in": subjects}})
        if err == ERR.OK:
            review_classes = {"PersonSpecialization": SpecializationReview,
                              "PersonHS": HSReview,
                              "PersonSS": SSReview}
            review_cls = review_classes[subj_cls.__name__]
            review_qs = review_cls.objects.raw(query)
            reviews = list({"id": str(key["_id"])} for key in review_qs.values())
            result = {"result": ERR.OK, "list": reviews[start:limit:1], "length": len(reviews)}
        else:
            result = {"result": err}
    except KeyError:
        result = {"result": ERR.INPUT}
    except Exception as ex:
        result = {"result": ERR.DB,
                  "error_message": str(ex)}
    return jsonify(result), 200


@bp.route("/specialization_reviews", methods=['GET'])
def find_specialization_reviews():
    return find_reviews(PersonSpecialization)


@bp.route("/hard_skill_reviews", methods=['GET'])
def find_hard_skill_reviews():
    return find_reviews(PersonHS)


@bp.route("/soft_skill_reviews", methods=['GET'])
def find_soft_skill_reviews():
    return find_reviews(PersonSS)