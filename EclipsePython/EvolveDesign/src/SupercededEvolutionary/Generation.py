'''
Created on May 10, 2011

@author: UserXP
'''
from Batch2 import Batch2, DesignSpace

from SimulationRuns import TrnsysRunGA
import logging.config
import random
import re
import Variables

logging.config.fileConfig('..\\LoggingConfig\\logging.conf')


class Generation(Batch2):
    
    # Override the Batch object's INIT
    
    def __init__(
                 self,
                 name,
                 batchPath,
                 executablePath,
                 maxProcesses,
                 maxCPUtime,
                 ):
        
        # Call the batch
        super(Generation,self).__init__(
                 name,
                 batchPath,
                 executablePath,
                 maxProcesses,
                 maxCPUtime,
                 )

    def createInitialGeneration(self, popSize, designSpace, inputFilePath):
                
        self.popSize = popSize
        self.inputFilePath = inputFilePath
        self.designSpace = designSpace
        self.loadTemplate(inputFilePath)
        self.createRandomIndividuals(self.popSize)



#    def __init__(self):
#        
#        self.popSize = 20
#        self.lowBounds = [0,0,0]
#        self.upBounds = [1,1,1]
#        
#        self.runList = list()
#        self.individualRunList = list()
#        self.liveQueue = list()    
#    
    
#    def createRandomPopulation(self):
#        
#        batchPath = "asldk"
#        executablePath = "dsf"
#        inputFileTemplate = "h"
#        
#        #genome = [0.5, 0.5, 0.5]
#        
#        inputTranslationList = []
#        
#        # Create popSize individuals
#        for indiv in range(self.popSize):
#            
#            runID = indiv
#            prin "On indiv", indiv
#            
#            # Start this indiv genome
#            thisGenome = []
#            
#            # Append new random genes to the thisGenome
#            for geneCnt in range(len(self.lowBounds)):
#                thisGenome.append(random.uniform(self.lowBounds[geneCnt], self.upBounds[geneCnt]))
#            
#            
#            # Create the translation list
#            inputTranslationList = []
#            count = 0
#            for gene in thisGenome:
#                searchString = 'VarX' + str(indiv) + '_Test .+'
#                replaceString = 'VarX' + str(indiv) + '_Test = ' + str(gene)
#                prin searchString, replaceString
#                pair = (re.compile(searchString, re.U|re.M), replaceString)
#                inputTranslationList.append(pair)
#                count += 1            
#            
#            # Create the individual
#            self.runList.append(TrnsysRunGA(
#                        runID, 
#                        batchPath + "\\Run_" + str(runID),
#                        executablePath,
#                        inputFileTemplate,
#                        inputTranslationList,
#                                        )
#        )
#            #value = random.uniform(self.lowBound, self.upBound)
#            #prin value

if __name__ == "__main__":

  
    logging.info("Started BATCH test script")

    # Configure the batch
    genName = 'Gen1'
    popSize = 2
    projDirectory = r"D:\Doktorat\Phase4\Batch1"
    executablePath = "C:\Apps\Trnsys17\Exe\TRNEXE.exe"
    inputFilePath = r"D:\Doktorat\Phase4\TestTrnsysProject\Begin.dck"
    maxProc = 4
    maxCPU = 100
    
    v1 = Variables.RandomFloat("A1",r"VarX1",0,60)
    v2 = Variables.RandomFloat("A2",r"VarX2",0,3)        
    v3 = Variables.RandomStringList("A3",r"DefaultMaterial",("Wood","Steel","Cheese"))
    
    thisDesignSpace = DesignSpace('Test Design Space',[v1,v2,v3])
    
    
    thisGeneration = Generation(
                                genName,
                                projDirectory,
                                executablePath,
                                maxProc,
                                maxCPU,
                                )

