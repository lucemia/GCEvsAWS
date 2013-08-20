import os
import re

re_server = re.compile(r"Testing from (.*) \((.*)\)")
re_host = re.compile(r"Hosted by (.*) \((.*)\) \[(.*) km\]\: (.*) ms")
re_download = re.compile(r"Download: (.*) Mbit")
re_upload = re.compile(r"Upload: (.*) Mbit")

_date = '20130820'

for i in os.listdir("./gce/%s"%_date):
#	print i
	with open("./gce/%s/%s"%(_date, i)) as g_reader , open("./aws/%s/%s"%(_date, i)) as a_reader:
		g_content = g_reader.read()
		a_content = a_reader.read()
		if not re_upload.findall(g_content):
			continue
		print re_download.findall(g_content)[0],"\t", re_download.findall(a_content)[0]
#		print re_upload.findall(g_content)[0],"\t",  re_upload.findall(a_content)[0]

