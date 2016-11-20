#!/usr/bin/python2.7 -tt

import sys, getopt
import json
import os
import shutil
import re

# A more robust way to find the keys:values
def isinjson(jskey):
    if jskey in Testjson.keys():
        try:
            return Testjson[jskey] 
        except:
            print "Error with Key Retrival", jskey
            exit(4)
    else:
        return {}

def readjson(filename, localrun):
  try:
    with open(filename) as json_file:
      global Testjson 
      Testjson = json.load(json_file)
    
    #pprint(Testjson)
    print("find the top level")
    print(Testjson.keys())

    VMname = isinjson('name')
    VMlocation = isinjson('location')
    VMsub = isinjson('id')
    VMsize = isinjson('hardwareProfile')
    
    print "VM name :",VMname
    print "Location :",VMlocation
    print "VMID", VMsub 
    #print "Size", VMsize
    VMsizeStr = VMsize.get('vmSize')
    print VMsizeStr
    
    if VMsub.find("/") <> -1:
        VMIDlist = list(VMsub.split("/"))
        if VMIDlist[1] == "subscriptions":
            print VMIDlist[1], ":",  VMIDlist[2]  # subscription
            print VMIDlist[3], ":",  VMIDlist[4]  # resourceGroup
            VMsubscription = VMIDlist[2]
            VMresourcegrp = VMIDlist[4]
        else:
            print "Error reading ID line of VM " + VMname + " JSON."
            exit(5)
  
    VMstorage = isinjson('storageProfile')
    print VMstorage, "StorageProfile"
    VMOSdisk = VMstorage.get('osDisk')
    print VMOSdisk, "Disk"
    print VMstorage.get('osType'), "type"
    VMOSuri = VMOSdisk.get('vhd')
    print VMOSuri

    
    
    
    #VMosVHD = VMstorage[osDisk[vhd[uri]]]
    
  # Fail if JSON file is malformed 
  except ValueError:
    print("Could not parse JSON file.")
    print("Make sure that the is properly formated.")
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
