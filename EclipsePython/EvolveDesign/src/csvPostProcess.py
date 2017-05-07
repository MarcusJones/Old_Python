'''
Created on Jul 21, 2011

@author: UserXP
'''

#from win32com.client import Dispatch
import os
import logging.config

inputExcelPath = os.path.normpath("C:\Freelance\Simulation\ B Cool buildings baseline.csv")
inputExcelPath = os.path.normpath(r"C:\Freelancing\Simulation\RE1 As Designed.csv")
logging.debug("Start {0}".format(inputExcelPath))

import csv

ifile  = open(inputExcelPath, "rb")
reader = csv.reader(ifile)

rownum = 0

#print reader

#f = csv.reader(open('file.csv'))
array = zip(*reader)
ifile.close()

array = array[1:-1]

headerText = [col[0] for col in array]

dataMatrix = [col[1:-1] for col in array]


splitHeaderText =  [text.split(':') for text in headerText]

print len(splitHeaderText)
print len(dataMatrix)

# INit the dict
dictionary = dict()
for headerTextItem in splitHeaderText:
    dictionary[headerTextItem[1]] = 0

#print dictionary

#print zip(array)
#dictionary = dict()
#summedValues = list()
#index = 0
for col in array:
    #pass
    #print list(row)
    #print col[0],
    
    thisHeaderFull = col[0]
    thisHeaderSplit = thisHeaderFull.split(':')[1]
    
    thisSum = sum([float(data) for data in col[1:-1]])
    
    dictionary[thisHeaderSplit] = dictionary[thisHeaderSplit] + thisSum/1000
    
    #for item in row[1:-1]:

#dictionary = dict(zip(headerText, summedValues))
#dictionary = dict(zip(headerText, list()))
for key, value in dictionary.items(): # returns the dictionary as a list of value pairs -- a tuple.
        print "{0:75} {1:20.2f}".format(key, value)

print dictionary      

    #print sum(float(row[1:-1]))
#print [[float(data) for data] in for col in dataMatrix]
#
#print [float(data) for data in [col for col in dataMatrix]]

#print [float(data) for data in [col[1:-1] for col in array]]



#[sum(dataCol) for dataCol in [float(data) for data in row]]

#dictionary = dict(zip(headerText, values))
