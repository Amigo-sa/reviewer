import requests
import time

me = {"ip":"10.0.0.10", "port": 1000}
status = False
while not status:
    try:
        r = requests.post('http://127.0.0.1:5000/register', json = me)
        if r.status_code == requests.codes.ok:
            status = True
    except:
        print("Сервер не доступен")


existing_nodes = None
while True:
    time.sleep(2)
    try:
        r = requests.get('http://127.0.0.1:5000/get_network_info')
        existing_nodes = r.json()
        print(existing_nodes)
    except:
        print("Сервер не доступен")
