import requests
import time
from threading import Thread
import settings.constants as CONSTANTS
from flask import Flask


status = False
#while not status:
#    time.sleep(2)
#    try:
#        r = requests.post(CONSTANTS.core_server_url +'/register', json = CONSTANTS.node_id)
#        if r.status_code == requests.codes.ok:
#            status = True
#    except Exception as ex:
#        print(ex)


existing_nodes = None

class UpdateNetwork(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(2)
            try:
                r = requests.get(CONSTANTS.core_server_url +'/get_network_info')
                existing_nodes = r.json()
                print(existing_nodes)
            except Exception as ex:
                print(ex)

update_network_thread = UpdateNetwork()
#update_network_thread.start()

app = Flask(__name__)

import test.read_data


print("Script ended")