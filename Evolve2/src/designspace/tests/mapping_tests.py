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
from ..design_space import Variable, DesignSpace, ObjectiveSpace, Mapping
from ..individuals import BasicIndividual
from ..evaluators import random_fitness

#from ..design_space import Variable, DesignSpace, ObjectiveSpace, Individual, Mapping

#===============================================================================
# Logging
#===============================================================================
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#===============================================================================
# Unit testing
#===============================================================================

class MappingBasicTests(unittest.TestCase):
    def setUp(self):
        #print "**** TEST {} ****".format(whoami())
        myLogger.setLevel("CRITICAL")
        
        # Create DSpace
        basisVariables = [
                          Variable("C1",50),
                        Variable.ordered("C2",3.14),
                        Variable.ordered('v100',(1,2,3,4)),
                        Variable.unordered('VarStr',["Blue","Red","Green"]),
                        ]
        thisDspace = DesignSpace(basisVariables)
        self.D1 = thisDspace
        
        # Create OSpace
        objective_names = ('obj1','obj3')
        objective_goals = ('Max', 'Min')
        this_obj_space = ObjectiveSpace(objective_names, objective_goals)
        self.obj_space1 = this_obj_space
        
        myLogger.setLevel("DEBUG")

    def test010_SimpleCreation(self):
        print("**** TEST {} ****".format(whoami()))
        this_mapping = Mapping(self.D1, self.obj_space1, BasicIndividual, random_fitness)

    def test020_GetRandomIndividuals(self):
        print("**** TEST {} ****".format(whoami()))
        this_mapping = Mapping(self.D1, self.obj_space1, BasicIndividual, random_fitness)
        
        randomPt1 = this_mapping.get_random_mapping()
        print("random individual 1:", randomPt1)
        randomPt2 = this_mapping.get_random_mapping()
        print("random individual 2:", randomPt2)
        randomPt3 = this_mapping.get_random_mapping()
        print("random individual 3:", randomPt3)

        print("Variables inside the first random point;")
        for var in randomPt1:
            print(var)
        print
        print("Last item;",  randomPt1[-1])

        print("Each individual is unique in memory; ")

        print(id(randomPt1), id(randomPt2), id(randomPt3))
        assert(randomPt1 is not randomPt2 is not randomPt3)
        
        print("But points can have the same hash;")
        print(randomPt1.__hash__(), randomPt2.__hash__(), randomPt3.__hash__())

    def test030_Get10RandomsIndividuals(self):
        print("**** TEST {} ****".format(whoami()))
        this_mapping = Mapping(self.D1, self.obj_space1, BasicIndividual, random_fitness)
        
        this_mapping.get_random_population(10)
        #for i in range(0,10):
        #    self.D1.get_random_mapping()
        #print "Percent coverage:", self.D1.percentFinished

    def test040_Get10000RandomIndividuals(self):
        print("**** TEST {} ****".format(whoami()))
        this_mapping = Mapping(self.D1, self.obj_space1, BasicIndividual, random_fitness)
        
        pop = this_mapping.get_random_population(10000)

        hash_list = [indiv.__hash__() for indiv in pop]
        print("Given a size 10000 random sample from such a small domain,") 
        print("with overwhelming likelihood, all the possible combinations of variables should be encountered")
        print("Therefore, the number of unique hash values (dentity values) for individuals should be equal to the cardinality of the basis set")

        print("Number unique individuals:", len(set(hash_list)))
        assert(len(set(hash_list)) == 12)

    def test050_GlobalSearch(self):
        print("**** TEST {} ****".format(whoami()))
        print("Dimensions:", self.D1.dimension)
        print("Cardinality:", self.D1.cardinality)

        this_mapping = Mapping(self.D1, self.obj_space1, BasicIndividual, random_fitness)
        
        pop = this_mapping.get_random_population(10000)

        run_list = this_mapping.get_global_search()
        
    def test070_LargeGlobalSearch2(self):
        print("**** TEST {} ****".format(whoami()))

        basisVariables = [
                          Variable("C1",50),
                        Variable.ordered('v100',(1,2,3,4)),
                        Variable.unordered('VarStr',["Blue","Red","Green"]),
                        Variable.from_range('var2','-333.000000', '0.05', '5')

                        ]

        thisDspace = DesignSpace(basisVariables)
        this_mapping = Mapping(thisDspace, self.obj_space1, BasicIndividual, random_fitness)
        
        run_list = this_mapping.get_global_search()

