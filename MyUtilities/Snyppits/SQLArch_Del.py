# deleting_data.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from SQLAlch_CreateDB import Album, Artist
 
engine = create_engine('sqlite:///mymusic.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
res = session.query(Artist).filter(Artist.name=="MXPX").first()
 
session.delete(res)
session.commit()