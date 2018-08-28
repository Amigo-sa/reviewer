# -*- coding: utf-8 -*-
from bson import ObjectId
import node.settings.errors as ERR
import node.settings.constants as constants
from flask import Blueprint, request, jsonify
from data.reviewer_model import *
from node.api.auth import required_auth
from node.api.base_functions import delete_resource, list_resources

bp = Blueprint('groups', __name__)


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


@bp.route("/departments/<string:id>/groups", methods = ['GET'])
def list_groups(id):
    return list_resources(Group,
                          {"id": "_id",
                           "name": "name"},
                          Department,
                          id,
                          "department_id")


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
    return list_resources(GroupRole,
                          {"id": "_id",
                           "name": "name"})


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
    return list_resources(GroupPermission,
                          {"id": "_id",
                           "name": "name"})


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


@bp.route("/groups/<string:id>/group_members", methods=['GET'])
def list_group_members_by_group_id(id):
    return list_resources(GroupMember,
                          {"id": "_id"},
                          Group,
                          id,
                          "group_id")


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
def set_group_member_status(id):
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