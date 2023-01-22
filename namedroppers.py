#!/usr/bin/env python

import time
import requests
from bs4 import BeautifulSoup
import os

base_url = 'https://marc.info/?l=namedroppers&m='
#start_msg = '95837667426457' #error at 95837667426596 and 95837667426600
#start_msg = '95837667426602' #error at 95837667426596 and 95837667426606
start_msg = '95837667426609'

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
    time.sleep(0.5) # Be polite
    print("Fetching:" + msg)
    req = requests.get(base_url + msg)
    if req.status_code == 200:
      write_file(req.text, msg)
      soup = BeautifulSoup(req.text, 'html.parser')
    else:
      print("ERROR grabbing: " + msg)
      return None, None

  links = soup.find_all('a')
  prev = links[0].get('href').split('&m=')[1].split('&')[0]
  nex =  links[1].get('href').split('&m=')[1].split('&')[0]
    
  #print("prev:" + prev)
  #print("nex:" + nex)
  return prev, nex

walk_back = walk_forward = True
prev, nex = grab(start_msg)
while walk_back or walk_forward:
  if walk_back:
    prev, _ = grab(prev)
    if not prev:
      print("stopped walking backwards")
      walk_back = False
  if walk_forward:
    _, nex = grab(nex)
    if not nex:
      print("stopped walking forwards")
      walk_forward = False

