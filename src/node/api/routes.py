# -*- coding: utf-8 -*-
from bson import ObjectId
import node.settings.errors as ERR
import node.settings.constants as constants
from flask import Blueprint, request, jsonify
from data.reviewer_model import *
from node.api.routes_auth import required_auth

bp = Blueprint('routes', __name__)


def delete_resource(cls, _id):
    try:
        if cls(_id=_id) in cls.objects.raw({"_id":ObjectId(_id)}):
            cls(_id=_id).delete()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result":ERR.DB}
    return jsonify(result), 200


@bp.route("/organizations", methods = ['POST'])
@required_auth("admin")
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


@bp.route("/organizations/<string:id>", methods = ['DELETE'])
@required_auth("admin")
def delete_organization(id):
    return delete_resource(Organization, id)


@bp.route("/persons/<string:id>", methods = ['DELETE'])
@required_auth("user")
def delete_person(id):
    return delete_resource(Person, id)


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
@required_auth("admin")
def add_department(id):
    req = request.get_json()
    try:
        name = req['name']
        if Organization(_id=id) in Organization.objects.raw({"_id": ObjectId(id)}):
            department = Department(name, Organization(_id=id))
            department.save()
            result = {"result":ERR.OK,
                      "id": str(department.pk)}
        else:
            result = {"result": ERR.NO_DATA}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/departments/<string:id>", methods = ['DELETE'])
@required_auth("admin")
def delete_department(id):
    return delete_resource(Department, id)


@bp.route("/organizations/<string:id>/departments", methods = ['GET'])
def list_departments(id):
    list = []
    try:
        if Organization(_id=id) in Organization.objects.raw({"_id": ObjectId(id)}):
            for department in  Department.objects.raw({"organization_id":ObjectId(id)}):
                list.append({"id":str(department.pk),
                             "name":department.name}
                            )
            result = {"result": ERR.OK, "list":list}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/departments/<string:id>/groups", methods = ['POST'])
@required_auth("admin")
def add_group(id):
    req = request.get_json()
    try:
        name = req['name']
        if Department(_id=id) in Department.objects.raw({"_id": ObjectId(id)}):
            group = Group(Department(_id=id), name)
            group.save()
            result = {"result":ERR.OK,
                      "id": str(group.pk)}
        else:
            result = {"result": ERR.NO_DATA}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/groups/<string:id>", methods = ['DELETE'])
@required_auth("admin")
def delete_group(id):
    return delete_resource(Group, id)


@bp.route("/groups/<string:id>/role_list", methods=['POST'])
@required_auth("admin")
def set_role_list_for_group(id):
    req = request.get_json()
    try:
        role_list = req['role_list']
        err = ERR.OK
        for group_role_id in role_list:
            if not GroupRole.objects.raw({"_id": ObjectId(group_role_id)}).count():
                err = ERR.NO_DATA
        if Group(_id=id) in Group.objects.raw({"_id": ObjectId(id)}) and err == ERR.OK:
            group = Group(_id=id)
            group.refresh_from_db()
            group.role_list = role_list
            group.save()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except:
        result = {"result": ERR.DB}

    return jsonify(result), 200


@bp.route("/groups/<string:id>/role_list", methods=['GET'])
def get_role_list_for_group(id):
    list = []
    try:
        if Group(_id=id) in Group.objects.raw({"_id": ObjectId(id)}):
            group =  Group(_id=id)
            group.refresh_from_db()
            for role in group.role_list:
                list.append({"id" : str(role.pk)})
            result = {"result": ERR.OK, "list": list}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/departments/<string:id>/groups", methods = ['GET'])
def list_groups(id):
    list = []
    try:
        if Department(_id=id) in Department.objects.raw({"_id": ObjectId(id)}):
            for group in  Group.objects.raw({"department_id":ObjectId(id)}):
                list.append({"id":str(group.pk),
                             "name":group.name}
                            )
            result = {"result": ERR.OK, "list":list}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/group_roles", methods = ['POST'])
@required_auth("admin")
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
@required_auth("admin")
def delete_group_role(id):
    return delete_resource(GroupRole, id)


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
@required_auth("admin")
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
@required_auth("admin")
def delete_group_permission(id):
    return delete_resource(GroupPermission, id)

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


