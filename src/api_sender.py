import json, requests, time, logging
from vars import ZABBIX_API_URL, zabbix_api_headers
from http.client import responses

def apiSender(json_body):
    payload = json_body['payload']
    payload = json.dumps(payload)
    try:
      api_resp = requests.request("POST", ZABBIX_API_URL, headers=zabbix_api_headers, data=payload)

    except Exception as e:
      error_msg = str(e) + " . Url used for GET request = " + ZABBIX_API_URL 
      logging.error(error_msg)
      return "failed", error_msg
      
    if api_resp.status_code == 200:
        logging.info(f"Send data to Zabbix via API - {api_resp.status_code} {responses[api_resp.status_code]}")
        #print(time.ctime() + " | send data to zabbix (API) - " + str(api_resp.status_code) " " + responses[api_resp.status_code])
        return "succeeded", str(api_resp.text)
    else:
        logging.error(f"Send data to Zabbix via API failed - {api_resp.status_code} {responses[api_resp.status_code]}")
        return "failed", f"Send data to Zabbix via API failed - {api_resp.status_code} {responses[api_resp.status_code]}"