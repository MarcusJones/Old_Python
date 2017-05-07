#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""Operators always receive the 
DesignSpace - The logic of how to move within the design space
population - The points in the design space, as a list of type Individual including fitness 
settings - Settings for the particular operators

The operators CLONE the individuals
The operators return only the new individuals


#The Selection operator creates a futureQueue
#DSpace.futureQueue must exist, it is normally a copy of the previous generation
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:
from __future__ import division    

from config import *

import logging.config
import unittest
import random

from utility_inspect import whoami
from utility_inspect import whoami, whosdaddy
from design_space import Individual, DesignSpace

from variable import Variable

class Operator(object):
    def __init__(self, settings):
        self.settings = settings
        self.checkParams()

    def operate(self, DSpace, population):
        pass

    def checkParams(self):
        for paramName in self.parameterList:
            self.getParameter(paramName)
                
            
    def getParameter(self, paramName):
        #print "Get"
        #print self.settings['parameters']
        for param in self.settings['parameters']:
            #print param
            if paramName in param:
                return param[paramName]
            else:
                pass
        # If we exit the loop without finding the param and returning, error
        raise Exception("Can't find parameter: {} in ".format(paramName, param))
            
#- Search Utilities ----------------------- 
class Neutral(Operator):
    """
    This operator does nothing
    """
    @property 
    def parameterList(self):
        paramList = []
        return paramList
        
    def operate(self, DSpace, population):
        return DSpace, population

#- Mutate  --------------------------------
class SimpleMutate(Operator):
    
    @property 
    def parameterList(self):
        paramList = ["numberToPerturb","stepSize"
                          ]
        return paramList

    def operate(self, DSpace, population):
        """
        """
        numberToPerturb = self.getParameter("numberToPerturb")
        stepSize = self.getParameter("stepSize")
        
        assert(numberToPerturb >= 1)
        
        assert isinstance(population, list)
        
        #clonedIndiv = individual.clone()
        
        # We can only perturb variables, not constants (only 1 value)
        perturbableIndices = [DSpace.basis_set.index(var) for var in DSpace.basis_set if len(var) > 1]
        assert(numberToPerturb <= len(perturbableIndices))
        
        # Now we randomly choose "numberToPerturb" locii to mutate
        chosenMutateLocii = list()
        for idx in range(numberToPerturb):
            # Choose a position to perturb
            thisChoiceIdx = random.choice(perturbableIndices)
            chosenMutateLocii.append(thisChoiceIdx)
            # Don't perturb this again
            perturbableIndices.pop(perturbableIndices.index(thisChoiceIdx))
        
        new_individuals = list()
        # Do it for all invidividuals
        for individual in population:
            
            # Loop over the design space genome
            newChromosome = list()
            for var in DSpace.basis_set:
                
                thisIdx = DSpace.basis_set.index(var)
                # Find the corresponding allele for this individual
                flgFound = False
                
                for allele in individual.chromosome:
                    
                    thisAlleleName  = allele[0]
                    if var.name == thisAlleleName: # Got it
                        flgFound = True
                        var.generated_value = allele[1] # Set up the gene
                        # Check if this locus is actually perturbed
                        if thisIdx in chosenMutateLocii: # YES, TRY TO STEP
                            # Perturb this one
                            var.step_random(stepSize)
                            newAllele = (var.name, var.generated_value)
                            newChromosome.append(newAllele)
                        else: # NO, JUST COPY
                            oldAllele = (var.name, var.generated_value)
                            newChromosome.append(oldAllele)
                            
            new_individuals.append(Individual(newChromosome))         
                
            #try: assert(flgFound)
            #except: 
             #   print "Allele:", thisAlleleName, var.name 
             #   raise 
    
        #self.addToCurrentQueue(newIndividual)
        return new_individuals
    
    
    

#- Recombine --------------------------------
         #numberToPerturb = 1, stepSize = 1, flgVerbose = False)
