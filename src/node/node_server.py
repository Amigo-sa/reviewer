# -*- coding: utf-8 -*-
import context
import requests
import time
from threading import Thread
from node.settings import constants
import pymongo
from flask import Flask
from node.api.routes import bp as routes
from node.api.debug import bp as debug
from node.api.auth import bp as auth
from node.api.organizations import bp as organizations
from node.api.departments import bp as departments
from pymodm.connection import connect

app = Flask(__name__)
app.register_blueprint(debug)
app.register_blueprint(auth)
app.register_blueprint(routes)
app.register_blueprint(organizations)
app.register_blueprint(departments)


def start_server(port, protocol="http"):
    if protocol == "http":
        app.run(port=port)
    elif protocol == "https":
        app.run(port=port, ssl_context=('cert.pem', 'key.pem'))


if __name__ == "__main__":
    start_server(constants.node_server_port, protocol="https")

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

