# coding: UTF-8

import urllib 
import urllib2 
#import requests  

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
url = 'http://www.cninfo.com.cn//cninfo-new/disclosure/fund_listed/download/1201902743'
name =  "968004 968004 摩根总收益债.pdf"
name = name.decode('UTF-8')
print "downloading with urllib"
urllib.urlretrieve(url, name,cbk)   
 
