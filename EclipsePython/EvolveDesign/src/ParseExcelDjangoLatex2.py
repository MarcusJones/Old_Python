'''
Created on Sep 24, 2011

@author: UserXP
'''

#!/usr/bin/env python
#coding=utf-8

import django
from django.template import Template, Context
#import csv
import os
import logging.config
#from win32com.client import Dispatch
import xlrd
from decimal import Decimal

# Functions
def braced(string):
    # Braces a string, utility for Django template
    return "{" + string + "}"

def searchTable(searchString,wholeTable):
    # Search a table for searchString, return locations
    indexList = []
    for row in range(len(wholeTable)):
        for col in range(len(wholeTable[row])):
            if searchString == wholeTable[row][col].value:
                #print "Found"
                indexList.append([row,col])
    return indexList

def getHeaderRowNums(wholeTable):
    locations = searchTable("Header:",wholeTable)
    return [location[0] for location in locations]

def getRowNums(wholeTable):
    locations = searchTable("Row:",wholeTable)
    return [location[0] for location in locations]

def getColNums(wholeTable):
    locations = searchTable("Column:",wholeTable)
    return [location[1] for location in locations]

def getColWidths(wholeTable):
    locations = searchTable("Column:",wholeTable)
    #print locations
    #print [[location[0] + 1,location[1]] for location in locations]
    widthsList = [wholeTable[location[0] + 1][location[1]].value for location in locations]
    #widthFactors = [Decimal("{0:.2f}".format(width / sum(widthsList))) for width in widthsList]
    widthFactors = [(width / sum(widthsList)) for width in widthsList]
    return widthFactors

def getTableLabel(wholeTable):
    locations = searchTable("Table:",wholeTable)
    row = locations[0][0]
    col = locations[0][1] + 1 
    return wholeTable[row][col].value

def getTableCaption(wholeTable):
    locations = searchTable("Caption:",wholeTable)
    row = locations[0][0]
    col = locations[0][1] + 1 
    return wholeTable[row][col].value

if __name__ == "__main__":
    logging.config.fileConfig('..\\LoggingConfig\\logging.conf')
    
    logging.info("Starting")

    # File paths
    rootPath = r"C:\Freelance\Automated Reporting Dev"
    excelFilePath = os.path.join(rootPath, "namesExcel.xls")
    excelFilePath = r"C:\Freelance\062_RasGhurabMos\Input Data\Input Data Ras Ghurab Mosque rev. 04.xls"
    tableTempalatePath = os.path.join(rootPath, "table_template4.tex")
    tableOutputPath = os.path.join(rootPath, "table.tex")
    
    # This line is required for Django configuration
    django.conf.settings.configure()
    
    # Open and read template
    with open(tableTempalatePath) as f:
        t = Template(f.read())
    
    logging.debug("Loaded template from {0}".format(tableTempalatePath))

    # Open and read excel file
    book = xlrd.open_workbook(excelFilePath) #open our xls file, there's lots of extra default options in this call, for logging etc. take a look at the docs
    logging.debug("Opening excel file {0}".format(excelFilePath))

    sheet = book.sheets()[1] #book.sheets() returns a list of sheet objects... alternatively...
    
    logging.debug("Opening excel sheet {0}".format(sheet.name))
    
    # Read in the table
    wholeTable = []
    for rowNum in range(sheet.nrows):
        wholeTable.append(sheet.row(rowNum))
    
    logging.debug("Read in a table over {0} rows from {1}".format(rowNum,sheet.name))
    
    # Get table info
    
    caption = getTableCaption(wholeTable)
    logging.debug("Table caption: '{0}'".format(caption))

    label = getTableLabel(wholeTable)
    logging.debug("Table label: '{0}'".format(label))

    tableRowNums = getRowNums(wholeTable)
    tableColNums = getColNums(wholeTable)
    tableHeadNums = getHeaderRowNums(wholeTable)
    
    table = []
    for rowNum in tableRowNums:
        tableRow = []
        for colNum in tableColNums:
            tableRow.append(wholeTable[rowNum][colNum].value)
        table.append(tableRow)
    
    logging.debug("Table data: {0} rows by {1} columns".format(len(table),len(table[0])))
    
    header = []
    for rowNum in tableHeadNums:
        tableRow = []
        for colNum in tableColNums:
            tableRow.append(wholeTable[rowNum][colNum].value)
        header.append(tableRow)

    widthFactors = getColWidths(wholeTable)
    
    roundedWidthFactors = ["p{{{0:.2f}\\textwidth}}".format(widthFactor) for widthFactor in widthFactors]
    #bracketedWidthFactors = ["p{{0}}".format(wf) for wf in roundedWidthFactors]
    #print bracketedWidthFactors
    columnSpecifier = " ".join(roundedWidthFactors)
    
    logging.debug("Table header: {0} rows by {1} columns".format(len(header),len(header[0])))

    
    c = Context({"head": header, 
                 "table": table, 
                 "caption": braced(caption),
                 "label": braced(label),
                 "columnDefinition": columnSpecifier,
                 #"columnDefinition": "X"*len(tableColNums),
                 "tableWidth":" \\textwidth",
                 })

    # Render template
    output = t.render(c)

    # Write the output to a file
    with open(tableOutputPath, 'w') as out_f:
        out_f.write(output)
        
    logging.debug("Table rendered to: {0} ".format(tableOutputPath))
    
    logging.info("Finished")
    
    
    
    
    
    """
    print wholeTable
    
    sheet.nrows
    
    wholeTable[8][0]
    
    row = 1
    col = 1
    searchString = "Row:"
    searchTable("Row:",wholeTable)
    
    
    
    
    
    
    
    
    
    
    sheet.row(0)
    
    sheet.nrows
    
    dir(sheet)
    
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
    """
    
    
    
    
    
    
    
    
    
    
    
    

