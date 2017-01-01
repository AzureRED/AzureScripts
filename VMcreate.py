#!/usr/bin/python2.7

### This script will create a azure CLI command to rebuild a VM.
### There needs to be a JSON file that was created from the VM before deletion. 
###
### Writen by: Richard Eseke  2016 - 
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
def MePrint(prestring, poststring):
    if printit:
        print (prestring, poststring) #tee to stderr
    
    
### List Helper for JSON parsing  
### pulls the first element from a list  
def Curtailist(choplist):  
    if len(choplist) > 0:
        choplist = choplist[0]
        if not choplist:
            #print "Null List", choplist
            pass
        else:
            return choplist 
    elif len(choplist) == 0:   
        MePrint("CHOPLIST zero", str(choplist))
        return choplist
    else:
        MePrint("Nothing in List", "[ ]")
        return choplist

        
### Parses the JSON to pull the corect data to build the azure vm create command
def Jsonparse(Testjson):
    VMbuild = ''  # the start of the VM create command     
    # these calls will output lists and more then one element 
    VMname = ''.join(Curtailist(JsonValue(Testjson, 'name')))  # top level
    MePrint("VM name :" , VMname) 
    VMlocation = ''.join(Curtailist(JsonValue(Testjson, 'location')))
    MePrint("Location :", VMlocation)   
    VMsize = ''.join(Curtailist(JsonValue(Testjson, 'vmSize')))
    MePrint("Size: ", VMsize)    
    VMostype = ''.join(Curtailist(JsonValue(Testjson, 'osType')))
    MePrint("VMostype :", VMostype)
    VMsub = ''.join(Curtailist(JsonValue(Testjson, 'id')))
    MePrint("VMID :", VMsub)
    
    # Pull apart the VMID to its' components
    if VMsub.find("/") <> -1:
        VMIDlist = list(VMsub.split("/"))
        if VMIDlist[1] == "subscriptions":
            MePrint (VMIDlist[1],  VMIDlist[2])  # subscription and subscription ID
            MePrint(VMIDlist[3],  VMIDlist[4])  # resourceGroup
            VMsubscription = VMIDlist[2]
            VMresourcegrp = VMIDlist[4]
        else:
            sys.exit("Error reading subscriptions ID line of VM " + VMname + " JSON.")
    else:
        sys.exit("Error reading ID line of VM.  Missing delimiters. " + VMname + " JSON.") 
    
    MePrint ("## start Networking ## ", VMresourcegrp)
    Networkstub = Curtailist(JsonValue(Testjson, 'networkInterfaces'))  
    if not Networkstub:
        sys.exit("Error Missing Networking Interfaces")
    else:
        NICliststr = ''        
        for NIC in Networkstub:
            VMnetlist = ''.join(JsonValue(NIC, "id")) 
            MePrint ("VMnetlist :", VMnetlist)
            if VMnetlist.find("/") <> -1:
                VMnetlist = list(VMnetlist.split("/"))
                if VMnetlist[7] == "networkInterfaces":  #is the networkInterface there?
                    MePrint ("network NIC name :", VMnetlist[8]) 
                    NICliststr = NICliststr + VMnetlist[8] + ', '
        NICliststr = NICliststr[:-2]  # Take the last comma off the end 
        MePrint("NIC list String :", NICliststr)
     
    # OS disk location
    VMosdiskset = Curtailist(JsonValue(Testjson, 'osDisk'))
    VMosdisk = ''.join(JsonValue(VMosdiskset, 'uri')) 
    if VMosdisk:
        VMosdisk = '"' + VMosdisk + '"'
        if VMosdisk.find("/") <> -1:
            VMstoragegrp = re.split('/|\.', VMosdisk)
            MePrint ("Storage Group : ", VMstoragegrp[2])
            VMstoragegrp = ''.join(VMstoragegrp[2])
    else:
        sys.exit(" Missing OS Disk, HALTING. \n")
    
    # Datadisk, possible list
    dataDisks = Curtailist(JsonValue(Testjson, 'dataDisks'))
    if dataDisks:
        MePrint ("DATA DISKS FOUND: ", dataDisks)
        Datalist = ''
        for DDisks in dataDisks:
            DataDStr = '"' + ''.join(JsonValue(DDisks, "uri")) 
            MePrint ("Datadisk :", DDisks)
            Datalist = Datalist + DataDStr + '"' + ", "
        Datalist = Datalist[:-2] # Take the last comma off the end
        MePrint ("DataDisk List:", Datalist)
        
    # Username and Passord/Key is built in to the OS disk and not used
    # Build the create vm command
    VMbuild = VMbuild + "azure vm create" + " -s " + VMsubscription + " -n " + VMname + " -g " + VMresourcegrp + " -o " + VMstoragegrp + " -d " + VMosdisk 
    if NICliststr.find(',') <> -1:
        VMbuild = VMbuild + " -N " + NICliststr  # Multipule NICs
    else:   
        VMbuild = VMbuild + " -f " + NICliststr  # Single NIC   
    if dataDisks:   # If there is data disk(s) then add it to the command
        VMbuild = VMbuild + " -Y " + Datalist
    VMbuild = VMbuild + " -l " + VMlocation + " -z " + VMsize + " -y " + VMostype      
    
    return VMbuild
   
   
###  -=:=-  MAIN -=:=-  ###  
def main():
    global runcommand, printit
    runcommand = False
    printit = False  #Default to not run the vm create
    args = sys.argv[1:]
    if len(sys.argv) == 1:
        sys.exit(" Missing arguments. \n This script will convert the jason file to an azuere vm create command. \n Use [-h,-r,-v] <jsonfile> \n")
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
# $> jsonread.py [-r,-h,-v] <jsonfile> 
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
                            print '\nRunning Command\n'
                            print VMcreate
                            ### run comm VM create
                        else:
                            print "\nPaste this command into the Azure CLI to run the create for the VHD.\n"                        
                            print VMcreate
                except ValueError:
                        sys.exit(" Could not parse JSON file. \n Make sure that the JSON is properly formated.\n")                      
            else:
                sys.exit('** Error parsing Command!! **')
    
if __name__=='__main__':
    main() 