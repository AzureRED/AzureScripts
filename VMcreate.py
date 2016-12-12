#!/usr/bin/python2.7

### This script will create a azure CLI command to rebuild a VM.
### There needs to be a JSON file that was created from the VM before deletion. 
###
### Writen by: Richard Eseke  2016
###
### Microsoft Corp.



import sys, getopt
import json
import os
import shutil
import re
    
    
   
### recursive search in the jason file 
### Will search JSON dicts and lists    
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

    
    
### Is is to print to screen    
def MePrint(thestring):
    if printit:
        print (thestring) #tee to stderr
    
    
    
### List Helper for JSON parsing  
### Need to find why this needs to be list[0] join disapears
def Curtailist(choplist):  
    if len(choplist) > 0:
        choplist = choplist[0]
        if not choplist:
            print "Null List", choplist
        else:
            return choplist 
    elif len(choplist) == 0:    
        return choplist
    else:
        print "Nothing in List", choplist
        return choplist

        
### Parses the JSON to pull the corect data to build the azure vm create command
def Jsonparse(Testjson):
    # these calls will output lists and more then one element 
    VMname = ''.join(Curtailist(JsonValue(Testjson, 'name')))  # top level
    print "VM name :" , VMname
   
    VMlocation = ''.join(Curtailist(JsonValue(Testjson, 'location')))
    print "Location :", VMlocation 
    
    VMsize = ''.join(Curtailist(JsonValue(Testjson, 'vmSize')))
    print "Size: ", VMsize
    
    VMsub = ''.join(Curtailist(JsonValue(Testjson, 'id')))
    print "VMID :", VMsub
   
    # Pull apart the VMID to its' components
    if VMsub.find("/") <> -1:
        VMIDlist = list(VMsub.split("/"))
        if VMIDlist[1] == "subscriptions":
            print VMIDlist[1], ":",  VMIDlist[2]  # subscription
            print VMIDlist[3], ":",  VMIDlist[4]  # resourceGroup
            VMsubscription = VMIDlist[2]
            VMresourcegrp = VMIDlist[4]
        else:
            print "Error reading subscriptions ID line of VM " + VMname + " JSON."
            exit(5)

    print "## start Networking ##"
    Networkstub = JsonValue(Testjson, 'networkInterfaces')[0]  # pull the list from the JSON
    if not Networkstub:
        print "Error Missing Networking Interfaces"
        exit(7)
    else:
        NICliststr = ''        
        for NIC in Networkstub:
            VMnetlist = ''.join(JsonValue(NIC, "id")) 
            print "VMnetlist :", VMnetlist
            if VMnetlist.find("/") <> -1:
                VMnetlist = list(VMnetlist.split("/"))
                if VMnetlist[7] == "networkInterfaces":  #is the networkInterface there?
                    print "network NIC name :", VMnetlist[8] 
                    NICliststr = NICliststr + VMnetlist[8] + ', '
        NICliststr = NICliststr[:-2]  # Take the last comma off the end 
        print "NIC list String :", NICliststr
    
    # OS disk location
    VMosdisk = ''.join(JsonValue(Testjson, 'uri'))
    print "URI join: ", VMosdisk
    
    return("The Comamnd")
   
   
###  -=:=-  MAIN -=:=-  ###  
def main():
    runcommand = False  #Default to not run the vm create
    # global printit == False
    args = sys.argv[1:]
    if len(sys.argv) == 1:
        print("# Missing arguments.")
        print('# This script will convert the jason file to an azuere vm create command. #')
        print('# Use [-h,-r,-v] <jsonfile>')
        sys.exit(2)
    else:
        for arg in args:
            if arg == '-h':  #Help option, A sinple abrivated help card for the script    
                Helpstr = """# This script will convert the jason file to an azuere vm create command. #
#
# -h help.
# -r run azure vm create [...] when done.
# -v verbose output.
# By default the script will just print the command.
#
# $> jsonread.py [-r,-h] <jsonfile> 
"""
                print Helpstr
                sys.exit(0)
            elif arg == '-r':   #Run the vm create
                runcommand = True 
            elif arg == "-v":   #Print out all data from script
                printit = True
            elif os.path.exists(str(arg)):
                try:
                    with open(arg) as json_file:
                        VMcreate = Jsonparse(json.load(json_file))
                        if runcommand:
                            print VMcreate
                        else:
                            print "No run"                          
                except ValueError:
                        print("Could not parse JSON file.")
                        print("Make sure that the is properly formated.")
                        sys.exit(3)                       
            else:
                print('** Error parsing Command!! **')
                sys.exit(1)
    
if __name__=='__main__':
    main() 