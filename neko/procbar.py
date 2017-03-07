#!/usr/bin/env python 
# -*- coding: utf-8 -*- 


import time

import sys
from platform import system
from random import choice
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
LINUX = system() in ['Linux', 'Unix']
WINDOWS = system() in ['Windows']

from threading import Thread, Lock
from colorstr import color_str

class ProcBar(Thread):
	"""
	"""

	__default_timeout = -1
	__default_frequency = 10

	# 字符将从左至右循环显示，同组中的每个串的长度必须相同，建议前面留一个空格
	__default_symbols = {\
		'round': [' -', ' \\', ' |', ' /', ],\
		'smile': ['   ^-^  ', '    ^-^ ','     ^-^', ' ^    ^-', ' -^    ^',' ^-^    ','  ^-^   ',],\
		'smile2': ['   ^-^  ','   ^v^  ',],\
		'bubble': [' o0ooo', ' oo0oo', ' ooo0o', ' oooo0', ' 0oooo',],\
		'cat': [' =^.^=', ' =^o^=',],\
		'pig': [' ^(oo)^', ' ^(.o)^', ' ^(..)^', ' ^(o.)^', ],\
		}

	def __init__(self, name = '', timeout = -1, frequency = 10, mod = 'normal', symbol=''):
		if not LINUX:
			raise Exception("current operation system is '%s' but 'Linux'" % system())
		self.__mod = mod
		if mod in ['normal']:
			self.__ready = True
		elif mod in ['details']:
			self.__ready = False
		else:
			self.__ready = False
		self.__symbol = symbol

		Thread.__init__(self, target=self.run, args=self)
		Thread.setDaemon(self, True)
		self.__mutex = Lock()
		self.__name = name
		self.__timeout = timeout > 0 and timeout or self.__default_timeout
		self.__frequency = frequency > 0 and frequency or self.__default_frequency

		self.__isrun = False
		self.__cur_symbol = ""
		self.__context = ""
		self.__pre_context_len = 0
		self.__final = False
		
	def __lock(self):
		return self.__mutex.acquire()

	def __unlock(self):
		return self.__mutex.release()

	def __select_symbol(self):
		return self.__default_symbols.get(self.__symbol, choice(self.__default_symbols.items())[1]) 

	def __clear_context(self, final = False):
		if self.__final:
			self.__final = final
			return
		sys.stdout.write('\b'*self.__pre_context_len + ' '*self.__pre_context_len + '\b'*self.__pre_context_len)
		sys.stdout.flush()

	def __print_context(self):
		context = self.__cur_symbol + " " + self.__context
		sys.stdout.write(context)
		sys.stdout.flush()
		self.__pre_context_len = len(context)
		return context

	def run(self):
		try:
			self.__isrun = True
			if self.__timeout != -1:
				cnt = self.__timeout * self.__frequency
				forever_loop = False
			else:
			 	cnt = sys.maxint
			 	forever_loop = True
			sleep_time = 1 / float(self.__frequency)
			symbol = self.__select_symbol()[::-1]
			symbols_len = len(symbol)
			frist = True
			while (cnt or forever_loop) and self.__isrun:
				self.__lock()
				self.__cur_symbol = symbol[cnt % symbols_len]
				if frist:
					frist = False
				else:
					self.__clear_context()
				self.__print_context()
				self.__unlock()
				time.sleep(sleep_time)
				cnt -= 1
				
			self.stop()
		except Exception as err:
			self.stop()

	def __proc_details(self):
		if self.__widget_type in ["count"]:
			s = self.__widget_format % (self.__step, self.__total)
		elif self.__widget_type in ["percent"]:
			if self.__end < self.__begin or self.__begin < 0 or self.__end > 100:
				return ""
			need_percent = self.__end - self.__begin
			s = "(%0.2f%%)" % ((float(self.__step) / float(self.__total)) * need_percent + self.__begin)
		else:
			s = self.__widget_format % (self.__step, self.__total)
		return s

	def set_details(self, total, step = 1, widget_type = "count", begin = 0, end = 100, widget_format = "(%d/%d)"):
		if self.__mod == 'details':
			self.__step = 0
			self.__total = total
			self.__widget_type = widget_type
			self.__begin = begin
			self.__end = end
			self.__widget_format = widget_format
			self.__context = self.__proc_details()
			self.__ready = True
		return self

	def move(self, step = 1):
		if not self.__ready or not self.__isrun or self.__mod != 'details':
			return False
	
		self.__step += 1
		self.__context = self.__proc_details()
		if self.__step > self.__total:
			p.stop()
		return True

	def start(self, tips=""):
		if not self.__ready:
			raise Exception("not ready")

		if tips:
			sys.stdout.write(tips)
			sys.stdout.flush()
		Thread.start(self)
			
		return self

	def stop(self, tips=""):
		if self.__isrun:
			self.__lock()
			self.__clear_context(True)
			self.__unlock()
			self.__isrun = False
			self.__ready = False
		if tips:
			print(tips)
		return self

if __name__ == '__main__':
	try:
		#月光舞法 法苏天女 变身! Dancingbaby 法苏 Trans out! [变身完] Lightning!
		p = ProcBar(timeout=5)
		print("yeah!yeah!yeah! ~~SHOW TIME~~")
		p.start("月光舞法 法苏天女 变身! Dancing baby 法苏 Trans out...")
		time.sleep(2)
		p.stop(color_str("lightning", "red"))
		time.sleep(1)
		del p

		sys.stdout.write("月光舞法 法苏天女 变身! Dancing baby 法苏 Trans out...")
		sys.stdout.flush()
		p = ProcBar(timeout=5, frequency=5, symbol='pig')
		p.start()
		time.sleep(6)
		p.stop(color_str("lightning", "yellow"))
		del p

		sys.stdout.write("月光舞法 法苏天女 变身! Dancing baby 法苏 Trans out...")
		sys.stdout.flush()
		p = ProcBar(timeout=5, frequency=5, symbol='smile')
		p.start()
		time.sleep(6)
		p.stop(color_str("lightning", "blue"))
		del p

		p = ProcBar(timeout=5, frequency=5, symbol='cat')
		p.start("月光舞法 法苏天女 变身! Dancing baby 法苏 Trans out...")
		time.sleep(6)
		p.stop(color_str("lightning", "green"))
		del p
		
		#炫光舞法 朵蜜天女 变身!Dancing baby 朵蜜 Dance up! [变身完] Shining!
		p = ProcBar(mod='details')
		total = 56
		p.set_details(total, widget_type="percent").start("炫光舞法 朵蜜天女 变身! Dancing baby 朵蜜 Dance up...")
		for i in range(0, total + 1):
			if p.move():
				time.sleep(0.1)
		p.stop(color_str("shining", "sky_blue"))
		time.sleep(1)
		del p

		#灿星舞法 拉媞天女 变身!Dancing baby 拉媞 Dance up! [变身完] Blinking!
		p = ProcBar(frequency=20, mod='details', symbol='bubble')
		total = 102
		p.set_details(total, widget_type="count").start("灿星舞法 拉媞天女 变身! Dancing baby 拉媞 Dance up...")
		for i in range(0, total + 1):
			if p.move():
				time.sleep(0.1)
		p.stop(color_str("blinking", "sky_blue"))
		time.sleep(1)
		del p

		print("yeah!yeah!yeah! ~~ENDING~~")
	except Exception as err:
		raise Exception(err)
