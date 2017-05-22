import sys
import requests
import socket
import nmap
from log import *


def finger_print(name,ip, mac):

    flag = 1

    cLog ("Start the finger printing ...")
    if name != '':
        return name

    # whether it has a webinterface
    cLog ("Finger printing the ip address ...")
    #try:
    #    socket.gethostbyaddr(ip)
    #except socket.herror:
    #      flag = 0
    #     print ("The device doesn't have a web interface. Match 100 devices.")


    r = requests.get('http://'+ ip)
    if r.status_code == 401:
        cLog (r.text)
        cLog ("Identify the features of the device's web interface. Match 50 devices.")
    else:
        flag = 0

    # match the mac address

    print ("Finger printing the mac address ...")
    if mac == '00:8f:bd:ae:a3:ec':
        cLog ("Mac address matched. Match 300 devices.")
        print("text")
    else:
        flag = 0

    cLog ("Finger printing the open ports ...")

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
    cLog ("Finger printing the authetication ...")
    if upPorts == [80, 23] :
        cLog ('Identify the ports that are up. Match 10 devices.')
    else:
        flag = 0

    # return the device name
    if flag == 1:
        cLog ("Device identified! This device ( IP: " + str(ip) + ", MAC: " + str(mac) + " is a P2PCamera")
        return "P2PCamera"
    return "unknown";

result = finger_print( '','192.168.1.232', '00:8f:bd:ae:a3:ec')
print result

