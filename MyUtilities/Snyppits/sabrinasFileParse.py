'''
Created on 2012-09-07

@author: mjones
'''
import re
from scipy.io import savemat
import numpy as np

filePath = r"C:\Users\mjones\Desktop\LS9105-6313_all.txt"
outPath = r"C:\Users\mjones\Desktop\LS9105-6313_all.m"

fIn = open(filePath,'r')

allLines = fIn.readlines()
#heads = list()
#datas = list()
header = list()
data = list()

frame = list()

for line in allLines:
    line = line.rstrip()
    if re.match('^#',line):
        # HEADER
        items = line.split(":",1)
        header.append(items)
    elif re.match('^$',line):
        print "BREAK"
        mHead = np.array(header,dtype=object)
        mData = np.array(data,dtype=float)
        frame.append((mHead,mData))
        header = list()
        data = list()
    else:
        items = line.split(" ")
        print items
        data.append(items)
        
finalFrames = list()
for thisFrame in frame:
    if len(thisFrame[0]):
        finalFrames.append(thisFrame)


savemat(outPath, mdict={'data': finalFrames})

 