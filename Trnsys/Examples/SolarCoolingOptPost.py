# -*- coding: utf-8 -*-
"""
Created on Mon Nov 07 20:37:49 2011

@author: UserXP
"""
import os
import scipy.io as sio
import re
import csv

projectDir = os.path.normpath(r"c:\SolarCoolOptSP20")
#
#out
#
#for item in os.listdir(projectDir):
#    os.path.basename(item)
#
#for item in os.walk(projectDir):
#    print item

loadsFiles = list()
[loadsFiles.append(os.path.join(projectDir, name, "OUT", "loads.out")) 
    for name in os.listdir(projectDir) 
    if os.path.isdir(os.path.join(projectDir, name)) ]

temperatureFiles = list()
[temperatureFiles.append(os.path.join(projectDir, name, "OUT", "temperatures.out")) 
    for name in os.listdir(projectDir) 
    if os.path.isdir(os.path.join(projectDir, name)) ]

loadsFileData = list()
for thisFile in loadsFiles:
    # Following slice operator skips 1st row and 1st col
    data = genfromtxt(thisFile)[1:,1:]
    #print sum(data[:,1])
    data = data.astype(float32)
    #print sum(data[:,1])
    loadsFileData.append(data)
    

temperaturesFileData = list()
for thisFile in temperatureFiles:
    # Following slice operator skips 1st row and 1st col
    data = genfromtxt(thisFile)[1:,1:]
    #print sum(data[:,1])
    data = data.astype(float32)
    #print sum(data[:,1])
    data = mean(data,1)    
    temperaturesFileData.append(data)

    
sio.savemat('c:\\SolarCoolSummarySP20.mat', {"loads":loadsFileData,"temperatures":temperaturesFileData})

thisFile = open(projectDir + "\\thisRunList.txt")

while 1:
    line = thisFile.readline()
    if not line:
        break
    pass # do something


testArr = array()

thisFile = open(projectDir + "\\thisRunList.txt")
spamWriter = csv.writer(open('c:\\runList.csv', 'wb'))
for line in thisFile.readlines():
    thisLine = line
    t1 = re.split(r"[)(/w,.\\]", thisLine)
    final = t1[13], t1[25], t1[37]
    spamWriter.writerow(final)
    

thisFile.close()


fromfile('c:\\runList.csv')

>>> import csv
>>> spamWriter = csv.writer(open('eggs.csv', 'wb'), delimiter=' ',
...                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
>>> spamWriter.writerow(['Spam'] * 5 + ['Baked Beans'])
>>> spamWriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
