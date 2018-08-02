# -*- coding: utf-8 -*-
from bson import ObjectId
import node.settings.errors as ERR
from node.settings.constants import mock_smsc_url
from flask import Blueprint, request, jsonify
from data.reviewer_model import *
import datetime
import random
import requests

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


    from pymodm.connection import _get_db


    @bp.route("/wipe", methods=['POST'])
    def wipe():
        try:
            revDb = _get_db("reviewer")
            colList = revDb.list_collection_names()
            for col in colList:
                revDb[col].delete_many({})
            result = {"result": ERR.OK}
        except:
            result = {"result": ERR.DB}
        return jsonify(result), 200


    @bp.route("/shutdown", methods = ['POST'])
    def shutdown():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        result = {"result": ERR.OK}
        return jsonify(result), 200

# TODO добавить в док
@bp.route("/confirm_phone_no", methods= ["POST"])
def register_user():
    req = request.get_json()
    try:
        phone_no = req["phone_no"]
        person = Person.objects.get({"phone_no": phone_no})
        person.refresh_from_db()
        auth_info = AuthInfo.objects.raw({"phone_no": phone_no})
        infoCount = auth_info._collection.count_documents({})
        if infoCount:
            print(infoCount)
            old_auth_info = auth_info.first()
            old_auth_info.last_send = datetime.datetime.now()
            code = gen_sms_code()
            session_id = gen_session_id()
            old_auth_info.session_id = session_id
            old_auth_info.auth_code = code
            old_auth_info.save()
            result = {"result": ERR.OK,
                      "session_id": session_id}
        else:
            new_auth_info = AuthInfo()
            new_auth_info.phone_no = phone_no
            new_auth_info.person_id = person.pk
            new_auth_info.last_send = datetime.datetime.now()
            code = gen_sms_code()
            session_id = gen_session_id()
            new_auth_info.session_id = session_id
            new_auth_info.auth_code = code
            new_auth_info.save()
            send_sms(phone_no, code)
            result = {"result": ERR.OK,
                  "session_id" : session_id}
        # check phone
        # generate auth code
        # store auth code
        # check timeout
        # contact smsc
        # generate session id

    except KeyError as e:
        result = {"result": ERR.INPUT}
        print(str(e))
    except Exception as e:
        result = {"result": ERR.DB}
        print(str(e))
    return jsonify(result), 200

def gen_sms_code():
    code = random.randint(0,9999)
    codestr = "{0:04}".format(code)
    print(codestr)
    return codestr
#TODO генерация сделана намеренно ущербной, чтобы в будущем устроить это всё по-человечески безопасно
def gen_session_id():
    code = random.randint(0,99999999)
    codestr = "{0:08}".format(code)
    print(codestr)
    return codestr

def send_sms(phone_no, message):
    requests.post(mock_smsc_url + "/send_sms",json={
        "auth_code" : message,
        "phone_no" : phone_no
    })


# TODO добавить в док
@bp.route("/finish_phone_confirmation", methods= ["POST"])
def confirm_registration():
    req = request.get_json()
    try:
        auth_code = req["auth_code"]
        session_id = req["session_id"]
        auth_info = AuthInfo.objects.get({"session_id": session_id})
        if auth_info.auth_code == auth_code:
            result = {"result": ERR.OK}
            auth_info.is_approved = True
            auth_info.auth_code = None
            auth_info.session = None
            auth_info.save()
            print("user registered")
        else:
            result = {"result": ERR.INPUT}
    except KeyError as e:
        result = {"result": ERR.INPUT}
        print(str(e))
    except Exception as e:
        result = {"result": ERR.DB}
        print(str(e))

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

@bp.route("/persons", methods = ['POST'])
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

@bp.route("/persons/<string:id>", methods = ['DELETE'])
def delete_person(id):
    try:
        if Person(_id=id) in Person.objects.raw({"_id":ObjectId(id)}):
            Person(_id=id).delete()
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

