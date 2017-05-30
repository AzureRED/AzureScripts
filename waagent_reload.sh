#!/bin/bash

#For Modern redhat/centos 7+
#Uses systemctl

#check for systemctl
if [ ! -e /bin/systemctl ]; then
        echo "Wrong OS verion, missing systemctl."
        exit 1
fi

systemctl stop waagent
sleep 1

#Remove the waagent (force if needed)
yum remove WALinuxAgent.noarch -y
echo "** Wait for completion. **"
sleep 15

#Double check to see if the binary is gone.
if [ -e /usr/sbin/waagent ]; then
        rm /usr/sbin/waagent*
        echo "Waagent found: Removing waagent binary"
fi
 
# Now, install the waagent
yum install WALinuxAgent.noarch -y
echo "** Wait for completion. **"
sleep 15

# Lastly verify that the waagent is active
systemctl start waagent
echo `(systemctl status waagent | grep active)`
sleep 1

# When the agent is up and running then enable it to start on boot.
systemctl enable waagent
