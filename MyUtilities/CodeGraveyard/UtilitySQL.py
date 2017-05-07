
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

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
#===============================================================================
# Code
#===============================================================================
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password
    
    def __repr__(self):
       return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)


class Individual(Base):
    __tablename__ = 'individuals'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password
    
    def __repr__(self):
       return "<Individual({}',{}, {})>".format()


#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):
    
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
            
    def test010_SimpleCreation(self):
        print "**** TEST {} ****".format(whoami())
        
        print User
        print User.__table__ 
        print User.__mapper__ 
        ed_user = User('ed', 'Ed Jones', 'edspassword')
        print ed_user
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
    