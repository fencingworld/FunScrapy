#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
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

	print len(str(soup))


	soup.style.extract()
	print len(str(soup))
	t  = soup.find(id="pf1")
	print  t
	#t.img.extract()

	print  t
	matchObj = re.search(pattern, string, re.S)
	if matchObj:
	   	st =  matchObj.group()
	
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
        if num>2011:
            Lparas.append(f)
            #print f
print "ddd"
simpleHtml("000001_2012.html")
"""
pool = threadpool.ThreadPool(10)  
requests = threadpool.makeRequests(simpleHtml, Lparas)  
[pool.putRequest(req) for req in requests]  
pool.wait()



st = sthread("test.html")

st.start()
print threading.enumerate()
print threading.activeCount()
st.join()
print threading.enumerate()
print threading.activeCount()

print threading.activeCount()
t= thread.start_new_thread(simpleThead,("test.html",))

print t
while threading.activeCount()>0:
	print threading.activeCount()
	pass

print "end"
"""
