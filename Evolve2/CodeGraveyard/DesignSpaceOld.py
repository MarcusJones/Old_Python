

#    @property
#    def allIndividuals(self):
#        individualsList = [self.currentQueue, self.runningIndividuals, self.finishedIndividuals]
#        return set.union(*individualsList)
#
#    @property
#    def runOrDoneIndividuals(self):
#        individualsList = [self.runningIndividuals, self.finishedIndividuals]
#        return set.union(*individualsList)

#    @property
#    def percentFinished(self):
#        percentage = -1
#            # len(self.finishedIndividuals)/self.cardinality * 100
#        assert(percentage <= 100)
#        return percentage
#        #print("{}% - {} out of {} values have been generated".format(self.percentFinished,len(self.currentQueue),self.size)

#    @property
#    def lenAllHistory(self):
#        return len(self.currentQueue)
#
#    @property
#    def lenPendingIndividuals(self):
#        pendingIndividuals = [thisIndiv for thisIndiv in self.currentQueue if not thisIndiv.fitness]
#        return len(pendingIndividuals)
#
#    @property
#    def lenFinishedIndivuals(self):
#        completeMaps = [thisIndiv for thisIndiv in self.currentQueue if thisIndiv.fitness != None]
#        return len(completeMaps)
#

def get_global_search_OLD(self, flgVerbose = False):
        raise
        '''
        This will create a nested for-loop on the fly, so that each
        possible combination is represented

        Example, for 3 variables:
        [<Variables.FloatList object at 0x00D012F0>, <Variables.FloatList object at 0x00D01990>, <Variables.StringList object at 0x00D019D0>]

        The exec code is:
        for v0 in self.designSpace.variableList[0]:
            for v1 in self.designSpace.variableList[1]:
                for v2 in self.designSpace[2].variableList:
                     self.currentgeneratedTuple = (v0,v1,v2,)
                     self.addToCurrentQueue()
                     runList.append(self.currentgeneratedTuple)
        for v0 in self.basis_set[0]:
            for v1 in self.basis_set[1]:
                for v2 in self.basis_set[2]:
                     runList.append((v0,v1,v2,))
        Which will produce:
        [
        (('VarX1', '0.0'), ('VarX2', '0.0'), ('DefaultMaterial', 'Wood')),
        (('VarX1', '0.0'), ('VarX2', '0.0'), ('DefaultMaterial', 'Steel')),
        (('VarX1', '0.0'), ('VarX2', '0.0'), ('DefaultMaterial', 'Cheese')),
        (('VarX1', '0.0'), ('VarX2', '1.0'), ('DefaultMaterial', 'Wood')),
        (('VarX1', '0.0'), ('VarX2', '1.0'), ('DefaultMaterial', 'Steel')),
        ... ETC..
        ]

        '''
        #print(self.basis_set)
        i = 0
        evalValuesStr = ""
        evalForStr = ""
        #prin self.designSpace
        count = 0
        for variable in self.design_space.basis_set:
            #evalValuesStr += "v" + str(i) + ".value,"
            evalValuesStr += "v" + str(i) + ","
            evalForStr += "\t"*i + "for v" + str(i) + " in self.design_space.basis_set[" + str(i) + "]:\n"
            i += 1

        #evalValueStr = "\t"*i + " runList.append( (" + evalValueStr + ") ,None))\n"
        evalTupleStr =  "(" + evalValuesStr +  ")"
        #stringInsideForLoop =  "\t"*i + "self.addToCurrentQueue(" + evalMappingStr + ")\n"
        stringInsideForLoop0 =  "\t"*i + "thisChromo = generate_chromosome(" + evalTupleStr + ")\n"

        stringInsideForLoop1 =  "\t"*i + "thisIndiv = self.individual(thisChromo, self.evaluator)\n"
        #stringInsideForLoop2 =  "\t"*i + "self.addToCurrentQueue(" + "thisIndiv" + ")\n"
        stringInsideForLoop3 =  "\t"*i + "count += 1\n"
        stringInsideForLoop4 =  "\t"*i + "runList.append(thisIndiv)\n"

         #Individual(generate_chromosome(variables))
        completeExecString = evalForStr + stringInsideForLoop0 + stringInsideForLoop1  + stringInsideForLoop3 + stringInsideForLoop4
        #print(evalForStr
        #print(evalMappingStr
        #print(stringInsideForLoop
        #evalValueStr = "\t"*i + " self.addToCurrentQueue( (" + evalValueStr + ") ,None))\n"
        #evalValueStr2 = "\t"*i + " print( (" + evalValueStr + ") \n"

        #evalValueStr = "\t"*i + " print((" + evalValueStr + "))\n"
        #evalStr = evalForStr + evalValueStr + evalValueStr2
        runList = []


        #self.mapping = tuple([var.get_random().value for var in  self.basis_set])

        #self.addToCurrentQueue((self.mapping,None))
        if flgVerbose:
            print("--- GLOBAL SEARCH ---\n" +  completeExecString + "\n --- GLOBAL SEARCH ---")
        exec(completeExecString)

        logString = "Retrieved {0} individual points over the {1}-variable design space basis set".format(count,self.design_space.dimension)
        logging.info(logString)

        return runList
      

