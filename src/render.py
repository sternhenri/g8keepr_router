#!/usr/bin/env python
import sys
import io
from jinja2 import Template
import datetime
import json

def render(template_file, devices_json, output_file):
	template = Template(io.open(template_file, 'r', encoding="utf-8").read())

	devices = json.load(open(devices_json,'r'))
	print devices

	rendered = template.render(devices=devices, 
														 updatetime=datetime.datetime.now().ctime(),
														 notifications_count=0)
	
	with io.open(output_file, 'w', encoding='utf-8') as output:
		output.write(rendered)


def main():
	template_file, devices_json, output_file = sys.argv[1:]
	render(template_file, devices_json, output_file)

if __name__ == '__main__':
	main()