#TODO внести метод в документацию
@bp.route("/groups/<string:id>/role_list", methods=['POST'])
def set_role_list_for_group(id):
    req = request.get_json()
    try:
        role_list = req['role_list']
    except:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        group = Group(_id=id)
        group.refresh_from_db()
        group.role_list = role_list
        group.save()
        result = {"result": ERR.OK}
    except:
        result = {"result": ERR.DB}

    return jsonify(result), 200

#TODO внести метод в документацию
@bp.route("/groups/<string:id>/role_list", methods=['GET'])
def get_role_list_for_group(id):
    list = []
    try:
        group =  Group(_id=id)
        group.refresh_from_db()
        for role in group.role_list:
            list.append({"id" : str(role.pk)})
        result = {"result": ERR.OK, "list": list}
    except:
        result = {"result": ERR.DB}
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


@bp.route("/groups/<string:id>/group_members", methods=['POST'])
def add_group_member(id):
    req = request.get_json()
    try:
        person_id = req['person_id']
        if 'role_id' in req:
            role_id = req['role_id']
            group_role = GroupRole(_id=role_id)
        else:
            group_role = None
        if 'default_permission_id' in req:
            default_permission_id = req['default_permission_id']
            permissions = [GroupPermission(_id=default_permission_id)]
        else:
            permissions = []

        role_in_group = GroupMember(Person(_id=person_id),
                                    Group(_id=id),
                                    group_role,
                                    permissions)
        role_in_group.save()
        result = {"result":ERR.OK,
                  "id": str(role_in_group.pk)}
    except KeyError:
        return jsonify({"result": ERR.INPUT}), 200
    except Exception as ex:
        print(ex)
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/group_members/<string:id>", methods=['DELETE'])
def delete_group_member(id):
    try:
        if GroupMember(_id=id) in GroupMember.objects.raw({"_id":ObjectId(id)}):
            GroupMember(_id=id).delete()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.NO_DATA}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200

# TODO переименуй остальные role_in_group, а то неаккуратненько
@bp.route("/groups/<string:id>/group_members", methods=['GET'])
def list_group_members_by_group_id(id):
    list = []
    try:
        for role_in_group in  GroupMember.objects.raw({"group_id": ObjectId(id)}):
            list.append({"id": str(role_in_group.pk)})
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/persons/<string:id>/group_members", methods=['GET'])
def list_group_members_by_person_id(id):
    list = []
    try:
        for role_in_group in GroupMember.objects.raw({"person_id": ObjectId(id)}):
            list.append({"id": str(role_in_group.pk)})
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200

# TODO осветить в доках is_active
@bp.route("/group_members/<string:id>", methods=['GET'])
def get_group_member_info(id):
    try:
        if GroupMember(_id=id) in GroupMember.objects.raw({"_id": ObjectId(id)}):
            role_in_group = GroupMember(_id=id)
            role_in_group.refresh_from_db()
            perm = []
            for item in role_in_group.permissions:
                perm.append(str(item.pk))
            data = {}
            data.update({   "person_id": str(role_in_group.person_id.pk),
                            "group_id": str(role_in_group.group_id.pk),
                            "permissions": perm,
                            "is_active": str(role_in_group.is_active)})
            if role_in_group.role_id:
                data.update({"role_id": str(role_in_group.role_id.pk)})

            result = {"result": ERR.OK, "data": data}
        else:
            result = {"result": ERR.NO_DATA}
    except Exception as e:
        result = {"result": ERR.DB,
                  "error_message" :str(e)}
    return jsonify(result), 200


@bp.route("/group_members/<string:id>/permissions", methods = ['POST'])
def add_permissions_to_group_member(id):
    req = request.get_json()
    try:
        group_permission_id = req['group_permission_id']
    except:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        if GroupMember(_id=id) in GroupMember.objects.raw({"_id": ObjectId(id)}):
            role_in_group = GroupMember(_id=id)
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


@bp.route("/group_members/<string:id1>/permissions/<string:id2>", methods = ['DELETE'])
def delete_permissions_from_group_member(id1, id2):
    try:
        if GroupMember(_id=id1) in GroupMember.objects.raw({"_id": ObjectId(id1)}):
            role_in_group = GroupMember(_id=id1)
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

