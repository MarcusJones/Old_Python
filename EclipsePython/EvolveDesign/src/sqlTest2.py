# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 13:32:16 2011

@author: UserXP
"""

from sqlite3 import *
#from win32com.client import Dispatch
import os
import logging.config

def getVariableVector(curs, variableName, environmentName,):
    curs.execute(
    """
        SELECT Time.TimeIndex, Month, Day, Hour, Minute, VariableValue
        FROM ReportVariableDataDictionary RVDD 
          INNER JOIN ReportVariableData RVD
            ON RVDD.ReportVariableDataDictionaryIndex = RVD.ReportVariableDataDictionaryIndex
          INNER JOIN Time 
            ON RVD.TimeIndex = Time.TimeIndex 
          INNER JOIN EnvironmentPeriods EP
            ON Time.EnvironmentPeriodIndex = EP.EnvironmentPeriodIndex
        WHERE 
           VariableName = "{0}"
           AND
           EnvironmentName = "{1}"
    """.format(variableName, environmentName)
    )
    
    data = curs.fetchall()
    
    return data

def _newStuff():
    inputFile = r"C:\Freelance\00_MyTestProject\SampleSQL\eplusout.sql"
    
    projectDir = os.path.normpath(r"D:\Freelancing\Project Expansion Test Dir")
    
    inputFile = os.path.join(projectDir, "2.0_3.0_0.5_0.5_0.5_0.5_0.5.sql")
    
    conn = connect(inputFile)
    curs = conn.cursor()
#    
#    getVariableVector(curs, variableName, environmentName,)
#    
#    curs.execute(
#    """
#        SELECT Time.TimeIndex, Month, Day, Hour, Minute, VariableValue
#        FROM ReportVariableDataDictionary RVDD 
#          INNER JOIN ReportVariableData RVD
#            ON RVDD.ReportVariableDataDictionaryIndex = RVD.ReportVariableDataDictionaryIndex
#          INNER JOIN Time 
#            ON RVD.TimeIndex = Time.TimeIndex 
#          INNER JOIN EnvironmentPeriods EP
#            ON Time.EnvironmentPeriodIndex = EP.EnvironmentPeriodIndex
#        WHERE 
#           VariableName = "Outdoor Dry Bulb"
#           AND
#           EnvironmentName = "SUMMER"
#    """    
#    )
#    
    variableName = "Outdoor Dry Bulb"
    environmentName = "SUMMER"
    
    data = getVariableVector(curs, variableName, environmentName,)
    
    for line in  data:
        print line

def _workingSQLSnips():
    # THIS WORKS, - Select only TIMES in the SUMMER period
    """
        SELECT *
        FROM Time INNER JOIN ENVIRONMENTPERIODS where EnvironmentName = "SUMMER"
    """

    """
        SELECT *
        FROM Constructions
    """  

    """
        SELECT *
        FROM ReportVariableDataDictionary INNER JOIN ReportVariableData INNER JOIN Time INNER JOIN EnvironementPeriods
    """    

def _oldStuff():
    # Select constructions and save table
    curs.execute("""
        SELECT *
        FROM Constructions
        """)
    
    
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

if __name__ == "__main__":
    logging.config.fileConfig('..\\LoggingConfig\\loggingNofile.conf')
    logging.debug("Started _main".format())


    #_test1()
    _newStuff()

    
    logging.debug("Started _main".format())    