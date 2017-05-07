#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""This module does A and B. 
Etc.
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:
from __future__ import division    

from config import *

import logging.config
import unittest

from UtilityInspect import whoami
from UtilityInspect import whoami, whosdaddy
import datetime
from UtilityPathsAndDirs import getNewerFileRevName
from UtilitySQL import sqliteDBWrapper
from Variable import Variable
from DesignSpace import DesignSpace

#===============================================================================
# Code
#===============================================================================

def SQL_TABLE_VARIABLES():
    return """
        CREATE TABLE Variables
        (
        P_Id int NOT NULL,
        Name varchar(50) NOT NULL,
        Ordered BOOLEAN,
        Magnitude INT,
        PRIMARY KEY (P_Id)
        CONSTRAINT UniqueName UNIQUE (Name)
        )
        """


def SQL_TABLE_VARX_VALUES(theDB, variable):
    # -- Create the table
    thisTableName = "Vals_{}".format(variable.name)
    SQL_STRING =  """
        CREATE TABLE {}
        (
        Val_ID INT,
        Value varchar(50) NOT NULL
        )
        """.format(thisTableName)
    theDB.execCommand(SQL_STRING)
    #-- Populate with values
    varNum = 0

    #variable
    varNum = varNum + 1
    #myDB.insertDataRows("Variables", [[varNum, indiv.name, indiv.ordered, len(indiv)]])
    #valueRows = [[None, val,] for val in ]
     
    valueRows = zip(range(len(variable)), variable.vTuple)
    
    #print valueRows
    theDB.insertDataRows(thisTableName, valueRows)
    

        
def SQL_TABLE_GENERATIONS():
    return """
        CREATE TABLE Generations
        (
        Gen_ID INT,
        Individual INT,
        PRIMARY KEY (Gen_ID),
        FOREIGN KEY (Individual) REFERENCES Results(Hash)
        )
        """
        
def SQL_TABLE_RESULTS(dSpace):
    sqlString = """
        CREATE TABLE Results
        (
        Hash INT NOT NULL,
        Start DATETIME,
        Finish DATETIME,"""
        
    variableColsString = str()
    constraintString = str()
    for indiv in dSpace.basisSet:
        variableColsString = variableColsString + """
            Var_{} INT NOT NULL,""".format(indiv.name)
        constraintString = constraintString + """
        CONSTRAINT fk_{0} FOREIGN KEY (Var_{0}) REFERENCES Vals_{0}(Val_Id),""".format(indiv.name,)
        #"""FOREIGN KEY (Var_{0}) REFERENCES Vals_{0}(Val_ID),""".format(indiv.name,)
    
  #FOREIGN KEY(trackartist) REFERENCES artist(artistid)
            
            
    objectiveColString = str()        
    for x in range(dSpace.numObjectives):
        objectiveColString = objectiveColString + """
            Obj_{} REAL NOT NULL,""".format(x)        
            
    completeString = sqlString + variableColsString + objectiveColString + constraintString + "\nPRIMARY KEY (Hash)\n)"
    print completeString    
    return completeString


def addResults(theDB, results):
    assert (type(results[0]) is list)
    theDB.insertDataRows("Results", results)


def createTables(dSpace, fullDBpath):
    fullDBpathREV = getNewerFileRevName(fullDBpath)
    myDB = sqliteDBWrapper(fullDBpathREV)
    
    #--- Variables table
    # | P_Id |  Name  | Ordered | Magnitude |
    myDB.execCommand(SQL_TABLE_VARIABLES())

    #--- Vector table
    # | Val_ID | Value | Variable |
    for variable in dSpace.basisSet:
        SQL_TABLE_VARX_VALUES(myDB,variable)
    
    #--- Results table
    # |  Hash  |           Start            |           Finish           | Var_C1 | Var_C2 | Var_v100 | Var_VarStr |  Obj_0   |
    myDB.execCommand(SQL_TABLE_RESULTS(dSpace))
    
    #--- Generations table
    # | Gen_ID | Individual |
    myDB.execCommand(SQL_TABLE_GENERATIONS())

    
    
    sqlString = """
        SELECT Variables.Name, VariableVals.Value
        FROM Variables
        INNER JOIN VariableVals
        ON Variables.P_Id=VariableVals.Variable
        """
    
    sqlString = """
        SELECT Results.Obj_0, VariableVals.Value
        FROM Results
        INNER JOIN VariableVals
        ON Results.Var_C1=VariableVals.Val_ID
        """
        
    #variableValuesRows = myDB.execCommand(sqlString)
    
    #for item in variableValuesRows:
    #    print item
    return myDB
#===============================================================================
# Unit testing
#===============================================================================

class testDataBase(unittest.TestCase):
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        
        myLogger.setLevel("CRITICAL")
        
        
        basisVariables = [
                          Variable("C1",50),
                        Variable.ordered("C2",3.14),
                        Variable.ordered('v100',(1,2,3,4)),
                        Variable.unordered('VarStr',["Blue","Red","Green"]),
                        ]
        
        thisDspace = DesignSpace(basisVariables)
        self.D1 = thisDspace 
        
        myLogger.setLevel("DEBUG")
        
    def test010_(self):
        theDB = createTables(self.D1, 'C:\TestSQL\DSpaceTest.sql')
    
        

        addResults(theDB, [
                       [334235, datetime.datetime.now(), datetime.datetime.now(), "SSES", 4, 4, 5, 33.45666],
                       [-334236, datetime.datetime.now(), datetime.datetime.now(), 3, 4, 4, 5, 33.45666],
                       ])
    
        
        testGens = [[0 ,334235],
                    [0 ,334235]
                    ]
    
        theDB.getAllPrintedTables()
        
        
        theDB.printAllSchemas()

#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print ABSOLUTE_LOGGING_PATH
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())
    
    #print FREELANCE_DIR
    
    unittest.main()
        
    logging.debug("Finished _main".format())
    