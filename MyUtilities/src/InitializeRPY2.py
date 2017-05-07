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

from utility_inspect import whoami, whosdaddy, listObject
import rpy2.rinterface as rinterface

#===============================================================================
# Code
#===============================================================================
class MyClass(object):
    """This class does something for someone. 
    """
    def __init__(self, aVariable): 
        pass
    
class MySubClass(MyClass):
    """This class does
     
    """
    def __init__(self, aVariable): 
        super(MySubClass,self).__init__(aVariable)
    def a_method(self):
        """Return the something to the something."""
        pass

def some_function():
    """Return the something to the something."""
    pass

#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):
    
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
            
    def test010_SimpleCreation(self):
        print "**** TEST {} ****".format(whoami())

#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print ABSOLUTE_LOGGING_PATH
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())
    
    print os.environ["R_HOME"]
    
    #print FREELANCE_DIR
    rinterface.initr()
    
    
    
    
    #unittest.main()
        
    logging.debug("Finished _main".format())
    