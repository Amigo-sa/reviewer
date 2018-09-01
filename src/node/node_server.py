# -*- coding: utf-8 -*-
import context
import requests
import time
from threading import Thread
from node.settings import constants
import pymongo
from flask import Flask
from node.api.debug import bp as debug
from node.api.auth import bp as auth
from node.api.organizations import bp as organizations
from node.api.departments import bp as departments
from node.api.groups import bp as groups
from node.api.specializations import bp as specializations
from node.api.reviews import bp as reviews
from node.api.persons import bp as persons
from node.api.skills import bp as skills
from node.api.group_tests import bp as group_tests
from node.api.surveys import bp as surveys
from pymodm.connection import connect
import logging
import logging.handlers
import os

app = Flask(__name__)
app.register_blueprint(debug)
app.register_blueprint(auth)
app.register_blueprint(organizations)
app.register_blueprint(departments)
app.register_blueprint(groups)
app.register_blueprint(specializations)
app.register_blueprint(reviews)
app.register_blueprint(persons)
app.register_blueprint(skills)
app.register_blueprint(group_tests)
app.register_blueprint(surveys)


try:
    app_mode = os.environ["REVIEWER_APP_MODE"]
except Exception as e:
    logging.error(str(e))
    app_mode = "development"

fh = None
if app_mode == "production":
    try:
        log_path = os.path.abspath(constants.log_path)

        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.DEBUG)

        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        root_logger.addHandler(fh)
        app.logger.addHandler(fh)
        #root_logger.addHandler(sh)
        #app.logger.addHandler(sh)

        from flask.logging import default_handler
        app.logger.removeHandler(default_handler)
    except Exception as e:
        logging.exception(str(e))


def start_server(port, protocol="http", log=True):
    if fh and not log:
        root_logger.removeHandler(fh)
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


def get_app_mode():
    return app_mode