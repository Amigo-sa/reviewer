# -*- coding: utf-8 -*-
import context
import requests
import time
from threading import Thread
from node.settings import constants
import pymongo
from flask import Flask
from node.api.routes import bp as routes
from node.api.routes_debug import bp as routes_debug
from pymodm.connection import connect

app = Flask(__name__)
app.register_blueprint(routes_debug)
app.register_blueprint(routes)


def start_server(port):
    app.run(port=port)


if __name__ == "__main__":
    start_server(constants.node_server_port)

def is_db_exists():
    rev_client = pymongo.MongoClient(constants.mongo_db)

    try:
        rev_db_names = rev_client.list_database_names()
        if constants.db_name in rev_db_names:
            return True
        else:
            return False
    except Exception as ex:
        print(ex)
        return False


if __debug__:
    def print_something_from_db():

        rev_client = pymongo.MongoClient(constants.mongo_db)
        rev_db = rev_client[constants.db_name_test]
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



class UpdateNetwork(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        status = False
        while not status:
            time.sleep(2)
            try:
                r = requests.post(constants.core_server_url + '/register', json=constants.node_id)
                if r.status_code == requests.codes.ok:
                    status = True
            except Exception as ex:
                print(ex)

        while True:
            time.sleep(2)
            try:
                r = requests.get(constants.core_server_url +'/get_network_info')
                existing_nodes = r.json()
                print(existing_nodes)
            except Exception as ex:
                print(ex)

update_network_thread = UpdateNetwork()
#update_network_thread.start()

