from pyzabbix import ZabbixMetric, ZabbixSender
from vars import ZABBIX_SERVER_URL
import json, logging

def zabbixSender(json_body, SITE_NAME):


    if type(json_body) == list:
      params = len(json_body)
      packet = []
      for data in json_body:
        packet.append(ZabbixMetric(SITE_NAME, data['key'], data['status']))
    
    else:
      params = 1
      packet = [
        ZabbixMetric(SITE_NAME, json_body["key"], json_body['status'])
    ]
    
    try:
      result = ZabbixSender(ZABBIX_SERVER_URL).send(packet)
    
    except Exception as e:
      error_msg = str(e) + ". Url used for GET request = " + ZABBIX_SERVER_URL 
      logging.error(error_msg)
      return "failed", error_msg
    
    jsonres = json.loads(str(result))

    if jsonres["processed"] == params:
      logging.info("Sent to Zabbix successfully (ZABBIX_SENDER)")
      return "succeeded", "Sent to Zabbix successfully"
      
    elif jsonres["failed"] == params:
      logging.error("Sent to Zabbix failed for all Data (ZABBIX_SENDER)")
      return "failed", "Sent to Zabbix failed"
    else:
      logging.error("Sent to Zabbix (ZABBIX_SENDER). Failed: " + jsonres["failed"] + "- Processed: " + jsonres["processed"])
      return "partially failed", "Sent to Zabbix partially failed"
     
    #print(time.ctime() + " | send data to zabbix (ZABBIX_SENDER) - " + result)

