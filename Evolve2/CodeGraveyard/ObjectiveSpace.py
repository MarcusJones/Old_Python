#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""This module does stuff
Etc.
"""

#===============================================================================
# Set up
#===============================================================================
from __future__ import division    
import logging.config
from UtilityInspect import whoami, whosdaddy
import unittest
from DesignSpace import DesignSpace, getTupleString, getPureTuple
from Variable import Variable

#===============================================================================
# Code
#===============================================================================
class ObjectiveSpace(object):
    def __init__(self,objectiveFunction):
        self.objectiveFunction =  objectiveFunction
        logging.info("Init DesignSpace, {0}".format(self))
        
        self.historicalMappings = set()
        
    def evaluate(self,designTuple):
        alreadyEvaluated = False
        for mapping in self.historicalMappings:
            #print designTuple, mapping[0]
            if getPureTuple(designTuple) == getPureTuple(mapping[0]):
                logging.debug("This has already been evaluated {}".format(mapping))
                alreadyEvaluated = True
                break
        
        if not alreadyEvaluated:
            objectiveVector = self.objectiveFunction(designTuple)
        else:
            objectiveVector = mapping[1]

        self.historicalMappings.add((designTuple,objectiveVector))
 
        
    def __str__(self):
        return "ObjectiveSpace: {}".format(self.objectiveFunction)
    
def getObjectiveVectorStr(vector):
    
    vectorString = ["{}".format(var) for var in vector]
    
    vectorStr = "(" + ", ".join(vectorString) + ")"
    return vectorStr    

def getMappingStr(mappingTuple):
    
    inputStr = getTupleString(mappingTuple[0])
    outputStr = getObjectiveVectorStr(mappingTuple[1])

    return inputStr + " Maps to: " + outputStr

#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):

    def setUp(self):
        # Create a test design space
        basisVariables = [
                          Variable("C1",50),
                        Variable.ordered('v100',(1,2,3,4)),
                        Variable.fromRange("X1", '0', '0.5', '10')                   
                        ]
        
        self.thisDspace = DesignSpace(basisVariables) 
        
        def simpleSumFunction(inputTuple):
            thisSum = 0
            for var in inputTuple:
                thisSum = thisSum + var.generatedValue
            
            objectiveVector = (thisSum,)
            return objectiveVector 
        
        self.simpleSumFunction = simpleSumFunction
        

    def test010_SinglePointEval(self):
        print "**** TEST {} ****".format(whoami())
        
        # Get a point
        singlePoint = self.thisDspace.getRandomPoint()
        print "Single point in space:", getTupleString(singlePoint)
            
        # Create an objective space
        thisMspace = ObjectiveSpace(self.simpleSumFunction)
        
        thisMspace.evaluate(singlePoint)

        for mapping in thisMspace.historicalMappings:
            print getMappingStr(mapping)        
        
    def test020_GlobalMapping(self):
        print "**** TEST {} ****".format(whoami())

        thisMspace = ObjectiveSpace(self.simpleSumFunction)
        
        # Get a point
        for designPoint in self.thisDspace.globalSearch():
            thisMspace.evaluate(designPoint)
            
        for mapping in thisMspace.historicalMappings:
            print getMappingStr(mapping),
        print 
        
        # Get one more point
        # Since all points have been mapped, this should skip the eval function
        newRandomPt = self.thisDspace.getRandomPoint()
        thisMspace.evaluate(newRandomPt)
        
    def test0X0_(self):
        print "**** TEST {} ****".format(whoami())
        pass

#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    logging.config.fileConfig('..\\..\\MyUtilities\\LoggingConfig\\loggingNofile.conf')
    myLogger = logging.getLogger()
    myLogger.setLevel("INFO")

    logging.debug("Started _main".format())

    unittest.main()
        
    logging.debug("Started _main".format())
    