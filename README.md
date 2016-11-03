# Python_Scripts
A repo for more scripts dealing with OS and or cloud

This Repo is to contain the scripts to help with VM creation with Azure CLI
This script will create VM or create the Azure VM create command for that json.
 
You need the Azure CLI installed on your computer/VM to use this script.
And you will need Python 2.7.

1. Azure CLI installed on your machine

2. Logged in to Azure
 a. Azure login
  i. log in to the subscription that has the VM in question.

3. Set mode to Azure Resource Mode (ARM)
 a. Azure set mode arm

4. Create a JSON file of your system
 a. azure vm get-instance-view -n <VM name> -g <group name> --json > <file>
 b. <b> This must be done before you delect the VM. </b>

5. Run script
 a. jsoncreate.py [-r, -h] <file> 
  i.  -r  Will run the create command(s).
  ii. -h  A quick help box explaining the switches.
 b. The script will not run the create command by default.  The -r switch is need to automaticly run create.