def getUniqueRandomPoint(self):
    """
    DEFINATELY BROKEN - fails for large spaces for obvious reasons - it will keep searching for those last few values!

    Same as before, but now we garauntee a random point
    Could be optimized - use SET to remove items from a list of all possible values
    BUT this might also use up too much space? Have to store all possible values?
    
    """
    
    raise Exception("")
    
    while 1:
        self.mapping = tuple()
        for var in self.basisSet:
            self.mapping = self.mapping + (var.getRandom(),)
        
        simpleVector = tuple()
        for SR in self.mapping:
            simpleVector = simpleVector + (SR.value,)
        
        if simpleVector not in self.newIndividuals:
            break 
        #if simpleVector in self.newIndividuals:
        #    print "Match", simpleVector
        
        #self.updatePercentageOfCoverage()
        
        #print self.percentTotalMaps
        
        if self.percentTotalMaps >= 100:
            break

    self.addToQueue(simpleVector)
        
    return self.mapping







'''
Created on 2012-01-23

@author: mjones
'''

from __future__ import division    
#import random
#import Utilities
import logging.config
#import math
#import re
from SimFile import SimFile
from decimal import *

logging.config.fileConfig('..\\LoggingConfig\\logging.conf')


class DesignSpace(object):
    """
    Design space 
    """
    
    def __init__(self, variableList, name="NoName"): 
        self.name = name
        self.variableList = variableList
        
        logString = "Created DesignSpace '{0}' with dimension: {1}, size: {2}, listing follows:".format(self.name, len(self.variableList), self.totalSpaceSize())
        
        logging.info(logString)

        count = 0
        for variable in self.variableList:
            logging.info("   Variable {0} in {1}: {2}".format(count, self, variable))
            count += 1

    def totalSpaceSize(self):
        
        #print len(self)
        
        
        
        piProd = 1
        for variable in self.variableList:
            try:
                thisVarLength = len(variable) 
            except:
                thisVarLength = float('inf')
    
            piProd = piProd * thisVarLength
            
        return piProd
            


    def __len__(self):
        # This is also the Dimension of the vector space
        return len(self.variableList)
    
    def __iter__(self):
        self.iterIndex = 0
        return self
    
    def __str__(self):
        return "DSpace '{}'".format(self.name)
    
    # Custom iterator, the variable will return the target Regex with 
    # the current variable
    def next(self):
        if self.iterIndex < len(self):
            current = self.variableList[self.iterIndex]
        else: 
            raise StopIteration
        self.iterIndex += 1
        return (current)    


def _test():
    
    targetFile = SimFile(r"c:\\root\\","mainInput.idf")
    
    print "Create some Variables;"
    variableList = [
                    Constant(r"A1",r"VarX1",targetFile),
                    Constant(r"A1",r"VarX1",targetFile),
                    SequentialList(r"VarX1",["apple","orange","pear","Jack in a box"],targetFile),
                    #RandomList(r"VarX1",["apple","orange","pear","Jack in a box"],targetFile),
                    BoundedSequentialNumber(r"VarX1",targetFile,'0.0','0.1','1')
                    ]
    
    print "Create a DesignSpace;"
    
    testDSpace = DesignSpace(variableList)
    
    print "Look at a Value List;"
    myVar = variableList[2]
    
    print "Iterate it to the end;"
    for var in myVar:
        pass 
    
    print "Should be now last value of list;"
    print myVar
    
    
    if 0:
        print "Look at a RandomList being initialized;"
        myVar = variableList[3]
        print myVar
        
        print "Generate a new RandomList value;"
        myVar.next()
        print myVar
    
        print "Generate a new RandomList value;"
        myVar.next()
        print myVar
    
    
    print "Look at the bounded sequential number;"
    myVar = variableList[3]
    print myVar
    
    for var in myVar:
        print myVar
 
        #    
#    v2 = RandomFloat("A1",r"VarX1",0,60)
#    
#    v3 = RandomStringList("A3",r"DefaultMaterial",("Wood","Steel","Cheese"))
#    
#    print v3.value
#    v3.new()
#    print v3.value
#    
#    #print v1
#    #print len(v1)
#    
#    print v2.value
#    v2.new()
#    print v2.value
#    
#    #print v1.value
#    #print v1.value
#    #print v1.value
#
##    for value in v1:
##        print 'Val', value
#
#    


