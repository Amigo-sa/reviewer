# -*- coding: utf-8 -*-
import sys
from pymodm import MongoModel, fields, ReferenceField
from pymongo.write_concern import WriteConcern
from pymodm.errors import ValidationError
from pymongo.operations import IndexModel
import pymongo
from pymodm.connection import connect
import context
from node.settings import constants
import node.settings.errors as ERR
import os
import logging
from bson import ObjectId

from collections import Counter

model_version = constants.db_model_version


# Функция для определения перечня зависимых документов
def get_dependent_list(doc, dep_id_list):
    """
    Recursive function to find all dependent documents.
    :param doc: referred document
    :param dep_id_list: list of all referencing documents
    :return: list of all referencing documents.
    Always includes the doc itself
    """
    current_del_rules = doc._mongometa.delete_rules
    dep_id_list.append(doc)
    for item, rule in current_del_rules.items():
        related_model, related_field = item
        dependent_docs = related_model.objects.raw({related_field: doc.pk})
        for dep in dependent_docs:
            if dep not in dep_id_list:
                get_dependent_list(dep, dep_id_list)


# Ручное добавление правил удаления для списков ссылок
def init_model():
    GroupRole.register_delete_rule(
        Group, "role_list", fields.ReferenceField.PULL)
    GroupPermission.register_delete_rule(
        GroupMember, "permissions", fields.ReferenceField.PULL)

try:
    if os.environ["REVIEWER_APP_MODE"] == "production":
        db_name = constants.db_name
    elif os.environ["REVIEWER_APP_MODE"] == "development":
        db_name = constants.db_name_develop
    elif os.environ["REVIEWER_APP_MODE"] == "load":
        db_name = constants.db_name_load_test
    elif os.environ["REVIEWER_APP_MODE"] == "local":
        db_name = constants.db_name
    else:
        logging.error("Environment variable REVIEWER_APP_MODE value incorrect!")
except:
    logging.error("Environment variable REVIEWER_APP_MODE must be defined !")
    raise

print("DB initialized with argv: " + str(sys.argv))
if len(sys.argv) > 1:
    if '--test' in str(sys.argv):
        db_name = constants.db_name_test
    if '--load_test' in str(sys.argv):
        db_name = constants.db_name_load_test
    if '--develop' in str(sys.argv):
        db_name = constants.db_name_develop

print("Working with DB '%s' \n" % db_name)
connect(constants.mongo_db + "/" + db_name, alias="reviewer")

# TODO по идее, от этого нового класса можно избавиться с помощью validators
# https://pymodm.readthedocs.io/en/latest/api/
class ValidatedReferenceField(fields.ReferenceField):
    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)
        old_clean = getattr(cls, "clean", None)

        def new_clean(instance):
            ref_field = getattr(instance, name, None)
            ref_class = getattr(cls, name, None)
            if ref_field is None:
                if not ref_class.blank:
                    raise ValidationError("ссылка на _id несуществующего объекта")
            else:
                if not self.related_model.objects.get({"_id": ref_field.pk}):
                    raise ValidationError("ссылка на _id несуществующего объекта %s" % self.related_model.__name__)
            old_clean(instance)

        setattr(cls, "clean", new_clean)


class ValidatedReferenceList(fields.ListField):
    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)
        old_clean = getattr(cls, "clean", None)

        def new_clean(instance):
            ref_list = getattr(instance, name, None)
            for item in ref_list:
                if item is None:
                    raise ValidationError("ссылка на _id несуществующего объекта")
                else:
                    if not self._field.related_model.objects.get({"_id": item.pk}):
                        raise ValidationError("ссылка на _id несуществующего объекта")
            old_clean(instance)

        setattr(cls, "clean", new_clean)


class Service(MongoModel):
    db_version = fields.CharField()
    api_version = fields.CharField()

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True


