#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import os
import thread
import threading
import threadpool
import sys
import MySQLdb


reload(sys)
sys.setdefaultencoding( "utf-8" )
import os
from bs4 import BeautifulSoup
          
ORIPath = "..\ResFile\html"
RESPath = "..\ResFile\html_sp"

def simpleHtml(title):
	print title,"s"
	
	pattern = r'<div id="page-container">.*<div class="loading-indicator">'
	fo = open(ORIPath+"\\"+title, "r+")
	string = fo.read()
	fo.close()
	soup = BeautifulSoup(string,'html.parser',from_encoding = 'utf-8')
	print len(str(soup))
	i = soup.find_all("img")
	for j in i:
		j["src"] =""

	i = soup.find_all("style")
	for j in i:
		j.string =""
	i = soup.find_all("script")
	for j in i:
		j.string =""

	print len(str(soup))

	fo = open(RESPath+"\\"+title, "w+")
	#fo.write(st)
	fo.write(str(soup))
	fo.close()
	print title,"e"
	


Lparas = []

dirlists = os.listdir(ORIPath)
for f in dirlists:
    m = re.search("_\d{4}\.html",f)
    if m!=None:
        num = int(f[7:11])
        if num>2011 and os.path.exists(RESPath+"\\"+f) !=True :
            Lparas.append(f)
print "ddd"
#simpleHtml("000001_2012.html")

pool 		= threadpool.ThreadPool(5)  
requests 	= threadpool.makeRequests(simpleHtml, Lparas)  
[pool.putRequest(req) for req in requests]  
pool.wait()
