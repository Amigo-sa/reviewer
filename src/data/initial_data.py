# -*- coding: utf-8 -*-
from pymodm.connection import connect, _get_db
import reviewer_model as model
import re, os, sys
parentPath = os.path.abspath("..//..//src")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from node.api.auth import hash_password, gen_session_id
from node.settings import constants

group_permissions =[
    "full_control",
    "read_info",
    "modify_info",
    "add_members",
    "remove_members",
    "create_survey",
    "participate_survey",
    "participate_test"
]

def wipe_db():
    try:
        rev_db = _get_db("reviewer")
        print("working database is %s" % rev_db)
        colList = rev_db.list_collection_names()
        for col in colList:
            rev_db[col].delete_many({})
    except Exception as e:
        print("Failed to wipe DB")
        print(str(e))

def prepare_hard_skills(hs_path):
    hard_skills = read_skill_list(hs_path)
    for skill_sub in hard_skills:
        skill_type = model.SkillType(skill_sub[0])
        skill_type.save()
        skill_sub.pop(0)
        for skill in skill_sub:
            hard_skill = model.HardSkill()
            hard_skill.name = skill
            hard_skill.skill_type_id = skill_type.pk
            hard_skill.save()

def prepare_soft_skills(ss_path):
    hard_skills = read_skill_list(ss_path)
    for skill_sub in hard_skills:
        skill_type = model.SkillType(skill_sub[0])
        skill_type.save()
        skill_sub.pop(0)
        for skill in skill_sub:
            soft_skill = model.SoftSkill()
            soft_skill.name = skill
            soft_skill.skill_type_id = skill_type.pk
            soft_skill.save()

# TODO это не безопасно
def prepare_initial_admin():
    try:
        auth_info = model.AuthInfo()
        auth_info.is_approved = True
        auth_info.phone_no = "79032233223"
        auth_info.password = hash_password("SomeSecurePass")
        #session_id = gen_session_id()
        #auth_info.session_id = session_id
        auth_info.permissions = 1
        auth_info.save()
        #return auth_info.session_id
    except Exception as e:
        print("Failed to prepare first admin")
        print(str(e))


def prepare_group_permissions():
    for permission in group_permissions:
        g_perm = model.GroupPermission()
        g_perm.name = permission
        g_perm.save()


def prepare_auth_permission():
    pass


def prepare_group_roles():
    pass

def prepare_version_info():
    service = model.Service()
    service.db_version = constants.db_model_version
    service.api_version = constants.api_version


def read_skill_list(filename):
    skill_list = []
    file = open(filename)
    header = file.readline()
    header = header.splitlines()[0]
    skill_types = header.split(";")
    for t in skill_types:
        skill_list.append([t])
    type_count = len(skill_types)
    #print(type_count)
    #print(skill_types)
    lines = file.readlines()
    for line in lines:
        line = line.splitlines()[0]
        skill_names = line.split(";")
        if len(skill_names) != type_count:
            raise SyntaxError("Ошибка парсинга skills.csv")
        for index, name in enumerate(skill_names):
            if len(name) > 0:
                skill_list[index].append(name)
    return skill_list

def fill_initial_data(hs_path, ss_path):
    wipe_db()
    prepare_version_info()
    prepare_hard_skills(hs_path)
    prepare_soft_skills(ss_path)
    prepare_auth_permission()
    prepare_group_roles()
    prepare_group_permissions()
    prepare_initial_admin()


if __name__ == "__main__":
    fill_initial_data("hard_skills.csv", "soft_skills.csv")


