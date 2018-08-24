import reviewer_model
import sys, inspect
import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Digraph, ENGINES, FORMATS

members = inspect.getmembers(reviewer_model, inspect.isclass)

doc_class_list = []
class_names = []
for name, desc in members:
    if "reviewer_model." in str(desc):
        doc_class_list.append(desc)
        class_names.append(name)

links = {}

for doc_class in doc_class_list:
    print("--------------------------------------------------")
    cur_class = str(doc_class.__name__)
    print(cur_class + " references:")
    links.update({cur_class : []})
    member_list = inspect.getmembers(doc_class, None)
    for name,cls in member_list:
        if "pymodm.fields.ReferenceField" in str(cls)\
                or "reviewer_model.ValidatedReferenceField" in str(cls)\
                and "__dict__" not in str(name):
            #print(cls)
            rel_model = cls.related_model.__name__
            print(rel_model)
            links[cur_class].append(rel_model)
        if "reviewer_model.ValidatedReferenceList" in str(cls) \
                and "__dict__" not in str(name):
            member_list = inspect.getmembers(cls, None)
            rel_model = cls._field.related_model.__name__
            print(rel_model)
            links[cur_class].append(rel_model)

print(links)
links.pop("Service")
links.pop("ValidatedReferenceField")
links.pop("ValidatedReferenceList")
class_names.remove("Service")
class_names.remove("ValidatedReferenceField")
class_names.remove("ValidatedReferenceList")

dot = Digraph(comment='Reviewer')

dot.attr("node", shape="ellipse")
dot.attr(overlap='false')
for cls in class_names:
    dot.node(cls,cls)

for main, refs in links.items():
    for r in refs:
        dot.edge(main,r)

dot.engine="dot"
dot.format="svg"
dot.render('test-output/schema', view=True)
#for eng in ENGINES:
#    dot.engine=eng
#    dot.render('test-output/schema_'+eng, view=True)
