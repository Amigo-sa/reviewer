import requests
import time
from threading import Thread

me = {"ip":"10.0.0.10", "port": 1000}
status = False
while not status:
    time.sleep(2)
    try:
        r = requests.post('http://127.0.0.1:5000/register', json = me)
        if r.status_code == requests.codes.ok:
            status = True
    except:
        print("Сервер не доступен")


existing_nodes = None

class UpdateNetwork(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(2)
            try:
                r = requests.get('http://127.0.0.1:5000/get_network_info')
                existing_nodes = r.json()
                print(existing_nodes)
            except:
                print("Сервер не доступен")

update_network_thread = UpdateNetwork()
update_network_thread.start()
print("Script ended")