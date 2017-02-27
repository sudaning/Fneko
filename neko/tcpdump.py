#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import os
from struct import pack
from fcntl import ioctl
from socket import socket, inet_ntoa, AF_INET, SOCK_DGRAM
import subprocess
import datetime
from optparse import OptionParser

import sys
from platform import system
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
LINUX = system() in ['Linux', 'Unix']
WINDOWS = system() in ['Windows']

class tcpdump:
	"""
	run tcpdump to capture the net packet on Linux
	"""
	def __init__(self, protocol='', eth='eth0', w='', port=0, debug=False):
		if not LINUX:
			raise Exception("current operation system is '%s' but 'Linux'" % system())
		self.protocol = protocol
		self.eth = eth
		self.w = w
		self.port = port
		self.debug = debug

		self.check(eth)

	@staticmethod
	def check(eth):
		s = socket(AF_INET, SOCK_DGRAM)
		try:
			# test eth name is exist or not
			inet_ntoa(ioctl(s.fileno(), 0X8915, pack('256s', eth[:15]))[20:24])
		except IOError as err:
			if 'No such device' in str(err):
				print(str(err) + ":" + eth)
				raise Exception(str(err) + ":" + eth)

	def run(self):
		"""
		run tcpdump capture the net packet
		"""
		cmd = ['tcpdump']
		if self.protocol:
			cmd += [self.protocol]
		if self.eth:
			cmd += ['-i', self.eth]
		if self.w:
			cmd += ['-w', self.w]
		if self.port:
			cmd += ['port', str(self.port)]

		self.cmd = cmd
		self.p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn = os.setpgrp)
		if self.debug:
			print("run process. [%s]" % " ".join(self.cmd))
		return self.p

	def pid(self):
		"""
		return the subprocess's pid
		"""
		return self.p.pid if self.p else 0

	def terminate(self, timeout=0):
		"""
		terminated tcpdump immediately if timeout is 0 or after timeout(seconds)
		"""
		if not self.p:
			return

		if timeout:
			start = datetime.datetime.now()
			end = start + datetime.timedelta(seconds=timeout)
			while True:
				delta = (end - datetime.datetime.now()).seconds
				if delta <= 0 or delta > timeout:
					break
		
		if self.debug:
			print("terminate process. pid:%s [%s]" % (self.p.pid if self.p else "", " ".join(self.cmd)))
		self.p.terminate()

if __name__ == '__main__':

	parser = OptionParser()
	parser.add_option('-c', '--protocol', dest='protocol', default='')
	parser.add_option('-i', '--eth', dest='eth')
	parser.add_option('-w', '--write', dest='write', default='test.pcap')
	parser.add_option('-p', '--port', dest='port', type='int', default=0)
	parser.add_option('-t', '--timeout', dest='timeout', type='int', default=0)
	(options, args) = parser.parse_args()  

	t = tcpdump(options.protocol, options.eth, options.write, options.port)
	if t.run():
		t.terminate(options.timeout)

	
	

