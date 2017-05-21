#!/usr/bin/env python
import sys
import io
from jinja2 import Template
import datetime
import json

def render(template_file, devices_json, authtarget, output):
	template = Template(io.open(template_file, 'r', encoding="utf-8").read())

	devices = json.load(open(devices_json,'r'))
	# print devices

	stream = template.stream(devices=devices, 
													 updatetime=datetime.datetime.now().ctime(),
													 notifications_count=0,
													 authtarget=authtarget)
	stream.dump(output, encoding='utf-8')


def main():
	template_file, devices_json, output_file = sys.argv[1:]

	with open(output_file, 'w') as output:
		render(template_file, devices_json, authtarget='#', output)

if __name__ == '__main__':
	main()
