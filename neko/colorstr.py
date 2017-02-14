#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
import sys
from platform import system

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
LINUX = system() in ['Linux']
WINDOWS = system() in ['Windows']

def color_str(s, color = 'white', need = True):
	if LINUX and need:
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

if __name__ == '__main__':
	print(color_str("red", "red"))
	print(color_str("yellow", "yellow"))
	print(color_str("blue", "blue"))
	print(color_str("green", "green"))
	print(color_str("purple", "purple"))
	print(color_str("gray", "gray"))
	print(color_str("sky_blue", "sky_blue"))
	print(color_str("white", "white"))