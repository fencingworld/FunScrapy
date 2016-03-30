#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
# 打开一个文件
pattern = r'<div id="page-container">.*<div class="loading-indicator">'
regex = r'alt src="'
fo = open("test.html", "r+")
string = fo.read()
matchObj = re.search(pattern, string, re.S)
if matchObj:
   	st =  matchObj.group()
   	result, number = re.subn(regex, newstring, subject)
	#print "读取的字符串是 : ", st
# 关闭打开的文件
fo.close()
fo = open("testSimple.html", "w+")
fo.write(st)
fo.close()

