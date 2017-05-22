import sys
import requests
import socket
import nmap



def finger_print(ip, mac):

    flag = 1

    print ("Start the finger printing ...")


    # whether it has a webinterface
    print ("Finger printing the ip address ...")
    #try:
    #    socket.gethostbyaddr(ip)
    #except socket.herror:
    #      flag = 0
    #     print ("The device doesn't have a web interface. Match 100 devices.")


    r = requests.get('http://'+ ip)
    if r.status_code == 401: 
        print (r.text)
        print ("Identify the features of the device's web interface. Match 50 devices.")
    else:
        flag = 0

    # match the mac address

    print ("Finger printing the mac address ...")
    if mac == '00:8f:bd:ae:a3:ec':
        print ("Mac address matched. Match 300 devices.")
    else:
        flag = 0

    print ("Finger printing the open ports ...")

    targetHost = ip
    targetPorts = '1-100'
    upPorts = []
    try:
        scanner = nmap.PortScanner()
        scanner.scan(targetHost, targetPorts)
        for targetPort in scanner[targetHost]['tcp']:
            print str(targetHost) + ':' + str(targetPort) + 'is up'
            upPorts.append(targetPort)
    except Exception, e:
        print '[-] Something bad happened during the scan: ' + str(e)
    # whether it uses digist authetication
    print ("Finger printing the authetication ...")
    if upPorts == [80, 23] :
        print 'Identify the ports that are up. Match 10 devices.'
    else:
        flag = 0

    # return the device name
    if flag == 1:
        print ("Device identified! This device ( IP: " + str(ip) + ", MAC: " + str(mac) + " is a P2PCamera")
        return "P2PCamera"
    return "unknown";

#finger_print('192.168.1.232', '00:8f:bd:ae:a3:ec')
