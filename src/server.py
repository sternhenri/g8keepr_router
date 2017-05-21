#!/usr/bin/env python
from render import render
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse

template = '../dashboard/dashboard.html'
devices_json = '../dashboard/devices.json'
base = '../dashboard'

class G8KeeprHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		path = urlparse.urlparse(self.path).path
		self.send_response(200)
		mimetype = 'text/html'
		if self.path.endswith('.png'):
			mimetype = 'image/png'
		elif self.path.endswith('.jpg'):
			mimetype = 'image/jpg'
		elif self.path.endswith('.gif'):
			mimetype = 'image/gif'
		elif self.path.find('/fonts/') != -1:
			mimetype = 'application/font-woff'

		self.send_header('Content-type', mimetype)
		self.end_headers()
		if mimetype=='text/html':
			render(template, devices_json, '#', self.wfile)
		else:
			with open(base + path, 'rb') as f:
				self.wfile.write(f.read())

def main():
	server = HTTPServer(('',8000), G8KeeprHandler)
	server.serve_forever()

if __name__ == '__main__':
	main()