class Person(MongoModel):
    first_name = fields.CharField()
    middle_name = fields.CharField()
    surname = fields.CharField()
    birth_date = fields.DateTimeField()
    phone_no = fields.CharField()
    photo = fields.BinaryField()

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("phone_no", pymongo.DESCENDING)],
                              unique=True,
                              partialFilterExpression= { "phone_no": { "$exists": True } }),
                   IndexModel("first_name"),
                   IndexModel("middle_name"),
                   IndexModel("surname")]

    @staticmethod
    def find(args):
        if 'query_limit' in args:
            limit = int(args['query_limit'])
        else:
            limit = 100
        if 'query_start' in args:
            skip = int(args['query_start'])
        else:
            skip = 0
        pipeline = ()
        person_spec_project_filter = 1
        err = ERR.OK
        target_cls = Person
        if "group_id_mod" in args:
            target_cls = GroupMember
            group_id = args['group_id_mod']
            group_qs = Group.objects.raw({"_id": ObjectId(group_id)})
            if group_qs.count():
                pipeline += ({"$match": {"group_id": ObjectId(group_id)}},)
                pipeline += ({"$lookup":
                                  {"from": "person"
                                      , "localField": "person_id"
                                      , "foreignField": "_id"
                                      , "as": "target_person"}
                              },)

                pipeline += ({"$project":
                    {
                        # TODO это вообще нормально, что приходится брать 1-й элемент массива?
                        # по идее, должно возвращаться просто значение, а не как массив
                        "first_name": {"$arrayElemAt": ["$target_person.first_name", 0]},
                        "middle_name": {"$arrayElemAt": ["$target_person.middle_name", 0]},
                        "surname": {"$arrayElemAt": ["$target_person.surname", 0]},
                        "_id": {"$arrayElemAt": ["$target_person._id", 0]}
                    }},)
            else:
                err = ERR.NO_DATA

        if "specialization" in args:
            spec_type = args["specialization"]
            spec_qs = Specialization.objects.raw({"type": spec_type});
            if spec_qs.count():
                # Find specializations by specialization type
                specializations = list(key["_id"] for key in spec_qs.values())
                # Find persons match specialization type
                person_spec_qs = PersonSpecialization.objects.raw({"specialization_id": {"$in": specializations}})
                specialists = list(key["person_id"] for key in person_spec_qs.values())
                # Prepare query
                pipeline += ({"$match": {"_id": {"$in": specialists}}},)
                person_spec_project_filter = \
                    {"$filter": {"input": "$person_specialization",
                                 "as": "spec",
                                 "cond": {"$in": ["$$spec.specialization_id", specializations]}}}
            else:
                return {"result": ERR.INPUT}

        if "specialization_mod" in args:
            target_cls = PersonSpecialization
            spec_type = args["specialization_mod"]
            spec_qs = Specialization.objects.raw({"type": spec_type});
            if spec_qs.count():
                pipeline += ({"$lookup":
                                  {"from": "specialization"
                                      , "localField": "specialization_id"
                                      , "foreignField": "_id"
                                      , "as": "spec"}
                              },)
                pipeline += ({"$match": {"spec.type": spec_type}},)
                pipeline += ({"$lookup":
                                  {"from": "person"
                                      , "localField": "person_id"
                                      , "foreignField": "_id"
                                      , "as": "target_person"}
                              },)
                pipeline += ({"$project":
                    {
                        "first_name": {"$arrayElemAt": ["$target_person.first_name", 0]},
                        "middle_name": {"$arrayElemAt": ["$target_person.middle_name", 0]},
                        "surname": {"$arrayElemAt": ["$target_person.surname", 0]},
                        "_id": {"$arrayElemAt": ["$target_person._id", 0]}
                    }},)
            else:
                return {"result": ERR.INPUT}

        if 'group_id' in args:
            group_id = args['group_id']
            # Find group
            group_qs = Group.objects.raw({"_id": ObjectId(group_id)})
            if group_qs.count():
                # Find group members persons by group id
                group_members_qs = GroupMember.objects.raw({"group_id": ObjectId(group_id)});
                group_members = list(key["person_id"] for key in group_members_qs.values())
                # Find department_id
                department_id = str(group_qs.first().department_id.pk)
                # Prepare query
                pipeline += ({"$match": {"_id": {"$in": group_members}}},)
                # person_spec_project_filter = \
                #     {"$filter": {"input": "$person_specialization",
                #                  "as": "spec",
                #                  "cond": {"$in": ["$$spec.department_id", [ObjectId(department_id)]]}}}
            else:
                err = ERR.NO_DATA
        elif 'department_id' in args:
            department_id = args['department_id']
            dep_qs = Department.objects.raw({"_id": ObjectId(department_id)})
            if dep_qs.count():
                # Find persons match department
                person_spec_qs = PersonSpecialization.objects.raw({"department_id": ObjectId(department_id)})
                specialists = list(key["person_id"] for key in person_spec_qs.values())
                # Prepare query
                pipeline += ({"$match": {"_id": {"$in": specialists}}},)
                person_spec_project_filter = \
                    {"$filter": {"input": "$person_specialization",
                                 "as": "spec",
                                 "cond": {"$in": ["$$spec.department_id", [ObjectId(department_id)]]}}}
            else:
                err = ERR.NO_DATA
        elif 'organization_id' in args:
            organization_id = args['organization_id']
            if Organization.objects.raw({"_id": ObjectId(organization_id)}).count():
                # Find departments in organization
                dep_qs = Department.objects.raw({"organization_id": ObjectId(organization_id)})
                departments = list(key["_id"] for key in dep_qs.values())
                # Find persons match departments
                person_spec_qs = PersonSpecialization.objects.raw({"department_id": {"$in": departments}})
                specialists = list(key["person_id"] for key in person_spec_qs.values())
                # Prepare query
                pipeline += ({"$match": {"_id": {"$in": specialists}}},)
                person_spec_project_filter = \
                    {"$filter": {"input": "$person_specialization",
                                 "as": "spec",
                                 "cond": {"$in": ["$$spec.department_id", departments]}}}
            else:
                err = ERR.NO_DATA
        if "surname" in args:
            pipeline += ({"$match":
                              {"surname": {"$regex": args['surname'], "$options": "i"}}},
                         )
        if "first_name" in args:
            pipeline += ({"$match":
                              {"first_name": {"$regex": args['first_name'], "$options": "i"}}},
                         )
        if "middle_name" in args:
            pipeline += ({"$match":
                              {"middle_name": {"$regex": args['middle_name'], "$options": "i"}}},
                         )
        pipeline += ({"$skip": skip},
                     {"$limit": limit})
        pipeline += ({"$lookup":
                          {"from": "person_specialization",
                           "localField": "_id",
                           "foreignField": "person_id",
                           "as": "person_specialization"}},
                     {"$project":
                          {"first_name": 1,
                           "middle_name": 1,
                           "surname": 1,
                           "person_specialization": person_spec_project_filter}},
                     {"$project":
                          {"first_name": 1,
                           "middle_name": 1,
                           "surname": 1,
                           "person_specialization": {"$arrayElemAt": ["$person_specialization", 0]}}},
                     {"$lookup":
                          {"from": "specialization",
                           "localField": "person_specialization.specialization_id",
                           "foreignField": "_id",
                           "as": "specialization"}},
                     {"$lookup":
                          {"from": "department",
                           "localField": "person_specialization.department_id",
                           "foreignField": "_id",
                           "as": "department"}},
                     {"$lookup":
                          {"from": "organization",
                           "localField": "department.organization_id",
                           "foreignField": "_id",
                           "as": "organization"}},
                     )
        if err == ERR.NO_DATA:
            {"result": ERR.NO_DATA}
        try:
            lst = []

            for person in target_cls.objects.aggregate(*pipeline):
                if "person_specialization" in person and person["person_specialization"]:
                    specialization = person["specialization"][0]["type"]
                    org_name = person["organization"][0]["name"]
                else:
                    specialization = None
                    org_name = "None"
                lst.append({"id": str(person["_id"]),
                            "first_name": person["first_name"],
                            "middle_name": person["middle_name"],
                            "surname": person["surname"],
                            "specialization": specialization,
                            "organization_name": org_name})

            result = {"result": ERR.OK, "list": lst}
        except Exception as e:
            result = {"result": ERR.DB,
                      "error_message": str(e)}
        return result


