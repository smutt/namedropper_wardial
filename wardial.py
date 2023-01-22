#!/usr/bin/env python

import time
import requests
from bs4 import BeautifulSoup
import os
import random


base_url = 'https://marc.info/?l=namedroppers&m='
msg_prefix = '95837'
msg_start = 667426365
msg_end = 798827125


def write_file(ss, name):
  fn = open(name, 'w')
  fn.write(ss)
  fn.close()

def grab(msg):
  print("Grabbing:" + msg)

  try:
    os.stat(msg)
    fn = open(msg, 'r')
    soup = BeautifulSoup(fn.read(), 'html.parser')
    
  except OSError:
    time.sleep(2) # Be polite
    print("Fetching:" + msg)
    req = requests.get(base_url + msg)
    if req.status_code == 200:
      write_file(req.text, msg + '.war')
      print("Grabbed:" + msg)
    else:
      print("ERROR grabbing: " + msg)


# START
random.seed()

while True:
  mid = str(random.randrange(msg_start, msg_end))
  grab(msg_prefix + mid)
