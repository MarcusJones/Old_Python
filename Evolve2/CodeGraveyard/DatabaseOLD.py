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
import os


# The actual database mapped objects:
from DesignSpace import Individual
from DesignSpace import DesignSpace
from Variable import Variable

# SQL 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,mapper
from sqlalchemy import MetaData
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Date, Integer, String, Float
from sqlalchemy import Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


#===============================================================================
# Code
#===============================================================================

def getAllTableNames(session):

    thisCmd = """SELECT name FROM sqlite_master
    WHERE type='table'
    ORDER BY name;
    """
    result = session.execute(thisCmd)
    #print result
    tableNames = list()
    for row in result:
        #print row
        tableNames.append(row)
    return tableNames

#        thisCmd = "SELECT * FROM {}".format(this_table_name[0])

def deleteAllData(session):
    allTableNames  = getAllTableNames(session)
    for this_table_name in allTableNames:
        thisCmd = "DELETE FROM {}".format(this_table_name[0])
        
        #print thisCmd
        result = session.execute(thisCmd)
        #for item in result:
        #    print result
        #session.execute)
        session.commit()
        
    logging.debug("Deleted all data from {}".format(allTableNames))
 
    return 

#===============================================================================
# Unit testing
#===============================================================================

class testDynamics(unittest.TestCase):
    # http://stackoverflow.com/questions/2580497/database-on-the-fly-with-scripting-languages/2580543#2580543
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        
        ThisDBfullPath = 'C:\TempDel\myDataBaseDSpace.db'
        try:
            os.remove(ThisDBfullPath)
        except:
            pass
        # Create a DSpace first
        basisVariables = [
                            Variable("C1",50),
                            Variable.ordered("C2",3.14),
                            Variable.ordered('v100',(1,2,3,4)),
                            Variable.unordered('VarStr',["Blue","Red","Green"]),
                            ]
        thisDspace = DesignSpace(basisVariables)
        self.D1 = thisDspace 
        # Create a table with;
        # One primary key column 
        # Additional columns for each variable present, to store the actual values of the var
        # The fitness column
        
        #creationString = 
        engine = create_engine(r'sqlite:///' + ThisDBfullPath, echo=0)

        Base.metadata.create_all(engine)

        metadata = MetaData(bind=engine)
        
        # Need to 
        table = Table('foo', metadata, 
                    Column('id', Integer, primary_key=True),
                    Column('fitness', Float),
                    *(Column("VAR_"+variable.name, String()) for variable in self.D1.basisSet)
                    )
        
        print table
        table.create()
        
        #mapper(Individual, table, non_primary=True)
        mapper(Individual, table)
        
        metadata = MetaData(engine)
        

        if 0: print "Tables:", metadata.tables.keys()
        #
        if 0:
            print "Reflect", metadata.reflect(engine)
            print "Engine metadata;", metadata
        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()
        metadata = MetaData(session)
        if 0: print "Session metadata;", metadata
        
        if 0:
            for k,v in session.__dict__.iteritems():
                pass
                #print k, ":", v
        self.session = session
        
        res = self.session.query(Individual)
        print res

    def test010_TableNames(self):
        print "**** TEST {} ****".format(whoami())
        print getAllTableNames(self.session)
        
    def tearDown(self):
        print "**** TEST {} ****".format(whoami())
        
        deleteAllData(self.session)

        self.session.close()

        
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
    
    
    
    
    
    
    
    
    

#class Variable(Base):
#    """"""
#    __tablename__ = "variables"
#    
#    # Two columns in table
#    
#    id = Column(Integer, primary_key=True)
#    name = Column(String)  
# 
#    #----------------------------------------------------------------------
#    def __init__(self, name):
#        """"""
#        self.name = name
#    
#    def __str__(self):
#        return self.name
#    
#class Individual(Base):
#    """"""
#    __tablename__ = "individuals"
#    
#    # 5 columns
#    
#    
#    id = Column(Integer, primary_key=True)
#    title = Column(String)
#    release_date = Column(Date)
#    publisher = Column(String)
#    media_type = Column(String)
#    
#    
#    # Link each row of album to one row of artist
#    # One artist to many albums
#    individual_id = Column(Integer, ForeignKey("variables.id"))
#    
#    # Establish this relationship, 
#    artist = relationship("Variable", backref=backref("individuals", order_by=id))
# 
#    #----------------------------------------------------------------------
#    def __init__(self, title, release_date, publisher, media_type):
#        """"""
#        self.title = title
#        self.release_date = release_date
#        self.publisher = publisher
#        self.media_type = media_type
# 
#
#    def __str__(self):
#        return "{}, {}, {}".format(self.id, self.title,self.publisher)
    
    
    
    

#
#
#class testEmptyTable(unittest.TestCase):
#    
#    def setUp(self):
#        print "**** TEST {} ****".format(whoami())
#        
#        engine = create_engine(r'sqlite:///C:\TempDel\myDataBase.db', echo=0)
#
#        Base.metadata.create_all(engine)
#        
#        metadata = MetaData(engine)
#        if 0: print "Tables:", metadata.tables.keys()
#        #
#        if 0:
#            print "Reflect", metadata.reflect(engine)
#            print "Engine metadata;", metadata
#        # create a Session
#        Session = sessionmaker(bind=engine)
#        session = Session()
#        metadata = MetaData(session)
#        if 0: print "Session metadata;", metadata
#        
#        if 0:
#            for k,v in session.__dict__.iteritems():
#                pass
#                #print k, ":", v
#        self.session = session
#        
#        
#    def test010_TableNames(self):
#        print "**** TEST {} ****".format(whoami())
#        print getAllTableNames(self.session)
#        
#    @unittest.skip("Just too slow")
#    def test020_SimpleCreation(self):
#        print "**** TEST {} ****".format(whoami())
#        
#        result = self.session.query(Album).all()
#        print result
#        
#
#        #print self.session.query(tables.items())
#        
#    @unittest.skip("Just too slow")
#    def test030_DeleteAllData(self):
#        print "**** TEST {} ****".format(whoami())
#        deleteAllData(self.session)
#        #delete(synchronize_session='fetch')
#        #self.session.execute(delete())
#
#    def test040_AddSomeData(self):
#        print "**** TEST {} ****".format(whoami())
#        
#        new_variable = Variable("Newsboys")
#        new_variable.individuals = [Individual("Read All About It", 
#                                   datetime.date(1988,12,01),
#                                   "Refuge", "CD")]
#        
#        new_variable.individuals = [Individual("Read All About It", 
#                                   datetime.date(1988,12,01),
#                                   "Refuge", "CD")]
#        
#        # Add the record to the session object
#        self.session.add(new_variable)
#        # commit the record the database
#        self.session.commit()
#        result = self.session.query(Individual).all()
#        print result
#        itemNum = 0
#        for row in result:
#            print itemNum, row
#            #print itemNum, row.__dict__
#            #print itemNum, dir(row)
#            #for item in dir(row):
#            #    print item
#            #print itemNum, row.__table__
#            #print itemNum, row.__doc__
#            itemNum += 1
#
#
#    def tearDown(self):
#        print "**** TEST {} ****".format(whoami())
#        
#        deleteAllData(self.session)
#
#        self.session.close()
#    
#    