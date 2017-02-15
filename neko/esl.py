#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import sys,os
from colorstr import color_str

# ESL包要先安装
try:
	import ESL
except ImportError as err:
	if "No module named" in str(err):
		print(color_str("this script base on ESL, I will install it first, please wait a moment", "purple"))
		result = os.system("yum -y install python-devel")
		result += os.system("yum -y install epel-release")
		result += os.system("yum -y install python-setuptools")
		result += os.system("yum -y install python-pip")
		result += os.system("pip install --upgrade pip")
		result += os.system("pip install python-esl")
		if 0 != result:
			print(color_str("sorry, there have some problems on auto-install ESL, please install it manually", "red"))
			sys.exit(result)
		else:
			import ESL
			print(color_str("auto-install ESL successful", "green"))
	else:
		print(err)
except Exception as err:
	print(err)
	

class ESLEvent:

	def __init__(self, ip, port, password, reconnect_time = 4, debug=False):
		self.__ip = ip
		self.__port = port
		self.__password = password
		# 顺序很重要，“CUSTOM”之后的自定义消息，若放在前面，ESL会抓不到消息??? 应该是他自己版本的BUG
		self.__subscribe_event = " ".join(["CHANNEL_CREATE", "CHANNEL_ANSWER", "CHANNEL_PROGRESS", 
			"CHANNEL_HANGUP", "CHANNEL_HANGUP_COMPLETE", 
			"RECORD_START", "RECORD_STOP", 
			"CUSTOM", "sippout::hangup", "sippin::hangup", "ras::hangup"])
		self.__reconnect_time = reconnect_time
		self.__esl = ESL.ESLconnection(self.__ip, self.__port, self.__password)
		self.__debug = debug
		self.__run = True
		self.__recv_event_interval = 1000
		if self.__debug:
			print("ESL connected")
		pass

	def __del__(self):
		self.__esl.disconnect()

	def esl(self):
		return self.__esl

	def channel_create(self, event):
		#print(event.serialize())
		pass	
		
	def channel_progress(self, event):
		#print(event.serialize())
		pass

	def channel_progress_media(self, event):
		#print(event.serialize())
		pass

	def channel_answer(self, event):
		#print(event.serialize())
		pass

	def channel_hangup(self, event):
		#print(event.serialize())
		pass

	def channel_hangup_complete(self, event):
		#print(event.serialize())
		pass

	def record_start(self, event):
		#print(event.serialize())
		pass

	def record_stop(self, event):
		#print(event.serialize())
		pass

	def server_disconnected(self, event):
		#print("disconnect...bye")
		return "end"

	def custom_ras_hangup(self, event):
		#print(event.serialize())
		pass

	def custom_sippin_hangup(self, event):
		#print(event.serialize())
		pass

	def custom_sippout_hangup(self, event):
		#print(event.serialize())
		pass

	def __process(self, timeout):
		self.__esl.events('json', self.__subscribe_event)
		import datetime
		start = datetime.datetime.now()
		seconds = int(timeout)
		end = start + datetime.timedelta(seconds=seconds)
		while self.__run:
			if timeout:
				delta = (end - datetime.datetime.now()).seconds
				if delta <= 0 or delta > seconds:
					if self.__debug:
						print("ESL timeout")
					break
			event = self.__esl.recvEventTimed(self.__recv_event_interval)
			if event:
				event_name = event.getHeader("Event-Name")
				event_sub_name = event.getHeader("Event-Subclass")
				#print("event_sub_name:%s" % event_sub_name)

				proc = event_name in ['CHANNEL_CREATE'] and self.channel_create or \
					event_name in ['CHANNEL_ANSWER'] and self.channel_answer or \
					event_name in ['CHANNEL_PROGRESS'] and self.channel_progress or \
					event_name in ['CHANNEL_PROGRESS_MEDIA'] and self.channel_progress_media or \
					event_name in ['CHANNEL_HANGUP'] and self.channel_hangup or \
					event_name in ['CHANNEL_HANGUP_COMPLETE'] and self.channel_hangup_complete or \
					event_name in ['RECORD_START'] and self.record_start or \
					event_name in ['RECORD_STOP'] and self.record_stop or \
					event_name in ['SERVER_DISCONNECTED'] and self.server_disconnected or \
					event_name in ['SHUTDOWN'] and self.server_disconnected or \
					event_name in ['CUSTOM'] and \
						(event_sub_name in ['ras::hangup'] and self.custom_ras_hangup or \
						event_sub_name in ['sippin::hangup'] and self.custom_sippin_hangup or \
						event_sub_name in ['sippout::hangup'] and self.custom_sippout_hangup or None) or \
					None
				if proc and proc(event) == "end":
					return True
			elif not self.__esl.connected():
				return True

		return False

	def run(self, timeout=10):
		#print("connecting freeswitch... ip:%s prot:%s pwd:%s" % (self.__ip, self.__port, self.__password))
		res = True
		if self.__esl.connected():
			#print("conneted...conn:%s, socket:%s info:%s" % (self.__esl.connected(), self.__esl.socketDescriptor(), self.__esl.getInfo()))
			if not self.__process(timeout):
				#print("ERR :timeout")
				#print(1)
				res = False
		else:
			print("ERR :conntect freeswitch failed. %s:%d@%s" % (self.__ip, self.__port, self.__password))
			res = False

		# 断开freeswtich的连接
		self.__esl.disconnect()
		if self.__debug:
			print("ESL disconnect")
		return res

	def terminate(self):
		self.__run = False
		try:
			self.__esl.disconnect()
			if self.__debug:
				print("ESL disconnect")
		except Exception as err:
			pass
		
if __name__ == '__main__':
	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option('-s', '--host', dest='host', help='FreeSWITCH server IP address')
	parser.add_option('-p', '--port', dest='port', default=8021, help='FreeSWITCH server event socket port')
	parser.add_option('-a', '--password', dest='password', default='ClueCon', help='ESL password')
	(options, args) = parser.parse_args()  

	event = ESLEvent(options.host, options.port, options.password)
	event.run()



	
