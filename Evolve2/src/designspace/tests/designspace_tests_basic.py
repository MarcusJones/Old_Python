#===============================================================================
# Set up
#===============================================================================
# Standard:
from __future__ import division
from __future__ import print_function

from config import *

import logging.config
import unittest

from utility_inspect import whoami, whosdaddy, listObject

# Testing imports
from ..design_space import Variable, DesignSpace, ObjectiveSpace

#===============================================================================
# Logging
#===============================================================================
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#===============================================================================
# Unit testing
#===============================================================================

class ObjectiveSpaceTests(unittest.TestCase):
    def test010_CreateObjSpace(self):
        objective_names = ('obj1','obj3')
        objective_goals = ('Max', 'Min')
        this_obj_space = ObjectiveSpace(objective_names, objective_goals)

class DesignSpaceBasicTests(unittest.TestCase):
    def setUp(self):
        #print "**** TEST {} ****".format(whoami())
        myLogger.setLevel("CRITICAL")
        basisVariables = [
                          Variable("C1",50),
                        Variable.ordered("C2",3.14),
                        Variable.ordered('v100',(1,2,3,4)),
                        Variable.unordered('VarStr',["Blue","Red","Green"]),
                        ]
        
        thisDspace = DesignSpace(basisVariables)
        self.D1 = thisDspace
        #print self.D1
        myLogger.setLevel("DEBUG")

    def test000_DspaceCreation(self):
        print("**** TEST {} ****".format(whoami()))
        basisVariables = [
                          Variable("C1",50),
                        Variable.ordered("C2",3.14),
                        Variable.ordered('v100',(1,2,3,4)),
                        Variable.unordered('VarStr',["Blue","Red","Green"]),
                        ]
        thisDspace = DesignSpace(basisVariables)
        self.D1 = thisDspace
        print(self.D1)

    def test010_SimpleCreation(self):
        print("**** TEST {} ****".format(whoami()))
        assert(self.D1.dimension == 4)
        assert(self.D1.cardinality == 12)

  