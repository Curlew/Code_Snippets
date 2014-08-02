#! /usr/bin/env python
"""Returns an Array consisting of a tupel with the name and the ip-address of
all online machines in the local network."""
import os, socket, commands, re, time
from threading import Thread
import myDHCPip


class Pinger():
	def __init__(self, iface):
		self.ip = myDHCPip.myDHCPip(iface)
		ip = self.ip
		self.x = ip.getip()[-2:]
		x = self.x
		
	#Return all Hosts in the given Ip-Range
	def AllHosts(self):
		first = str(self.GetFirstNumbers())
		testit.lifeline = re.compile(r"(\d) received")
		return(self.Pinger(first))
	
	#Return all Active Hosts
	def ActiveHosts(self):
		first = str(self.GetFirstNumbers())
		x = self.AllHosts()
		for i in range(0,len(x)+1):
			if x.get(first+str(i)) == 0:
				del x[first+str(i)]
		results = []
		for ip, value in x.items():
			if value == 2:
				results.append((ip, self.HostName(ip)))
		return results
		#for ip, value in x.items():
		#	print '%s hat %s' % (ip, value)
		
	# Make a ping and save the results
	def Pinger(self, first, start=1, end=255):
		report = ("None","Partial","Alive")
		pinglist = []
		results = {}
		for host in range(start,end):
			ip = first+str(host)
			current = testit(ip)
			pinglist.append(current)
			current.start()
		for pingle in pinglist:
			pingle.join()
			results[pingle.ip]= pingle.status
		return results
		
	# give the first numbers of the ip-range
	def GetFirstNumbers(self):
		l = len(self.GetOwnLastNr())*-1
		x = self.GetIp()[0:l]
		return x
		
	# give the last numbers
	def GetOwnLastNr(self):
		x = self.GetIp()[-3:]
		if (x[0]=='.'):
			x = x[-2:]
		return x
	
	# Return the Hostname of a PC in the Network
	def HostName(self, ip):
		if (ip[-1] != '1') and (ip[-2] != '.'):
			if ip == self.GetIp():
				return 'Yourself ('+str(socket.gethostname())+')'
			try:
				host, aliases, ips = socket.gethostbyaddr(ip)
				return str(host)
			except socket.herror:
				return 'Cannot get the Hostname of the given Ip'
		else:
			#Implementation Mac Vendor ?
			return 'Router'
	
	def GetIp(self):
		return self.ip.getip()
	def GetConfData(self):
		return self.ip.getdata()
	

class testit(Thread):
	def __init__ (self,ip):
		Thread.__init__(self)
		self.ip = ip
		self.status = -1
	def run(self):
		pingaling = os.popen("ping -q -c2 "+self.ip,"r")
		while 1:
			line = pingaling.readline()
			if not line: break
			igot = re.findall(testit.lifeline,line)
			if igot:
				self.status = int(igot[0])

if __name__ == "__main__":
	p = Pinger('eth1')
	x = p.ActiveHosts()
	print x