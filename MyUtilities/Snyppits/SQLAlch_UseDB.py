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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from SQLAlch_CreateDB import Album, Artist
from sqlalchemy import MetaData



#===============================================================================
# Code
#===============================================================================
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Artist(Base):
    """"""
    __tablename__ = "artists"
    
    # Two columns in table
    
    id = Column(Integer, primary_key=True)
    name = Column(String)  
 
    #----------------------------------------------------------------------
    def __init__(self, name):
        """"""
        self.name = name    
    
class Album(Base):
    """"""
    __tablename__ = "albums"
    
    # 5 columns
    
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    publisher = Column(String)
    media_type = Column(String)
    
    
    # Link each row of album to one row of artist
    # One artist to many albums
    artist_id = Column(Integer, ForeignKey("artists.id"))
    
    # Establish this relationship, 
    artist = relationship("Artist", backref=backref("albums", order_by=id))
 
    #----------------------------------------------------------------------
    def __init__(self, title, release_date, publisher, media_type):
        """"""
        self.title = title
        self.release_date = release_date
        self.publisher = publisher
        self.media_type = media_type
 

    def __str__(self):
        return "{}, {}, {}".format(self.id, self.title,self.publisher)


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

class testEmptyTable(unittest.TestCase):
    
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        
        engine = create_engine(r'sqlite:///C:\TempDel\myDataBase.db', echo=0)

        Base.metadata.create_all(engine)
        
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
        
        
    def test010_TableNames(self):
        print "**** TEST {} ****".format(whoami())
        print getAllTableNames(self.session)
        
    @unittest.skip("Just too slow")
    def test020_SimpleCreation(self):
        print "**** TEST {} ****".format(whoami())
        
        result = self.session.query(Album).all()
        print result
        

        #print self.session.query(tables.items())
        
    @unittest.skip("Just too slow")
    def test030_DeleteAllData(self):
        print "**** TEST {} ****".format(whoami())
        deleteAllData(self.session)
        #delete(synchronize_session='fetch')
        #self.session.execute(delete())

    def test040_AddSomeData(self):
        print "**** TEST {} ****".format(whoami())
        
        new_artist = Artist("Newsboys")
        new_artist.albums = [Album("Read All About It", 
                                   datetime.date(1988,12,01),
                                   "Refuge", "CD")]
        
        new_artist.albums = [Album("Read All About It", 
                                   datetime.date(1988,12,01),
                                   "Refuge", "CD")]
        
        # Add the record to the session object
        self.session.add(new_artist)
        # commit the record the database
        self.session.commit()
        result = self.session.query(Album).all()
        print result
        itemNum = 0
        for row in result:
            print itemNum, row
            print itemNum, row.__dict__
            print itemNum, dir(row)
            #for item in dir(row):
            #    print item
            print itemNum, row.__table__
            #print itemNum, row.__doc__
            itemNum += 1


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
    


if 0: 
    
    # Create an artist
    new_artist = Artist("Newsboys")
    new_artist.albums = [Album("Read All About It", 
                               datetime.date(1988,12,01),
                               "Refuge", "CD")]
    
    new_artist.albums = [Album("Read All About It", 
                               datetime.date(1988,12,01),
                               "Refuge", "CD")]
     
    
    
    
    
    
    print "Table;"
    
    for k,v in Album.__dict__.iteritems():
        pass
        #print k, ":", v
    
    print "Try some access;"
    
    
    res = session.query(Artist).first()
    #res = session.query("sqlite_master")
    #res = session.query("")
    """
    SELECT name FROM sqlite_master
    WHERE type='table'
    ORDER BY name;
    """
    print "Query result:", res
    raise
    print Album.__table__
    
    
    
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(meta.sorted_tables):
            con.execute(table.delete())
        trans.commit()
    
    
    # Create an artist
    new_artist = Artist("Newsboys")
    new_artist.albums = [Album("Read All About It", 
                               datetime.date(1988,12,01),
                               "Refuge", "CD")]
     
    # add more albums
    more_albums = [Album("Hell Is for Wimps",
                         datetime.date(1990,07,31),
                         "Star Song", "CD"),
                   Album("Love Liberty Disco", 
                         datetime.date(1999,11,16),
                         "Sparrow", "CD"),
                   Album("Thrive",
                         datetime.date(2002,03,26),
                         "Sparrow", "CD")]
    new_artist.albums.extend(more_albums)
     
    # Add the record to the session object
    session.add(new_artist)
    # commit the record the database
    session.commit()
     
    # Add several artists
    session.add_all([
        Artist("MXPX"),
        Artist("Kutless"),
        Artist("Thousand Foot Krutch")
        ])
    session.commit()
    
    
    
    
    
    










