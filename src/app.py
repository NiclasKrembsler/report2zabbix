import json, time, requests, logging, time
from api_sender import apiSender
from zabbix_sender import zabbixSender
from send_back import sendBack
from vars import BEAM_URL, beam_headers 
import threading

#wait for proxy to start
time.sleep(5)

def checkForTask():
    wait_url = BEAM_URL + "/v1/tasks?filter=todo&wait_count=1"
    payload = {}
    start = time.time()
    try:
        response = requests.request("GET", wait_url, headers=beam_headers, data=payload)
    except Exception as e:
        logging.error(f"{e}. Url used for GET request = {wait_url}")
        time.sleep(10)
        return None
        
    if response.status_code == 502:
        end = time.time() 
        logging.warning(f"GET timeout after {end-start}s")
        return None
    if response.status_code == 200:
        for task in response.json():
            try:
                if task["metadata"][0] == "passive_monitoring":
                    return task
            except:
                continue
    return None

def performTask(task):
    json_body = json.loads(task["body"])
    logging.info(f"Received new task - {task['metadata'][1]}")
    #print(time.ctime() + " | received new task - " + task["metadata"][1])
    
    if json_body["url"] == "ZABBIX_API_URL":
        status, result = apiSender(json_body)
    elif json_body["url"] == "ZABBIX_SERVER_URL":
        status, result = zabbixSender(json_body, task["metadata"][2])
        
    sendBack(task["id"], task["from"], result, status)

while True:
    task = None
    while task is None:
        task = checkForTask()
        if task is None:
            time.sleep(1) # Verzögerung zwischen den Abfragen, um Ressourcen zu schonen
    threading.Thread(target=performTask, args=(task,)).start()
    time.sleep(1)
    #performTask(task)