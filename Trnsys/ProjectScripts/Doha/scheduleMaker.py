'''
Created on 2012-11-04

@author: Anonymous
'''

"""This module does A and B. 
Etc.
"""

#===============================================================================
# Set up
#===============================================================================
import logging.config
from UtilityInspect import whoami, whosdaddy
import unittest
from config import *
from ScheduleMakerSCWE import makeSched

def dohaMetroProj():
    schedBookPath = FREELANCE_DIR + r"\101_DohaMetro\Input\Schedules r07.xlsx"
    simulationDirPath = FREELANCE_DIR + r"DohaMetroSim\\"
    
    makeSched(schedBookPath,simulationDirPath)
    
if __name__ == "__main__":
    
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")
    logging.debug("Started _main".format())

    dohaMetroProj()
    #_decathLoad()
    
    
    logging.debug("Finished _main".format())

        