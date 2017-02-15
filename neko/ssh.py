#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

from colorstr import color_str

# paramiko包要先安装
try:
	import paramiko
except ImportError as err:
	if "No module named" in str(err):
		print(color_str("this script base on paramiko, I will install it first, please wait a moment...", "purple"))
		import os
		result = os.system("yum -y install python-devel")
		result += os.system("yum -y install epel-release")
		result += os.system("yum -y install python-setuptools")
		result += os.system("yum -y install python-pip")
		result += os.system("pip install --upgrade pip")
		result += os.system("pip install pycrypto")
		result += os.system("pip install paramiko")
		if 0 != result:
			print(color_str("sorry, there have some problems on auto-install paramiko, please install it manually", "red"))
			import sys
			sys.exit(result)
		else:
			import paramiko
			print(color_str("auto-install paramiko successful", "green"))
	else:
		print(err)
except Exception as err:
	print(err)

class Ssh:

	__ssh = None

	def __init__(self, ip, port = 22, username = 'root', password = 'root', connect_timeout = 4, debug=False):
		self.__ssh = paramiko.SSHClient()
		self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			self.__ssh.connect(ip, port, username=username, password=password, timeout=connect_timeout)
		#except paramiko.ssh_exception.AuthenticationException as err:
		except Exception as err:
			raise Exception(err)

		pass

	def __del__(self):
		if self.__ssh:
			self.__ssh.close()

	def ssh(self):
		return self.__ssh

	def exec_command(self, cmd):
		return self.__ssh.exec_command(cmd)

if __name__ == '__main__':
	from optparse import OptionParser
	import os,sys

	parser = OptionParser()
	parser.add_option('-s', '--host', dest='host', default='10.9.0.109', help='ip address')
	parser.add_option('-u', '--user', dest='user', default='root', help='user name')
	parser.add_option('-p', '--password', dest='password', default='root', help='password')
	parser.add_option('-c', '--cmd', dest='cmd', default='', help='cmd')

	(options, args) = parser.parse_args()
	try:
		s = Ssh(options.host, username = options.user, password = options.password)	
		stdin, stdout, stderr = s.exec_command(options.cmd)
		for l in stdout.readlines():
			sys.stdout.write(l)	
	except Exception as err:
		print(err)