@bp.route("/groups/<string:id>/group_members", methods=['POST'])
@required_auth("admin")
def add_group_member(id):
    req = request.get_json()
    try:
        person_id = req['person_id']
        if Group.objects.raw({"_id": ObjectId(id)}).count() \
                and Person.objects.raw({"_id": ObjectId(person_id)}).count():
            err = ERR.OK
        else:
            err = ERR.NO_DATA
        if 'role_id' in req:
            role_id = req['role_id']
            if not GroupRole.objects.raw({"_id": ObjectId(role_id)}).count():
                err = ERR.NO_DATA
            else:
                group_role = GroupRole(_id=role_id)
        else:
            group_role = None
        if 'default_permission_id' in req:
            default_permission_id = req['default_permission_id']
            if not GroupPermission.objects.raw({"_id": ObjectId(default_permission_id)}).count():
                err = ERR.NO_DATA
            else:
                permissions = [GroupPermission(_id=default_permission_id)]
        else:
            permissions = []
        if err == ERR.OK:
            group_member = GroupMember(Person(_id=person_id),
                                        Group(_id=id),
                                        group_role,
                                        permissions)
            group_member.save()
            result = {"result":ERR.OK,
                      "id": str(group_member.pk)}
        else:
            result = {"result": ERR.NO_DATA}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except Exception as ex:
        print(ex)
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/group_members/<string:id>", methods=['DELETE'])
@required_auth("admin")
def delete_group_member(id):
    return delete_resource(GroupMember, id)


@bp.route("/groups/<string:id>/group_members", methods=['GET'])
def list_group_members_by_group_id(id):
    list = []
    try:
        if Group(_id=id) in Group.objects.raw({"_id": ObjectId(id)}):
            for group_member in  GroupMember.objects.raw({"group_id": ObjectId(id)}):
                list.append({"id": str(group_member.pk)})
            result = {"result": ERR.OK, "list":list}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/persons/<string:id>/group_members", methods=['GET'])
def list_group_members_by_person_id(id):
    list = []
    try:
        if Person(_id=id) in Person.objects.raw({"_id": ObjectId(id)}):
            for group_member in GroupMember.objects.raw({"person_id": ObjectId(id)}):
                list.append({"id": str(group_member.pk)})
            result = {"result": ERR.OK, "list":list}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/group_members/<string:id>", methods=['GET'])
@required_auth("group_member")
def get_group_member_info(id):
    try:
        if GroupMember(_id=id) in GroupMember.objects.raw({"_id": ObjectId(id)}):
            group_member = GroupMember(_id=id)
            group_member.refresh_from_db()
            perm = []
            for item in group_member.permissions:
                perm.append(str(item.pk))
            data = {}
            data.update({   "person_id": str(group_member.person_id.pk),
                            "group_id": str(group_member.group_id.pk),
                            "permissions": perm,
                            "is_active": str(group_member.is_active)})
            if group_member.role_id:
                data.update({"role_id": str(group_member.role_id.pk)})

            result = {"result": ERR.OK, "data": data}
        else:
            result = {"result": ERR.NO_DATA}
    except Exception as e:
        result = {"result": ERR.DB,
                  "error_message" :str(e)}
    return jsonify(result), 200


@bp.route("/group_members/<string:id>/permissions", methods = ['POST'])
@required_auth("admin")
def add_permissions_to_group_member(id):
    req = request.get_json()
    try:
        group_permission_id = req['group_permission_id']
        if GroupMember.objects.raw({"_id": ObjectId(id)}).count() \
                and GroupPermission.objects.raw({"_id": ObjectId(group_permission_id)}).count():
            group_member = GroupMember(_id=id)
            group_member.refresh_from_db()
            permission = GroupPermission(_id=group_permission_id)
            permission.refresh_from_db()
            group_member.permissions.append(permission)
            group_member.save()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/group_members/<string:id1>/permissions/<string:id2>", methods = ['DELETE'])
