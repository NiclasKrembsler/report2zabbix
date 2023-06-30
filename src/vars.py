import logging, colorlog, os

ZABBIX_SERVER_URL = os.environ['ZABBIX_SERVER_URL']
ZABBIX_API_URL = "https://" + ZABBIX_SERVER_URL + "/zabbix/api_jsonrpc.php"
BEAM_URL = os.environ['BEAM_URL']
PROXY_ID = os.environ['PROXY_ID']
KEY = os.environ['KEY']

beam_headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': 'ApiKey ' + PROXY_ID + " " + KEY
    }  
    
zabbix_api_headers = {
            'content-type': 'application/json',
            'Accept': 'application/json',
    }
#set up logger

log_colors = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}
# Konfiguration des Logging-Handlers
handler = colorlog.StreamHandler()
formatter_str = '%(asctime)s | %(log_color)s%(levelname)s%(reset)s::%(funcName)s | %(message)s'
handler.setFormatter(colorlog.ColoredFormatter(formatter_str, log_colors=log_colors, reset=True, datefmt='%Y-%m-%d %H:%M:%S'))
logging.basicConfig(level=logging.INFO, handlers=[handler]) # Log-Level auf INFO setzen

logging.root.addHandler(handler)