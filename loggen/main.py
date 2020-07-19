from faker import Faker
import requests
import random
import logging
import sys
import time
import re

class MultilineTracebackFormatter(logging.Formatter):
  def __init__(self, formatter):
    self._formatter = formatter
  def format(self, record):
    msg = self._formatter.format(record)
    if record.exc_info is not None:
      msg = msg.replace('\n', '\nTRACE:')
    return msg

# Create faker instance before configuring logging to keep it surpressed
faker = Faker()
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
log = logging.getLogger(__name__)
ip_addresses = [faker.ipv4_public() for i in range(0, 20)]
error_codes  = [20000+i for i in range(0, 20)]

for hdlr in logging.getLogger().handlers:
  fmtr = hdlr.formatter
  hdlr.formatter = MultilineTracebackFormatter(fmtr)

def log_new_connection():
  addr = random.choice(ip_addresses)
  log.info(f'New connection from peer:{addr}')

def log_reconnect():
  addr = random.choice(ip_addresses)
  log.info(f'Peer reconnected peer:{addr}')

def log_errors():
  addr = random.choice(ip_addresses)
  code = random.choice(error_codes)
  log.error(f'Error code:{code} from peer:{addr}')

def log_http_request():
  url = 'http://nginx'
  try:
    r = requests.get(url)
    log.debug(f'Got status:{r.status_code} from url:{url}')
  except:
    log.exception(f'Failed to GET from {url}')

functions = [
  log_new_connection,
  log_reconnect,
  log_errors,
  log_http_request
]

if __name__ == "__main__":
  log = logging.getLogger('server')
  while True:
    time.sleep(random.choice([0.125, 0.5, 1, 2]))
    fn = random.choice(functions)
    fn()    