class Organization(MongoModel):
    name = fields.CharField()

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("name", pymongo.DESCENDING)],
                              unique=True)]


class Department(MongoModel):
    name = fields.CharField()
    organization_id = ValidatedReferenceField(Organization, on_delete=ReferenceField.CASCADE)

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("name", pymongo.DESCENDING),
                               ("organization_id", pymongo.DESCENDING)],
                              unique=True),
                   IndexModel("organization_id")]


class SkillType(MongoModel):
    name = fields.CharField()

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("name", pymongo.DESCENDING)],
                              unique=True)]


class HardSkill(MongoModel):
    name = fields.CharField()
    skill_type_id = ValidatedReferenceField(SkillType, on_delete=ReferenceField.CASCADE)

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("name", pymongo.DESCENDING),
                               ("skill_type_id", pymongo.DESCENDING)],
                              unique=True)]


class PersonHS(MongoModel):
    person_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE)
    hs_id = ValidatedReferenceField(HardSkill, on_delete=ReferenceField.CASCADE)
    level = fields.FloatField()

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("person_id", pymongo.DESCENDING),
                               ("hs_id", pymongo.DESCENDING)],
                              unique=True)]


class SoftSkill(MongoModel):
    name = fields.CharField()
    skill_type_id = ValidatedReferenceField(SkillType, on_delete=ReferenceField.CASCADE)

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("name", pymongo.DESCENDING),
                               ("skill_type_id", pymongo.DESCENDING)],
                              unique=True)]


