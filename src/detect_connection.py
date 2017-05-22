#!/tmp/usr/bin/python

"""This module handles new connections and is the main entry point for g8keepr"""
import json
import os
import sys
import pickle
import ndsutils
from fingerprinting import fingerprint
from time import gmtime, strftime
os.system("echo 'py' >> /root/g8keepr/log/debug.log")
""" 2 main options: arp + cron job || dchp.leases + /etc/dnsmasq.conf addition
                                                    |-> dhcp-script=~/g8keepr/src/detect_connection.py
other options:
    - using dhcp                                         : https://gist.github.com/jwalanta/53f55d03fcf5265938b64ffd361502d5
    - using arp                                          : https://serverfault.com/questions/226046/how-to-get-a-list-of-the-connected-wifi-clients-in-openwrt-10-03
    - using nmap                                         : https://stackoverflow.com/questions/11643347/how-to-get-the-devices-details-that-are-connected-to-my-router
    - for selected network interfaces                    : https://wiki.openwrt.org/doc/faq/faq.wireless
"""


DEBUG = True
CUSTOM_LOG = '/root/g8keepr/log/events.log'
WHITELIST_LOC = '/root/g8keepr/lists/whitelist.pickle'
DEVICES_LOC= 'root/g8keepr/devices.json'
MAIN_CLIENT= '60:c5:47:0d:1f:70'
### Methods ####

def log(string, path):
    with open(path, 'ab') as log:
        now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        log.write(now)
        log.write(" -- ")
        log.write(string)
	log.write("\n")
    if DEBUG:
        print string

def cLog(string):
    log(string, CUSTOM_LOG)
def overwriteStatus(mac,ip,name,status,comment=""):
    with open(DEVICES_LOC,'wb') as device_file:
        devices=json.load(device_file)
        for device in devices:
            if device["IP"]==ip and device["MAC"]==mac and device["name"]==name:
                device["status"]=status
def analyzeNewDevice(mac,ip):
    cLog("New device connected:")
    cLog(mac)
    name=fingerprint(mac,ip,"")
    overwriteStatus(mac,ip,name,"FINGERPRINTING")
    status="OK"
    if status<>"OK":
        print "Vulnerable devices at ip/mac {}/{} detected. Shutting down devices and prompting user input".format(ip,mac)
        ndsutils.unauthorize_client(mac)
        ndsutils.unauthorize_client(MAIN_CLIENT)
def analyzeReconnection(id_):
    cLog("Reconnection from untrusted device:")
    cLog(id_)

#### Main Execution ####

def main():

	if len(sys.argv) < 4:
		cLog("Script called with invalid arguments: %s" % sys.argv)
		sys.exit('Quitting...')

	# reap arguments
	new_conn, mac, ip = sys.argv[1:4]
	name = None
	if len(sys.argv) == 5:
		name = sys.arv[4]

	cLog("New connection: %s, %s, %s, %s" % (new_conn, mac, ip, name))
	# load whitelist -- or something
	try:
		with open(WHITELIST_LOC, 'rb') as whitelistFile:
			whitelist = pickle.load(whitelistFile)
	except:
		whitelist = []

	# fingerprinting will be handy here
	deviceIdentifier = mac
	if new_conn == 'add':
		analyzeNewDevice(deviceIdentifier)
	elif deviceIdentifier not in whitelist:
		analyzeReconnection(deviceIdentifier)

if __name__ == '__main__':
	main()
