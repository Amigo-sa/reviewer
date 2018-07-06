import requests
import time
from threading import Thread
import settings.constants as constants
import pymongo


def is_db_exists():
    rev_client = pymongo.MongoClient(constants.mongo_db)
    rev_db = rev_client["reviewer"]

    try:
        col_list = rev_db.list_collection_names()
    except Exception as ex:
        print(ex)
        return False
    if col_list == []:
        return False
    return True


def print_something_from_db():

    rev_client = pymongo.MongoClient(constants.mongo_db)
    rev_db = rev_client["reviewer"]
    col_person = rev_db["Person"]
    cursor = col_person.find({})

    try:
        for person in cursor:
            print(person["Name"])
    except Exception as ex:
        print(ex)

    return


if (is_db_exists()):
    print_something_from_db()

status = False
while not status:
    time.sleep(2)
    try:
        r = requests.post(constants.core_server_url +'/register', json = constants.node_id)
        if r.status_code == requests.codes.ok:
            status = True
    except Exception as ex:
        print(ex)


existing_nodes = None

class UpdateNetwork(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(2)
            try:
                r = requests.get(constants.core_server_url +'/get_network_info')
                existing_nodes = r.json()
                print(existing_nodes)
            except Exception as ex:
                print(ex)

update_network_thread = UpdateNetwork()
update_network_thread.start()

