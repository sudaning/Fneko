#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

#
# 只能在Linux/Unix上运行
#

from platform import system as osys
import sys
import time
from threading import Thread, Lock

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

# 语言设置"Chinese" "English"
language = 'Chinese'

def color_str(s, color = 'white', need = True):
	if osys() in ['Linux'] and need:
		color_code = color.lower() == 'red' and 91 or \
			color.lower() == 'yellow' and 93 or \
			color.lower() == 'blue' and 94 or \
			color.lower() == 'green' and 92 or \
			color.lower() == 'purple' and 95 or \
			color.lower() == 'gray' and 90 or \
			color.lower() == 'sky_blue' and 36 or \
			97
		return '\033[0m\033[' + str(color_code) + 'm' + s + '\033[0m'
	else:
		return s

def print_proc(process, total, step = 1, widgetType = "count", begin = 0, end = 100, widgetFormat = "(%d/%d)"):
	if osys() not in ['Linux']:
		return process
	try:
		if widgetType in ["count"]:
			s = widgetFormat % (process, total)
		elif widgetType in ["percent"]:
			if end < begin or begin < 0 or end > 100:
				return process
			needPercent = end - begin
			s = "(%0.2f%%)" % ((float(process) / float(total)) * needPercent + begin)
		else:
			s = widgetFormat % (process, total)
		s += "\b" * len(s)
		sys.stdout.write(s)
		sys.stdout.flush()
		return process + step
	except Exception as err:
		return process

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

	def __init__(self, name = '', timeout = -1, frequency = 10, mod = 'normal', symbol='round'):
		if osys() not in ['Linux']:
			raise Exception("current operation system is '%s' not 'Linux/Unix'" % osys())
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
		return self.__default_symbols.get(self.__symbol, self.__default_symbols['round']) 

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
		#月光舞法 法苏天女 变身!Dancing baby 法苏 Trans out! [变身完] Lightning!
		sys.stdout.write("yeah!yeah!yeah! SHOW TIME!\njust lightning... lightning... lightning...")
		sys.stdout.flush()
		p = ProcBar(timeout=5)
		p.start()
		time.sleep(2)
		p.stop()
		time.sleep(1)
		del p

		sys.stdout.write("\nagain lightning... lightning... lightning...")
		sys.stdout.flush()
		p = ProcBar(timeout=5, frequency=5, symbol='pig')
		p.start()
		time.sleep(6)
		del p

		sys.stdout.write("\nagain lightning... lightning... lightning...")
		sys.stdout.flush()
		p = ProcBar(timeout=5, frequency=5, symbol='smile')
		p.start()
		time.sleep(6)
		del p

		sys.stdout.write("\nagain lightning... lightning... lightning...")
		sys.stdout.flush()
		p = ProcBar(timeout=5, frequency=5, symbol='cat')
		p.start()
		time.sleep(6)
		del p
		
		#炫光舞法 朵蜜天女 变身!Dancing baby 朵蜜 Dance up! [变身完] Shining!
		sys.stdout.write("\npercent with shining... shining... shining...")
		sys.stdout.flush()
		p = ProcBar(mod='details')
		total = 56
		p.set_details(total, widget_type="percent").start()
		for i in range(0, total + 1):
			if p.move(i):
				time.sleep(0.1)
		p.stop()
		time.sleep(1)
		del p

		#灿星舞法 拉媞天女 变身!Dancing baby 拉媞 Dance up! [变身完] Blinking!
		sys.stdout.write("\ncount with blinking... blinking... blinking...")
		sys.stdout.flush()
		p = ProcBar(frequency=20, mod='details', symbol='bubble')
		total = 102
		p.set_details(total, widget_type="count").start()
		for i in range(0, total + 1):
			if p.move(i):
				time.sleep(0.1)
		p.stop()
		time.sleep(1)
		del p

		print("\nyeah!yeah!yeah! ENDING!")
	except Exception as err:
		raise Exception(err)