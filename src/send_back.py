import requests, json, time, logging
from vars import beam_headers, BEAM_URL
from http.client import responses

def sendBack(id, to,  result, status):
    
    url = BEAM_URL + "/v1/tasks/" + id + "/results/" + to
    
    payload = json.dumps({
      "from": "zabbix.niclas-dev.broker.dev.ccp-it.dktk.dkfz.de",
      "metadata": status,
      "status": "succeeded",
      "body": result,
      "task": str(id),
      "to": [
        str(to)
      ]
    })
    
    try:
      response = requests.request("PUT", url, headers=beam_headers, data=payload)
    except Exception as e:
      logging.error(str(e) + " Url used for PUT request = " + url)
    
    if response.status_code == 201:
      logging.info("Task created successfully") 
    
    else:
      logging.error("Task could not be created" + str(response.status_code) + " " + responses[response.status_code])