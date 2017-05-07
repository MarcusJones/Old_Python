#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""This module does A and B. 
Etc.
"""
from __future__ import division       
#===============================================================================
# Set up
#===============================================================================
# Standard:


from config import *

import logging.config
import unittest

from utility_inspect import whoami, whosdaddy, listObject
import json
from pprint import pprint

def loadSettingsFile(projectFilePath):
        fh=open(projectFilePath)
        settings = json.load(fh)
        fh.close()
        
        return settings
    

#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):
    
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        projectFile = r"C:\EclipseWorkspace\Evolve2\Config\testProject_LoadDSpace.json"
        loadSettingsFile(projectFile)


        
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
    
    #print FREELANCE_DIR
    
    unittest.main()
        
    logging.debug("Finished _main".format())
    
