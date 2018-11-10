# -*- coding: utf-8 -*-
import sys

from bson import ObjectId
from pymodm import MongoModel, fields, ReferenceField
from pymongo.write_concern import WriteConcern
from pymodm.errors import ValidationError, DoesNotExist
from pymongo.operations import IndexModel
import pymongo
from pymodm.connection import connect
import context
from node.settings import constants
import os
import logging

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

def update_subject_level(review_cls, subj):
    pipeline = ({"$match": {"subject_id": subj.pk}},
                {"$group": {"_id": "null",
                            "value": {"$avg": "$value"}
                            }
                 },
                )
    result = list(review_cls.objects.aggregate(*pipeline))
    subj.refresh_from_db()
    subj.level = result[0]["value"] if result else None
    subj.save()

def update_person_subrating(skill_cls, person):
    pipeline = ({"$match": {"person_id": person.pk}},
                {"$match": {"level": {"$ne": None}}}
                )
    if skill_cls == PersonSS:
        pipeline += (
            {"$lookup":
                 {"from": "soft_skill",
                  "localField": "ss_id",
                  "foreignField": "_id",
                  "as": "soft_skill"}},
            {"$project":
                 {"level": 1,
                  "soft_skill": {"$arrayElemAt": ["$soft_skill", 0]}}},
            {"$group": {"_id": "null",
                            "sum": {"$sum": {"$multiply" : ["$level", "$soft_skill.weight"]}},
                            "count": {"$sum": "$soft_skill.weight"}
                        }},
        )
    else:
        pipeline += ({"$group": {"_id": "null",
                                 "level": {"$avg": "$level"}
                                }
                      },)

    result = list(skill_cls.objects.aggregate(*pipeline))
    person.refresh_from_db()
    if skill_cls == PersonSpecialization:
        person.spec_rating = result[0]["level"] if result else None
    if skill_cls == PersonHS:
        person.hs_rating = result[0]["level"] if result else None
    if skill_cls == PersonSS:
        person.ss_rating = result[0]["sum"]/result[0]["count"] if result else None
    person.save()

# TODO возможно, это лишнее. Сейчас валидация происходит, даже если запись была отредактирована и поле-ссылка не менялась
class ValidatedReferenceField(fields.ReferenceField):
    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)
        old_clean = getattr(cls, "clean", None)

        def new_clean(instance):
            ref_field = getattr(instance, name, None) # эта строчка делает запрос в базу (find по id)
            ref_class = getattr(cls, name, None)
            if ref_field is None:
                if not ref_class.blank:
                    raise DoesNotExist("ссылка на _id несуществующего объекта")
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
                    raise DoesNotExist("ссылка на _id несуществующего объекта")
                else:
                    if not self._field.related_model.objects.get({"_id": item.pk}):
                        raise DoesNotExist("ссылка на _id несуществующего объекта")
            old_clean(instance)

        setattr(cls, "clean", new_clean)

def add_person_skill_review(skill_review_cls, reviewer_id, person_id, skill_id, value, topic, description, date):
    #здесь намеренно не проверяем объекты, на которые ссылаемся. Проверки осуществляются методами ValidatedReferenceField
    query = {}
    query.update({"person_id": ObjectId(person_id)})
    if skill_review_cls == HSReview:
        person_skill_cls = PersonHS
        query.update({"hs_id": ObjectId(skill_id)})
    elif skill_review_cls == SSReview:
        person_skill_cls = PersonSS
        query.update({"ss_id": ObjectId(skill_id)})
    try:
        person_s = person_skill_cls.objects.get(query)
    except DoesNotExist:
        person_s = person_skill_cls(person_id, skill_id, None)
        person_s.save()
    s_review = skill_review_cls(reviewer_id, person_s.pk, value, topic, description, date)
    s_review.save()
    return str(s_review.pk)


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
    notes = fields.CharField()
    ss_rating = fields.FloatField(default=None, blank=True)
    hs_rating = fields.FloatField(default=None, blank=True)
    spec_rating = fields.FloatField(default=None, blank=True)
    auth_key = fields.CharField(blank=True)
    #rating = fields.FloatField(default=None, blank=True)
    # TODO нужно оставить либо поле rating, либо метод get_rating - смотреть по производиельности
    def get_rating(self):
        if (self.ss_rating == self.hs_rating == self.spec_rating == None):
            return None
        return (  (self.ss_rating or 50)
                + (self.hs_rating or 50)
                + (self.spec_rating or 50) * 2)\
               / 4

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
    display_text = fields.CharField()

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("name", pymongo.DESCENDING)],
                              unique=True)]


