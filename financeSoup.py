#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2016年4月4日

@author: dell
'''
import sys
import MySQLdb
import os
reload(sys)
sys.setdefaultencoding('utf8')
import urllib2
import cookielib
import re
from bs4 import BeautifulSoup

codeItem=[
r"营业.*收入",
r"归属于上市公司股东的净利润",
r"归属于上市公司股东的扣除非经常性损益的净利润",
r"^经营活动产生的现金流量净额",
r"基本每股收益",
r"稀释每股收益",
r"净资产收益率",
r"总资产",
r"归属于上市公司股东的(净资产|股东权益)"]


#print len(codeItem)


def find_item(data):
    return True,




def MyParser(ORIPath,title,RESPath):
    print title[:11]
    fp = open(ORIPath+"\\"+title,'r+')
    html_doc = fp.read()
    fp.close()
    

    soup = BeautifulSoup(html_doc,'html.parser',from_encoding = 'utf-8')
    #print str(soup)
    

    links =soup.find_all('div',class_=re.compile(r'^c'))
    print "c",len(links)
    for link in links:
        data = link.get_text().encode('utf8')
        data = "".join(data.split())#delete space 除去空格
    
        num = len(link.contents)
        while num!=0:
            link.contents[0].extract()
            num = len(link.contents)
            
        link.append(data)
        
    links =soup.find_all('div',class_=re.compile(r'^t'))
    print "t",len(links)
    for link in links:
        data = link.get_text().encode('utf8')
        data = "".join(data.split())
        num = len(link.contents)
        while num!=0:
            link.contents[0].extract()
            num = len(link.contents)
        link.append(data)    
    
    
    db = MySQLdb.connect("localhost","root","root","funscrapy" )

    cursor = db.cursor()

    cursor.execute("SELECT VERSION()")

    codeFind = [0]*len(codeItem)


    fp = open(RESPath+"\\"+title[:11]+"_ex.html","w+")
    links =soup.find_all('div',class_=re.compile(r'^[c|t]'))
    print "links",len(links)
    state = 0
    clist =[]
    itfind=-1;
    codeItemV=codeItem[:]
    for link in links:
        #print link
        #fp.write(str(link))
        data = link.get_text().encode('utf8')
        if data ==' ':
            data ='-'
        if state ==0:
            m = re.search(r'.*会计数据和.*',data)
            if m!=None :
                print "find"
                state = 1
        if state ==1:
            #fp.write(str(link))
            m = re.search(r'.*国际会计准则.*',data)
            if m==None :
                #fp.write("<div class=\"My\">"+data+"</div>")
                #fp.write(str(link))
                #print link.get_text("|", strip=True)
                if (itfind!=-1):
                    print codeItem[itfind],data
                    sql ='INSERT INTO finance values("%s","%s","%s","%s")' %( title[0:6],title[7:11],itfind,data)
                    cursor.execute(sql)
                    db.commit()
                    codeItemV[itfind]= data
                    codeFind[itfind] = 1
                    itfind=-1
                else:
                    itc=0
                    for it in codeItem:
                        #print it,data
                        res = re.search(it,data)
                        if res!=None:
                            if codeFind[itc]==0:
                                itfind = itc
                            else:
                                itfind=-1
                            break
                        itc= itc+1
                #clist.append(data)
            else :
                state = 2
        if state ==2:
            break
    #print codeItemV
    fp.write("<table>")
    ccc =0 
    for a in codeItem:
        fp.write("<tr>")
        
        fp.write("<td>")
        fp.write(a);
        fp.write("</td>")
        fp.write("<td>")
        fp.write(codeItemV[ccc])
        fp.write("</td>")
      
        fp.write("</tr>")
        ccc=ccc+1
    fp.write("</table>")
    fp.close()
    db.close()



op = 1

  
ORIPath = "..\ResFile\html"
RESPath = "..\ResFile\html_ex"
if op ==1:

    dirlists = os.listdir(ORIPath)
    for f in dirlists:
        m = re.search("_\d{4}\.html",f)
        if m!=None:
            num = int(f[7:11])
            if num>2011:
                MyParser(ORIPath,f,RESPath)
                print f
else :
    MyParser(ORIPath,"000023_2013.html",RESPath)
