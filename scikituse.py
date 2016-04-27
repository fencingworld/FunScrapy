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
import requests  
import threading
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import cluster, datasets

db = MySQLdb.connect("127.0.0.1","root","root","funscrapy" ,charset='utf8')
cursor = db.cursor()
a_sql = "SELECT sValue FROM financeuse WHERE sYear=2014 AND sKey='营业.*收入'  ORDER BY sCode "
b_sql = "SELECT sValue FROM financeuse WHERE sYear=2014 AND sKey ='总资产'     ORDER BY sCode"
pre  = "null"
myData = []
x=-1
vec=[0]*2
try:
  cursor.execute(a_sql)
  a_results = cursor.fetchall()
except Exception,e:
  print e

try:
  cursor.execute(b_sql)
  b_results = cursor.fetchall()
except Exception,e:
  print e

for i in range(len(a_results)):
  vec=[]
  vec.append(float(a_results[i][0].replace(",","")))
  vec.append(float(b_results[i][0].replace(",","")))
  myData.append(vec)

k_means = cluster.KMeans(n_clusters=8)
k_means.fit(myData) 
sdata=[]
for i in range(len(a_results)):
  lab = k_means.labels_[i]
  aaa  = int(float(a_results[i][0].replace(",",""))/1000000)
  bbb  = int (float(b_results[i][0].replace(",",""))/1000000)
  sdata.append((lab,aaa,bbb))

ssdata = sorted(sdata,key=lambda a:a[0])
for it in ssdata:
  print it
#print(y_iris[::10])
