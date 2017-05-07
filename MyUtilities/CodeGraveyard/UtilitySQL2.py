
from __future__ import division    
'''
Created on 2012-12-10

@author: mjones
'''



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

from config import *

import logging.config
import unittest

from UtilityInspect import whoami
from UtilityInspect import whoami, whosdaddy

import sqlite3
from UtilityPrintTable import PrettyTable
#===============================================================================
# Code
#===============================================================================

#===============================================================================
# Unit testing
#===============================================================================



class sqliteDBWrapper(object):
    def __init__(self,fullPath):
        self.fullPath = fullPath
        self.conn = sqlite3.connect(fullPath)
        
        self.setFKsupport()
        logging.debug("Database: {}".format(self.fullPath))
        
        
          
#   def openDB(self):
#       self.connection = 
#       cur = self.connection.cursor()

    def getVersion(self):
        with self.conn:
            cur = self.conn.cursor()
            
            cur.execute('SELECT SQLITE_VERSION()')
            return cur.fetchone()
        
    def getFKsupport(self):
        with self.conn:
            cur = self.conn.cursor()
            
            return "{}".format( cur.execute("PRAGMA foreign_keys").fetchone()[0])
    
    
    def setFKsupport(self):
        with self.conn:
            cur = self.conn.cursor()
            
            rows = cur.execute('PRAGMA foreign_keys=ON')
            print rows
            for row in rows:
                print row            
        logging.debug("FOREIGN KEYS ON".format())

    def createTable(self, tableName ):
        with self.conn:
            cur = self.conn.cursor()
                    
            cmd = "CREATE TABLE {}({} {})".format(tableName, "P_id", "INT")
            cur.execute(cmd )
            logging.debug("Created table {} in {}".format(tableName, self.fullPath))

    def getTableNames(self,):
        with self.conn:
            cur = self.conn.cursor()
                    
            cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
            return cur.fetchall()
        
    def addColumn(self, tableName, colName, colType):
        with self.conn:
            cur = self.conn.cursor()
                    
            cmd = "ALTER TABLE {} ADD {} {}".format(tableName, colName, colType)
            cur.execute(cmd)
        
    def getColumnInfo(self, tableName):
        with self.conn:
            cur = self.conn.cursor()     
            cur.execute("PRAGMA table_info( {} )".format(tableName))
            return cur.fetchall()
    
    def getAllSchemas(self):
        
        allTableNames = self.getTableNames()
        allInfo = list()
        for name in allTableNames:
            
            allInfo.append(
                           (name[0], self.getColumnInfo(name[0]), self.getConstraints(name[0])
                            )
                           )
        return allInfo
    
    def printAllSchemas(self):
        for table in self.getAllSchemas():
            print table[0]
            for col in table[1]:
                print "\t", col
            for constraint in table[2]:
                print "\t\t", constraint                 
    
    def getColumnNames(self, tableName):
        return [col[1] for col in self.getColumnInfo(tableName)]
    
    def getPrintedTable(self,tableName):
        #print 
        
        myTable = PrettyTable(self.getColumnNames(tableName))
        with self.conn:    
            
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM {}".format(tableName))
        
            rows = cur.fetchall()

            for row in rows:
                #print row
                myTable.add_row(row)
                
        print myTable
                
                
    def getAllPrintedTables(self):
        for tableName in self.getTableNames():
            print "***", tableName[0], "***"
            self.getPrintedTable(tableName[0])
               
                
    def dropTable(self, tableName):
        with self.conn:
            cur = self.conn.cursor()
            cmd = "DROP TABLE {}".format(tableName)
            #print cmd
            cur.execute(cmd)
            logging.debug("Dropped table {} from {}".format(tableName, self.fullPath))

    def dropAllTables(self, dbName):
        with self.conn:
            cur = self.conn.cursor()
            cmd = "DROP DATABASE {}".format(dbName)
            print cmd
            cur.execute(cmd)
            logging.debug("Dropped all tables from {}".format(dbName))

            
            
    def execCommand(self, cmd):
        with self.conn:
            cur = self.conn.cursor()
            #print cmd
            result = cur.execute(cmd)
            theCmd = cmd.splitlines()
            theCmd = [string.strip() for string in theCmd]
            logging.debug("Executed long command; {}".format(" ".join(theCmd)))
            #logging.debug("Dropped table {} from {}".format(tableName, self.fullPath))
        return result
    
#    def execCommandReturnAll(self, cmd):
#        with self.conn:
#            cur = self.conn.cursor()
#            #print cmd
#            cur.execute(cmd)
#            theCmd = cmd.splitlines()
#            theCmd = [string.strip() for string in theCmd]
#            logging.debug("Executed long command; {}".format(" ".join(theCmd)))
#            #logging.debug("Dropped table {} from {}".format(tableName, self.fullPath))
#            
            
    def getConstraints(self,tableName):
        with self.conn:
            cur = self.conn.cursor()
            cmd = "select sql from sqlite_master where type='table' and name='{}'".format(tableName)    
            cur.execute(cmd)
            schema = cur.fetchone()
        #print schema
        for line in schema[0].splitlines():
            pass
            #print line.find("CONSTRAINT")
        #lines = schema[0].splitlines().tolower()
        entries = [ tmp.strip() for tmp in schema[0].splitlines() if tmp.lower().find("constraint")>=0 or tmp.lower().find("unique")>=0 ]
        return entries
    
    def insertDataRowsNoString(self, tableName, dataRows):
        with self.conn:
            cur = self.conn.cursor()
            for row in dataRows: 
                
                #print ",".join(str(x) for x in row)
                #print
                #print
                #row = (str(x) for x in row)
                #row = ("'" + x + "'" for x in row)
                cmd = """
                INSERT INTO {}
                VALUES ({})
                """.format(tableName, ",".join(row))
                #print cmd
                #print cmd
                cur.execute(cmd)
    
    def insertDataRows(self, tableName, dataRows):
        with self.conn:
            cur = self.conn.cursor()
            for row in dataRows: 
                
                #print ",".join(str(x) for x in row)
                #print
                #print
                #
                #row = (str(x) for x in row if x != None)
                if None in row:
                    #print "YES"
                    row[row.index(None)] = "NULL"
                    
                row = [str(x) for x in row]
                #row = ( )
                
                newRow = list()
                for item in row:
                    if item != "NULL":
                        #print item
                        item = "'" + item + "'"
                    newRow.append(item)
                         
                cmd = """
                INSERT INTO {}
                VALUES ({})
                """.format(tableName, ",".join(newRow))
                #print cmd
                #print cmd
                cur.execute(cmd)
        logging.debug("Inserted {} rows into {}".format(len(dataRows), tableName, ))