@bp.route("/group_members/<string:id>/group_roles", methods = ['POST'])
def add_group_role_to_group_member(id):
    req = request.get_json()
    try:
        group_role_id = req['group_role_id']
        if GroupMember(_id=id) in GroupMember.objects.raw({"_id": ObjectId(id)}):
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


@bp.route("/general_roles", methods=['POST'])
def add_general_role():
    req = request.get_json()
    try:
        person_id = req['person_id']
        department_id = req['department_id']
        role_type = req['role_type']
        description = req['description']
    except:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        if role_type == "Tutor":
            tutor_role = TutorRole(Person(_id=person_id),
                                   Department(_id=department_id),
                                   description)
            tutor_role.save()
            result = {"result": ERR.OK,
                      "id": str(tutor_role.pk)}
        else:
            if role_type == "Student":
                student_role = StudentRole(Person(_id=person_id),
                                           Department(_id=department_id),
                                           description)
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
    if 'query_limit' in request.args:
        limit = int(request.args['query_limit'])
    else:
        limit = 100
    if 'query_start' in request.args:
        skip = int(request.args['query_start'])
    else:
        skip = 0
    pipeline = ({"$lookup":
                     {"from": "tutor_role",
                      "localField": "_id",
                      "foreignField": "person_id",
                      "as": "tutor_role"}},
                {"$lookup":
                     {"from": "student_role",
                      "localField": "_id",
                      "foreignField": "person_id",
                      "as": "student_role"}})
    if 'group_id' in request.args:
        group_id = request.args['group_id']
        pipeline += ({"$lookup":
                        {"from": "group_member",
                         "localField": "_id",
                         "foreignField": "person_id",
                         "as": "role"}},
                     {"$match":
                         {"role.group_id": ObjectId(group_id)}},
                     )
    else:
        if 'department_id' in request.args:
            department_id = request.args['department_id']
            pipeline += ({"$match":
                             {"$or": [{"tutor_role.department_id": ObjectId(department_id)},
                                      {"student_role.department_id": ObjectId(department_id)}]}},
            )
        else:
            if 'organization_id' in request.args:
                organization_id = request.args['organization_id']
                departments = []
                for department in Department.objects.raw({"organization_id": ObjectId(organization_id)}):
                    departments.append(department.pk)
                pipeline += ({"$match":
                                 {"$or": [{"tutor_role.department_id": {"$in" : departments}},
                                          {"student_role.department_id": {"$in" : departments}}]}},
                            )
            """ #оставим этот код на случай если понадобится отфильтровать безрольных пользователей
            else:
                pipeline += ({"$match":
                                  {"$or": [{"tutor_role.department_id": {"$exists": True}},
                                           {"student_role.department_id": {"$exists": True}}]}},
                             )"""
    pipeline += ({"$skip": skip},
                 {"$limit": limit})
    try:
        list = []
        for person in Person.objects.aggregate(*pipeline):
            if person["tutor_role"]:
                department_id = person["tutor_role"][0]["department_id"]
                role = "Tutor"
            else:
                if person["student_role"]:
                    department_id = person["student_role"][0]["department_id"]
                    role = "Student"
                else:
                    role = "None"
                    department_id = None
            if (department_id):
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
                         "role": role,
                         "organization_name": org_name})
        result = {"result": ERR.OK, "list": list}
    except Exception as ex:
        print(ex)
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/persons/<string:id>", methods=['GET'])
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

# TODO добавить в документацию
@bp.route("/reviews/<string:id>", methods=['GET'])
def get_review_info(id):
    try:
        subject = None
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
        result = {"result": ERR.DB, "error_info" : str(e)}
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
            "GroupMember":
                GroupMemberReview(reviewer_id, subject_id, value, description)
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
        for review in GroupMemberReview.objects.raw(query):
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
            list.append({"id": str(group_test.pk),
                        "name": group_test.name})
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200

# TODO посмотри плиз, что у тебя с кодами ошибок вот в каком смысле:
# вот в данном роуте NO_DATA вообще не возвращается,
# а есть роуты, когда если id не найден, возвращается NO_DATA
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