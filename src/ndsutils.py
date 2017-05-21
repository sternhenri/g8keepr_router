#!/tmp/usr/bin/python
import os

CLIENT_PARAMS = ('client_id','ip','mac','added','active','duration','token','state','downloaded','avg_down_speed','uploaded','avg_up_speed')

def ndsread(ndsresponse):
	return ndsresponse.readline().split('=')[1]

def read_client_status(ndsresponse):
	client_status = {}
	for param in CLIENT_PARAMS:
		client_status[param] = ndsread(ndsresponse)
	ndsresponse.readline()
	return client_status

def get_clients():
	ndsresponse = os.popen('ndsctl clients')
	num_clients = int(ndsresponse.readline())
	print num_clients
	ndsresponse.readline()
	
	for i in xrange(num_clients):
		client_status = read_client_status(ndsresponse)

def main():
	get_clients()

if __name__ == '__main__':
	main()
