#!/usr/bin/python
 
"""
script from https://gist.github.com/sternhenri/2bb2236cc3783e1c7a22695a81260ecb
Who owns the OUI? IEEE knows.
 
Auto-refreshes once a month.
Run with -u to force update.
"""
 
from urllib2 import urlopen
from getpass import getuser
import codecs
import sys
import time
import os
import re
 
USER_HOME = "~" + getuser()
OUI_FILE_STORE = os.path.join(os.path.expanduser(USER_HOME), ".oui-cache")
CACHE_TIME = 2592000 # 30 days should be fine
IEEE_URL = "http://standards.ieee.org/develop/regauth/oui/oui.txt"
UNKNOWN_MAN = "unknown"
 
def clean_input(user_input):
    """
    Strip colons
    """
    return "".join(user_input.split(':')[:3])
 
def update_cache():
    """
    Update our local file from the IEEE OUI
    list
    """
    print(">>> Updating Cache. This can take a few minutes.")
    with open(OUI_FILE_STORE, 'wb') as outfile:
        for lne in urlopen(IEEE_URL).readlines():
            outfile.write(lne)
    print(">>> Done")
 
def process_args():
    """
    Parse our args
    """
    if sys.argv[1] == "-u":
        update_cache()
        if len(sys.argv) > 2:
            user_input = sys.argv[2]
        else:
            sys.exit(0)
    else:
        user_input = sys.argv[1]
 
    return user_input

def get_manufacturer(raw_mac):

    clean_mac = clean_input(raw_mac)
    try:
        if time.time() - os.stat(OUI_FILE_STORE).st_ctime > CACHE_TIME:
            update_cache()
     
    except OSError as err:
        if err.errno == 2:
            update_cache()
    
    with codecs.open(OUI_FILE_STORE,'r',encoding='utf8') as oui_list:
        for line in iter(oui_list):
            if re.search(clean_mac, line, re.IGNORECASE):
                return line.split("\t")[-1].strip()
    return UNKNOWN_MAN

if __name__ == "__main__":

    print get_manufacturer(process_args())
