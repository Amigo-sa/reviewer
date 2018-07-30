# -*- coding: utf-8 -*-
from pymodm import MongoModel, fields, ReferenceField
from pymongo.write_concern import WriteConcern
from pymodm.errors import ValidationError
from pymongo.operations import IndexModel
import pymongo
from pymodm.connection import connect, _get_db
import data.settings as settings

from collections import Counter

# TODO внедрить в базу номер версии модели и номер версии скрипта-заполнителя
model_version = "0.3"


def get_dependent_list(doc, dep_id_list):
    current_del_rules = doc._mongometa.delete_rules
    dep_id_list.append(doc)
    for item, rule in current_del_rules.items():
        related_model, related_field = item
        dependent_docs = related_model.objects.raw({related_field: doc.pk})
        for dep in dependent_docs:
            if dep not in dep_id_list:
                get_dependent_list(dep, dep_id_list)


def init_model():
    GroupRole.register_delete_rule(
        Group, "role_list", fields.ReferenceField.PULL)
    GroupPermission.register_delete_rule(
        GroupMember, "permissions", fields.ReferenceField.PULL)


connect(settings.mongo.conn_string + "/" + settings.mongo.db_name,
        alias="reviewer")


class ValidatedReferenceField(fields.ReferenceField):
    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)
        old_clean = getattr(cls, "clean", None)

        def new_clean(instance):
            ref_field = getattr(instance, name, None)
            if not self.related_model.objects.get({"_id": ref_field.pk}):
                raise ValidationError("ссылка на _id несуществующего объекта")
            old_clean(instance)

        setattr(cls, "clean", new_clean)

class Service(MongoModel):
    version = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True


class Person(MongoModel):
    first_name = fields.CharField()
    middle_name = fields.CharField()
    surname = fields.CharField()
    birth_date = fields.DateTimeField()
    phone_no = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("phone_no", pymongo.DESCENDING)],
                              unique=True)]


class Organization(MongoModel):
    name = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("name", pymongo.DESCENDING)],
                              unique=True)]


class Department(MongoModel):
    name = fields.CharField()
    organization_id = ValidatedReferenceField(Organization, on_delete=ReferenceField.CASCADE)

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("name", pymongo.DESCENDING),
                               ("organization_id", pymongo.DESCENDING)],
                              unique=True)]


class HardSkill(MongoModel):
    name = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("name", pymongo.DESCENDING)],
                              unique=True)]


class PersonHS(MongoModel):
    person_id = fields.ReferenceField(Person, on_delete=ReferenceField.CASCADE)
    hs_id = fields.ReferenceField(HardSkill, on_delete=ReferenceField.CASCADE)
    level = fields.FloatField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("person_id", pymongo.DESCENDING),
                               ("hs_id", pymongo.DESCENDING)],
                              unique=True)]


class SoftSkill(MongoModel):
    name = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("name", pymongo.DESCENDING)],
                              unique=True)]


class PersonSS(MongoModel):
    person_id = fields.ReferenceField(Person, on_delete=ReferenceField.CASCADE)
    ss_id = fields.ReferenceField(SoftSkill, on_delete=ReferenceField.CASCADE)
    level = fields.FloatField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("person_id", pymongo.DESCENDING),
                               ("ss_id", pymongo.DESCENDING)],
                              unique=True)]


class TutorRole(MongoModel):
    person_id = fields.ReferenceField(Person, on_delete=ReferenceField.CASCADE)
    department_id = fields.ReferenceField(Department, on_delete=ReferenceField.CASCADE)
    discipline = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("person_id", pymongo.DESCENDING),
                               ("department_id", pymongo.DESCENDING),
                               ("discipline", pymongo.DESCENDING)],
                              unique=True)]


class StudentRole(MongoModel):
    person_id = fields.ReferenceField(Person, on_delete=ReferenceField.CASCADE)
    department_id = fields.ReferenceField(Department, on_delete=ReferenceField.CASCADE)
    description = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("person_id", pymongo.DESCENDING),
                               ("department_id", pymongo.DESCENDING)],
                              unique=True)]


class GroupRole(MongoModel):
    name = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("name", pymongo.DESCENDING)],
                              unique=True)]


class GroupPermission(MongoModel):
    name = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("name", pymongo.DESCENDING)],
                              unique=True)]


class Group(MongoModel):
    department_id = ValidatedReferenceField(Department, on_delete=ReferenceField.CASCADE)
    name = fields.CharField()
    role_list = fields.ListField(field=
                                 fields.ReferenceField(GroupRole))

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("name", pymongo.DESCENDING),
                               ("department_id", pymongo.DESCENDING)],
                              unique=True)]