def simpleRecombine(DSpace, individuals, settings, flgVerbose = False):
    assert(len(individuals)==2)
    mother = individuals[0]
    father = individuals[1]
    
    locii = len(mother.chromosome)
    newChromosome1 = list()
    newChromosome2 = list()
    for locus in range(locii):
        if flgVerbose: print "Locus;", locus
        thisChoice = random.choice(["mother","father"])
        if flgVerbose: print "Choice;", thisChoice
        if thisChoice == "mother":
            newChromosome.append(mother.chromosome[locus])
        elif thisChoice == "father":
            newChromosome.append(father.chromosome[locus])
        
    newIndividual = Individual(newChromosome)
    
    #self.addToCurrentQueue(newIndividual)
    return newIndividuals

def neutralRecombine(DSpace, individuals, settings):
    return DSpace, individuals


#def simpleRecombine(DSpace, settings):
#    assert(DSpace.futureQueue)    
#    updatedQueue = list()
#    for idx in range(int(len(DSpace.futureQueue))):
#        mother = random.choice(DSpace.futureQueue)
#        father = random.choice(DSpace.futureQueue)
#    
#        locii = len(mother.chromosome)
#        newChromosome = list()
#        for locus in range(locii):
#            thisChoice = random.choice(["mother","father"])
#            if thisChoice == "mother":
#                newChromosome.append(mother.chromosome[locus])
#            elif thisChoice == "father":
#                newChromosome.append(father.chromosome[locus])
#        
#        updatedQueue.append(Individual(newChromosome))
#
#    DSpace.futureQueue = updatedQueue
#
#    return DSpace

#- Selection --------------------------------

def neutralSelection(DSpace, settings):
    DSpace.copyFromCurrentToNew()
    return DSpace

def simpleSelection(DSpace, settings):
    DSpace.copyFromCurrentToNew()
    
    #selectionQueue = DSpace.futureQueue()
    for indiv in DSpace.futureQueue:
        print indiv
    return DSpace



class testOperators(unittest.TestCase):
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        
        myLogger.setLevel("CRITICAL")
        
        
        basisVariables = [
                          Variable("C1",50),
                        Variable.ordered("C2",3.14),
                        Variable.ordered('v100',(1,2,3,4)),
                        Variable.unordered('VarStr',["Blue","Red","Green"]),
                        ]
        
        thisDspace = DesignSpace(basisVariables)
        self.D1 = thisDspace 
        
        myLogger.setLevel("DEBUG")
        
    def test010_perturbations(self):
        print "**** TEST {} ****".format(whoami())
        randomIndiv = self.D1.get_random_mapping()
        
        print "Selected random individual:", randomIndiv

        self.assertRaises(Exception, simpleMutate, randomIndiv, 4)

        self.assertRaises(Exception, simpleMutate, randomIndiv, 0)
        
        #print self.D1.percentFinished
        #print self.D1.lenPendingIndividuals
        print "performing 3 successive mutations over the both possible locii:" 
        population = [randomIndiv]
        for idx in range(3): 
            #(DSpace, individuals, settings, numberToPerturb = 1, stepSize = 1, flgVerbose = False):
            DSpace, population = simpleMutate(self.D1,population, None)
            
            #self.D1
            print "    Perturbed child:", population[0]
        #print "Pending list", self.D1.lenPendingIndividuals
        print "Percentage of Dspace covered:", self.D1.percentFinished

    def test090_recombine(self):
        mother = self.D1.get_random_mapping()
        father = self.D1.get_random_mapping()
        print "Mother:", mother
        print "Father:", father
        print "Child1:", recombine(self.D1, [mother, father], None , True)
        print "Child2:", recombine(self.D1, [mother, father], None, True)
        #print "Percentage of Dspace covered:", self.D1.percentFinished




#- Main --------------------------------

if __name__ == "__main__":
    print ABSOLUTE_LOGGING_PATH
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())
    
    #print FREELANCE_DIR
    
    unittest.main()


    import System
    # Get the external test
    suites = [unittest.defaultTestLoader.loadTestsFromName("System")]
    testSuite = unittest.TestSuite(suites)
    text_runner = unittest.TextTestRunner().run(testSuite)
    
    logging.debug("Finished _main".format())
    