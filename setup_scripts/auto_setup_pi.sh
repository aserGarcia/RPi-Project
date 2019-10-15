#!/bin/bash

#This script configures the pi for VNC connection

clear
echo -e "Auto configuring VNC connection for Pi...\n"

#Updating
echo "Updating and Upgrading..."
apt-get update && apt-get upgrade
echo -e "Done Updating and Upgrading...\n"


#Installing VNC
echo "Installing VNC Server and VNC Viewer..."
apt-get install realvnc-vnc-server realvnc-vnc-viewer
echo -e "Done Installing VNC Server and VNC Viewer...\n"

#enable VNC Viewer
echo "Enabling SSH and VNC Interface..."
raspi-config nonint do_ssh 1
raspi-config nonint do_vnc 1
echo -e "Done Enabling SSH and VNC Interface...\e"

echo "Printing Wifi IP Address"
ifconfig
echo -e "\n Take note of the wlan inet address (very bottom)...\n"

read -p "Reboot needed. Press the Enter key to reboot..."
reboot
