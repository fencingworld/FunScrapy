#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2016年4月4日

@author: dell
'''
import sys
import MySQLdb
import os
import threadpool
reload(sys)
sys.setdefaultencoding('utf8')
import urllib2
import cookielib
import re
from bs4 import BeautifulSoup
rc = re.compile('^[0123456789\-\.,]{1,25}(%?)$')
zh = re.compile(u'[\u4e00-\u9fa5]+')
sql     = "SELECT distinct sCode,sYear FROM finance"

db = MySQLdb.connect("localhost","root","root","funscrapy" ,charset="utf8")
cursor = db.cursor()
cursor.execute(sql )
results = cursor.fetchall()
for row in results:
	sql1 = "SELECT * FROM finance WHERE sCode = %s and sYear= %s" % (row[0],row[1])
	cursor.execute(sql1)
	res = cursor.fetchall()
	mark = 0
	for r in res:
		l = len(r[3])
		z = zh.search(r[3])
		m = rc.match(r[3])
		if not (m and not z and l<=25):
			mark =1
			break
	if  mark == 0:
		for r in res:
			cursor.execute("INSERT INTO `funscrapy`.`financeuse` (`sCode`, `sYear`, `sKey`, `sValue`) VALUES ('%s', '%s', '%s', '%s');" % (r[0],r[1],r[2],r[3]))
			db.commit()

	
db.close
