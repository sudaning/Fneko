#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

from colorstr import color_str

# redis包要先安装
try:
	import redis
except ImportError as err:
	if "No module named" in str(err):
		print(color_str("this script base on redis, I will install it first, please wait a moment...", "purple"))
		import os
		result = os.system("yum -y install python-devel")
		result += os.system("yum -y install epel-release")
		result += os.system("yum -y install python-setuptools")
		result += os.system("yum -y install python-pip")
		result += os.system("pip install --upgrade pip")
		result += os.system("pip install --upgrade setuptools")
		result += os.system("pip install redis")
		if 0 != result:
			print(color_str("sorry, there have some problems on auto-install redis, please install it manually", "red"))
			import sys
			sys.exit(result)
		else:
			import redis
			print(color_str("auto-install redis successful", "green"))
	else:
		print(err)
except Exception as err:
	print(err)


class redisCluterBee:

	__pool = {}
	__primary_addr = ""

	def __init__(self, addrs, debug=False):
		self.addrs = addrs
		self.debug = debug

		for addr in addrs.split(','):
			host, port = addr.split(':')
			self.__pool[addr] = redis.Redis(host=host, port=int(port), db=0, password=None, socket_timeout=3)
			if self.debug:
				print("redis init %s:%d %s" % (host, int(port), self.__pool[addr]))
		else:
			self.__primary_addr = addr
			if self.debug:
				print("redis pool: %s" % self.__pool)
				print("redis primary addr: %s" % self.__primary_addr)

	def __fun__(self, r, method):
		if r:
			return method == 'set' and r.set or \
				method == 'get' and r.get or \
				method == 'hset' and r.hset or \
				method == 'hget' and r.hget or \
				method == 'hgetall' and r.hgetall or \
				method == 'incr' and r.incr or \
				method == 'decr' and r.decr or \
				method == 'delete' and r.delete or \
				None
		else:
			return None

	def __run__(self, method, *argv):
		ret = None
		f = self.__fun__(self.__pool.get(self.__primary_addr, None), method)
		if self.debug:
			print("%s %s %s" % (method, argv, f))
		try:
			ret = f and f(*argv)
		except redis.exceptions.ResponseError as err:
			res = str(err).split(' ')
			if self.debug:
				print(res)
			# 重定向redis服务器
			if len(res) and res[0] == "MOVED":
				if len(res) >= 2:
					r = self.__pool.get(res[2], None)
					if not r:
						host, port = res[2].split(':')
						r = redis.Redis(host=host, port=int(port), db=0, password=None, socket_timeout=3)
						self.__pool[res[2]] = r
						if self.debug:
							print("redis init %s:%d %s" % (host, int(port), r))

					f = self.__fun__(r, method)
					return f and f(*argv)
			else:
				raise redis.exceptions.ResponseError(err)
		except redis.exceptions.ConnectionError as err:
			raise redis.exceptions.ConnectionError(err)
		else:
			return ret

	def set(self, key, value):
		return self.__run__('set', key, value)

	def get(self, key):
		return self.__run__('get', key)

	def incr(self, key, amount = 1):
		return self.__run__('incr', key, amount)

	def decr(self, key, amount = 1):
		return self.__run__('decr', key, amount)

	def hset(self, space, key, value):
		return self.__run__('hset', space, key, value)

	def hget(self, space, key):
		return self.__run__('hget', space, key)

	def hgetall(self, space):
		return self.__run__('hgetall', space)

	def delete(self, *argv):
		return self.__run__('delete', *argv)
		

if __name__ == '__main__':
	r = redisCluterBee('10.0.33.54:7000', debug=False)
	print(r.set('123',456))
	print(r.get('123'))
	print(r.set('789','aaa'))
	print(r.get('sf'))
	print(r.get('789'))
	print(r.get('1234'))
	print(r.incr('total', 100))
	print(r.incr('total', 200))
	print(r.decr('total', 50))
	print(r.hset('city', 'cq', '023'))
	print(r.hset('city', 'bj', '010'))
	print(r.hget('city', 'sz'))
	print(r.hget('city', 'cq'))
	print(r.hgetall('city'))