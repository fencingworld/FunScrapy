# coding: UTF-8
import sys
import httplib
import urllib
import urllib2
import json

#import psycopg2
import MySQLdb
#import demjson
reload(sys)

typeTup = (["fund","最新"],
	["fund_listed","年度报告"],
	["fund_sse","半年度报告"],
	["fund_other","季度报告"]
	)
sys.setdefaultencoding('utf-8')

def saveUrlToDB(idxtype):

	print idxtype[1].encode('utf-8')
	targetDownloadBaseUrl = \
		"http://www.cninfo.com.cn/cninfo-new/disclosure/"+idxtype[0]+"/download/"
	print targetDownloadBaseUrl
	#return
	headers = {
	"Host": "www.cninfo.com.cn",
	"Connection":" keep-alive",
	#"Content-Length":" 257",
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
	fields['stock'] 	=  ""      
	fields['searchkey'] =  ""      
	fields['plate'] 	=  ""      
	fields['category'] 	=  ""      
	fields['trade'] 	=  ""      
	fields['column'] 	=  idxtype[0] ################################
	fields['columnTitle'] 		= "%E5%9F%BA%E9%87%91%E5%85%AC%E5%91%8A"
	fields['pageNum'] 	=  1	#max = 133
	fields['pageSize'] 	=  30
	fields['tabName=latest']	= ""
	fields['sortName'] 	=  ""      
	fields['sortType'] 	=  ""      
	fields['limit'] 	=  ""      
	fields['showTitle'] =  ""      
	fields['exchange'] 	=  ""      
	fields['fundtype'] 	=  ""      
	fields['seDate'] 	=  "%E8%AF%B7%E9%80%89%E6%8B%A9%E6%97%A5%E6%9C%9F"

	params = urllib.urlencode(fields) 
	#print params


	# 打开数据库连接
	db = MySQLdb.connect("127.0.0.1","root","root","funscrapy" ,charset='utf8')

	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()

	# 使用execute方法执行SQL语句
	cursor.execute("SELECT VERSION()")

	# 使用 fetchone() 方法获取一条数据库。
	data = cursor.fetchone()

	print "Database version : %s " % data

	# 关闭数据库连接


	countInsert 	= 0
	countRollBack 	= 0

	DIR = "/cninfo-new/disclosure/"+idxtype[0]# dir 1最新################################
	hostURL = "www.cninfo.com.cn"

	conn = httplib.HTTPConnection(hostURL+":80") 

	idx =	0
	while (True):
		idx = idx + 1
		fields['pageNum'] = idx
		print "get page : %d" % idx
		params = urllib.urlencode(fields) 
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
		conn.close()
		dataDict = json.loads(data)
		#dataList=  dataDict.values()
		#urlBase 	= "http://www.cninfo.com.cn/cninfo-new/disclosure/fund_listed/bulletin_detail/true/"
		targetDownloadBaseUrl = \
		"http://www.cninfo.com.cn/cninfo-new/disclosure/"+idxtype[0]+"/download/"
		targetName	= ""
		dataAncmtList = dataDict["announcements"]
		#print type (dataAncmtList)
		#print dataAncmtList[0].items()
		#print dataAncmtList 
		#print len(dataAncmtList)
		#ing =  "My name is %s and weight is %d kg!" % ('Zara', 21) 
		#print ing
		for item in dataAncmtList:
			# 使用cursor()方法获取操作游标 
		#	print "################################"
			#print item
			#cursor = db.cursor()
			# SQL 插入语句
			targetUrl 	= targetDownloadBaseUrl + item["announcementId"]
			targetTitle =  item["secCode"] +" "+ item["secName"] +" "+ item["announcementTitle"]

			sql = """
				INSERT INTO `funscrapy`.`announcements` (
				`adjunctSize`, `adjunctType`, `adjunctUrl`, 
				`announcementContent`, `announcementId`, `announcementTime`, 
				`announcementTitle`, `announcementType`, `announcementTypeName`, 
				`associateAnnouncement`, `batchNum`, `columnId`,
				`id`, `important`, `orgId`, 
				`pageColumn`, `secCode`, `secName`, 
				`storageTime`,`targetUrl`, `targetTitle`) 
				VALUES (
				'%s', '%s', '%s',
				%s, '%s', '%s',
				'%s', '%s', %s,
				%s, '%s', '%s', 
				%s, '%s', '%s', 
				'%s', '%s', '%s',
				'%s', '%s','%s')  
				""" % ( \
				item["adjunctSize"] , item["adjunctType"] , item["adjunctUrl"] , \
				"NULL"   , item["announcementId"] , item["announcementTime"] ,\
				item["announcementTitle"] , item["announcementType"] , "NULL" , \
				"NULL" , item["batchNum"] , item["columnId"] , \
				"NULL", 0, item["orgId"] , \
				item["pageColumn"] , item["secCode"] , item["secName"] , \
				item["storageTime"],targetUrl,targetTitle)
		#	print "##########==================="
			sql1 = """
				INSERT INTO `funscrapy`.`announcements` (
				`announcementId`, `secCode`, `secName`) 
				VALUES ('%s','%s','%s')  
				""" % ( item["announcementId"] , item["secCode"],item["secName"] )
			#print sql

			try:
		   # 执行sql语句
		   		cursor.execute(sql)
		   # 提交到数据库执行
		   		db.commit()
		   		
		   		countInsert = countInsert + 1
			except Exception, e:
		   # Rollback in case there is any error
		   		#print "nimeiaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
		   		#print e
		   		db.rollback()
		   		countRollBack = countRollBack  + 1
		print "[countInsert] = %d [countRollBack] = %d " % (countInsert,countRollBack)
		if len(dataAncmtList) < 30 :
			break
	"""
		setCode = item["secCode"]
		secName = item["secName"]
		targetUrl = urlDownBase + item["announcementId"]
		print setCode+ " " +targetUrl+ " " + secName 
	"""
	#urllib.urlretrieve(url, name,cbk)  
	''''
	score = json.loads(data.decode('UTF-8'))
	print score
	print type(score)
	'''

	db.close()
	return #saveUrlToDB
h=0
for typeIdx in typeTup:
	saveUrlToDB(typeIdx,h)
	h = h+1
