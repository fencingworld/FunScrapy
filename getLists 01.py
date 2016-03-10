# coding: UTF-8
import sys
import httplib
import urllib
import urllib2
import json
import psycopg2
#import demjson
reload(sys)


sys.setdefaultencoding('utf-8')


headers = {
"Host": "www.cninfo.com.cn",
"Connection":" keep-alive",
"Content-Length":" 257",
"Accept":" application/json, text/javascript, */*; q=0.01",
"Origin":" http://www.cninfo.com.cn",
"X-Requested-With":" XMLHttpRequest",
"User-Agent":" Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36",
"Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
"Referer":" http://www.cninfo.com.cn/cninfo-new/disclosure/fund_listed",
"Accept-Encoding":" gzip, deflate",
"Accept-Language":" zh-CN,zh;q=0.8",
"Cookie":"COLLPCK=361493945; JSESSIONID=0E07A2BCD6B917B480DEF5ED76666906"
} 

fields 	= 	{}



################################

fields['stock'] 	=  ""      
fields['searchkey'] =  ""      
fields['plate'] 	=  ""      
fields['category'] 	=  ""      
fields['trade'] 	=  ""      
fields['column'] 	=  "fund_listed" 
fields['columnTitle'] = "%E5%9F%BA%E9%87%91%E5%85%AC%E5%91%8A"
fields['pageNum'] 	=  133			#max = 133
fields['pageSize'] 	=  30
fields['tabName=latest'] = ""
fields['sortName'] 	=  ""      
fields['sortType'] 	=  ""      
fields['limit'] 	=  ""      
fields['showTitle'] =  ""      
fields['exchange'] 	=  ""      
fields['fundtype'] 	=  ""      
fields['seDate'] 	="%E8%AF%B7%E9%80%89%E6%8B%A9%E6%97%A5%E6%9C%9F"

params = urllib.urlencode(fields) 
print params

###############################################
try:
	pgdb_conn = pg.connect(dbname = 'kevin_test', host = '192.168.230.128', user = 'dyx1024', passwd = '888888')  
except Exception, e:
	print e.args[0]  


###############################################
DIR = "/cninfo-new/disclosure/fund_listed_latest"
hostURL = "www.cninfo.com.cn"

conn = httplib.HTTPConnection(hostURL+":80") 
while (True):
	
	conn.request("POST", DIR, params, headers)  
	response = conn.getresponse()  
	print response.status, response.reason 
	

	if response.status==200:
		break
	if response.status==307:
		head = response.getheaders()
		print head [0][1]

		headers["Cookie"] =head[0][1]
	
data = response.read() 
dataDict = json.loads(data)
#dataList=  dataDict.values()
#urlBase 	= "http://www.cninfo.com.cn/cninfo-new/disclosure/fund_listed/bulletin_detail/true/"
urlDownBase = "http://www.cninfo.com.cn/cninfo-new/disclosure/fund_listed/download/"
dataAncmtList = dataDict["announcements"]
print type (dataAncmtList)
print dataAncmtList[0].items()
print dataAncmtList 
print len(dataAncmtList)
for item in dataAncmtList:
	setCode = item["secCode"]
	secName = item["secName"]
	targetUrl = urlDownBase + item["announcementId"]
	print setCode+ " " +targetUrl+ " " + secName 

#urllib.urlretrieve(url, name,cbk)  
''''
score = json.loads(data.decode('UTF-8'))
print score
print type(score)
'''
conn.close()
