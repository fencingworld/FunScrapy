#!/usr/bin/python  
# -*- coding:utf8 -*-  

import os 
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from distutils import filelist
fileList = []
path = 'F:/workspace/financeSoup/download/newdir'
files = os.listdir(path) 
for f in files: 
    
    if(os.path.isfile(path + '/' + f)):  
        # 添加文件  
        #fileList.append(f)  
        #print type(f)
        #unicode( f , errors='ignore')
        #f=f.encode('utf8')
        f=path + '/' + f
        nf = f.replace(" ","_")
        os.rename(f,nf)
        print nf


