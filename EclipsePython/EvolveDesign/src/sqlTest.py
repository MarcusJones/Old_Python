# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 13:32:16 2011

@author: UserXP
"""

from sqlite3 import *
from win32com.client import Dispatch
import os


#h = Dispatch('matlab.application')
#h.Execute ("plot([0 18], [7 23])")
#h.Execute ("1+1")
#u'\nans =\n\n     2\n\n'


inputFile = r"C:\Freelance\00_MyTestProject\SampleSQL\eplusout.sql"


projectDir = os.path.normpath(r"D:\Freelancing\Project Expansion Test Dir")

inputFile = os.path.join(projectDir, "2.0_3.0_0.5_0.5_0.5_0.5_0.5.sql")



#outputExcelPath = r"C:\Freelance\00_MyTestProject\SamplePostprocess\test.xlsx"
#
## Open the input file
#book = xl.Workbooks.Open(outputExcelPath)
#
## Select the sheet
#sheet = book.Sheets(1)
#
#sheet.Cells(row,1).Value != None:
#book.Close(False)
#xl.Application.Quit()

conn = connect(inputFile)
curs = conn.cursor()


# Select constructions and save table
curs.execute("""
    SELECT *
    FROM Constructions
    """)
tabConstructions = curs.fetchall()
curs.execute("PRAGMA table_info('Constructions')")
colheadsConstructions = curs.fetchall()
# The materials table header
curs.execute("PRAGMA table_info('Materials')")
colheadsMaterials = curs.fetchall()
colheadsMaterials = [colDescriptions[1] for colDescriptions in colheadsMaterials]

for row in tabConstructions:
    thisIndex = row[0]
    thisConstuctionsName = row[1]
    #
    #    rows = curs.execute("""
    #        SELECT Constructions.Name, ConstructionLayers.LayerIndex, Materials.Name, 
    #        Materials.Thickness
    #        FROM Constructions, ConstructionLayers, Materials
    #        WHERE
    #        Constructions.ConstructionIndex=ConstructionLayers.ConstructionIndex
    #        AND ConstructionLayers.MaterialIndex=Materials.MaterialIndex
    #        AND ConstructionLayers.ConstructionIndex = ?""", [thisIndex])
    #
    # Select the material table which matches the construction
    # Statement below must have bindings on same line in spyder!!
    rows = curs.execute("""
    SELECT Materials.*
    FROM Constructions, ConstructionLayers, Materials
    WHERE
    Constructions.ConstructionIndex=ConstructionLayers.ConstructionIndex
    AND ConstructionLayers.MaterialIndex=Materials.MaterialIndex
    AND ConstructionLayers.ConstructionIndex = ?""", [thisIndex])
    #
    print ""
    print "Construction breakdown for {0}".format(thisConstuctionsName)
    headStr = ''.join([item + ", " for item in colheadsMaterials])
    print headStr
    for row in rows:
        for item in row:
            print item, ", ",
        #
        print ""


rows = curs.execute("""CREATE VIEW ReportVariableWithTime AS SELECT ReportVariableData.*, Time.*, ReportVariableDataDictionary.*, ReportVariableExtendedData.* FROM ReportVariableData LEFT OUTER JOIN ReportVariableExtendedData INNER JOIN Time INNER JOIN ReportVariableDataDictionary ON (ReportVariableData.ReportVariableExtendedDataIndex = ReportVariableExtendedData.ReportVariableExtendedDataIndex) AND (ReportVariableData.TimeIndex = Time.TimeIndex) AND (ReportVariableDataDictionary.ReportVariableDataDictionaryIndex = ReportVariableData.ReportVariableDataDictionaryIndex)""")

rows = curs.execute(
"""
SELECT * 
FROM
ReportVariableWithTime
"""
)

cnt = 0
for row in rows:
    print row, ","
    cnt += 1

curs.execute("PRAGMA table_info('ReportVariableWithTime')")
header = curs.fetchall()

for head in header:
    print head[1]

 
 
 
 
 
 
 
 
 
 
 
 
 
 
#    tabConstructionSummary = curs.fetchall()
#    print "Construction: {0}".format(row[1])
#     tabConstructionSummary
#    print ""
#















curs.execute("""
    SELECT Constructions.Name, ConstructionLayers.LayerIndex, Materials.Name, 
    Materials.Thickness
    FROM Constructions, ConstructionLayers, Materials
    WHERE
    Constructions.ConstructionIndex=ConstructionLayers.ConstructionIndex
    AND ConstructionLayers.MaterialIndex=Materials.MaterialIndex
    AND ConstructionLayers.ConstructionIndex = 2
    """)
tabConstructionSummary = curs.fetchall()

for row in tabConstructionSummary:
    print row
    
    

curs.execute("""
SELECT *
 FROM sys.tables
""")    

curs.execute("""
select * from sqlite_master WHERE type = \'table\' 
""")    
print curs.fetchall()


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
'''
Created on Jun 5, 2011

@author: UserXP
'''

from sqlite3 import *

inputFile = r"C:\Freelance\00_MyTestProject\SampleSQL\eplusout.sql"

conn = connect(inputFile)
curs = conn.cursor()

#print curs.execute('select * from sqlite_master')

#print curs.fetchall()

tableRows = curs.execute('select * from sqlite_master WHERE type = \'table\' ')

for row in tableRows:
    print row[1],
print
    
curs.execute('select distinct * from Constructions')

tabConstructions  = curs.fetchall()

for row in tabConstructions:
    
    p_id = str(row[0])
    print row
    curs.execute('select * from ConstructionLayers where ConstructionIndex = ?', p_id)
    tabMaterials = curs.fetchall()
    print tabMaterials

curs.execute("""
SELECT Constructions.Name, ConstructionLayers.MaterialIndex
FROM Constructions
INNER JOIN ConstructionLayers
ON Constructions.ConstructionIndex=ConstructionLayers.ConstructionIndex
""")
tabConstructionSummary = curs.fetchall()
for row in tabConstructionSummary:
    print row

curs.execute("""
SELECT Constructions.Name, ConstructionLayers.MaterialIndex
FROM Constructions
INNER JOIN ConstructionLayers
ON Constructions.ConstructionIndex=ConstructionLayers.ConstructionIndex
""")
tabConstructionSummary = curs.fetchall()
for row in tabConstructionSummary:
    print row

"""
 SELECT lastname, firstname, tag, open_weekends
 FROM drivers, vehicles, locations
 WHERE drivers.location = vehicles.location
 AND vehicles.location = locations.location
 AND locations.open_weekends = 'Yes'
"""
#    for item in items:
#        
#        print item, ",",
#    print 
#'select * from sqlite_master'

#curs.execute('select * from ReportVariableData LIMIT 20')
#
#count = 0
#for items in curs.fetchall():
#    count += 1 
#    for item in items:
#        print item, ",",
#    print 
#    if count > 20:
#        break    