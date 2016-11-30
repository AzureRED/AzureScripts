#!/usr/bin/python2.7 -tt

import sys, getopt
import json
import os
import shutil
import re
    
## recursive search in the jason file     
def JsonValue(searchdict, Dkey):
    answer_out = []  # start with blank
    for key, value in searchdict.iteritems():
        if key == Dkey: # is Dkey found at top level then stop
            answer_out.append(value) 
            
        elif isinstance(value, dict):  # if in dictionary then parse sub-section
            results = JsonValue(value, Dkey)
            for resultdict in results:
                answer_out.append(resultdict)

        elif isinstance(value, list):  # if in list then parse sub-section
            for item in value:
                if isinstance(item, dict):
                    moreresults = JsonValue(item, Dkey)
                    for result2 in moreresults:
                        answer_out.append(result2)
    return answer_out
    
# A more robust way to find the keys:values
def isinjson(tempjson, jskey):
    if jskey in tempjson.keys():
        try:
            return tempjson[jskey] 
        except:
            print "Error with Key Retrival", jskey
            exit(4)
    else:
        return {}

def readjson(filename, localrun):
  try:
    with open(filename) as json_file:
      #global Testjson 
      Testjson = json.load(json_file)
    
    #pprint(Testjson)
    print("###### top level #######")
    topkeys = (Testjson.keys())

    VMname = isinjson(Testjson, 'name')
    VMlocation = isinjson(Testjson, 'location')
    VMsub = isinjson(Testjson,'id')
    VMsize = isinjson(Testjson,'hardwareProfile')
    
    print "VM name :",VMname
    print "Location :",VMlocation
    print "VMID :", VMsub 
    print "Size", VMsize
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
  
    
    
    print "## start ##"
    print "^^^ Output :", JsonValue(Testjson, 'type')
    
    print "^^^ name :", JsonValue(Testjson, 'name')

    Networksub = JsonValue(Testjson, 'networkProfile')
    print "^VV Networksub :", Networksub
  
    print "^^^ uri :", JsonValue(Testjson, 'uri')
  
    #print FindDict('storageProfile', 'url')
  
    #VMstorage = isinjson('storageProfile')
    #print VMstorage, "StorageProfile"
    #VMOSdisk = VMstorage.get('osDisk')
    #print VMOSdisk, "Disk"
    #print VMstorage.get('osType'), "type"
    #VMOSuri = VMOSdisk.get('vhd')
    #print VMOSuri

    
    
    
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