'''
Created on Feb 27, 2011

@author: UserXP
'''
#!/usr/bin/python
import sys
#import time
#import subprocess
from win32com.client import Dispatch
#import os
#import time
#import win32com.client as win32
 
# Load local configuration libraries
localLibrariesPath = "C:\\Scripting\\L Python\\01 Libraries"
#localLibrariesPath = "D:\\AllScripts\\L Python\\01 Libraries"
projectPath = "C:\Doktorat\Phase2"
#projectPath = "D:\Doktorat\Phase2"
sys.path.append(localLibrariesPath) 
#print sys.path

http://snippets.dzone.com/posts/show/2036
http://icodeguru.com/WebServer/Python-Programming-on-Win32/ch09.htm

# Load settings
#http://msdn.microsoft.com/en-us/library/bb157882.aspx
def excelRow(workSheet, rowIndx):
    # Returns the row as a tuple
    #entireRow = workSheet.Range("rowIndx:rowIndx").End
    #print workSheet.Range("A1").End.value
    #workSheet.Range("1:1").End(XlDirection.xlToRight);
    #print workSheet.Range("1:1", workSheet.Range("1:1").End(-4161)).Value
    print workSheet.Range(Cells(1,1))
    #.End(-4161)).Value
    #.Value[0]
    #for singleCell in entireRow:
    #    print singleCell
    
def loadSettings():
    excel           = Dispatch('Excel.Application')
    excel.Visible   = True  #If we want to see it change, it's fun
    settingsExcelBookPath = projectPath + "\\INI\\ini.xls"
    settingsExcelBook = excel.Workbooks.Open(settingsExcelBookPath)
    print "Opened " + settingsExcelBookPath
    settingsSheet = settingsExcelBook.Worksheets(1)
    excelRow(settingsSheet,1)
    #settingsSheet = settingsExcelBook.Worksheet(1)
    #ss = settingsExcelSheet.Workbooks.Add()
    #openpyxl.worksheet
 
    # xl.Visible = True
    # time.sleep(1)
 
    # sh.Cells(1,1).Value = 'Hacking Excel with Python Demo'
 
    # time.sleep(1)
    # for i in range(2,8):
        # sh.Cells(i,1).Value = 'Line %i' % i
        # time.sleep(1)
 
    # ss.Close(False)
    # xl.Application.Quit()
    settingsExcelBook.Close(SaveChanges=0) #to avoid prompt
    #excel.Quit()
    #excel.Visible = 0 
    
loadSettings()
