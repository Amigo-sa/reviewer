import sys
import context

from pymodm.connection import connect, _get_db
from node.settings import constants

db_name = constants.db_name
print("DB initialized with argv: " + str(sys.argv))
if len(sys.argv) > 1:
    if '--test' in str(sys.argv):
        db_name = constants.db_name_test
print("Working with DB '%s' \n" % db_name)
connect(constants.mongo_db + "/" + db_name, alias="reviewer")

print("clearing db...")
revDb = _get_db("reviewer")
colList = revDb.list_collection_names()
for col in colList:
    revDb.drop_collection(col)
    print("dropped collection " + col)
print("done")
