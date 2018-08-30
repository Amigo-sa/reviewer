# -*- coding: utf-8 -*-
from pymodm.connection import connect, _get_db
import reviewer_model as model
import re

skills = []


def wipe_db(db_name):
    try:
        revDb = _get_db(db_name)
        colList = revDb.list_collection_names()
        for col in colList:
            revDb[col].delete_many({})
    except Exception as e:
        print("Failed to wipe DB")
        print(str(e))


def prepare_soft_skills():
    for skill in skills[1]:
        soft_skill = model.SoftSkill(skill)
        soft_skill.save()


def prepare_hard_skills():
    for skill in skills[0]:
        hard_skill = model.HardSkill(skill)
        hard_skill.save()


def prepare_initial_admin():
    pass


def prepare_group_permissions():
    pass


def prepare_auth_permission():
    pass


def read_skill_list(filename):
    file = open(filename)
    header = file.readline()
    header = header.splitlines()[0]
    print(header)
    skill_cats = header.split(";")
    for cat in skill_cats:
        skills.append([])
    cat_count = len(skill_cats)
    print(skill_cats)
    lines = file.readlines()
    print(lines)
    for line in lines:
        line = line.splitlines()[0]
        print(line)
        skill_names = line.split(";")
        if len(skill_names) != cat_count:
            raise SyntaxError("Ошибка парсинга skills.csv")
        for index, name in enumerate(skill_names):
            print("%d %s" % (index, name))
            if len(name) > 0:
                skills[index].append(name)
    print(skills)


if __name__ == "__main__":
    wipe_db("reviewer")
    read_skill_list("skills.csv")
    prepare_soft_skills()
    prepare_hard_skills()
    prepare_auth_permission()
    prepare_group_permissions()
    prepare_initial_admin()
