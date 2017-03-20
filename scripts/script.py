#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

from neko import ProcBar, color_str, ESLEvent, redisCluterBee, MySQL, Ssh, tcpdump

def pat_ProcBar():
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
		p.set_details(total, widget_type="percent")
		p.start("炫光舞法 朵蜜天女 变身! Dancing baby 朵蜜 Dance up...")
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

if __name__ == '__main__':
	pat_ProcBar()