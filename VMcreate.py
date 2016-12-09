#!/usr/bin/python2.7

# This script will create a azure CLI command to rebuild a VM.
# There needs to be a JSON file that was created from the VM before deletion. 

import sys, getopt
import json
import os
import shutil
import re
    
# recursive search in the jason file     
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

def Curtailist(choplist)  #need to find why this needs to be  list[0] join disapears
    if choplist.len > 1:
        choplist = choplist[0]
    
# A sinple abrivated help card for the script    
def help():
    print('# This script will convert the jason file to an azuere vm create command. #')
    print('#')
    print('# -h help.')
    print('# -r run azure vm create [...] when done.')
    print('# By default the script will just print the command.')
    print('#')
    print('# $> jsonread.py [-r,-h] <jsonfile> ')
  
def jsonparse(Testjson):
     
    # these calls will output lists and more then one element 
    VMname = ''.join(JsonValue(Testjson, 'name'))  # top level
    print "VM name :" , VMname
    VMlocation = ''.join(JsonValue(Testjson, 'location'))
    print "Location :", VMlocation 
    VMsize = ''.join(JsonValue(Testjson, 'vmSize'))  #take list and gererate a string
    print "Size: ", VMsize
    VMsub = ''.join(JsonValue(Testjson, 'id'))
    print "VMID :", VMsub
   
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
    print "^^^ name :", JsonValue(Testjson, 'name')

    Networksub = JsonValue(Testjson, 'networkProfile')
    print "^VV Networksub :", Networksub
    print "^^^ uri :", JsonValue(Testjson, 'uri')
   
    return("The Comamnd")
  
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
                try:
                    with open(arg) as json_file:
                        VMcreate = jsonparse(json.load(json_file))
                        if runcommand:
                            print VMcreate
                        else:
                            print "No run"                          
                except ValueError:
                        print("Could not parse JSON file.")
                        print("Make sure that the is properly formated.")
                        sys.exit(3)                       
            else:
                print('** Error in Command!! **')
                sys.exit(1)
    
if __name__=='__main__':
    main() 