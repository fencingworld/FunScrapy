#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import urllib 
import urllib2 
import random
import MySQLdb
import os
reload(sys)
sys.setdefaultencoding('utf-8')
#import requests  


import threading
import time
def cbk(NumBlockGet, SizeBlock, SizeFile): 
    '''回调函数
    @a: 已经下载的数据块
    @b: 数据块的大小
    @c: 远程文件的回调函数大小
    ''' 
    float(SizeFile)
    print NumBlockGet," ",SizeBlock," ",SizeFile
    k=1024
    per = 100.0 * NumBlockGet * SizeBlock / (3088*k)
    if per > 100: 
        per = 100 
    print '%.2f%%' % per 


class downloadThread(threading.Thread):
    def __init__(self,url,title,currtask,adjunctSize):
        threading.Thread.__init__(self)
        self.url    = url
        self.title  = title
        self.currtask = currtask
        self.adjunctSize = adjunctSize
    def run(self):
        #print self.url.encode('utf-8') + " " + self.title.encode('utf-8') 
        print "downloading task : %d" % currtask
        #time.sleep(random.uniform(0.1,0.9))
        #print "exit title"
        while True:

        
          try :

            u = urllib.urlopen(self.url)
            data = u.read()
            f = open(self.title+".pdf", 'wb')
            f.write(data)
            f.close()

            fileSize = os.path.getsize(self.title+".pdf")
            print "%d\t\t%d" % (fileSize,self.adjunctSize*1024)
            
            if fileSize/1024 - self.adjunctSize < 10:
              break
            else :
              os.remove(self.title+".pdf")
          except Exception, e:
            print e
            print "try again %d" % currtask
        




url = 'http://www.cninfo.com.cn//cninfo-new/disclosure/fund_listed/download/1201902743'

name =  "968004 968004 摩根总收益债.pdf"
name = name.decode('UTF-8')
print "downloading with urllib"
db = MySQLdb.connect("127.0.0.1","root","root","funscrapy" ,charset='utf8')

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

# 使用execute方法执行SQL语句
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取一条数据库。
data = cursor.fetchone()

print "Database version : %s " % data
finish = 0
cursor = db.cursor()
sql =   "SELECT targetUrl,targetTitle,adjunctSize,adjunctSize\
         FROM   announcements \
         WHERE  download = 0 and typeMark = 0"
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results  = cursor.fetchall()
    taskNum  = len(results)
    currtask = 0
    #print type(results)
   
    while True:
      threadNum = len(threading.enumerate())
      if threadNum < 40 :
        print "tread numbers : %d" % (threadNum)
        url   = results[currtask][0]
        title = results[currtask][1]
        adjunctSize = results[currtask][2]
        task  = downloadThread(url,title,currtask,adjunctSize)
        task.start()
        currtask +=1
        if currtask >= taskNum:
          break
    print "exit main process"
   #for row in results:
      #print finish 
      #print row[1].decode('utf8')
      #print row[2]
    #  finish = finish + 1

      #urllib.urlretrieve(row[0], row[1]+ ".pdf",cbk)   
except Exception, e:
        print e
        print "Error: unable to fecth data"

# 关闭数据库连接
db.close()

print "Finish"
