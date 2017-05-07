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
from __future__ import print_function

from config import *

import logging.config
import unittest

from UtilityInspect import whoami, whosdaddy, listObject
import pandas as pd

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
        print("**** TEST {} ****".format(whoami()))
        
    def test010_SimpleCreation(self):
        print("**** TEST {} ****".format(whoami()))
        excel_path = r"D:\Dropbox\03 Side project\00 iC\Forecast.xlsx"
        logging.debug("XLSX file at {}".format(excel_path))

        xlsx = pd.ExcelFile(excel_path)
        logging.debug("XLSX object {} with sheets {}".format(xlsx,xlsx.sheet_names))
        
        hours = xlsx.parse('Hours',header=2,skiprows=2,index_col=None)
        print(hours.head())
        print(hours.transpose().head())
        #hours[colname]
        
        
        
        
        
#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print(ABSOLUTE_LOGGING_PATH)
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)


    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())

    #print FREELANCE_DIR

    unittest.main()

    logging.debug("Finished _main".format())
