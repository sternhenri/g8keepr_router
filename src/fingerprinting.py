import sys
import requests
import socket
import nmap
from log import *


def fingerprint(name,ip, mac):

    flag = 1

    cLog ("Start fingerprinting ...")
    if name != '':
        return name

    # whether it has a webinterface
    cLog ("Fingerprinting by IP address...")
    #try:
    #    socket.gethostbyaddr(ip)
    #except socket.herror:
    #      flag = 0
    #     print ("The device doesn't have a web interface.")


    r = requests.get('http://'+ ip)
    if r.status_code == 401:
        cLog ("Identify the features of the device's web interface.")
        cLog ("Web intercace detected.")
    else:
        flag = 0

    # match the mac address

    print ("Fingerprinting by MAC address...")
    if mac == '00:8f:bd:ae:a3:ec':
        cLog ("MAC address prefix matches a known vendor.")
    else:
        flag = 0

    cLog ("Scanning for open ports...")

    targetHost = ip
    targetPorts = '1-100'
    upPorts = []
    try:
        scanner = nmap.PortScanner()
        scanner.scan(targetHost, targetPorts)
        for targetPort in scanner[targetHost]['tcp']:
            cLog (str(targetHost) + ':' + str(targetPort) + 'is up')
            upPorts.append(targetPort)
    except Exception, e:
        cLog ('[-] Something bad happened during the scan: ' + str(e))

    # whether it uses digist authetication
    cLog ("Fingerprinting the authetication ...")
    if upPorts == [80, 23] :
        cLog ('Open ports:' + str(upPorts))
    else:
        flag = 0

    # return the device name
    if flag == 1:
        cLog ("Device identified! IP: " + str(ip) + ", MAC: " + str(mac) + " is ICAM-608")
        return "ICAM-608"
    return "unknown";