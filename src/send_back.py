import requests, json, time, logging
from vars import beam_headers, BEAM_URL, PROXY_ID
from http.client import responses

def sendBack(id, to,  result, status):
    
    url = BEAM_URL + "/v1/tasks/" + id + "/results/" + PROXY_ID
    
    payload = json.dumps({
      "from": PROXY_ID,
      "metadata": str(status),
      "status": "succeeded",
      "body": str(result),
      "task": str(id),
      "to": [
        str(to)
      ]
    })
    
    try:
      response = requests.request("PUT", url, headers=beam_headers, data=payload)
    except Exception as e:
      logging.error(f"{e}. Url used for PUT request = {url}")
    
    if response.status_code != 201:
      logging.error(f"Task could not be created {response.status_code} {responses[response.status_code]}")