#!/usr/bin/env python
import sys
import io
from jinja2 import Template
import datetime
import json

def main():
	template = Template(io.open(sys.argv[1],'r', encoding="utf-8").read())

	devices = json.load(open('devices.json','r'))
	print devices

	rendered = template.render(devices=devices, 
														 updatetime=datetime.datetime.now().ctime(),
														 notifications_count=0)
	
	with io.open(sys.argv[2], 'w', encoding='utf-8') as output:
		output.write(rendered)

if __name__ == '__main__':
	main()
