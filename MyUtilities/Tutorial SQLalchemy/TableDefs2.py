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
    __table_args__ = ({'autoload':True})

########################################################################
class Album(Base):
    """"""
    __tablename__ = "albums"
    __table_args__ = ({'autoload':True})

Base.metadata.create_all(engine)