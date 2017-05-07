'''
Created on Dec 21, 2011

@author: UserXP
'''
import re
import logging.config
import os
from win32com.client import Dispatch

   
if __name__ == "__main__":

    # Load the logging configuration
    
    logging.config.fileConfig('..\\LoggingConfig\\logging.conf')
    
    logging.info("Started IDF test script")

    # The templates    
    #templatesFile = r"C:\Freelance\IDF_Library\Templates.xlsx"
    inputSheetPath = r"C:\Freelance\046_Al_Ain_Tech_Two\Input Data\Testing for Auto Schedules.xlsx"
    schedulesSheet = r"Schedules"
    inputSheetPath = os.path.normpath(inputSheetPath)

   
    logging.debug("Loading schedules from {0}".format(inputSheetPath))
    
    # Attach the excel COM object
    
    xl = Dispatch('Excel.Application')
    
    #xl = win32.gencache.EnsureDispatch('Excel.Application')
    
    # Open the input file
    book = xl.Workbooks.Open(inputSheetPath)
    
    # Select the sheet
    sheet = book.Sheets(schedulesSheet
                        )      

    xl.Visible = False
    
    variantsList = list()    
    # Scan down
    for row in range(1,1000):
        # Found a variant section row
        if sheet.Cells(row,1).Value != None:
            
            dayType = sheet.Cells(row,1).Value
            
            logging.debug("Loading schedules for {0} day type".format(dayType))

            print "For: {0}".format(dayType)
            
            # Keep looking down second column, as long as there is a value
            col = 2
            row += 1
            while sheet.Cells(row,col).Value != None:
                
                #sht.Range(sht.Cells(row1, col1), sht.Cells(row2,
                #col2)).Value
                wholeDataRow = sheet.Range(sheet.Cells(row,col),sheet.Cells(row,col+25)).Value[0]
                
                wholeDataRow = list(wholeDataRow)
                
                ASHRAEspaceName = wholeDataRow.pop(0)
                zoneReference = wholeDataRow.pop(0)
                scheduleList = wholeDataRow
                
                #logging.debug("Loaded schedul for {0} day type".format(dayType))
                
                for hour in range(0,24):
                    print "Until : {0:02d}:00".format(hour+1) 
                    print scheduleList[hour]
                row += 1
    
    """
                # Load the general data
                ID = str(sheet.Cells(row,2).Value)
                #sourceFileRelPath = str(sheet.Cells(row,4).Value)
                #sourceFileRelPath = os.path.normpath(sourceFileRelPath)
                sourceFileAbsPath = str(sheet.Cells(row,4).Value)
                sourceFileAbsPath = os.path.normpath(sourceFileAbsPath)            
                targetDirRelPath = str(sheet.Cells(row,5).Value)
                targetDirRelPath = os.path.normpath(targetDirRelPath)
                # Load the templates
                templateDescriptions = list() 
                # First place cursor at first template 
                row = row + 3
                col = 3
                while sheet.Cells(row,col).Value != None:
                    thisTemplate = list()
                    for col in range(3,5):
                        thisTemplate.append(sheet.Cells(row,col).Value)
                    templateDescriptions.append(thisTemplate)
                    # Now carriage return
                    row += 1
                    col = 3
                    
                # Load the changes
                changesList = list() 
                # First place cursor at first template 
                row = row + 1
                row = row + 1
                col = 3
                while sheet.Cells(row,col).Value != None:
                    thisChange = list()
                    for col in range(3,7):
                        aValue = str(sheet.Cells(row,col).Value)
                        thisChange.append(aValue)
                        #print aValue, "at", col
                    changesList.append(thisChange)
                    # Now carriage return
                    row += 1
                    col = 3       
                
                #sourceFileAbsPath = os.path.join(inputAbsDirStem,sourceFileRelPath)
                #sourceFileAbsPath = os.path.normpath(sourceFileAbsPath)
                targetDirAbsPath = os.path.join(targetAbsDirStem,targetDirRelPath,ID + ".idf")
                targetDirAbsPath = os.path.normpath(targetDirAbsPath)                                
                variantsList.append(Variant(
                                            ID=ID,
                                            #sourceFileRelPath = sourceFileRelPath,
                                            sourceFileAbsPath = sourceFileAbsPath,
                                            #targetDirRelPath=targetDirRelPath,
                                            targetDirAbsPath = targetDirAbsPath,
                                            templateDescriptions=templateDescriptions,
                                            changesList=changesList,
                                            )
                                            )
    """

    book.Close(SaveChanges=0) #to avoid prompt
    
    
    logging.info("Finished")
