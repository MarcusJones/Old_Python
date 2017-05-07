'''
Created on Jun 4, 2011

@author: UserXP
'''
#!/usr/bin/env python
#coding=utf-8

import django
from django.template import Template, Context
import csv
#import pywin32

import time
import win32com.client as win32

import os 
import sys

def getCurrPath():
    
    return os.path.dirname(__file__)
    #return os.path.dirname(os.path.abspath(sys.argv[0]))
 
def other():
    # This line is required for Django configuration
    django.conf.settings.configure()

    # Open and read CSV file
    fid = open("..\\Reporting\\TestInputTable.csv")
    reader = csv.reader(fid)
   
    # Open and read template
    with open("..\\Reporting\\TestTemplate.tex") as f:
        t = Template(f.read())
   
    # Define context with the table data
    head = reader.next()
    c = Context({"head": head, "table": reader})

    # Render template
    output = t.render(c)

    fid.close()

    # Write the output to a file
    with open("..\\Reporting\\TestOutput.tex", 'w') as out_f:
        out_f.write(output)

def excel():
    """"""
    reportProcessDir = "C:\\Freelance\\045_PremierInn\\Reports\\Process"
    texOutDir = "C:\\Freelance\\045_PremierInn\\Reports\\Include\\"
    aliasOutFile = texOutDir + "alias.tex"
    
        # This line is required for Django configuration
    django.conf.settings.configure()
    # Open and read template
    with open("..\\Reporting\\AliasTemplate.tex") as f:
        aliasTemplateFile = Template(f.read())
    
 
    
    #print os.path.dirname(__file__)
    inputXlsx = reportProcessDir + "\\Aliases.xlsx"
    print inputXlsx
    
    xl = win32.gencache.EnsureDispatch('Excel.Application')
    
    book = xl.Workbooks.Open(inputXlsx)    
    sheet = book.ActiveSheet
 
    xl.Visible = False
    #time.sleep(1)
 
    numberAliases = int(sheet.Cells(1,2))
    #print numberAliases
    #print int(numberAliases)
    #print numberAliases + 5
    #sheet.Cells(1,1).Value = 'Hacking Excel with Python Demo'
 
    #time.sleep(1)
    #aliasNameList = []
    #aliasTextList = []
    aliasList = []
    for i in range(3,3+numberAliases):
        #aliasNameList.append(sheet.Cells(i,1).Value,) 
        #aliasTextList.append(sheet.Cells(i,2).Value)
        aliasList.append([sheet.Cells(i,1).Value,sheet.Cells(i,2).Value])
        #print aliasNameList
        #print aliasTextList
        #print sheet.Cells(i,1).Value
        #print sheet.Cells(i,2).Value
        #sheet.Cells(i,1).Value = 'Line %i' % i
        #time.sleep(1)
    #book.SaveAs(outputXlsx)
 
    book.Close(False)
    xl.Application.Quit()
    
    print aliasList
    
    c = Context({"aliasList": aliasList})

    # Render template
    output = aliasTemplateFile.render(c)


    # Write the output to a file
    with open(aliasOutFile, 'w') as out_f:
        out_f.write(output)    
    
    print "Wrote", aliasOutFile
    
    #aliasTemplateFile.close()      
 
if __name__ == "__main__":
    excel()



