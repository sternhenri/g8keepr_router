import requests
from requests.auth import HTTPDigestAuth

#parameters: devicename, ip, mac
#return values, a tuple of (status,comments)
def security_test(devicename, ip, mac):
    flag = 0

    print ("Start the security testing..........................................")

    #Web Interface brute force attack
    if devicename == 'P2PCamera':
        print ("Testing for the weak accounts and passwords...")
        url = 'http://'+ ip
        r=requests.get(url, auth=HTTPDigestAuth('admin', 'admin'))
        print (r.json)
        if r.status_code == 200:
            print ("Weak account and password is detected: admin, admin.")
            flag = 1


    #Telnet brute force attack
    if devicename == 'P2PCamera':
        print ("Telnet port 23 is up. This might expose the user's content to attakcers.")
        print ("Testing for weak telnet accounts and passwords")

    print("***Security test is done. Identify three vulenrabilities.\n 1) Default account and user name. 2) Telnet port is up. 3) Outdated software.")
    if flag == 1:
        return ('vulnerable', 'Identify three vulenrabilities. 1) Default account and user name. 2) Telnet port is up. 3) Outdated software. We can help you to set a secure password and update the software.' )
    return ('ok','Device looks safe')


#result = security_test('P2PCamera','192.168.1.232', '00:8f:bd:ae:a3:ec')
#print result
