#!/tmp/usr/bin/python

"""This module handles new connections and is the main entry point for g8keepr"""
import json
import os
import sys
import pickle
from time import gmtime, strftime
import ndsutils
from finger_print import finger_print
from security_test import security_test
from log import *
from render import render
os.system("echo 'py' >> /root/g8keepr/log/debug.log")
""" 2 main options: arp + cron job || dchp.leases + /etc/dnsmasq.conf addition
                                                    |-> dhcp-script=~/g8keepr/src/detect_connection.py
other options:
    - using dhcp                                         : https://gist.github.com/jwalanta/53f55d03fcf5265938b64ffd361502d5
    - using arp                                          : https://serverfault.com/questions/226046/how-to-get-a-list-of-the-connected-wifi-clients-in-openwrt-10-03
    - using nmap                                         : https://stackoverflow.com/questions/11643347/how-to-get-the-devices-details-that-are-connected-to-my-router
    - for selected network interfaces                    : https://wiki.openwrt.org/doc/faq/faq.wireless
"""



WHITELIST_LOC = '/root/g8keepr/lists/whitelist.pickle'
TEMPLATE_LOC = '/root/g8keepr/dashboard/dashboard.html'
OUTPUT_LOC = '/root/g8keepr/dashboard/captive.html'
DEVICES_LOC = '/root/g8keepr/dashboard/devices.json'
MAIN_CLIENT = '60:c5:47:0d:1f:70'
SEEN_DEVICES_LOC = 'root/g8keepr/seendevices.pickle'
### Methods ####


def overwriteStatus(mac,ip,name,status,comment=""):
    with open(DEVICES_LOC,'r') as device_file:
        devices=json.load(device_file)
        found_device=False
        for device in devices:
            if device["IP"]==ip and device["MAC"]==mac and device["name"]==name:
                device["status"]=status
                device["comment"]=comment
                found_device=True
        if not found_device:
            new_device={"IP":ip,"MAC":mac,"name":name,"status":status,"comment":comment}
            devices.append(new_device)
        with open(DEVICES_LOC, 'w') as device_file:
            json.dump(devices,device_file)
def analyzeNewDevice(mac,ip,name):
    cLog("New device connected:")
    cLog(mac)
    overwriteStatus(mac, ip, name, "FINGERPRINTING")
    name = finger_print(name, ip, mac)
    overwriteStatus(mac, ip, name, "TESTING")
    status, comment = security_test(name, ip, mac)
    overwriteStatus(mac, ip, name, status,comment)
    if status <> "OK":
        cLog("Vulnerable devices at ip/mac {}/{} detected. Shutting down devices".format(ip, mac))
        ndsutils.unauthorize_client(mac)
        cLog("Prompting user input from client {} about handeling vulnerable device".format(MAIN_CLIENT))
        ndsutils.unauthorize_client(MAIN_CLIENT)
    cLog("Rendering new captive portal")
    render(TEMPLATE_LOC,DEVICES_LOC,OUTPUT_LOC)
    cLog("Captive portal successfully rendered")
def analyzeReconnection(id_):
    cLog("Reconnection from untrusted device:")
    cLog(id_)

#### Main Execution ####

def main():
    cLog("G8keepr called with {}".format(sys.argv))
    if len(sys.argv) < 4:
        cLog("Script called with invalid arguments: %s" % sys.argv)
   	sys.exit('Quitting...')
    try:
	# reap arguments
        new_conn, mac, ip = sys.argv[1:4]
        name = None
        if len(sys.argv) == 5:
            name = sys.argv[4]
        else:
            name=""
        cLog("New connection: %s, %s, %s, %s" % (new_conn, mac, ip, name))
        # load whitelist -- or something
        try:
        	with open(WHITELIST_LOC, 'rb') as whitelistFile:
        		whitelist = pickle.load(whitelistFile)
        except:
        	whitelist = []

        # fingerprinting will be handy here
        #For testing you can simply make condition true
        if new_conn == 'add' or new_conn == 'old':
        	analyzeNewDevice(mac,ip,name)
        elif mac not in whitelist:
        	analyzeReconnection(mac)
    except:
        e = sys.exc_info()[0]
        cLog(e)
if __name__ == '__main__':
	main()
