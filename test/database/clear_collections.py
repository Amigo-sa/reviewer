from pymodm.connection import connect, _get_db
from node.settings import constants

connect(constants.mongo_db + "/" + constants.db_name, alias="reviewer")

print("clearing db...")
revDb = _get_db("reviewer")
colList = revDb.list_collection_names()
for col in colList:
    revDb.drop_collection(col)
    print("dropped collection " + col)
print("done")