class PersonSS(MongoModel):
    person_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE)
    ss_id = ValidatedReferenceField(SoftSkill, on_delete=ReferenceField.CASCADE)
    level = fields.FloatField()

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("person_id", pymongo.DESCENDING),
                               ("ss_id", pymongo.DESCENDING)],
                              unique=True)]


class Specialization(MongoModel):
    # type подразумевает "преподаватель", "лаборант", "студент" и т.п.
    # при этом поле detail можно сделать недоступным для заполнения если type=="студент"
    type = fields.CharField(required=True)
    detail = fields.CharField()

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("detail", pymongo.DESCENDING)],
                              unique=False)]


class PersonSpecialization(MongoModel):
    person_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE)
    department_id = ValidatedReferenceField(Department, on_delete=ReferenceField.CASCADE)
    specialization_id = ValidatedReferenceField(Specialization, on_delete=ReferenceField.CASCADE)
    level = fields.FloatField(default=None, blank=True)
    details = fields.DictField()

    is_active = fields.BooleanField(required=True, default=True)

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("person_id", pymongo.DESCENDING),
                               ("department_id", pymongo.DESCENDING),
                               ("specialization_id", pymongo.DESCENDING)],
                              unique=True),
                   IndexModel("department_id"),
                   IndexModel("specialization_id")]


class GroupRole(MongoModel):
    name = fields.CharField()

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("name", pymongo.DESCENDING)],
                              unique=True)]


class GroupPermission(MongoModel):
    name = fields.CharField()

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("name", pymongo.DESCENDING)],
                              unique=True)]


class Group(MongoModel):
    department_id = ValidatedReferenceField(Department, on_delete=ReferenceField.CASCADE)
    name = fields.CharField()
    role_list = ValidatedReferenceList(field=
                                       fields.ReferenceField(GroupRole))

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("name", pymongo.DESCENDING),
                               ("department_id", pymongo.DESCENDING)],
                              unique=True)]


class GroupMember(MongoModel):

    def clean(self):
        if self.role_id:
            target_group = Group.objects.get({"_id": self.group_id.pk})
            if self.role_id not in target_group.role_list:
                raise ValidationError("Группа %s не предусматривает роль %s" % (
                    target_group.name, self.role_id.name))
        if [x for n, x in enumerate(self.permissions) if x in self.permissions[:n]]:
            raise ValidationError("Разрешения не должны повторяться")

    person_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE, required=True, blank=False)
    group_id = ValidatedReferenceField(Group, on_delete=ReferenceField.CASCADE, required=True, blank=False)
    role_id = ValidatedReferenceField(GroupRole, on_delete=ReferenceField.DO_NOTHING, blank=True)
    permissions = ValidatedReferenceList(field=
                                         fields.ReferenceField(GroupPermission), blank=True)
    is_active = fields.BooleanField(required=True, default=True)

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("person_id", pymongo.DESCENDING),
                               ("group_id", pymongo.DESCENDING),
                               ("role_id", pymongo.DESCENDING)],
                              unique=True),
                   IndexModel("group_id")]

    def set_role(self, role: GroupRole):
        if not role:
            raise ValidationError("Необходимо указать id роли")
        if self.role_id:
            raise ValidationError("Роль уже задана")
        if not self.group_id:
            raise ValidationError("Перед установкой роли необходимо задать группу")
        self.role_id = role.pk
        self.save()


