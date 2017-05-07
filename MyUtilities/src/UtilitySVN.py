'''
Created on 2012-09-08

@author: mjones
'''
#===============================================================================
# Set up
#===============================================================================
from __future__ import division    
import logging.config
import os
import commands
from subprocess import Popen, PIPE
svnCommand = "svn status"
from config import *
import re
from utility_excel import ExcelBookRead

def SVNstat(searchDir):
    #print 
    #os.listdir(searchDir)
    #print os.listdir(searchDir)
    fullPaths = [os.path.join(searchDir,direct) for direct in os.listdir(searchDir)]
    fullPathsDirs = [direct for direct in fullPaths
           if os.path.isdir(direct)]
    
    
    for direct in fullPathsDirs:
        #print "                        ", direct
        #print "*** {} ***".format(direct)
        fullCommand = "{} \"{}\"".format(svnCommand, direct)
        #checked = os.system(fullComm and)
        #print "HH", checked
        result =  Popen(fullCommand , stdout=PIPE, shell=True).stdout.read()
        
        #print str(result)
        if result:
            #print re.search("is not a working copy",result)
            if not re.search("is not a working copy",result):
                print "*** {} ***".format(direct)
                print result
        #stream = os.popen(fullCommand)
        #print stream
    
#print re.search("string","test string")



def SVNback(bookPath, backUpPath):
    thisBook = ExcelBookRead(bookPath)
    allData = thisBook.getTable("Sheet1")
    items = [[row[1], backUpPath + row[2] + ".svn"] for row in allData]
    
    count = 0
    for item in items:
        #print count, item
        #count += 1
        fullCommand = "svnadmin dump \"{}\"> \"{}\"".format(item[0],item[1])
        print fullCommand
        raw_input()
        Popen(fullCommand , stdout=PIPE, shell=True).stdout.read()
        
    
        
    
#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print ABSOLUTE_LOGGING_PATH
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())
    
    #for searchDir in SEARCH_DIRS:
    #    print "Checking {} for local changes...".format(searchDir)
    #    SVNstat(searchDir)
    
    
    SVNback("C:\EclipseWorkspace\MyUtilities\SVN Repos.xlsx", "c:\SVN_BACKUP\\")
    
        
    logging.debug("Finished _main".format())    