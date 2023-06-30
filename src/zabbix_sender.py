from pyzabbix import ZabbixMetric, ZabbixSender
from vars import ZABBIX_SERVER_URL
import json, logging

def zabbixSender(json_body, SITE_NAME):
    
    if "list" in json_body:
      packet = []
      for data in json_body["list"]:
        packet.append(ZabbixMetric(SITE_NAME, data['key'], data['status']))
    
    else:
      packet = [
        ZabbixMetric(SITE_NAME, json_body["key"], json_body['status'])
    ]
    
    fails = []
    try:
      for p in packet:
        result = ZabbixSender(ZABBIX_SERVER_URL).send([p])
        jsonres = json.loads(str(result))
        if jsonres["failed"] == 1:
          fails.append(p)  
        
    except Exception as e:
      error_msg = str(e) + ". Url used for GET request = " + ZABBIX_SERVER_URL 
      logging.error(error_msg)
      return "failed", error_msg
    
    if not fails:
      logging.info("Sent to Zabbix successfully (ZABBIX_SENDER)")
      return "succeeded", "Sent to Zabbix successfully"
    
    elif len(fails) == len(packet):
      logging.error("Sent to Zabbix failed (ZABBIX_SENDER)")
      return "failed", "Sent to Zabbix failed"
    else:
      logging.error(f"Sent to Zabbix (ZABBIX_SENDER) partially failed - failes: {len(fails)} - processed: {len(packet) - len(fails)}")
      return "partially failed", f"Sent to Zabbix failed for: {fails}"
      
    jsonres = json.loads(str(result))

    if jsonres["processed"] == params:
      logging.info("Sent to Zabbix successfully (ZABBIX_SENDER)")
      return "succeeded", "Sent to Zabbix successfully"
      
    elif jsonres["failed"] == params:
      logging.error("Sent to Zabbix failed for all Data (ZABBIX_SENDER)")
      return "failed", "Sent to Zabbix failed"
    else:
      logging.error("Sent to Zabbix (ZABBIX_SENDER). Failed: " + str(jsonres["failed"]) + " - Processed: " + str(jsonres["processed"]))
      return "partially failed", "Sent to Zabbix partially failed"
     
    #print(time.ctime() + " | send data to zabbix (ZABBIX_SENDER) - " + result)

