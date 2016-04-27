#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import time
from nt import waitpid
reload(sys)
import numpy as np
import matplotlib.pyplot as plt

N = 5
menMeans = (307181306.75, 7767773.90, 5905384.91, 68698054.36, 674028043.80/5)
menStd =   (2, 3, 4, 1, 2)

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, menMeans, width, color='r', yerr=menStd)

womenMeans = (304448210.68, 22757953.94, 22001225.67, 66779806.41, 626625950.69/5)
womenStd =   (3, 5, 2, 3, 3)
rects2 = ax.bar(ind+width, womenMeans, width, color='y', yerr=womenStd)

# add some
ax.set_ylabel('Value')
ax.set_title('contrast between 2013 and 2014 for 000008')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('G1', 'G2', 'G3', 'G4', 'G5') )

ax.legend( (rects1[0], rects2[0]), ('2013', '2014') )

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

plt.show()
