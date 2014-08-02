#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) by Martin Jung | 2009
###
# This Script changes your MAC-Adress to a new random value
# It can be run automatically at startup for an example
# Parameter is the Interface addresse (eth0, ath1,...)
#############################################################

import os, sys
import subprocess

class changeMAC():
	def __init__(self, iface, pw):
		self.iface = iface
		self.pw = pw
		self.cmd = ['/usr/sbin/ifconfig',self.iface]
		self.oldmac = self.ReturnMAC()
		
	def ReturnMAC(self):
		try:
			subprocess.check_call(self.cmd,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		except subprocess.CalledProcessError:
			return False
		except OSError:
			print "huu"
		return True
			
if __name__ == "__main__":
	print "Trying to Change your Mac-Adress"
	print "--------------------------------"
	pw = raw_input("Tip in your root passwd : ")
	t = changeMAC('eth0',pw)