@unittest.skip("")
class allTests(unittest.TestCase):
    
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        #self.connection = sqlite3.connect('C:\TestSQL\myTest.db')
        self.DB = sqliteDBWrapper('C:\TestSQL\myTest.db')
    def test010_ClearDB(self):
        print "**** TEST {} ****".format(whoami())
        allTableNames = self.DB.getTableNames()
        for name in allTableNames:
            #print name
            self.DB.dropTable(name[0])
            
            
    def test020_createSomeData(self):
        print "**** TEST {} ****".format(whoami())
        
        self.DB.createTable("Individuals")
        print self.DB.getColumnInfo("Individuals")
        self.DB.insertDataRows("Individuals", [[0]])
        
        #print User
        ##print User.__table__ 
        #print User.__mapper__ 
        #ed_user = User('ed', 'Ed Jones', 'edspassword')
        #print ed_user
    
    
    
    def test030_execSimple(self):
        print "**** TEST {} ****".format(whoami())
        cmdSimple = """
        CREATE TABLE Persons
        (
        P_Id int NOT NULL,
        LastName varchar(255) NOT NULL,
        FirstName varchar(255),
        Address varchar(255),
        City varchar(255),
        PRIMARY KEY (P_Id)
        )
        """

        simpleData = (
                    
            (1,     "Hansen   ","  Ola    " ,"Timoteivn 10  " , 44  ),
            ("2",     "Svendson ","    Tove " ,"   Borgvn 23  " , "  Sandnes    "  ),
            ("3",     "Pettersen","     Kari" ,"    Storgt 20 " , "   Stavanger "  ),
            ("4",     "Nilsen   ","  Johan  " ,"  Bakken 2    " , "Stavanger    "  ) ,               
                                  )
                       
                       
                      
        cmdCompoundPK = """
        CREATE TABLE Persons2
        (
        P_Id int NOT NULL,
        LastName varchar(255) NOT NULL,
        FirstName varchar(255),
        Address varchar(255),
        City varchar(255),
        CONSTRAINT pk_PersonID PRIMARY KEY (P_Id,LastName)
        )
        """
        self.DB.execCommand(cmdSimple)
        self.DB.execCommand(cmdCompoundPK)
        
        self.DB.insertDataRows("Persons", simpleData)
        self.DB.insertDataRows("Persons2", simpleData)
    
    def test090_printSchemas(self):
        self.DB.printAllSchemas()
    
    def test100_printTable(self):
        self.DB.getPrintedTable("Persons")
        self.DB.getPrintedTable("Persons2")
        #print self.DB.getConstraints("Persons2")

class FK_Test(unittest.TestCase):
    
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        #self.connection = sqlite3.connect('C:\TestSQL\myTest.db')
        self.DB = sqliteDBWrapper('C:\TestSQL\myTest.db')

        self.DB.dropAllTables("myTest.sql")
        
        print self.DB.getVersion()
        print self.DB.getFKsupport()

    def test1(self):
        self.DB.dropAllTables()
        SQL_STR = """CREATE TABLE Persons
(
P_Id int NOT NULL,
LastName varchar(255) NOT NULL,
FirstName varchar(255),
Address varchar(255),
City varchar(255),
PRIMARY KEY (P_Id)
)"""
        self.DB.execCommand(SQL_STR)

        
        
        SQL_STR = """CREATE TABLE Orders
(
O_Id int NOT NULL,
OrderNo int NOT NULL,
P_Id int,
PRIMARY KEY (O_Id),
FOREIGN KEY (P_Id) REFERENCES Persons(P_Id)
)"""
        self.DB.execCommand(SQL_STR)

        simpleData = (
                    
            (1,     "Hansen   ","  Ola    " ,"Timoteivn 10  " , 44  ),
            ("2",     "Svendson ","    Tove " ,"   Borgvn 23  " , "  Sandnes    "  ),
            ("3",     "Pettersen","     Kari" ,"    Storgt 20 " , "   Stavanger "  ),
            ("4",     "Nilsen   ","  Johan  " ,"  Bakken 2    " , "Stavanger    "  ) ,
            )               
        self.DB.insertDataRows("Persons", simpleData)

        simpleData = (
                (1,     77895,     3),
                (2,     44678,     3),
                (3,     22456,     2),
                (4,     24562,     1),
                )
        self.DB.insertDataRows("Orders", simpleData)
        
        self.DB.getAllPrintedTables()
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
    