@required_auth("admin")
def delete_permissions_from_group_member(id1, id2):
    try:
        if GroupMember.objects.raw({"_id": ObjectId(id1)}).count()\
                and GroupPermission.objects.raw({"_id": ObjectId(id2)}).count():
            group_member = GroupMember(_id=id1)
            group_member.refresh_from_db()
            permission = GroupPermission(_id=id2)
            permission.refresh_from_db()
            if permission not in group_member.permissions:
                result = {"result": ERR.NO_DATA}
            else:
                group_member.permissions.remove(permission)
                group_member.save()
                result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/group_members/<string:id>/group_roles", methods = ['POST'])
@required_auth("admin")
def add_group_role_to_group_member(id):
    req = request.get_json()
    try:
        group_role_id = req['group_role_id']
        if GroupMember.objects.raw({"_id": ObjectId(id)}).count()\
                and GroupRole.objects.raw({"_id": ObjectId(group_role_id)}).count():
            group_member = GroupMember(_id=id)
            group_member.refresh_from_db()
            group_role = GroupRole(_id=group_role_id)
            group_role.refresh_from_db()
            group_member.set_role(group_role)
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except Exception as ex:
        print(ex)
        result = {"result":ERR.DB, "error_message": str(ex)}

    return jsonify(result), 200


@bp.route("/group_members/<string:id>", methods = ['PATCH'])
@required_auth("admin")
def change_group_member_status(id):
    if 'is_active' in request.args:
        string = request.args['is_active']
        if string == "true":
            is_active = True
        elif string == "false":
            is_active = False
        else:
            return jsonify({"result": ERR.INPUT}), 200
    else:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        if GroupMember(_id=id) in GroupMember.objects.raw({"_id": ObjectId(id)}):
            group_member = GroupMember(_id=id)
            group_member.refresh_from_db()
            group_member.is_active = is_active
            group_member.save()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except Exception as ex:
        print(ex)
        result = {"result":ERR.DB, "error_message": str(ex)}

    return jsonify(result), 200


@bp.route("/specializations", methods=['POST'])
@required_auth("admin")
def add_specializations():
    req = request.get_json()
    try:
        type = req['type']
        detail = req["detail"] if 'detail' in req else None
        specialization = Specialization(type)
        if detail: specialization.detail = detail
        specialization.save()
        result = {"result": ERR.OK,
                  "id": str(specialization.pk)}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except Exception as e:
        result = {"result": ERR.DB,
                  "error_message": str(e)}

    return jsonify(result), 200


@bp.route("/specializations/<string:_id>", methods=['DELETE'])
@required_auth("admin")
def delete_specialization(_id):
    return delete_resource(Specialization, _id)


@bp.route("/specializations", methods=['GET'])
def list_specializations():
    lst = []
    try:
        for specialization in Specialization.objects.all():
            d = {"id": str(specialization.pk),
                 "type": specialization.type}
            if specialization.detail: d.update({"detail": specialization.detail})
            lst.append(d)
        result = {"result": ERR.OK, "list": lst}
    except Exception as e:
        result = {"result": ERR.DB,
                  "error_message": str(e)}
    return jsonify(result), 200