class GroupMember(MongoModel):
    person_id = fields.ReferenceField(Person, on_delete=ReferenceField.CASCADE)
    group_id = fields.ReferenceField(Group, on_delete=ReferenceField.CASCADE)
    role_id = fields.ReferenceField(GroupRole, on_delete=ReferenceField.DO_NOTHING, blank=True)
    permissions = fields.ListField(field=
                                   fields.ReferenceField(GroupPermission), blank=True)
    is_active = fields.BooleanField(required=True, default=True)

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("person_id", pymongo.DESCENDING),
                               ("group_id", pymongo.DESCENDING),
                               ("role_id", pymongo.DESCENDING)],
                              unique=True)]

    # TODO лучше реализовать это в виде validator
    def clean(self):
        if self.role_id:
            target_group = Group.objects.get({"_id": self.group_id.pk})
            if self.role_id not in target_group.role_list:
                raise ValidationError("Группа %s не предусматривает роль %s" % (
                    target_group.name, self.role_id.name))
        if [x for n, x in enumerate(self.permissions) if x in self.permissions[:n]]:
            raise ValidationError("Разрешения не должны повторяться")

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
    group_id = fields.ReferenceField(Group, on_delete=ReferenceField.CASCADE)
    name = fields.CharField()
    info = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True


class TestResult(MongoModel):
    test_id = fields.ReferenceField(GroupTest, on_delete=ReferenceField.CASCADE)
    person_id = fields.ReferenceField(Person, on_delete=ReferenceField.CASCADE)
    result_data = fields.ListField(field=fields.CharField())

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("test_id", pymongo.DESCENDING),
                               ("person_id", pymongo.DESCENDING)],
                              unique=True)]


class SSReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete=ReferenceField.CASCADE)
    subject_id = fields.ReferenceField(PersonSS, on_delete=ReferenceField.CASCADE)
    value = fields.FloatField()
    description = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("reviewer_id", pymongo.DESCENDING),
                               ("subject_id", pymongo.DESCENDING)],
                              unique=True)]


class HSReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete=ReferenceField.CASCADE)
    subject_id = fields.ReferenceField(PersonHS, on_delete=ReferenceField.CASCADE)
    value = fields.FloatField()
    description = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("reviewer_id", pymongo.DESCENDING),
                               ("subject_id", pymongo.DESCENDING)],
                              unique=True)]


class SRReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete=ReferenceField.CASCADE)
    subject_id = fields.ReferenceField(StudentRole, on_delete=ReferenceField.CASCADE)
    value = fields.FloatField()
    description = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("reviewer_id", pymongo.DESCENDING),
                               ("subject_id", pymongo.DESCENDING)],
                              unique=True)]


class TRReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete=ReferenceField.CASCADE)
    subject_id = fields.ReferenceField(TutorRole, on_delete=ReferenceField.CASCADE)
    value = fields.FloatField()
    description = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("reviewer_id", pymongo.DESCENDING),
                               ("subject_id", pymongo.DESCENDING)],
                              unique=True)]


class GroupReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete=ReferenceField.CASCADE)
    subject_id = fields.ReferenceField(Group, on_delete=ReferenceField.CASCADE)
    value = fields.FloatField()
    description = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("reviewer_id", pymongo.DESCENDING),
                               ("subject_id", pymongo.DESCENDING)],
                              unique=True)]


class GroupMemberReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete=ReferenceField.CASCADE)
    subject_id = fields.ReferenceField(GroupMember, on_delete=ReferenceField.CASCADE)
    value = fields.FloatField()
    description = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("reviewer_id", pymongo.DESCENDING),
                               ("subject_id", pymongo.DESCENDING)],
                              unique=True)]


class GroupTestReview(MongoModel):
    reviewer_id = fields.ReferenceField(Person, on_delete=ReferenceField.CASCADE)
    subject_id = fields.ReferenceField(GroupTest, on_delete=ReferenceField.CASCADE)
    value = fields.FloatField()
    description = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("reviewer_id", pymongo.DESCENDING),
                               ("subject_id", pymongo.DESCENDING)],
                              unique=True)]


class Survey(MongoModel):
    group_id = fields.ReferenceField(Group, on_delete=ReferenceField.CASCADE)
    description = fields.CharField()
    survey_data = fields.DictField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True


init_model()
