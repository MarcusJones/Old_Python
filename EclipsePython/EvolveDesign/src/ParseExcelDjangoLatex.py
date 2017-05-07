'''
Created on Aug 6, 2011

@author: UserXP
'''

#!/usr/bin/env python
#coding=utf-8

import django
from django.template import Template, Context
import csv
import os
import logging.config
from win32com.client import Dispatch
import xlrd

def braced(string):
    return "{" + string + "}"

if __name__ == "__main__":
    

    logging.config.fileConfig('..\\LoggingConfig\\logging.conf')

    logging.info("Start ")
    
    rootPath = r"C:\Freelance\Automated Reporting Dev"
    
    #csvPath = os.path.join(rootPath, "names.csv")
    tableTempalatePath = os.path.join(rootPath, "table_template.tex")
    tableOutputPath = os.path.join(rootPath, "table.tex")
    excelFilePath = os.path.join(rootPath, "namesExcel.xls")
    
    # This line is required for Django configuration
    django.conf.settings.configure()

#    # Open and read CSV file
#    fid = open(csvPath)
#    reader = csv.reader(fid)
#    
    # Open and read template
    with open(tableTempalatePath) as f:
        t = Template(f.read())
   
    # Define context with the table data
#    
#    
#    
#    head = reader.next()
#    
#    print head
#    print reader
#    



    book = xlrd.open_workbook(excelFilePath) #open our xls file, there's lots of extra default options in this call, for logging etc. take a look at the docs
     
    sheet = book.sheets()[0] #book.sheets() returns a list of sheet objects... alternatively...
    
        
    startRow = 1
    endRow = 5
    
    startCol = 1
    endCol = 3
    
    entireTable = []
    for row in range(startRow-1,endRow):
        thisRow = []
        for col in range(startCol-1,endCol):
            thisRow.append(sheet.cell(row,col).value)
            #print sheet.cell(row,col).value, 
            #data.append(sheet.row_values(i)) #drop all the values in the rows into data
        entireTable.append(thisRow)
    
    head = entireTable.pop(0)
    table = entireTable
    caption = "Test caption"
    label = "tab:TestLabel"
    
    c = Context({"head": head, 
                 "table": table, 
                 "caption": braced(caption),
                 "label": braced(label),
                 })
    
    #print c["head"]
    #print c["table"]
    
    #for line in c["table"]:
    #    print line
        
    # Render template
    output = t.render(c)

    #fid.close()

    # Write the output to a file
    with open(tableOutputPath, 'w') as out_f:
        out_f.write(output)
        
    logging.info("Finished")
    #sheet = book.sheet_by_name("sheet1") #we can pull by name
    #sheet = book.sheet_by_index(0) #or by the index it has in excel's sheet collection
    
    #r = sheet.row(0) #returns all the CELLS of row 0,
    #print r
    #c = sheet.col_values(0) #returns all the VALUES of row 0,


def load():    
    logging.debug("Loading variants from {0}".format(inputExcelPath))
               
    # Attach the excel COM object
    
    xl = Dispatch('Excel.Application')
    
    #xl = win32.gencache.EnsureDispatch('Excel.Application')
    
    # Open the input file
    book = xl.Workbooks.Open(inputExcelPath)
    
    # Select the sheet
    sheet = book.Sheets('Variants')      

    xl.Visible = False
    
    variantsList = list()    
    # Scan down
    for row in range(1,1000):
        # Found a variant section row
        if sheet.Cells(row,1).Value != None:
            # Load the general data
            ID = str(sheet.Cells(row,3).Value)
            sourceFileRelPath = str(sheet.Cells(row,4).Value)
            sourceFileRelPath = os.path.normpath(sourceFileRelPath)            
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
                for col in range(3,6):
                    thisChange.append(str(sheet.Cells(row,col).Value))
                changesList.append(thisChange)
                # Now carriage return
                row += 1
                col = 3       
            
            sourceFileAbsPath = os.path.join(inputAbsDirStem,sourceFileRelPath)
            sourceFileAbsPath = os.path.normpath(sourceFileAbsPath)
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

    book.Close(SaveChanges=0) #to avoid prompt

