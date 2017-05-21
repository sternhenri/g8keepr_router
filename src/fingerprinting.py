#!/tmp/usr/bin/python

"""This module attempts to fingerprint a newly connected device and furthermore detect whether it is vulnerable or safe"""

# Device status enum
OK = 0
VULNERABLE = 1
UNKNOWN = 2
FINGERPRINTING = 4

def fingerprint(mac,ip,name,newdevice):
    return OK
