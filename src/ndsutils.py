#!/tmp/usr/bin/python
import os

CLIENT_PARAMS = ('client_id','ip','mac','added','active','duration','token','state','downloaded','avg_down_speed','uploaded','avg_up_speed')

def _ndsread(ndsresponse):
	return ndsresponse.readline().split('=')[1]

def _read_client_status(ndsresponse):
	client_status = {}
	for param in CLIENT_PARAMS:
		client_status[param] = _ndsread(ndsresponse)
	ndsresponse.readline()
	return client_status

def get_clients():
	ndsresponse = os.popen('ndsctl clients')
	num_clients = int(ndsresponse.readline())
	print num_clients
	ndsresponse.readline()
        clients=[_read_client_status(ndsresponse) for i in xrange(num_clients)]
        return clients
def unauthorize_client(ip_or_mac):
	os.sytem('ndsctl deauth ' + ip_or_mac)

def authorize_client(ip_or_mac):
	os.system('ndsctl auth ' + ip_or_mac)

def main():
	get_clients()

if __name__ == '__main__':
	main()