class HardSkill(MongoModel):
    name = fields.CharField()
    skill_type_id = ValidatedReferenceField(SkillType, on_delete=ReferenceField.CASCADE)
    display_text = fields.CharField()

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
    level = fields.FloatField(default=None, blank=True)

    def save(self, cascade=None, full_clean=True, force_insert=False):
        super().save(cascade, full_clean, force_insert)
        update_person_subrating(PersonHS, self.person_id)

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
    weight = fields.IntegerField()
    display_text = fields.CharField()

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
    level = fields.FloatField(default=None, blank=True)

    def save(self, cascade=None, full_clean=True, force_insert=False):
        super().save(cascade, full_clean, force_insert)
        update_person_subrating(PersonSS, self.person_id)

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

    def save(self, cascade=None, full_clean=True, force_insert=False):
        super().save(cascade, full_clean, force_insert)
        update_person_subrating(PersonSpecialization, self.person_id)

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
                              unique=True),
                   IndexModel("department_id")]


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
    topic = fields.CharField()
    description = fields.CharField()
    date = fields.DateTimeField()

    def save(self, cascade=None, full_clean=True, force_insert=False):
        super().save(cascade, full_clean, force_insert)
        update_subject_level(SSReview, self.subject_id)

    def delete(self):
        super().delete()
        update_subject_level(SSReview, self.subject_id)

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("reviewer_id", pymongo.DESCENDING),
                               ("subject_id", pymongo.DESCENDING)],
                              unique=True),
                   IndexModel("subject_id")]


class HSReview(MongoModel):
    reviewer_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE)
    subject_id = ValidatedReferenceField(PersonHS, on_delete=ReferenceField.CASCADE)
    value = fields.FloatField()
    topic = fields.CharField()
    description = fields.CharField()
    date = fields.DateTimeField()

    def save(self, cascade=None, full_clean=True, force_insert=False):
        super().save(cascade, full_clean, force_insert)
        update_subject_level(HSReview, self.subject_id)

    def delete(self):
        super().delete()
        update_subject_level(HSReview, self.subject_id)

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("reviewer_id", pymongo.DESCENDING),
                               ("subject_id", pymongo.DESCENDING)],
                              unique=True),
                   IndexModel("subject_id")]


class SpecializationReview(MongoModel):
    reviewer_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE)
    subject_id = ValidatedReferenceField(PersonSpecialization, on_delete=ReferenceField.CASCADE)
    value = fields.FloatField()
    topic = fields.CharField()
    description = fields.CharField()
    date = fields.DateTimeField()

    def save(self, cascade=None, full_clean=True, force_insert=False):
        super().save(cascade, full_clean, force_insert)
        update_subject_level(SpecializationReview, self.subject_id)

    def delete(self):
        super().delete()
        update_subject_level(SpecializationReview, self.subject_id)

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("reviewer_id", pymongo.DESCENDING),
                               ("subject_id", pymongo.DESCENDING)],
                              unique=True),
                   IndexModel("subject_id")]


class GroupReview(MongoModel):
    reviewer_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE)
    subject_id = ValidatedReferenceField(Group, on_delete=ReferenceField.CASCADE)
    value = fields.FloatField()
    topic = fields.CharField()
    description = fields.CharField()
    date = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("reviewer_id", pymongo.DESCENDING),
                               ("subject_id", pymongo.DESCENDING)],
                              unique=True),
                   IndexModel("subject_id")]


class GroupMemberReview(MongoModel):
    reviewer_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE)
    subject_id = ValidatedReferenceField(GroupMember, on_delete=ReferenceField.CASCADE)
    value = fields.FloatField()
    topic = fields.CharField()
    description = fields.CharField()
    date = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("reviewer_id", pymongo.DESCENDING),
                               ("subject_id", pymongo.DESCENDING)],
                              unique=True),
                   IndexModel("subject_id")]


class GroupTestReview(MongoModel):
    reviewer_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE)
    subject_id = ValidatedReferenceField(GroupTest, on_delete=ReferenceField.CASCADE)
    value = fields.FloatField()
    topic = fields.CharField()
    description = fields.CharField()
    date = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(w=1)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("reviewer_id", pymongo.DESCENDING),
                               ("subject_id", pymongo.DESCENDING)],
                              unique=True),
                   IndexModel("subject_id")]


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
                              unique=True),
                   IndexModel("session_id")]


init_model()
