from win32com.client import Dispatch
import os
 
#file path
file_name = 'D:\\dev\\PyWork\\ExcelWrite\\SensiTest.xls'
 
#The win32com function to open Excel
excel = Dispatch('Excel.Application')
excel.Visible = True #If we want to see it change, it's fun
 
#Open the file we want in Excel
workbook = excel.Workbooks.Open(file_name)
 
#Extract some of the file's components we may need
workBook = excel.ActiveWorkbook
activeSheet = excel.ActiveSheet
sheets = workBook.Sheets
 
#Add another sheet for example
sheets.Add(None, sheets('Sheet3')).Name = 'MySheetx'
 
#Activate the necessary sheet, assuming we know it exists,
#didn't put in the test for that, just verify its exitance in 'sheets'...
sheet = sheets('The_Sheet_I_Need')
sheet.Activate()
 
#Write smth in a Cell
line = 4
col = 5
sheet.Cells(line,col).Value = 99
 
#Read something is just as easy
print sheet.Cells(line,col).Value
 
#The remove doesn't work for me, but I simply save as different file...
#I just put the lines for you to see what I had found...
#if os.path.exists(file_name):
#os.remove(file_name)
workBook.SaveAs('D:\\dev\\PyWork\\ExcelWrite\\SensiTest_modif.xls')#change name
 
#The end...
workBook.Saved = 0 #p.248 Using VBA 5
workBook.Close(SaveChanges=0) #to avoid prompt
excel.Quit()
excel.Visible = 0
#must make Visible=0 before del self.excelapp or EXCEL.EXE remains in memory.
 
del excel