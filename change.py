#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import urllib 
import urllib2 
import random
import MySQLdb
import requests  
import os
import time
from nt import waitpid
reload(sys)
sys.setdefaultencoding('utf-8')
from distutils import filelist
fileList = []
path = "F:\\workspace\\financeSoup\\download\\newdir1\\"
print path
EXE = "F:\\workspace\\financeSoup\\change\\pdf2htmlEX\\pdf2htmlEX.exe"
print EXE
OUTPath = "F:\\workspace\\financeSoup\\change"
files = os.listdir(path) 
for f in files: 
    
    if(os.path.isfile(path + '/' + f)):  

        cmd =  EXE +" --dest-dir "+OUTPath+" "+path +f
        print cmd
        os.system(cmd)