#--- Obselete tests from design_space
#@unittest.skipIf(skip_stored,"")
@unittest.skip("")
class OLD_testDatabaseSTORED(unittest.TestCase):
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        self.SQLtestLocation = "C:\TestSQL\update.sql"
        self.SQLtestLocation = ":memory:"


    #@unittest.skip("")
    def test010_storeDB(self):
        print "**** TEST {} ****".format(whoami())

        #myLogger.setLevel("CRITICAL")


        basisVariables = [
                          Variable("C1",50),
                        Variable.ordered("C2",3.14),
                        Variable.ordered('v100',(1,2,3,4)),
                        Variable.unordered('varStr',["Blue","Red","Green"]),
                        ]


        self.SQLtestLocationNewRev = get_new_file_rev_path(self.SQLtestLocation)

        #self.SQLtestLocation = ":memory:"

        myLogger.setLevel("DEBUG")

        self.D1 = DesignSpace(basisVariables, ("Alpha","TestObj"))

        self.theDB = create_database(self.D1,self.SQLtestLocationNewRev)

    #@unittest.skip("")
    def test020_LoadAndExplore(self):
        print "**** TEST {} ****".format(whoami())

        #metadata, engine = util_sa.loadDatabase(self.SQLtestLocation)
        latestFile = getLatestRevisionFullPath(self.SQLtestLocation)
        DSpace, newDB = load_project_from_DB(latestFile)




    def test020_reloadAndCheck(self):
        print "**** TEST {} ****".format(whoami())

        #metadata, engine = util_sa.loadDatabase(self.SQLtestLocation)
        latestFile = getLatestRevisionFullPath(self.SQLtestLocation)
        DSpace, newDB = load_project_from_DB(latestFile)

        #util_sa.printOneTable(newDB.engine,newDB.metadata,  "results")

        util_sa.print_all_pretty_tables(newDB.engine)


#@unittest.skipIf(skip_storage2,"Just too slow")
@unittest.skip("")
class OLD_testStorage(unittest.TestCase):
    def setUp(self):
        print "**** TEST {} ****".format(whoami())

        myLogger.setLevel("CRITICAL")
        self.FILE_NAME = r"..\..\TestOutput\test1.out"


        basisVariables = [
                          Variable("C1",50),
                        Variable.ordered("C2",3.14),
                        Variable.ordered('v100',(1,2,3,4)),
                        Variable.unordered('VarStr',["Blue","Red","Green"]),
                        ]

        thisDspace = DesignSpace(basisVariables)
        self.D1 = thisDspace

        myLogger.setLevel("DEBUG")

    def test030_Store10RandomsPts(self):
        print "**** TEST {} ****".format(whoami())
        population1 = self.D1.get_random_population(10)
        # Fake the evaluation
        for indiv in population1:
            indiv.fitness = 1

        print "allIndivs:",
        for indiv in population1:
            print indiv
        print

#        history = dict()
#
#        history = updateHistory(history, population1, 1)
#
#        population2 = self.D1.get_random_population(10)
#
#        history = updateHistory(history, population2,2)
#
#        for key, value in history.iteritems():
#            print "{} -> {}".format(key, value)
#
#        print len(history)
#
#        #print zip(indiv)
#        #print indiv.__hash__, indiv.fitness
#
    def test040_NoDoubleEval(self):
        print "**** TEST {} ****".format(whoami())
        population1 = self.D1.get_random_population(5)
#        # Fake the evaluation
#        for indiv in population1:
#            indiv.fitness = 1
#
#        history = dict()
#        history = updateHistory(history, population1, 0)
#
#        avoidedTotal = 0
#        for generation in range(1):
#            thisGenAvoided = 0
#            newPopulation = self.D1.get_random_population(5)
#            for indiv in newPopulation:
#                if indiv.key in history:
#                    thisGenAvoided = thisGenAvoided + 1
#            history = updateHistory(history, newPopulation,generation)
#            print "In generation {}, {} evaluations avoided".format(generation,thisGenAvoided)
#
#            avoidedTotal += thisGenAvoided
#
#        print "{} avoided in total".format(avoidedTotal)
##        for key, value in history.iteritems():
##            print "{} -> {}".format(key, value)
##
#        print "{} total length".format(len(history))
#
#
#        #fh = open(FILE_NAME , 'w')
#        #print fh
#        pickleHistory(history, self.FILE_NAME)


    def test050_ReloadHist(self):
        print "**** TEST {} ****".format(whoami())
#        history = unpickleHistory(self.FILE_NAME)
#
#        for k, v in history.iteritems():
#            print k,v
#
#
#



if __name__ == "__main__":
    _test()
