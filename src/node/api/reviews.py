# -*- coding: utf-8 -*-
from bson import ObjectId
import node.settings.errors as ERR
import node.settings.constants as constants
from flask import Blueprint, request, jsonify
from data.reviewer_model import *
from node.api.auth import required_auth
from node.api.base_functions import delete_resource, list_resources

bp = Blueprint('reviews', __name__)


def post_review(review_type, subject_id):
    req = request.get_json()
    try:
        reviewer_id = ObjectId(req['reviewer_id'])
        subject_id = ObjectId(subject_id)
        value = req['value']
        description = req['description']
        obj = {
            "SpecializationReview":
                SpecializationReview(reviewer_id, subject_id, value, description),
            "Group":
                GroupReview(reviewer_id, subject_id, value, description),
            "GroupTest":
                GroupTestReview(reviewer_id, subject_id, value, description),
            "GroupMember":
                GroupMemberReview(reviewer_id, subject_id, value, description)
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
                    and subj.person_id.pk == reviewer_id:
                    result = {"result": ERR.AUTH}
                else:
                    obj[review_type].save()
                    result = {"result":ERR.OK,
                              "id": str(obj[review_type].pk)}
            else:
                result = {"result": ERR.NO_DATA}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/specializations/<string:id>/reviews", methods = ['POST'])
@required_auth("reviewer")
def post_specialization_review(id):
    return post_review("SpecializationReview", id)


@bp.route("/groups/<string:id>/reviews", methods = ['POST'])
@required_auth("reviewer")
def post_group_review(id):
    return post_review("Group", id)


@bp.route("/tests/<string:id>/reviews", methods = ['POST'])
@required_auth("reviewer")
def post_group_test_review(id):
    return post_review("GroupTest", id)


@bp.route("/group_members/<string:id>/reviews", methods = ['POST'])
@required_auth("reviewer")
def post_group_member_review(id):
    return post_review("GroupMember", id)


def post_person_skill_review(skill_review_cls, p_id, s_id):
    req = request.get_json()
    try:
        reviewer_id = ObjectId(req['reviewer_id'])
        value = req['value']
        description = req['description']
        if req["reviewer_id"] == p_id:
            return jsonify({"result": ERR.AUTH}), 200
        person_skill_cls = None
        query = {}
        query.update({"person_id": ObjectId(p_id)})
        if skill_review_cls == HSReview:
            person_skill_cls = PersonHS
            skill_cls = HardSkill
            query.update({"hs_id": ObjectId(s_id)})
        elif skill_review_cls == SSReview:
            person_skill_cls = PersonSS
            skill_cls = SoftSkill
            query.update({"ss_id": ObjectId(s_id)})
        else:
            raise Exception("post_person_skill_review() invalid args")
        if not Person.objects.raw({"_id":reviewer_id}).count():
            return jsonify({"result": ERR.NO_DATA}), 200
        if not Person.objects.raw({"_id":ObjectId(p_id)}).count():
            return jsonify({"result": ERR.NO_DATA}), 200
        if not skill_cls.objects.raw({"_id":ObjectId(s_id)}).count():
            return jsonify({"result": ERR.NO_DATA}), 200
        person_s = person_skill_cls.objects.raw(query)
        if person_s.count():
            person_s = person_s.first()
        else:
            default_level = 50.0
            person_s = person_skill_cls(Person(_id=p_id),
                                        skill_cls(_id=s_id),
                                        default_level)
            person_s.save()
        s_review = skill_review_cls(reviewer_id, person_s.pk, value, description)
        s_review.save()

        result = {"result": ERR.OK,
                  "id": str(s_review.pk)}

    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except Exception as e:
        result = {"result": ERR.DB,
                  "error_message": str(e)}

    return jsonify(result), 200


@bp.route("/persons/<string:p_id>/hard_skills/<string:hs_id>/reviews", methods = ['POST'])
@required_auth("reviewer")
def post_person_hard_skill_review(p_id, hs_id):
    return post_person_skill_review(HSReview, p_id, hs_id)


@bp.route("/persons/<string:p_id>/soft_skills/<string:ss_id>/reviews", methods = ['POST'])
@required_auth("reviewer")
def post_person_soft_skill_review(p_id, ss_id):
    return post_person_skill_review(SSReview, p_id, ss_id)


@bp.route("/reviews/<string:id>", methods=['DELETE'])
@required_auth("reviewer")
def delete_review(id):
    try:
        result = {"result": ERR.NO_DATA}
        if SpecializationReview(_id=id) in SpecializationReview.objects.raw({"_id":ObjectId(id)}):
            SpecializationReview(_id=id).delete()
            result = {"result": ERR.OK}
        if HSReview(_id=id) in HSReview.objects.raw({"_id":ObjectId(id)}):
            HSReview(_id=id).delete()
            result = {"result": ERR.OK}
        if SSReview(_id=id) in SSReview.objects.raw({"_id":ObjectId(id)}):
            SSReview(_id=id).delete()
            result = {"result": ERR.OK}
        if GroupReview(_id=id) in GroupReview.objects.raw({"_id":ObjectId(id)}):
            GroupReview(_id=id).delete()
            result = {"result": ERR.OK}
        if GroupTestReview(_id=id) in GroupTestReview.objects.raw({"_id":ObjectId(id)}):
            GroupTestReview(_id=id).delete()
            result = {"result": ERR.OK}
        if GroupMemberReview(_id=id) in GroupMemberReview.objects.raw({"_id":ObjectId(id)}):
            GroupMemberReview(_id=id).delete()
            result = {"result": ERR.OK}
    except:
        result = {"result": ERR.DB}
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
                "description" : subject.description}
        result = {"result": ERR.OK, "data": data}
    except Exception as e:
        result = {"result": ERR.DB, "error_message" : str(e)}
    return jsonify(result), 200


@bp.route("/reviews", methods=['GET'])
def find_reviews():
    lst = []
    query = {}
    try:
        err = ERR.OK
        if 'reviewer_id' in request.args:
            reviewer_id = request.args['reviewer_id']
            if Person.objects.raw({"_id":ObjectId(reviewer_id)}).count():
                query.update({"reviewer_id": ObjectId(reviewer_id)})
            else:
                err = ERR.NO_DATA
        if 'subject_id' in request.args:
            subject_id = request.args['subject_id']
            query.update({"subject_id": ObjectId(subject_id)})
        if err == ERR.OK:
            for review in SpecializationReview.objects.raw(query):
                lst.append({"id": str(review.pk)})
            for review in HSReview.objects.raw(query):
                lst.append({"id": str(review.pk)})
            for review in SSReview.objects.raw(query):
                lst.append({"id": str(review.pk)})
            for review in GroupReview.objects.raw(query):
                lst.append({"id": str(review.pk)})
            for review in GroupTestReview.objects.raw(query):
                lst.append({"id": str(review.pk)})
            for review in GroupMemberReview.objects.raw(query):
                lst.append({"id": str(review.pk)})
            result = {"result": ERR.OK, "list": lst}
        else:
            result = {"result": ERR.NO_DATA}
    except KeyError:
        result = {"result": ERR.INPUT}
    except Exception as ex:
        result = {"result": ERR.DB,
                  "error_message": str(ex)}
    return jsonify(result), 200