class GroupTest(MongoModel):
    group_id = ValidatedReferenceField(Group, on_delete=ReferenceField.CASCADE, blank=False)
    name = fields.CharField()
    info = fields.CharField()

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True

    """крайне важный нюанс работы pymodm:
    1. если объект создаётся как 
                    group_test = GroupTest(Group(_id=id), name, info)
                    group_test.save(),
    то в group_id, проходящей валидацию, всегда есть id. Путь даже и ссылается на
    несуществующий объект.
    2. если объект создаётся как 
                    group_test = GroupTest(id, name, info)
                    group_test.save(),
    _и_ при этом в методе clean идёт обращение к self.group_id, невалидный group_id
    устанавливается в None, валидный остаётся без изменений.
    Если метода нет обращения к self.group_id, всё происходит как в п.1 
    
    Справедливо для всех коллекций
    
    Выводы:
    - если предусмотреть оба варианта и быть готовым как к None, так и к невалидному
    id, получится надёжнее ценой одного лишнего обращения к базе с поиском по _id. 
    - использовать свои классы для валидации, пока не дойдём до суровой оптимизации.
    """


class TestResult(MongoModel):
    test_id = ValidatedReferenceField(GroupTest, on_delete=ReferenceField.CASCADE)
    person_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE)
    result_data = fields.ListField(field=fields.CharField())

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("test_id", pymongo.DESCENDING),
                               ("person_id", pymongo.DESCENDING)],
                              unique=True)]


class SSReview(MongoModel):
    reviewer_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE)
    subject_id = ValidatedReferenceField(PersonSS, on_delete=ReferenceField.CASCADE)
    value = fields.FloatField()
    description = fields.CharField()

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("reviewer_id", pymongo.DESCENDING),
                               ("subject_id", pymongo.DESCENDING)],
                              unique=True)]


class HSReview(MongoModel):
    reviewer_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE)
    subject_id = ValidatedReferenceField(PersonHS, on_delete=ReferenceField.CASCADE)
    value = fields.FloatField()
    description = fields.CharField()

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("reviewer_id", pymongo.DESCENDING),
                               ("subject_id", pymongo.DESCENDING)],
                              unique=True)]


class SpecializationReview(MongoModel):
    reviewer_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE)
    subject_id = ValidatedReferenceField(PersonSpecialization, on_delete=ReferenceField.CASCADE)
    value = fields.FloatField()
    description = fields.CharField()

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("reviewer_id", pymongo.DESCENDING),
                               ("subject_id", pymongo.DESCENDING)],
                              unique=True)]


class GroupReview(MongoModel):
    reviewer_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE)
    subject_id = ValidatedReferenceField(Group, on_delete=ReferenceField.CASCADE)
    value = fields.FloatField()
    description = fields.CharField()

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("reviewer_id", pymongo.DESCENDING),
                               ("subject_id", pymongo.DESCENDING)],
                              unique=True)]


class GroupMemberReview(MongoModel):
    reviewer_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE)
    subject_id = ValidatedReferenceField(GroupMember, on_delete=ReferenceField.CASCADE)
    value = fields.FloatField()
    description = fields.CharField()

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("reviewer_id", pymongo.DESCENDING),
                               ("subject_id", pymongo.DESCENDING)],
                              unique=True)]


class GroupTestReview(MongoModel):
    reviewer_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE)
    subject_id = ValidatedReferenceField(GroupTest, on_delete=ReferenceField.CASCADE)
    value = fields.FloatField()
    description = fields.CharField()

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("reviewer_id", pymongo.DESCENDING),
                               ("subject_id", pymongo.DESCENDING)],
                              unique=True)]


class Survey(MongoModel):
    group_id = ValidatedReferenceField(Group, on_delete=ReferenceField.CASCADE)
    description = fields.CharField(required=True)
    survey_options = fields.DictField(required=True)
    survey_result = fields.DictField(default=None)

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True


# TODO Добавить валидацию: вариант ответа должен быть предусмотрен
class SurveyResponse(MongoModel):
    survey_id = ValidatedReferenceField(Survey, on_delete=ReferenceField.CASCADE)
    person_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE)
    chosen_option = fields.CharField(required=True)

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("survey_id", pymongo.DESCENDING),
                               ("person_id", pymongo.DESCENDING)],
                              unique=True)]


class AuthInfo(MongoModel):
    phone_no = fields.CharField()
    auth_code = fields.CharField(blank=True)
    last_send_time = fields.DateTimeField(blank=True)
    last_auth_time = fields.DateTimeField(blank=True)
    attempts = fields.IntegerField(default=0)
    is_approved = fields.BooleanField(default=False)
    password = fields.CharField(blank=True)
    session_id = fields.CharField(blank=True)
    person_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE, blank=True)
    permissions = fields.IntegerField(default=0)

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("phone_no", pymongo.DESCENDING)],
                              unique=True)]


init_model()