@bp.route("/persons/<string:id>/specializations", methods=['POST'])
@required_auth("admin")
def add_person_specialization(id):
    req = request.get_json()
    try:
        person_id = id
        department_id = req['department_id']
        spec_id = req['specialization_id']
        value = req['value'] if "value" in req else None
        if not Person.objects.raw({"_id": ObjectId(person_id)}).count()\
                or not Department.objects.raw({"_id": ObjectId(department_id)}).count()\
                or not Specialization.objects.raw({"_id": ObjectId(spec_id)}).count():
            result = {"result": ERR.NO_DATA}
        else:
            person_spec = PersonSpecialization(
                Person(_id=person_id),
                Department(_id=department_id),
                Specialization(_id=spec_id),
                value
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
                     "type": p_spec.specialization_id.type
                     }
                if p_spec.specialization_id.detail: d.update({"detail": p_spec.specialization_id.detail})
                lst.append(d)

            result = {"result": ERR.OK, "list":lst}
        else:
            result = {"result": ERR.NO_DATA}
    except Exception as e:
        result = {"result": ERR.DB,
                  "error_message": str(e)}
    return jsonify(result), 200


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
                     {"from": "tutor",
                      "localField": "_id",
                      "foreignField": "person_id",
                      "as": "tutor"}},
                {"$lookup":
                     {"from": "student",
                      "localField": "_id",
                      "foreignField": "person_id",
                      "as": "student"}})
    err = ERR.OK
    if "specialization" in request.args:
        if request.args["specialization"] == "tutor":
            pipeline += ({"$match":
                              {"tutor._id": {"$exists": True}}},
                         )
        elif request.args["specialization"] == "student":
            pipeline += ({"$match":
                              {"student._id": {"$exists": True}}},
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
                                {"$or": [{"tutor.department_id": ObjectId(department_id)},
                                        {"student.department_id": ObjectId(department_id)}]}},
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
                                {"$or": [{"tutor.department_id": {"$in" : departments}},
                                        {"student.department_id": {"$in" : departments}}]}},
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
            if person["tutor"]:
                department_id = person["tutor"][0]["department_id"]
                specialization = "Tutor"
            else:
                if person["student"]:
                    department_id = person["student"][0]["department_id"]
                    specialization = "Student"
                else:
                    specialization = "None"
                    department_id = None
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


@bp.route("/persons/<string:id>", methods=['GET'])
@required_auth("user")
def get_person_info(id):
    try:
        if Person(_id=id) in Person.objects.raw({"_id": ObjectId(id)}):
            person = Person(_id=id)
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


@bp.route("/reviews/<string:id>", methods=['GET'])
def get_review_info(id):
    try:
        if SRReview(_id=id) in SRReview.objects.raw({"_id":ObjectId(id)}):
            subject = SRReview(_id=id)
        elif TRReview(_id=id) in TRReview.objects.raw({"_id": ObjectId(id)}):
            subject = TRReview(_id=id)
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


def post_review(review_type, subject_id):
    req = request.get_json()
    try:
        reviewer_id = ObjectId(req['reviewer_id'])
        subject_id = ObjectId(subject_id)
        value = req['value']
        description = req['description']
        obj = {
            "Student":
                SRReview(reviewer_id, subject_id, value, description),
            "Tutor":
                TRReview(reviewer_id, subject_id, value, description),
            "Group":
                GroupReview(reviewer_id, subject_id, value, description),
            "GroupTest":
                GroupTestReview(reviewer_id, subject_id, value, description),
            "GroupMember":
                GroupMemberReview(reviewer_id, subject_id, value, description)
        }
        subj_class = {
            "Student":
                Student,
            "Tutor":
                Tutor,
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
    try:
        if Student.objects.raw({"_id":ObjectId(id)}).count():
            review_type = "Student"
        elif Tutor.objects.raw({"_id":ObjectId(id)}).count():
            review_type = "Tutor"
        else:
            return jsonify({"result": ERR.NO_DATA}), 200
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except:
        return jsonify({"result": ERR.DB}), 200

    return post_review(review_type, id)


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
        if GroupMemberReview(_id=id) in GroupMemberReview.objects.raw({"_id":ObjectId(id)}):
            GroupMemberReview(_id=id).delete()
            result = {"result": ERR.OK}
    except:
        result = {"result": ERR.DB}
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
            for review in GroupMemberReview.objects.raw(query):
                lst.append({"id": str(review.pk)})
            result = {"result": ERR.OK, "list": lst}
        else:
            result = {"result": ERR.NO_DATA}
    except KeyError:
        result = {"result": ERR.INPUT}
    except Exception as ex:
        print(ex)
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


def list_skills(skill_cls):
    list = []
    try:
        for skill in  skill_cls.objects.all():
            list.append({"id":str(skill.pk),
                         "name":skill.name}
                        )
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
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
    return list_skills(SoftSkill)


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
    return list_skills(HardSkill)


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
    list = []
    try:
        if Group.objects.raw({"_id": ObjectId(id)}).count():
            for group_test in GroupTest.objects.raw({"group_id": ObjectId(id)}):
                list.append({"id": str(group_test.pk),
                            "name": group_test.name})
            result = {"result": ERR.OK, "list":list}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


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