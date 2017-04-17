#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
import time,sys,os
from neko import ProcBar, color_str

def pat_ProcBar():
	try:
		print("yeah!yeah!yeah! ~~SHOW TIME~~")
		#月光舞法 法苏天女 变身! Dancingbaby 法苏 Trans out! [变身完] Lightning!
		for i in range(0, 20):
			p = ProcBar(timeout=5)
			p.start("月光舞法 法苏天女 变身! Dancing baby 法苏 Trans out...")
			#time.sleep(1)
			p.stop(color_str("lightning", "red"))
			time.sleep(1)
			del p

		for i in range(0, 20):
			p = ProcBar(timeout=5, frequency=5, symbol='pig')
			p.start("月光舞法 法苏天女 变身! Dancing baby 法苏 Trans out...")
			#time.sleep(1)
			p.stop(color_str("lightning", "yellow"))
			del p

		for i in range(0, 20):
			p = ProcBar(timeout=5, frequency=5, symbol='smile')
			p.start("月光舞法 法苏天女 变身! Dancing baby 法苏 Trans out...")
			#time.sleep(1)
			p.stop(color_str("lightning", "blue"))
			del p

		for i in range(0, 20):
			p = ProcBar(timeout=5, frequency=5, symbol='cat')
			p.start("月光舞法 法苏天女 变身! Dancing baby 法苏 Trans out...")
			#time.sleep(1)
			p.stop(color_str("lightning", "green"))
			del p
		
		#炫光舞法 朵蜜天女 变身!Dancing baby 朵蜜 Dance up! [变身完] Shining!
		for i in range(0, 20):
			p = ProcBar(mod='details')
			total = 12
			p.set_details(total, widget_type="percent")
			p.start("炫光舞法 朵蜜天女 变身! Dancing baby 朵蜜 Dance up...")
			for i in range(0, total):
				if p.move():
					time.sleep(0.1)
			p.stop(color_str("shining", "sky_blue"))
			time.sleep(1)
			del p


		#灿星舞法 拉媞天女 变身!Dancing baby 拉媞 Dance up! [变身完] Blinking!
		for i in range(0, 2):
			p = ProcBar(frequency=20, mod='details', symbol='bubble')
			total = 23
			p.set_details(total, widget_type="count").start("灿星舞法 拉媞天女 变身! Dancing baby 拉媞 Dance up...")
			for i in range(0, total):
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