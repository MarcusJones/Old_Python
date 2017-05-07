#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""This module holds the "controllers" for a search
A controller recieves settings (dict), and a DSpace object 
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:
from __future__ import division    

from config import *

import logging.config
import unittest

from utility_inspect import whoami
from utility_inspect import whoami, whosdaddy

#from evaluators import sum_fitness

import numpy as np
import matplotlib as plt

from design_space import create_database

import graphics as Graphics
#from design_space import DspaceDataBase, DesignSpace, create_database

#queuesTemplate = dict(Pending = list(), Running = list(), Finished = list())


#-- Utilities -------------------------------

def printFitnesses(DSpace):
    fitnesses = [indiv.fitness for indiv in DSpace.finishedIndividuals]  
    #population = DSpace.get_random_population(popSize)
    if fitnesses:
        print " MAX:{}".format(max(fitnesses))
        print "MEAN:{}".format(sum(fitnesses)/len(fitnesses)) 
        print " MIN:{}".format(min(fitnesses))

def getOperators(settings):
    # Mutation
    if "Mutator" in settings:       
        if settings["Mutator"] == "Simple Mutate":
            settings["Mutator"] = simpleMutate
        elif settings["Mutator"] == "Another one":
            pass
        else:
            pass
        
    # Recombination
    if "Recombine" in settings:
        if settings["Recombine"] == "Simple Recomb":
            settings["Recombine"] = simpleRecombine

    # Selection
    if "Selection" in settings: 
        if settings["Selection"] == "Simple Select":
            settings["Selection"] = simpleSelection
        
    # Evaluation operator 
    if settings["Evaluator"] == "Simple Max":
        settings["Evaluator"] = sum_fitness
        return settings
    elif settings["Evaluator"] == "Another one":
        pass
    else:
        raise Exception("{} DNE".format(settings["Evaluator"]))    
    return settings


    
def printSettings(settings):
    #cleanedDict = dict()
    for k,v in settings.items():
        #k = str(k)
        #v = str(v)
        #cleanedDict[k] = v
        print "{0:<15} -> {1:10}".format(k,v)





#- Filter and run -------------------------------

def filterIndividuals(dSpace, DB, individuals, queues):
    """
    Analyze a list of individuals
    
    Split into 3 parts: Pending (to run), Running (initially empty) and Finished
    This is contained in a dictionary: queues
    queues = dict(Pending = list(), Running = list(), Finished = list())
    """
    #numberFiltered = len(dSpace.currentQueue)
    
    
    currentSet = set(individuals)
    
    numberUnique = len(currentSet)
    
    
    #numberAlreadyDone = 0
    while currentSet:
        # Get one individual
        newIndiv = currentSet.pop()
        
        # Make sure we are not running this individual (never happens)
        #if (newIndiv in dSpace.runningIndividuals):
        #    raise Exception("An individual in a population should never be double simulated")
        
        # Check if this has already been eval'd
        
        if DB.individual_in_DB( newIndiv ):
            queues["Finished"].append(newIndiv)
        else:
            queues["Pending"].append(newIndiv)
            
        #if newIndiv in dSpace.finishedIndividuals:
            # This is ugly
#            allFinished = list(dSpace.finishedIndividuals)
#            theDoneIndiv = [doneIndiv for doneIndiv in allFinished if newIndiv == doneIndiv]
#            assert(len(theDoneIndiv)==1)
#            theDoneIndiv = theDoneIndiv[0]
#            assert(isinstance(theDoneIndiv, DesignSpace.Individual))
#            assert(theDoneIndiv.fitness)
            #numberAlreadyDone += 1
            
#            dSpace.currentQueue.remove(newIndiv)

        # This is a new individual, add it to our run queue
#        elif newIndiv not in dSpace.finishedIndividuals:
#            # Add it to the run queue
#            dSpace.runningIndividuals.add(newIndiv)
#            #dSpace.currentQueue.remove(newIndiv)
#        # Nothing else should happen
#        else:
#            raise
#        
    logging.debug("Filtered {:5} individuals, {:5} unique, {:5} already in database, {:5} to simulate".format(
            len(individuals),
            numberUnique,
            len(queues["Finished"]),
            len(queues["Pending"]),
            )
            )
        
    return queues

def executeCurrentRunQueue(evaluator, queue):
    """
    
    All Indivs in runningIndividuals are executed
    All Indivs in runningIndividuals are moved to finishedIndividuals
    """
   
    numberInQueue = len(queue["Pending"])
    
    while queue["Pending"]:
        runIndiv = queue["Pending"].pop()

        runIndiv.fitness = evaluator(runIndiv)
        
        queue["Finished"].append(runIndiv)


    logging.debug("Simulated {} individuals".format(numberInQueue))
                
    return queue

