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


@bp.route("/add_organization", methods = ['POST'])
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


@bp.route("/delete_organization/<string:id>", methods = ['DELETE'])
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


@bp.route("/list_organizations", methods = ['GET'])
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


@bp.route("/add_department", methods = ['POST'])
def add_department():
    req = request.get_json()
    try:
        organization_id = req['organization_id']
        name = req['name']
    except:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        department = Department(name, Organization(_id=organization_id))
        department.save()
        result = {"result":ERR.OK,
                  "id": str(department.pk)}
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/delete_department/<string:id>", methods = ['DELETE'])
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


@bp.route("/list_departments/<string:id>", methods = ['GET'])
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


@bp.route("/add_group", methods = ['POST'])
def add_group():
    req = request.get_json()
    try:
        department_id = req['department_id']
        name = req['name']
    except:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        group = Group(Department(_id=department_id), name)
        group.save()
        result = {"result":ERR.OK,
                  "id": str(group.pk)}
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/delete_group/<string:id>", methods = ['DELETE'])
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


@bp.route("/list_groups/<string:id>", methods = ['GET'])
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


@bp.route("/add_group_role", methods = ['POST'])
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


@bp.route("/delete_group_role/<string:id>", methods = ['DELETE'])
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


@bp.route("/list_group_roles", methods = ['GET'])
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


@bp.route("/add_group_permission", methods = ['POST'])
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


@bp.route("/delete_group_permission/<string:id>", methods = ['DELETE'])
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


@bp.route("/list_group_permissions", methods = ['GET'])
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


# TODO разобраться стоит ли делать дополнительные проверки на
# корректность вносимых данных в этой функции и сделать их при необходимости
@bp.route("/add_role_in_group", methods=['POST'])
def add_role_in_group():
    req = request.get_json()
    try:
        person_id = req['person_id']
        group_id = req['group_id']
        role_id = req['role_id']
        default_permission_id = req['default_permission_id']
    except:
        return jsonify({"result": ERR.INPUT}), 200
    try:
        role_in_group = RoleInGroup(Person(_id=person_id),
                                    Group(_id=group_id),
                                    GroupRole(_id=role_id),
                                    [GroupPermission(_id=default_permission_id)])
        role_in_group.save()
        result = {"result":ERR.OK,
                  "id": str(role_in_group.pk)}
    except:
        result = {"result":ERR.DB}

    return jsonify(result), 200


@bp.route("/delete_role_in_group/<string:id>", methods=['DELETE'])
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


@bp.route("/list_roles_in_group_by_group_id/<string:id>", methods=['GET'])
def list_roles_in_group_by_group_id(id):
    list = []
    try:
        for role_in_group in  RoleInGroup.objects.raw({"group_id": ObjectId(id)}):
            list.append({"id": str(role_in_group.pk)})
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/list_roles_in_group_by_person_id/<string:id>", methods=['GET'])
def list_roles_in_group_by_person_id(id):
    list = []
    try:
        for role_in_group in RoleInGroup.objects.raw({"person_id": ObjectId(id)}):
            list.append({"id": str(role_in_group.pk)})
        result = {"result": ERR.OK, "list":list}
    except:
        result = {"result": ERR.DB}
    return jsonify(result), 200


@bp.route("/get_role_in_group_info/<string:id>", methods=['GET'])
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


@bp.route("/add_permissions_to_role_in_group/<string:id>", methods = ['POST'])
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


@bp.route("/delete_permissions_from_role_in_group/<string:id>", methods = ['DELETE'])
def delete_permissions_from_role_in_group(id):
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


# TODO у этой функции одна неприятная проблема:
# сейчас она может добавить роль несуществующему человеку в несуществующем
# департаменте. Выяснить сдесь или в базе надо исправлять
@bp.route("/add_general_role", methods=['POST'])
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


@bp.route("/delete_general_role/<string:id>", methods=['DELETE'])
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


@bp.route("/get_general_roles_data/<string:id>", methods=['GET'])
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


@bp.route("/list_roles_by_person_id/<string:id>", methods=['GET'])
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


@bp.route("/find_persons", methods=['GET'])
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


