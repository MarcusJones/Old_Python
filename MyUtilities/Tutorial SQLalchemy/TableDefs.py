from sqlalchemy import Column
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Integer, String, Date
import sqlalchemy as alc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

path_db = r'C:\EclipseWorkspace\MyUtilities\mymusic.db'
Base = declarative_base()
engine = alc.create_engine('sqlite:///{}'.format(path_db), echo=True)

class Artist(Base):
    """"""
    __tablename__ = "artists"

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

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    publisher = Column(String)
    media_type = Column(String)

    artist_id = Column(Integer, ForeignKey("artists.id"))
    artist = relationship("Artist", backref=backref("albums", order_by=id))

    #----------------------------------------------------------------------
    def __init__(self, title, release_date, publisher, media_type):
        """"""
        self.title = title
        self.release_date = release_date
        self.publisher = publisher
        self.media_type = media_type

Base.metadata.create_all(engine)