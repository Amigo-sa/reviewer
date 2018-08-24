# -*- coding: utf-8 -*-
import sys
from pymodm import MongoModel, fields, ReferenceField
from pymongo.write_concern import WriteConcern
from pymodm.errors import ValidationError
from pymongo.operations import IndexModel
import pymongo
from pymodm.connection import connect
import data.settings as settings
from node.settings import constants

from collections import Counter

model_version = "0.4"

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

db_name = constants.db_name
print("DB initialized with argv: " + str(sys.argv))
if len(sys.argv) > 1:
    if '--test' in str(sys.argv):
        db_name = constants.db_name_test
print("Working with DB '%s' \n"%db_name)
connect(constants.mongo_db + "/" + db_name, alias="reviewer")


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
                    raise ValidationError("ссылка на _id несуществующего объекта")
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
    person_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE)
    hs_id = ValidatedReferenceField(HardSkill, on_delete=ReferenceField.CASCADE)
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
    person_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE)
    ss_id = ValidatedReferenceField(SoftSkill, on_delete=ReferenceField.CASCADE)
    level = fields.FloatField()

    class Meta:
        write_concern = WriteConcern(j=True)
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
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("detail", pymongo.DESCENDING)],
                              unique=False)]

class PersonSpecialization(MongoModel):
    person_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE)
    department_id = ValidatedReferenceField(Department, on_delete=ReferenceField.CASCADE)
    specialization_id = ValidatedReferenceField(Specialization, on_delete=ReferenceField.CASCADE)
    details = fields.DictField()

    is_active = fields.BooleanField(required=True, default=True)

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("person_id", pymongo.DESCENDING),
                               ("department_id", pymongo.DESCENDING),
                               ("specialization_id", pymongo.DESCENDING)],
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
    role_list = ValidatedReferenceList(field=
                                       fields.ReferenceField(GroupRole))

    class Meta:
        write_concern = WriteConcern(j=True)
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
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("person_id", pymongo.DESCENDING),
                               ("group_id", pymongo.DESCENDING),
                               ("role_id", pymongo.DESCENDING)],
                              unique=True)]

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
        write_concern = WriteConcern(j=True)
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
        write_concern = WriteConcern(j=True)
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
        write_concern = WriteConcern(j=True)
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
        write_concern = WriteConcern(j=True)
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
        write_concern = WriteConcern(j=True)
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
        write_concern = WriteConcern(j=True)
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
        write_concern = WriteConcern(j=True)
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
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("reviewer_id", pymongo.DESCENDING),
                               ("subject_id", pymongo.DESCENDING)],
                              unique=True)]


class Survey(MongoModel):
    group_id = ValidatedReferenceField(Group, on_delete=ReferenceField.CASCADE)
    description = fields.CharField()
    survey_data = fields.DictField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True


class AuthInfo(MongoModel):
    phone_no = fields.CharField()
    auth_code = fields.CharField(blank=True)
    last_send_time = fields.TimestampField()
    attempts = fields.IntegerField(default=0)
    is_approved = fields.BooleanField(default=False)
    password = fields.CharField(blank=True)
    session_id = fields.CharField(blank=True)
    person_id = ValidatedReferenceField(Person, on_delete=ReferenceField.CASCADE, blank=True)
    permissions = fields.IntegerField(default=0)

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "reviewer"
        final = True
        indexes = [IndexModel([("phone_no", pymongo.DESCENDING)],
                              unique=True)]


init_model()
