#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

from colorstr import color_str

# ESL包要先安装
try:
	import ESL
except ImportError as err:
	if "No module named" in str(err):
		print(color_str("this script base on ESL, I will install it first, please wait a moment...", "purple"))
		import os
		result = os.system("yum -y install python-devel")
		result += os.system("yum -y install epel-release")
		result += os.system("yum -y install python-setuptools")
		result += os.system("yum -y install python-pip")
		result += os.system("pip install --upgrade pip")
		result += os.system("pip install --upgrade setuptools")
		result += os.system("pip install python-esl")
		if 0 != result:
			print(color_str("sorry, there have some problems on auto-install ESL, please install it manually", "red"))
			import sys
			sys.exit(result)
		else:
			import ESL
			print(color_str("auto-install ESL successful", "green"))
	else:
		print(err)
except Exception as err:
	print(err)
	

class ESLEvent:

	__recv_event_interval = 1000

	def __init__(self, ip, port, password, reconnect_time = 4, \
			standard_event = "CHANNEL_CREATE CHANNEL_ANSWER CHANNEL_PROGRESS CHANNEL_PROGRESS_MEDIA CHANNEL_HANGUP CHANNEL_HANGUP_COMPLETE RECORD_START RECORD_STOP",\
			constom_event = "sippout::hangup sippin::hangup ras::hangup"):
		self.__ip = ip
		self.__port = int(port)
		self.__password = password
		self.__reconnect_time = int(reconnect_time)
		self.__standard_event = standard_event
		self.__constom_event = constom_event
		self.__subscribe_event = " ".join([standard_event, ("CUSTOM " + constom_event) if constom_event else ""]) 
		try:
			self.__esl = ESL.ESLconnection(self.__ip, self.__port, self.__password)
		except Exception as err:
			self.__esl = None
			raise Exception(err)

		if not self.__esl.connected():
			raise Exception("Connect error")

	def __del__(self):
		self.__esl.disconnect()

	def esl(self):
		return self.__esl

	def channel_event(self, event):
		#print(event.serialize())
		pass	
	
	def __process(self, timeout):
		self.__esl.events('json', self.__subscribe_event)
		import datetime
		start = datetime.datetime.now()
		seconds = int(timeout)
		end = start + datetime.timedelta(seconds=seconds)

		while True:
			delta = (end - datetime.datetime.now()).seconds
			if 0 < delta <= seconds:
				event = self.__esl.recvEventTimed(self.__recv_event_interval)
				if event:
					if self.channel_event(event) == "end":
						return True
				elif not self.__esl.connected():
					return True
			else:
				break

		return False

	def run(self, timeout=10):
		#print("connecting freeswitch... ip:%s prot:%s pwd:%s" % (self.__ip, self.__port, self.__password))
		res = True
		if self.__esl.connected():
			#print("conneted...conn:%s, socket:%s info:%s" % (self.__esl.connected(), self.__esl.socketDescriptor(), self.__esl.getInfo()))
			if not self.__process(timeout):
				res = False
		else:
			print("ERR :conntect freeswitch failed. %s:%d@%s" % (self.__ip, self.__port, self.__password))
			res = False

		# 断开freeswtich的连接
		self.__esl.disconnect()
		return res

	def is_connected(self):
		return self.__esl.connected() if self.__esl else False

	def disconnect(self):
		return self.__esl.disconnect() if self.__esl else None

if __name__ == '__main__':
	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option('-s', '--host', dest='host', help='FreeSWITCH server IP address')
	parser.add_option('-p', '--port', dest='port', default=8021, help='FreeSWITCH server event socket port')
	parser.add_option('-a', '--password', dest='password', default='ClueCon', help='ESL password')
	parser.add_option('-t', '--timeout', dest='timeout', default=60, help='timeout')
	(options, args) = parser.parse_args()  

	class MyEvent(ESLEvent):
		def channel_event(self, event):
			event_name = event.getHeader("Event-Name")
			event_sub_name = event.getHeader("Event-Subclass")

			if event_name in ['CHANNEL_CREATE']:
				
				uuid = event.getHeader("unique-id")
				session_id = event.getHeader("variable_session_id")
				call_dir = event.getHeader("Caller-Direction")
				sip_call_id = event.getHeader("variable_sip_call_id")
				print("FREESWIRCH calling... uuid:%s session_id:%s direction:%s call-id:%s" % (uuid, session_id, call_dir, sip_call_id))
			pass

	event = MyEvent(options.host, options.port, options.password)
	event.run(options.timeout)



	
