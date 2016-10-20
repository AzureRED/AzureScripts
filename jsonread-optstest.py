#!/usr/bin/python2.7 -tt

import sys, getopt
import json
import os
import shutil
from pprint import pprint

def readjson(filename):
  try:
    with open(filename) as json_file:
      Testjson = json.load(json_file)
    
    #pprint(Testjson)
    print("find the top level")
    print(Testjson.keys())
    
  
  except IOError:
      print('** error file not accessable **')


def help():
  print('# This script will convert the jason file to an azuere vm create command. #')
  print('#')
  print('# -h help.')
  print('# -r run azure vm create [...] when done.')
  print('# By default the script will just print the command.')
  print('#')
  print('# $> jsonread.py [-r,-h] <jsonfile> ')
                                              
def main(argv):
  args = sys.argv[1:]
  if len(sys.argv) == 1:
    print("*** Missing arguments. ***")
  else:
      try:
        print("Try")
        opts, args = getopt.getopt(argv, "hr:")
      except getopt.GetoptError:
        print('# This script will convert the jason file to an azuere vm create command. #')
        print('# Use [-h,-r] <jsonfile>')
        sys.exit(2)
        
      print("opt and args")  
      for opt, args in opts:
        print(opt, args)
        if opt == '-h':
          help()
          sys.exit(0)
        elif opt == '-r':
          run = True
        elif os.path.exists(str(args)):
          print("file:",str(args))
          readjson(args)
          sys.exit(0)
        else:
          print('** Error in Command!! **')
          exit(1)
    
if __name__=='__main__':
  main(sys.argv[1:]) 

#>>> with open('test.json') as data_file:
#...     data= json.load(data_file)
