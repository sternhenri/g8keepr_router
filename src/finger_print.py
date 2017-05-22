import sys
import requests
import socket
import nmap
from log import *


def finger_print(name,ip, mac):

    flag = 1

    cLog ("Start the fingerprinting ...")
    if name != '':
        return name

    # whether it has a webinterface
    cLog ("Fingerprinting the ip address ...")
    #try:
    #    socket.gethostbyaddr(ip)
    #except socket.herror:
    #      flag = 0
    #     print ("The device doesn't have a web interface.")


    r = requests.get('http://'+ ip)
    if r.status_code == 401:
        cLog (r.text)
        cLog ("Identify the features of the device's web interface.")
    else:
        flag = 0

    # match the mac address

    print ("Fingerprinting the mac address ...")
    if mac == '00:8f:bd:ae:a3:ec':
        cLog ("Mac address matched.")
        print("text")
    else:
        flag = 0

    cLog ("Fingerprinting the open ports ...")

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
        cLog ('Identify that ports 23 and 80 are open.')
    else:
        flag = 0

    # return the device name
    if flag == 1:
        cLog ("Device identified! IP: " + str(ip) + ", MAC: " + str(mac) + " is ICAM-608")
        return "ICAM-608"
    return "unknown";

result = finger_print( '','192.168.1.232', '00:8f:bd:ae:a3:ec')
print result

