import os, sys

parentPath = os.path.abspath("..//..//src")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
