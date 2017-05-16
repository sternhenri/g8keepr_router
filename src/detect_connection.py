#!/tmp/usr/bin/python
import os
os.system("echo 'py' >> /root/g8keepr/log/debug.log")
""" 2 main options: arp + cron job || dchp.leases + /etc/dnsmasq.conf addition
                                                    |-> dhcp-script=~/g8keepr/src/detect_connection.py
other options:
    - using dhcp                                         : https://gist.github.com/jwalanta/53f55d03fcf5265938b64ffd361502d5
    - using arp                                          : https://serverfault.com/questions/226046/how-to-get-a-list-of-the-connected-wifi-clients-in-openwrt-10-03
    - using nmap                                         : https://stackoverflow.com/questions/11643347/how-to-get-the-devices-details-that-are-connected-to-my-router
    - for selected network interfaces                    : https://wiki.openwrt.org/doc/faq/faq.wireless
"""

import sys
import pickle
from time import gmtime, strftime

DEBUG = True
CUSTOM_LOG = '/root/g8keepr/log/events.log'
WHITELIST_LOC = '/root/g8keepr/lists/whitelist.pickle'

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

def analyzeNewDevice(id_):
    cLog("New device connected:")
    cLog(id_)
    if ("niceDevice" in id_):
        whitelist.append(id_)
        with open(WHITELIST_LOC, 'wb') as whitelistFile:
            pickle.dump(whitelist, whitelistFile)

def analyzeReconnection(id_):
    cLog("Reconnection from untrusted device:")
    cLog(id_)

#### Main Execution ####

# reap arguments
assert len(sys.argv) == 5
new_conn, mac, ip, name = sys.argv[1:]

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
