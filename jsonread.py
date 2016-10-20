#!/usr/bin/python2.7 -tt

import sys, getopt
import json
import os
import shutil
from pprint import pprint

def readjson(filename, localrun):
  try:
    with open(filename) as json_file:
      Testjson = json.load(json_file)
    
    #pprint(Testjson)
    print("find the top level")
    print(Testjson.keys())
    VMname = Testjson['name']
    VMinstance = Testjson['instanceView']
    #VMlocation = Testjson['location']
    print "name:",VMname
    pprint(VMinstance)
    
  except ValueError:
    print("Could not parse JSON file.")
    sys.exit(3)

def help():
  print('# This script will convert the jason file to an azuere vm create command. #')
  print('#')
  print('# -h help.')
  print('# -r run azure vm create [...] when done.')
  print('# By default the script will just print the command.')
  print('#')
  print('# $> jsonread.py [-r,-h] <jsonfile> ')
                                              
def main():
  runcommand = False  #Default to not run the vm create
  args = sys.argv[1:]
  if len(sys.argv) == 1:
    print("# Missing arguments.")
    print('# This script will convert the jason file to an azuere vm create command. #')
    print('# Use [-h,-r] <jsonfile>')
    sys.exit(2)
  else:
    for arg in args:
        if arg == '-h':
          help()
          sys.exit(0)
        elif arg == '-r':
          runcommand = True  #Run the vm create
        elif os.path.exists(str(arg)):
          readjson(arg, runcommand)
          sys.exit(0)
        else:
          print('** Error in Command!! **')
          exit(1)
    
if __name__=='__main__':
  main() 

#>>> with open('test.json') as data_file:
#...     data= json.load(data_file)
