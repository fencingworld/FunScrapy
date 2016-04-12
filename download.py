#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import urllib 
import urllib2 
import random
import MySQLdb
import requests  
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
    def __init__(self,url,title,currtaskid,adjunctSize):

        threading.Thread.__init__(self)
        self.url    = url
        self.title  = title#.replace("*", "")
        self.currtaskid = currtaskid
        self.adjunctSize = adjunctSize
    def run(self):
        self.title = self.title.replace("*", "")
        ic=0
        while True:
            ic= ic+ 1
            print "[%d]  for  (%d)  times" % (self.currtaskid ,ic)
            
            try :
                """
                u = urllib.urlopen("http://"+self.url)
                data = u.read()
                print data
                f = open(self.title+".pdf", 'wb')
                f.write(data)
                f.close()
                """
                r = requests.get("http://"+self.url)   
                with open(self.title+".pdf", "wb") as code:       
                    code.write(r.content)
                    
                """
                if os.path.exists(self.title+".pdf")==False:
                    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                else:
                    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
                """
                fileSize = os.path.getsize(self.title+".pdf")
                print fileSize
                
                
                if abs(fileSize/1024)  > 2:
                    print "[%d]  success in (%d)" % (self.currtaskid ,ic)
                    break
                else :
                    os.remove(self.title+".pdf")
                
                
                #break
            except Exception, e:
                print e
                
            
        


os.mkdir("newdir")
os.chdir("newdir")
url = 'http://www.cninfo.com.cn//cninfo-new/disclosure/fund_listed/download/1201902743'


print "downloading with urllib"
db = MySQLdb.connect("127.0.0.1","root","root","funscrapy" ,charset='utf8') 
cursor = db.cursor()

cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data

finish = 0
cursor = db.cursor()
sql =   """
SELECT targetUrl,targetTitle,adjunctSize
FROM   announcements_copy 
WHERE  download = 0 and typeMark = 1 
    and targetTitle not like "%摘要%"  
    and targetTitle not like "%取消%"   
    and targetTitle not like "%英文%"   
    ORDER BY secCode
    """
try:
    cursor.execute(sql)
    results  = cursor.fetchall()
    db.close()
    
    taskNum  = len(results)
    currtask = 0
    while True:
        
        threadNum = len(threading.enumerate())
        if threadNum < 400 :
            #print "tread numbers : %d" % (threadNum)
            url   = results[currtask][0]
            title = results[currtask][1]
            adjunctSize = results[currtask][2]
            task  = downloadThread(url,title,currtask,adjunctSize)
            task.start()
            currtask +=1
            #print "currtask",currtask
            if currtask >= taskNum:
                break
    print "exit main process"

except Exception, e:
        print e
        print "Error: unable to fecth data"
        db.close()

print "Finish"
