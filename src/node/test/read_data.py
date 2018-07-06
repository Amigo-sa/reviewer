from node_server import app
import pymongo
import settings.mongo as mongosettings

rev_client = pymongo.MongoClient(mongosettings.connString)
rev_db = rev_client["reviewer"]

@app.route('/')
@app.route('/index')
def index():
    collection_names = rev_db.list_collection_names()
    result_string = "Db content: <br>"
    for name in collection_names:
        result_string += "Column: {0}<br>".format(name)
        collection = rev_db[name]
        cursor = collection.find({})
        for document in cursor:
              result_string += "document: {0}<br>".format(document)
    return result_string
        


app.run (debug = True, port = 1000)