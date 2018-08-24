import os, sys

parentPath = os.path.abspath("..//..//src")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

import data.reviewer_model
import sys, inspect
from graphviz import Digraph, ENGINES, FORMATS

members = inspect.getmembers(data.reviewer_model, inspect.isclass)

doc_class_list = []
class_names = []
for name, desc in members:
    if "reviewer_model." in str(desc):
        doc_class_list.append(desc)
        class_names.append(name)

links = {}
fields = {}
for doc_class in doc_class_list:
    print("--------------------------------------------------")
    cur_class = str(doc_class.__name__)
    print(cur_class + " references:")
    links.update({cur_class : []})
    fields.update({cur_class : []})
    member_list = inspect.getmembers(doc_class, None)
    for name,cls in member_list:
        if "__dict__" not in str(name):
            if "pymodm.fields.ReferenceField" in str(cls)\
                    or "reviewer_model.ValidatedReferenceField" in str(cls):
                #print(cls)
                rel_model = cls.related_model.__name__
                print(rel_model)
                links[cur_class].append(rel_model)
            if "reviewer_model.ValidatedReferenceList" in str(cls):
                member_list = inspect.getmembers(cls, None)
                rel_model = cls._field.related_model.__name__
                print(rel_model)
                links[cur_class].append(rel_model)
            if "fields.CharField" in str(cls):
                field = name + ": char"
                fields[cur_class].append(field)
            if "fields.DateTimeField" in str(cls):
                field = name + ": datetime"
                fields[cur_class].append(field)
            if "fields.FloatField" in str(cls):
                field = name + ": float"
                fields[cur_class].append(field)
            if "fields.DictField" in str(cls):
                field = name + ": dict"
                fields[cur_class].append(field)
            if "fields.ListField" in str(cls):
                field = name + ": list"
                fields[cur_class].append(field)
            if "fields.IntegerField" in str(cls):
                field = name + ": int"
                fields[cur_class].append(field)
            if "fields.BooleanField" in str(cls):
                field = name + ": bool"
                fields[cur_class].append(field)

ignore_list = [
    "Service",
    "ValidatedReferenceField",
    "ValidatedReferenceList"
]
for item in ignore_list:
    links.pop(item)
    class_names.remove(item)
    fields.pop(item)

dot = Digraph(comment='Reviewer')

dot.attr("node", shape="ellipse")
dot.attr(overlap='false')
for cls, field_list in fields.items():
    label = cls + "\n"
    for field in field_list:
        label+= field + "\n"
    dot.node(cls,label)

for main, refs in links.items():
    for r in refs:
        dot.edge(main,r)

dot.engine="dot"
dot.format="svg"
dot.render('../db_model/drawer_output/schema', view=False)
dot.format="png"
dot.render('../db_model/drawer_output/schema', view=False)
#for eng in ENGINES:
#    dot.engine=eng
#    dot.render('test-output/schema_'+eng, view=True)
