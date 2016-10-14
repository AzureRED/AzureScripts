#!/usr/bin/python2.7 -tt

import sys
import json
import os
import shutil
from pprint import pprint

def readjson(filename):
  try:
    with open(filename) as json_file:
      Testjson = json.load(json_file)
    
    pprint(Testjson)
    print('/n')
  
  except IOError:
      print('** error file not accessable **')

def main():
  args = sys.argv[1:]
  if len(sys.argv) > 1:
    for arg in args:
      readjson(arg)
  else:
    print('** No file listed **')
    
if __name__=='__main__':
  main() 

#>>> with open('test.json') as data_file:
#...     data= json.load(data_file)
