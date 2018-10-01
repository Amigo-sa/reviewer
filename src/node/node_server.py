# -*- coding: utf-8 -*-
import context
import requests
import time
from threading import Thread
from node.settings import constants
import pymongo
from flask import Flask
from node.api.versioning import register_api_default, register_api_v1, register_api_v2
from node.api.logging import bp as bp_logging
from node.api.logging import configure_logger
from pymodm.connection import connect
import logging
import os


app = Flask(__name__)
register_api_default(app)
register_api_v1(app)
register_api_v2(app)

try:
    app_mode = os.environ["REVIEWER_APP_MODE"]
except Exception as e:
    logging.error("Environment variable REVIEWER_APP_MODE must be defined !")
    raise

if app_mode == "production" or app_mode == "development" or app_mode == "load":
    configure_logger(app)

app.register_blueprint(bp_logging)


def start_server(port, protocol="http", log=True):
    if not log:
        for handler in logging.getLogger().handlers:
            logging.getLogger().removeHandler(handler)
        for handler in app.logger.handlers:
            app.logger.removeHandler(handler)
    if protocol == "http":
        app.run(port=port)
    elif protocol == "https":
        app.run(port=port, ssl_context=('cert.pem', 'key.pem'))


if __name__ == "__main__":
    start_server(constants.node_server_port, protocol="http", log=False)


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


