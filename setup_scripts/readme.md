# Setup Raspberry Pi Zero (W) for Remote Access
This script is to be loaded on a Pi Zero and run to configure for VNC  
(Virtual Network Computing) with Chromebooks.  

## NOTE
Make sure Pi and Chromebook are on the same network and the network allows ssh connections.

## Steps on Raspberry Pi  
* Update System
```
$ - sudo apt-get update && apt-get upgrade
```
  
* Install VNC Server
```
$ - sudo apt-get install realvnc-vnc-server realvnc-vnc-viewer
```  
  
* Enable VNC Server
```
$ - sudo raspi-config
```  
Navigate to Interfacing options.  
VNC > yes.  
Exit interface  

* See IP address

```
$ - ifconfig wlan0
```
## Steps on Chromebook
* Search "VNC Viewer for Chromebook" in browser
* Download the app in the Chrome Store
* Open the app
