import os
import re
os.system("speedtest-cli --list > server.txt")

re_line = re.compile(r"([\d]+)\) (.*) \((.*), (.*)\) \[(.*) km\]")
vs = []
with open("server.txt") as reader:
	for line in reader:
		p= re_line.findall(line)
		if p:
			vs.append(p[0])

vs.sort(key=lambda i: i[0])
for v in vs:
	print v
	server_id, name, location, counter, distance = v
	if counter == "Taiwan":
		print "start testing", v
		os.system("speedtest-cli --server %s > %s.log"%(server_id, server_id))		
	
