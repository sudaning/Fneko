#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
from optparse import OptionParser 
from colorstr import color_str
import os,sys

try:
	import MySQLdb
except ImportError as err:
	if "No module named" in str(err):
		print(color_str("this script base on MySQLdb, I will install it first, please wait a moment...", "purple"))
		result = os.system("yum -y install python-devel")
		result += os.system("yum -y install epel-release")
		result += os.system("yum -y install python-setuptools")
		result += os.system("yum -y install python-pip")
		result += os.system("pip install --upgrade pip")
		result += os.system("pip install --upgrade setuptools")
		result += os.system("pip install mysql")
		if 0 != result:
			print(color_str("sorry, there have some problems on auto-install MySQLdb, please install it manually", "red"))
			sys.exit(result)
		else:
			import MySQLdb
			print(color_str("auto-install MySQLdb successful", "green"))
	else:
		print(err)
except Exception as err:
	print(err)
	
class MySQL:
	def __init__(self, host, port, user, password, dbname):
		try:
			self.__conn = MySQLdb.connect(
		        host = host,
		        port = port,
		        user = user,
		        passwd = password,
		        db = dbname)
			self.__cursor = self.__conn.cursor()
		except Exception as err:
			raise Exception(err)

	def __del__(self):
		if self.__conn:
			self.__conn.close()

	def execute(self, sql):
		try:
			self.__cursor.execute(sql)
			return self.__cursor.fetchall()
		except Exception as err:
			raise Exception(err)

if __name__ == '__main__':
	
	parser = OptionParser()
	parser.add_option('-s', '--host', dest='host', default='10.0.33.54', help='MySQL server IP address')
	parser.add_option('-p', '--port', dest='port', type="int", default=3306, help='MySQL server port')
	parser.add_option('-u', '--user', dest='user', default='root', help='MySQL server user')
	parser.add_option('-a', '--password', dest='password', default='33E9.com', help='MySQL server password')
	parser.add_option('-d', '--dbname', dest='dbname', default='e9cloud_home', help='MySQL server dbname')
	(options, args) = parser.parse_args()

	
	

	
