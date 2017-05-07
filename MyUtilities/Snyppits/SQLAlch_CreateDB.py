# table_def.py
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

#fh = open(r"C:\TempDel\nothing.txt", "wb")
#print fh
engine = create_engine(r'sqlite:///C:\TempDel\myDataBase.db', echo=True)
Base = declarative_base()
 
########################################################################
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
 
########################################################################
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
 
# create tables
# Anything that inherits Base!
Base.metadata.create_all(engine)




