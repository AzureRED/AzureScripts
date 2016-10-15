# Python_Scripts
A repo for more scripts dealing with OS and or cloud

This Repo is to contain the scripts to help with VM creation with Azure CLI

This script will create VM or create the Azure VM create command for that json.
 

You need the Azure CLI installed on your computer/VM

1. Azure CLI installed on your machine

2. Logged in to Azure
 a. Azure login

3. Set mode to Azure Resource Mode (ARM)
 a. Azure set mode arm

4. Create a JSON file of your system
 a. azure vm get-instance-view -n <VM name> -g <group name> --json > <file>
 b. remove the last line (for future ver of script)
  i. sed -i '$ d' <file>

5. Run script
 a. jsoncreate.py <file> [-t]
  i.  -t For output vm create command, won't create
  ii. (future switches)

### AzureScripts

