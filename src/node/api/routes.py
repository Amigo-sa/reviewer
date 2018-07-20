from bson import ObjectId
import node.settings.errors as ERR
from flask import Blueprint, request, jsonify
from data.reviewer_model import *


bp = Blueprint('routes', __name__)

if __debug__:
    import node.settings.constants as constants
    import pymongo
    rev_client = pymongo.MongoClient(constants.mongo_db)
    rev_db = rev_client["reviewer"]

    @bp.route('/')
    @bp.route('/index')
    def index():
        collection_names = rev_db.list_collection_names()
        result_string = "Db content: <br>"
        for name in collection_names:
            result_string += "Column: {0}<br>".format(name)
            collection = rev_db[name]
            cursor = collection.find({})
            for document in cursor:
                  result_string += "document: {0}<br>".format(document)
        return result_string

@bp.route("/shutdown", methods = ['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    result = {"result": ERR.OK}
    return jsonify(result), 200

@bp.route("/organizations", methods = ['POST'])
def add_organization():
    req = request.get_json()
    try:
        name = req['name']
    except:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        organization = Organization(name)
        organization.save()
        result = {"result":ERR.OK,
                  "id": str(organization.pk)}
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/organizations/<string:id>", methods = ['DELETE'])
def delete_organization(id):
    try:
        if Organization(_id=id) in Organization.objects.raw({"_id":ObjectId(id)}):
            Organization(_id=id).delete()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


@bp.route("/organizations", methods = ['GET'])
def list_organizations():
    list = []
    try:
        for organization in  Organization.objects.all():
            list.append({"id":str(organization.pk),
                         "name":organization.name}
                        )
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/organizations/<string:id>/departments", methods = ['POST'])
def add_department(id):
    req = request.get_json()
    try:
        name = req['name']
    except:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        department = Department(name, Organization(_id=id))
        department.save()
        result = {"result":ERR.OK,
                  "id": str(department.pk)}
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/departments/<string:id>", methods = ['DELETE'])
def delete_department(id):
    try:
        if Department(_id=id) in Department.objects.raw({"_id":ObjectId(id)}):
            Department(_id=id).delete()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


@bp.route("/organizations/<string:id>/departments", methods = ['GET'])
def list_departments(id):
    list = []
    try:
        for department in  Department.objects.raw({"organization_id":ObjectId(id)}):
            list.append({"id":str(department.pk),
                         "name":department.name}
                        )
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/departments/<string:id>/groups", methods = ['POST'])
def add_group(id):
    req = request.get_json()
    try:
        name = req['name']
    except:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        group = Group(Department(_id=id), name)
        group.save()
        result = {"result":ERR.OK,
                  "id": str(group.pk)}
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/groups/<string:id>", methods = ['DELETE'])
def delete_group(id):
    try:
        if Group(_id=id) in Group.objects.raw({"_id":ObjectId(id)}):
            Group(_id=id).delete()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


@bp.route("/departments/<string:id>/groups", methods = ['GET'])
def list_groups(id):
    list = []
    try:
        for group in  Group.objects.raw({"department_id":ObjectId(id)}):
            list.append({"id":str(group.pk),
                         "name":group.name}
                        )
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/group_roles", methods = ['POST'])
def add_group_role():
    req = request.get_json()
    try:
        name = req['name']
    except:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        group_role = GroupRole(name)
        group_role.save()
        result = {"result":ERR.OK,
                  "id": str(group_role.pk)}
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/group_roles/<string:id>", methods = ['DELETE'])
def delete_group_role(id):
    try:
        if GroupRole(_id=id) in GroupRole.objects.raw({"_id":ObjectId(id)}):
            GroupRole(_id=id).delete()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


@bp.route("/group_roles", methods = ['GET'])
def list_group_roles():
    list = []
    try:
        for group_role in  GroupRole.objects.all():
            list.append({"id":str(group_role.pk),
                         "name":group_role.name}
                        )
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/group_permissions", methods = ['POST'])
def add_group_permission():
    req = request.get_json()
    try:
        name = req['name']
    except:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        group_permission = GroupPermission(name)
        group_permission.save()
        result = {"result":ERR.OK,
                  "id": str(group_permission.pk)}
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/group_permissions/<string:id>", methods = ['DELETE'])
def delete_group_permission(id):
    try:
        if GroupPermission(_id=id) in GroupPermission.objects.raw({"_id":ObjectId(id)}):
            GroupPermission(_id=id).delete()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


@bp.route("/group_permissions", methods = ['GET'])
def list_group_permissions():
    list = []
    try:
        for group_permission in  GroupPermission.objects.all():
            list.append({"id":str(group_permission.pk),
                         "name":group_permission.name}
                        )
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/groups/<string:id>/roles_in_group", methods=['POST'])
def add_role_in_group(id):
    req = request.get_json()
    try:
        person_id = req['person_id']
        role_id = req['role_id']
        default_permission_id = req['default_permission_id']
    except:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        role_in_group = RoleInGroup(Person(_id=person_id),
                                    Group(_id=id),
                                    GroupRole(_id=role_id),
                                    [GroupPermission(_id=default_permission_id)])
        role_in_group.save()
        result = {"result":ERR.OK,
                  "id": str(role_in_group.pk)}
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/roles_in_group/<string:id>", methods=['DELETE'])
def delete_role_in_group(id):
    try:
        if RoleInGroup(_id=id) in RoleInGroup.objects.raw({"_id":ObjectId(id)}):
            RoleInGroup(_id=id).delete()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/groups/<string:id>/roles_in_group", methods=['GET'])
def list_roles_in_group_by_group_id(id):
    list = []
    try:
        for role_in_group in  RoleInGroup.objects.raw({"group_id": ObjectId(id)}):
            list.append({"id": str(role_in_group.pk)})
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/persons/<string:id>/roles_in_group", methods=['GET'])
def list_roles_in_group_by_person_id(id):
    list = []
    try:
        for role_in_group in RoleInGroup.objects.raw({"person_id": ObjectId(id)}):
            list.append({"id": str(role_in_group.pk)})
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/roles_in_group/<string:id>", methods=['GET'])
def get_role_in_group_info(id):
    try:
        if RoleInGroup(_id=id) in RoleInGroup.objects.raw({"_id": ObjectId(id)}):
            role_in_group = RoleInGroup(_id=id)
            role_in_group.refresh_from_db()
            perm = []
            for item in role_in_group.permissions:
                perm.append(str(item.pk))
            data = {"person_id": str(role_in_group.person_id.pk),
                    "group_id": str(role_in_group.group_id.pk),
                    "role_id": str(role_in_group.role_id.pk),
                    "permissions": perm}
            result = {"result": ERR.OK, "data": data}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/roles_in_group/<string:id>/permissions", methods = ['POST'])
def add_permissions_to_role_in_group(id):
    req = request.get_json()
    try:
        group_permission_id = req['group_permission_id']
    except:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        if RoleInGroup(_id=id) in RoleInGroup.objects.raw({"_id": ObjectId(id)}):
            role_in_group = RoleInGroup(_id=id)
            role_in_group.refresh_from_db()
            permission = GroupPermission(_id=group_permission_id)
            permission.refresh_from_db()
            role_in_group.permissions.append(permission)
            role_in_group.save()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/roles_in_group/<string:id1>/permissions/<string:id2>", methods = ['DELETE'])
def delete_permissions_from_role_in_group(id1, id2):
    try:
        if RoleInGroup(_id=id1) in RoleInGroup.objects.raw({"_id": ObjectId(id1)}):
            role_in_group = RoleInGroup(_id=id1)
            role_in_group.refresh_from_db()
            permission = GroupPermission(_id=id2)
            permission.refresh_from_db()
            if permission not in role_in_group.permissions:
                result = {"result": ERR.NO_DATA}
            else:
                role_in_group.permissions.remove(permission)
                role_in_group.save()
                result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/general_roles", methods=['POST'])
def add_general_role():
    req = request.get_json()
    try:
        person_id = req['person_id']
        department_id = req['department_id']
        role_type = req['role_type']
        role_data = req['role_data']
    except:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        if role_type == "Tutor":
            tutor_role = TutorRole(Person(_id=person_id),
                                   Department(_id=department_id),
                                   role_data)
            tutor_role.save()
            result = {"result": ERR.OK,
                      "id": str(tutor_role.pk)}
        else:
            if role_type == "Studend":
                student_role = StudentRole(Person(_id=person_id),
                                           Department(_id=department_id),
                                           role_data)
                student_role.save()
                result = {"result": ERR.OK,
                          "id": str(student_role.pk)}
            else:
                return jsonify({"result": ERR.INPUT}), 200
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/general_roles/<string:id>", methods=['DELETE'])
def delete_general_role(id):
    try:
        if TutorRole(_id=id) in TutorRole.objects.raw({"_id":ObjectId(id)}):
            TutorRole(_id=id).delete()
            result = {"result": ERR.OK}
        else:
            if StudentRole(_id=id) in StudentRole.objects.raw({"_id":ObjectId(id)}):
                StudentRole(_id=id).delete()
                result = {"result": ERR.OK}
            else:
                result = {"result": ERR.NO_DATA}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/general_roles/<string:id>", methods=['GET'])
def get_general_roles_data(id):
    try:
        if StudentRole(_id=id) in StudentRole.objects.raw({"_id": ObjectId(id)}):
            student_role = StudentRole(_id=id)
            student_role.refresh_from_db()
            data = {"person_id": str(student_role.person_id.pk),
                    "department_id": str(student_role.department_id.pk),
                    "role_type": "Student",
                    "description": student_role.description}
            result = {"result": ERR.OK, "data": data}
        else:
            if TutorRole(_id=id) in TutorRole.objects.raw({"_id": ObjectId(id)}):
                tutor_role = TutorRole(_id=id)
                tutor_role.refresh_from_db()
                data = {"person_id": str(tutor_role.person_id.pk),
                        "department_id": str(tutor_role.department_id.pk),
                        "role_type": "Tutor",
                        "description": tutor_role.discipline}
                result = {"result": ERR.OK, "data": data}
            else:
                result = {"result": ERR.NO_DATA}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/persons/<string:id>/general_roles", methods=['GET'])
def list_roles_by_person_id(id):
    list = []
    try:
        for role in StudentRole.objects.raw({"person_id": ObjectId(id)}):
            list.append({"id": str(role.pk)})
        for role in TutorRole.objects.raw({"person_id": ObjectId(id)}):
            list.append({"id": str(role.pk)})
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/persons", methods=['GET'])
def find_persons():
    lst = []
    if 'group_id' in request.args:
        group_id = request.args['group_id']
    else:
        group_id = None
    if 'department_id' in request.args:
        department_id = request.args['department_id']
    else:
        department_id = None
    if 'organization_id' in request.args:
        organization_id = request.args['organization_id']
    else:
        organization_id = None
    try:
        if group_id:
            for role in RoleInGroup.objects.raw({"group_id": ObjectId(group_id)}):
                lst.append({"id": str(role.person_id.pk)})
            list = [dict(t) for t in set([tuple(d.items()) for d in lst])]
            result = {"result": ERR.OK, "list":list}
        else:
            if department_id:
                for role in StudentRole.objects.raw({"department_id": ObjectId(department_id)}):
                    lst.append({"id": str(role.person_id.pk)})
                for role in TutorRole.objects.raw({"department_id": ObjectId(department_id)}):
                    lst.append({"id": str(role.person_id.pk)})
                list = [dict(t) for t in set([tuple(d.items()) for d in lst])]
                result = {"result": ERR.OK, "list": list}
            else:
                if organization_id:
                    for department in Department.objects.raw({"organization_id":ObjectId(organization_id)}):
                        for role in StudentRole.objects.raw({"department_id": department.pk}):
                            lst.append({"id": str(role.person_id.pk)})
                        for role in TutorRole.objects.raw({"department_id": department.pk}):
                            lst.append({"id": str(role.person_id.pk)})
                    list = [dict(t) for t in set([tuple(d.items()) for d in lst])]
                    result = {"result": ERR.OK, "list": list}
                else:
                    result = {"result": ERR.INPUT}
    except Exception as ex:
        print(ex)
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/reviews", methods = ['POST'])
def post_review():
    req = request.get_json()
    try:
        type = req['type']
        reviewer_id = ObjectId(req['reviewer_id'])
        subject_id = ObjectId(req['subject_id'])
        value = req['value']
        description = req['description']
    except:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        obj = {
            "StudentRole":
                SRReview(reviewer_id, subject_id, value, description),
            "TutorRole":
                TRReview(reviewer_id, subject_id, value, description),
            "HardSkill":
                HSReview(reviewer_id, subject_id, value, description),
            "SoftSkill":
                SSReview(reviewer_id, subject_id, value, description),
            "Group":
                GroupReview(reviewer_id, subject_id, value, description),
            "GroupTest":
                GroupTestReview(reviewer_id, subject_id, value, description),
            "RoleInGroup":
                RoleInGroupReview(reviewer_id, subject_id, value, description)
        }
        if type not in obj:
            result = {"result": ERR.INPUT}
        else:
            obj[type].save()
            result = {"result":ERR.OK,
                      "id": str(obj[type].pk)}
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/reviews/<string:id>", methods=['DELETE'])
def delete_review(id):
    try:
        result = {"result": ERR.NO_DATA}
        if SRReview(_id=id) in SRReview.objects.raw({"_id":ObjectId(id)}):
            SRReview(_id=id).delete()
            result = {"result": ERR.OK}
        if TRReview(_id=id) in TRReview.objects.raw({"_id":ObjectId(id)}):
            TRReview(_id=id).delete()
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
        if RoleInGroupReview(_id=id) in RoleInGroupReview.objects.raw({"_id":ObjectId(id)}):
            RoleInGroupReview(_id=id).delete()
            result = {"result": ERR.OK}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/reviews", methods=['GET'])
def find_reviews():
    lst = []
    query = {}
    if 'reviewer_id' in request.args:
        reviewer_id = request.args['reviewer_id']
        query.update({"reviewer_id": ObjectId(reviewer_id)})
    if 'subject_id' in request.args:
        subject_id = request.args['subject_id']
        query.update({"subject_id": ObjectId(subject_id)})

    try:
        for review in SRReview.objects.raw(query):
            lst.append({"id": str(review.pk)})
        for review in TRReview.objects.raw(query):
            lst.append({"id": str(review.pk)})
        for review in HSReview.objects.raw(query):
            lst.append({"id": str(review.pk)})
        for review in SSReview.objects.raw(query):
            lst.append({"id": str(review.pk)})
        for review in GroupReview.objects.raw(query):
            lst.append({"id": str(review.pk)})
        for review in GroupTestReview.objects.raw(query):
            lst.append({"id": str(review.pk)})
        for review in RoleInGroupReview.objects.raw(query):
            lst.append({"id": str(review.pk)})
        result = {"result": ERR.OK, "list": lst}
    except Exception as ex:
        print(ex)
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/soft_skills", methods = ['POST'])
def add_soft_skill():
    req = request.get_json()
    try:
        name = req['name']
        soft_skill = SoftSkill(name)
        soft_skill.save()
        result = {"result":ERR.OK,
                  "id": str(soft_skill.pk)}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/soft_skills/<string:id>", methods = ['DELETE'])
def delete_soft_skill(id):
    try:
        if SoftSkill(_id=id) in SoftSkill.objects.raw({"_id":ObjectId(id)}):
            SoftSkill(_id=id).delete()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


@bp.route("/soft_skills", methods = ['GET'])
def list_soft_skills():
    list = []
    try:
        for soft_skill in  SoftSkill.objects.all():
            list.append({"id":str(soft_skill.pk),
                         "name":soft_skill.name}
                        )
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/hard_skills", methods = ['POST'])
def add_hard_skill():
    req = request.get_json()
    try:
        name = req['name']
        hard_skill = HardSkill(name)
        hard_skill.save()
        result = {"result":ERR.OK,
                  "id": str(hard_skill.pk)}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/hard_skills/<string:id>", methods = ['DELETE'])
def delete_hard_skill(id):
    try:
        if HardSkill(_id=id) in HardSkill.objects.raw({"_id":ObjectId(id)}):
            HardSkill(_id=id).delete()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


@bp.route("/hard_skills", methods = ['GET'])
def list_hard_skills():
    list = []
    try:
        for hard_skill in  HardSkill.objects.all():
            list.append({"id":str(hard_skill.pk),
                         "name":hard_skill.name}
                        )
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/persons/<string:id>/soft_skills", methods=['POST'])
def add_person_soft_skill(id):
    req = request.get_json()
    try:
        ss_id = req['ss_id']
        default_level = 50.0
        person_ss = PersonSS(Person(_id=id),
                             SoftSkill(_id=ss_id),
                             default_level)
        person_ss.save()
        result = {"result":ERR.OK,
                  "id": str(person_ss.pk)}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/persons/<string:id>/hard_skills", methods=['POST'])
def add_person_hard_skill(id):
    req = request.get_json()
    try:
        hs_id = req['hs_id']
        default_level = 50.0
        person_hs = PersonHS(Person(_id=id),
                             HardSkill(_id=hs_id),
                             default_level)
        person_hs.save()
        result = {"result":ERR.OK,
                  "id": str(person_hs.pk)}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/persons/soft_skills/<string:id>", methods = ['DELETE'])
def delete_person_soft_skill(id):
    try:
        if PersonSS(_id=id) in PersonSS.objects.raw({"_id":ObjectId(id)}):
            PersonSS(_id=id).delete()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


@bp.route("/persons/hard_skills/<string:id>", methods = ['DELETE'])
def delete_person_hard_skill(id):
    try:
        if PersonHS(_id=id) in PersonHS.objects.raw({"_id":ObjectId(id)}):
            PersonHS(_id=id).delete()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


@bp.route("/persons/soft_skills", methods=['GET'])
def find_person_soft_skills():
    lst = []
    query = {}
    if 'person_id' in request.args:
        person_id = request.args['person_id']
        query.update({"person_id": ObjectId(person_id)})
    if 'ss_id' in request.args:
        ss_id = request.args['ss_id']
        query.update({"ss_id": ObjectId(ss_id)})
    try:
        for person_ss in PersonSS.objects.raw(query):
            lst.append({"id": str(person_ss.pk)})
        result = {"result": ERR.OK, "list": lst}
    except Exception as ex:
        print(ex)
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/persons/hard_skills", methods=['GET'])
def find_person_hard_skills():
    lst = []
    query = {}
    if 'person_id' in request.args:
        person_id = request.args['person_id']
        query.update({"person_id": ObjectId(person_id)})
    if 'hs_id' in request.args:
        hs_id = request.args['hs_id']
        query.update({"hs_id": ObjectId(hs_id)})
    try:
        for person_hs in PersonHS.objects.raw(query):
            lst.append({"id": str(person_hs.pk)})
        result = {"result": ERR.OK, "list": lst}
    except Exception as ex:
        print(ex)
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/persons/soft_skills/<string:id>", methods=['GET'])
def get_person_soft_skill_info(id):
    try:
        if PersonSS(_id=id) in PersonSS.objects.raw({"_id": ObjectId(id)}):
            person_ss = PersonSS(_id=id)
            person_ss.refresh_from_db()
            data = {"person_id": str(person_ss.person_id.pk),
                    "ss_id": str(person_ss.ss_id.pk),
                    "level": str(person_ss.level)}
            result = {"result": ERR.OK, "data": data}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/persons/hard_skills/<string:id>", methods=['GET'])
def get_person_hard_skill_info(id):
    try:
        if PersonHS(_id=id) in PersonHS.objects.raw({"_id": ObjectId(id)}):
            person_hs = PersonHS(_id=id)
            person_hs.refresh_from_db()
            data = {"person_id": str(person_hs.person_id.pk),
                    "hs_id": str(person_hs.hs_id.pk),
                    "level": str(person_hs.level)}
            result = {"result": ERR.OK, "data": data}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/groups/<string:id>/tests", methods = ['POST'])
def add_group_test(id):
    req = request.get_json()
    try:
        name = req['name']
        info = req['info']
        group_test = GroupTest(Group(_id=id), name, info)
        group_test.save()
        result = {"result":ERR.OK,
                  "id": str(group_test.pk)}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


@bp.route("/tests/<string:id>", methods = ['DELETE'])
def delete_group_test(id):
    try:
        if GroupTest(_id=id) in GroupTest.objects.raw({"_id":ObjectId(id)}):
            GroupTest(_id=id).delete()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


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
    list = []
    try:
        for group_test in GroupTest.objects.raw({"group_id": ObjectId(id)}):
            list.append({"id": str(group_test.pk)})
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/tests/<string:id>/results", methods = ['POST'])
def add_test_result(id):
    req = request.get_json()
    try:
        person_id = req['person_id']
        result_data = req['result_data']
        test_result = TestResult(GroupTest(_id=id), Person(_id=person_id), result_data)
        test_result.save()
        result = {"result":ERR.OK,
                  "id": str(test_result.pk)}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


@bp.route("/tests/results/<string:id>", methods = ['DELETE'])
def delete_test_result(id):
    try:
        if TestResult(_id=id) in TestResult.objects.raw({"_id":ObjectId(id)}):
            TestResult(_id=id).delete()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


@bp.route("/tests/results/<string:id>", methods=['GET'])
def get_test_result_info(id):
    try:
        if TestResult(_id=id) in TestResult.objects.raw({"_id": ObjectId(id)}):
            test_result = TestResult(_id=id)
            test_result.refresh_from_db()
            data = {"test_id": str(test_result.test_id.pk),
                    "person_id": str(test_result.person_id.pk),
                    "result_data": str(test_result.result_data)}
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
    if 'person_id' in request.args:
        person_id = request.args['person_id']
        query.update({"person_id": ObjectId(person_id)})
    if 'test_id' in request.args:
        test_id = request.args['test_id']
        query.update({"test_id": ObjectId(test_id)})
    try:
        for test_result in TestResult.objects.raw(query):
            lst.append({"id": str(test_result.pk)})
        result = {"result": ERR.OK, "list": lst}
    except Exception as ex:
        print(ex)
        result = {"result": ERR.DB}
    return jsonify(result), 200