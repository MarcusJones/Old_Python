#===============================================================================
# Set up
#===============================================================================
from __future__ import division
from __future__ import print_function

from config import *

import logging.config
import unittest

from utility_inspect import whoami, whosdaddy, listObject

# Testing imports
#from ..design_space import Variable, DesignSpace
from ..sockets_playground import this_sock
from ..sockets_playground import check_connection, get_local_ip, get_external_ip







#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):

    def setUp(self):
        print("**** TEST {} ****".format(whoami()))

    def test010_SimpleCreation(self):
        print("**** TEST {} ****".format(whoami()))
        print(check_connection())
        print("Local IP: {}".format(get_local_ip()))
        print("External IP: {}".format(get_external_ip()))

    def test020_SimpleCreation(self):
        print("**** TEST {} ****".format(whoami()))
        print(this_sock())

#===============================================================================
# Logging
#===============================================================================
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#===============================================================================
# Unit testing
#===============================================================================

class DesignSpaceBasicTests(unittest.TestCase):
    def setUp(self):
        #print "**** TEST {} ****".format(whoami())
        myLogger.setLevel("CRITICAL")
        print("Setup")
        myLogger.setLevel("DEBUG")

    def test010_SimpleCreation(self):
        print("**** TEST {} ****".format(whoami()))