def writeQueueToDB(DB, queue, genNumber):
    """
    
    All Indivs in runningIndividuals are executed
    All Indivs in runningIndividuals are moved to finishedIndividuals
    """
   
    numberInQueue = len(queue["Finished"])
    
    DB.add_population_db(queue["Finished"],genNumber)
        
    queue["Finished"]= list()

    logging.debug("Wrote {} individuals from Finished queue to the DB, {}".format(numberInQueue, DB))
                
    return queue


#-- Controllers -------------------------------


class ControllerBase(object):
    #--- Initialize
    def __init__(self, settings=None):
        self.settings= settings

    def registerDSpace(self, DSpace):
        self.DSpace = DSpace
        logging.debug("Registered DSpace with {}".format(self))

    def registerOperators(self, operators):
        self.operators = operators
        logging.debug("Registered {} operators with {}".format(len(operators),self))

    def registerEvaluator(self, evaluator):
        self.evaluator = evaluator
        logging.debug("Registered evaluator with {}".format(self))
    
    def loadDatabase(self, fullPath):
        """If resuming, link the DB
        """
        pass
    
    def createDatabase(self, fullPath):
        myLogger = logging.getLogger()        
        myLogger.setLevel("CRITICAL")
        self.DBpath = fullPath
        self.DB = create_database(self.DSpace,fullPath)
        myLogger.setLevel("DEBUG")
        logging.debug("Created database in {} path: {}".format(self, fullPath))
    
    #--- Execution
    def flgIsResuming(self):
        pass

    def execute(self):
        pass
    
    def postProc(self):
        pass
    
    #------- Print ------
    def __str__(self):
        return self.myName()
    
    def print_summary(self):
        print "Controller Summary", self
        print self.DSpace
        for var in self.DSpace.basis_set:
            print "\t", var
        print self.DB
        print "Operators:"
        for op in self.operators:
            print "\t", op
        print "Evaluator:", self.evaluator
    
    def myName(self):
        return "UNITIALIZED"

class Controller_randomSearch(ControllerBase):
    def execute(self):

        popSize = int(self.settings["populationSize"])
        numGenerations = int(self.settings["generations"])
        queues = dict(Pending = list(), Running = list(), Finished = list())
        
        logging.debug("Starting a random search over {} gens, with {} population".format(numGenerations, popSize))
        
        #generationsFig = Graphics.startGenerationsFigure()
        
        for genNum in range(numGenerations):
            thisPopulation = self.DSpace.get_random_population(popSize)
    
            thisQueue = filterIndividuals(self.DSpace, self.DB, thisPopulation,queues )
            thisQueue = executeCurrentRunQueue(self.evaluator, thisQueue )
            thisQueue = writeQueueToDB(self.DB, thisQueue , genNum)
            #logging.debug("Evaluated {} random individuals".format(len(thisPopulation) ))
            
            thisGenStats = self.DB.get_gen_stats(genNum)
            #generationsFig = Graphics.updateGenerationsPlot(thisGenStats, generationsFig)

        logging.debug("Finished random search".format())
    
    def myName(self):
        return "Random search"

    def postProc(self):
        
        #self.DB.printResultsTable()
        self.DB.plotGens()
        
    
def cntrl_globalSearch(settings, DSpace):
    logging.debug("Starting a global search".format())
    settings = finalizeSettings(settings)
    
    #numGens = 
    
    DSpace.get_global_search() # Loads queue
    
    DSpace = filterIndividuals(DSpace)
    
    DSpace = executeCurrentRunQueue(settings, DSpace)
    
    DSpace.currentQueue = list()

    
    printFitnesses(DSpace)

def cntrl_basicEvolutionary(settings, DSpace):
    """
    settings
        evaluator
        popSize
    """
    
    settings = finalizeSettings(settings)
    
    logging.debug("Starting a basic evo search".format())
    
    popSize = int(settings["Population size"])
    maxGens = int(settings["Max generations"])
    
    DSpace.get_random_population(popSize)
    
    for genNum in range(maxGens):

        DSpace = filterIndividuals(DSpace)
        
        DSpace = executeCurrentRunQueue(settings, DSpace)
        DSpace = settings["Selection"](DSpace, settings)
        DSpace = settings["Mutator"](DSpace, settings)
        DSpace = settings["Recombine"](DSpace, settings)
        
        DSpace.copyFromFutureToCurrent()
        
        logging.debug("Evaluated {} random individuals, {:10.2f}% coverage of space".format(len(DSpace.finishedIndividuals),DSpace.percentFinished))
    
    printFitnesses(DSpace)
    
    logging.debug("Evaluated {} random individuals".format(len(DSpace.finishedIndividuals) ))

if __name__ == "__main__":
    print ABSOLUTE_LOGGING_PATH
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())
    
    #print FREELANCE_DIR


    # Get the external test
    suites = [unittest.defaultTestLoader.loadTestsFromName("manager")]
    testSuite = unittest.TestSuite(suites)
    text_runner = unittest.TextTestRunner().run(testSuite)
    
    logging.debug("Finished _main".format())
    
    
   