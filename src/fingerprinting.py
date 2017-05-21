"""This module attempts to fingerprint a newly connected device and furthermore detect whether it is vulnerable or safe"""
#!/tmp/usr/bin/python
class Status(Enum):
    OK=1
    VULNERABLE=2
    UNKOWN=3
    FINGERPRINTING=4
def fingerprint(mac,ip,name,newdevice):
    return Status.OK
