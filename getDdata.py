#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2016年4月4日

@author: dell
'''
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import urllib2
import cookielib
import re
from bs4 import BeautifulSoup

fp = open("test2.html",'r+')
html_doc = fp.read()
#print html_doc
fp.close()


soup = BeautifulSoup(html_doc,'html.parser',from_encoding = 'utf-8')
#print str(soup)
imark = soup.img
while imark!=None :
    soup.img.extract()
    imark = soup.img
#print str(soup)
links =soup.find_all('div',class_=re.compile(r'^c'))
print len(links)
for link in links:
    data = link.get_text().encode('utf8')
    data = "".join(data.split())#delete space 除去空格

    num = len(link.contents)
    while num!=0:
        link.contents[0].extract()
        num = len(link.contents)
    link.append(data)
    
links =soup.find_all('div',class_=re.compile(r'^t'))
print len(links)
for link in links:
    data = link.get_text().encode('utf8')
    data = "".join(data.split())
    num = len(link.contents)
    while num!=0:
        link.contents[0].extract()
        num = len(link.contents)
    link.append(data)    


fp = open("new_test2.html","w+")
links =soup.find_all('div',class_=re.compile(r'^[t|c]'))
print len(links)
state = 0
xdi =0
ystr = '-1'
ylist = []
xlist =[]
xdic = {}
for link in links:
    fp.write(str(link))
    data = link.get_text().encode('utf8')
    if data ==' ':
        data ='-'
    if state ==0:
        m = re.search(r'\d\.\d资产负债表',data)
        if m!=None :
            state = 1
    if state ==1:
        m = re.search(r'\d\.\d利润表',data)
        if m!=None :
            ylist.append(xlist)
            state = 2
            continue
        if link['class'][0]!='c':
            continue
        x = link['class'][1]
        y = link['class'][2]
        if x not in xdic:
            xdic.update({x:xdi})
            xdi = xdi +1
        if y != ystr:
            ystr = y 
            ylist.append(xlist)
            xlist=[]
        xlist.append(data)

            
    
    if state ==2:
        break
    
fp.close()

fp=open("part.html",'w+')
fp.write("<table>")

for i in ylist:
    fp.write("<tr>")
    print len(i),
    for j in i:
        fp.write("<td>")
        fp.write(j)
        print j,
        fp.write("</td>")
    print ""
    fp.write("</tr>")
fp.write("</table>")
