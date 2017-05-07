'''
Created on 06.06.2011

@author: mjones
'''

import logging.config
import Variables
import time
from Batch2 import Generation, DesignSpace
#from Generation import Generation
import Utilities
import FileObject
import Genetics

class EvolutionarySystem():

    def __init__(self,
                    name,
                    designSpace,
                    popSize,
                    executablePath,
                    inputTemplateFileObjects,
                    maxProcesses,
                    maxCPUtime,
                    stopping,     
                    mutationProbabilityReal,
                    mutationProbabilityString,
                    crossoverDistributionIndex,
                    mutationDistributionIndex,                                               
                    ):

        self.mutationProbabilityReal        =mutationProbabilityReal, 
        self.mutationProbabilityString      =mutationProbabilityString
        self.crossoverDistributionIndex     =crossoverDistributionIndex
        self.mutationDistributionIndex      =mutationDistributionIndex
                                           
        # Assign from arguments
        self.name = name
        self.designSpace = designSpace
        self.popSize = popSize
        self.systemDirectory = "C:\\DoktoratSim\\" + self.name
        self.executablePath = executablePath
        self.inputTemplateFileObjects = inputTemplateFileObjects
        self.outputResultsFile = r"C:\\DoktoratSim\\" + self.name + "\\results.csv" 

        self.maxProcesses = maxProcesses
        self.maxCPUtime = maxCPUtime
        
        #self.mutationRate,      =  mutationRate,
        self.populationSize,    =  popSize,
        self.stopping,          =  stopping, 
        
        logging.info("Created {0}".format(self))

        self.generationList = list()
 
        #self.createInitialGeneration()

    def __str__(self):
        return "Evolutionary System, name: {0}, design space: {1}, directory: {2}, number input files: {3}".format(self.name, self.designSpace, self.systemDirectory, len(self.inputTemplateFileObjects))

#    def createNextGeneration(self,prevGeneration):
#
#    def createRandomGeneration(self):
#        pass
#        '''
#        The first generation is random
#        '''
        

    
    def createNextGenerationOBSELETE(self):
        
        # Copy the last one
        prevGeneration = self.generationList[-1]
        
        #prin 'Last generation name: ', prevGeneration.name
        #prin 'Last generation runs: ', prevGeneration.finishedQueue
        
        
        
        #prin "From the last generation;"
        for individual in prevGeneration.finishedQueue:
            pass
            #prin individual
#            , "with (", 
#            #prin "Variable vector of: (".format(str(individual.runID)), 
#            for variable in individual.variableVector:
#                prin variable.value, ",",
#            prin ")"
        
        nextGeneration = prevGeneration
        
        self.generationList.append(nextGeneration)
        
    def __iter__(self):
        return self
    
    def next(self):
        
        if len(self.generationList) > self.stopping:
            # The stopping criteria is met, stop system
            raise StopIteration

        elif len(self.generationList) == 0:
            #### CREATE P_0 ####
            
            # This is the first generation, create a random one
               
            logging.info("Evolutionary System '{0}' creating initial generation".format(self.name))
            
            # Create random population
            generationNumber = len(self.generationList)
            generationDirectory = self.systemDirectory + "\\Generation_{0:03d}".format(generationNumber)
            Q_0 = Generation(
                                         str(generationNumber),
                                         generationDirectory,
                                         self.executablePath,
                                         self.inputTemplateFileObjects,
                                         self.maxProcesses,
                                         self.maxCPUtime
                                         )
            Q_0.loadDesignSpace(self.designSpace)
            Q_0.createRandomRuns(self.popSize)
            self.generationList.append(Q_0)
            
            # Evaluate it
            self.generationList[-1].executeParallel()
            
            # Plot it
            print "This is generation", len(self.generationList)            
            self.generationList[-1].plotPopulation(self.systemDirectory)
            
            # Record it
            self.generationList[-1].listFitnesses()
            self.generationList[-1].printResult(self.outputResultsFile)
            
            # Sort it
            Q_0_finished = self.generationList[-1].finishedQueue
            
            Q_0_ranked = Genetics.nonDominatedSort(Q_0_finished)
            
            # Create the next generation
            Q_1 = Genetics.createQ_t(Q_0_ranked,self.popSize,
                                                            self.mutationProbabilityReal,
                       self.mutationProbabilityString,
                       self.crossoverDistributionIndex,
                       self.mutationDistributionIndex,
                                     )
            
            # Put Q_1 into a generation
            generationNumber = len(self.generationList)
            generationDirectory = self.systemDirectory + "\\Generation_{0:03d}".format(generationNumber)
            nextGenerationBlank = Generation(
                                         str(generationNumber),
                                         generationDirectory,
                                         self.executablePath,
                                         self.inputTemplateFileObjects,
                                         self.maxProcesses,
                                         self.maxCPUtime
                                         )
            #firstGeneration.loadDesignSpace(self.designSpace)
            #firstGeneration.createRandomRuns(self.popSize)
            nextGenerationBlank.individualRunList = Q_1
            self.generationList.append(nextGenerationBlank)
            self.generationList[-1].finishRunDefinitions()
            
            print "Hi, Delete"
        else: 
            
            # Evaluate Q_t            
            self.generationList[-1].executeParallel()
            
            # Plot Q_t
            print "This is generation", len(self.generationList)
            self.generationList[-1].plotPopulation(self.systemDirectory)
            
            # Record Q_t
            self.generationList[-1].listFitnesses()
            self.generationList[-1].printResult(self.outputResultsFile)
            
            # Sort it with the previous generation
            Q_t = self.generationList[-1].finishedQueue
            Q_t_minus1 = self.generationList[-2].finishedQueue
            
            R_t = list()
            for individual in Q_t:
                R_t.append(individual)
            for individual in Q_t_minus1:
                R_t.append(individual)
                
            R_t_ranked = Genetics.nonDominatedSort(R_t)
            
            # Create the next generation
            Q_t_plus1 = Genetics.createQ_t(R_t_ranked,self.popSize,
                       self.mutationProbabilityReal,
                       self.mutationProbabilityString,
                       self.crossoverDistributionIndex,
                       self.mutationDistributionIndex,
                                           )
            
            # Put Q_t into a generation
            generationNumber = len(self.generationList)
            generationDirectory = self.systemDirectory + "\\Generation_{0:03d}".format(generationNumber)
            nextGeneration = Generation(
                                         str(generationNumber),
                                         generationDirectory,
                                         self.executablePath,
                                         self.inputTemplateFileObjects,
                                         self.maxProcesses,
                                         self.maxCPUtime
                                         )
            nextGeneration.individualRunList = Q_t_plus1
            self.generationList.append(nextGeneration)   
            self.generationList[-1].finishRunDefinitions()

            
            print self.generationList[-1]
            print "Hi, Delete"

            return

def _oldCisbatScript():
 
    logging.info("Started Evolutionary System test script")

    # Configure the EvolutionarySystem

        
    if 0: # At work
        systemDirectory = r"D:\DoktoratSim\System1"
        outputResultsFile = r"D:\DoktoratSim\System1\results.csv"
        executablePath = r"D:\Programme\Trnsys17\Exe\TRNEXE.exe"
        inputTemplateFileObjects = [
                                    FileObject.FileObject(r"D:\Doktorat\Phase4\CISBATModelTest\B17\BuildingParameterized.b17"),
                                    FileObject.FileObject(r"D:\Doktorat\Phase4\CISBATModelTest\DCK\DeckParameterized.dck"),
                                    ]
        c1 = Variables.Constant("C1",r"ConstantC1","""D:\\Doktorat\Phase4\CISBATModelTest\WEA\CH-Geneve-Cointrin-67000.tm2""")
      
    if 1: # At home
        executablePath = r"C:\Apps\Trnsys17\Exe\TRNEXE.exe"
        inputTemplateFileObjects = [
                                    FileObject.FileObject(r"C:\Doktorat\Phase4\CISBATModelTest\B17\BuildingParameterizedNew.b17"),
                                    FileObject.FileObject(r"C:\Doktorat\Phase4\CISBATModelTest\DCK\DeckParameterized.dck"),
                                    ]
        #c1 = Variables.Constant("C1",r"ConstantC1","""C:\\Doktorat\Phase4\CISBATModelTest\WEA\CH-Geneve-Cointrin-67000.tm2""")
        #c1 = Variables.Constant("C1",r"ConstantC1","""C:\\Doktorat\Phase4\CISBATModelTest\WEA\CA-ON-Toronto-Metr-719920.tm2""")
    maxProc = 4
    maxCPU = 100
            
#    v1 = Variables.RandomFloat("Orientation",r"VarX1",0,180)
#    v2 = Variables.RandomFloat("Window Area",r"VarX2",0.01,6)        
#    v6 = Variables.RandomFloat("Window Area",r"VarX6",0.01,6)
#    v3 = Variables.RandomStringList("Exterior Wall Construction",r"VarX3",("EXT_WALL_LIGHT","EXT_WALL_MEDIUM","EXT_WALL_HEAVY"))
#    v4 = Variables.RandomStringList("Floor Construction",r"VarX4",("EXT_FLOOR_MEDIUM","EXT_WALL_HEAVY"))
#    v5 = Variables.RandomStringList("Window Selection",r"VarX5",("WIN_CASE600","WINASH1","WINASH2","WINASH4"))
#    c1 = Variables.Constant("C1",r"ConstantC1","""C:\\Doktorat\Phase4\CISBATModelTest\WEA\CA-ON-Toronto-Metr-719920.tm2""")
#    c2 = Variables.Constant("C2 Building file location",r"ConstantC2","""..\B17\Building.b17""")
#    c3 = Variables.Constant("C3 Hours",r"ConstantC3","8760")
#                

    designSpaceList = [ 
    Variables.RandomFloat("Orientation",r"VarX1",0,180),
    Variables.RandomFloat("Window Area S",r"VarX2",3,6),        
    Variables.RandomFloat("Window Area EW",r"VarX6",2,6),
    Variables.RandomStringList("Exterior Wall Construction",r"VarX3",("EXT_WALL_LIGHT","EXT_WALL_MEDIUM","EXT_WALL_HEAVY")),
    Variables.RandomStringList("Exterior Wall Construction",r"VarX7",("EXT_ROOF_LIGHT","EXT_ROOF_MEDIUM","EXT_ROOF_HEAVY")),
    Variables.RandomStringList("Floor Construction",r"VarX4",("EXT_FLOOR_LIGHT","EXT_FLOOR_MEDIUM","EXT_FLOOR_HEAVY")),
    Variables.RandomStringList("Window Selection",r"VarX5",("WIN_CASE600","WINASH1","WINASH2","WINASH4")),
    Variables.Constant("C1",r"ConstantC1","""C:\\Doktorat\Phase4\CISBATModelTest\WEA\CH-Geneve-Cointrin-67000.tm2"""),
    Variables.Constant("C2 Building file location",r"ConstantC2","""..\B17\Building.b17"""),
    Variables.Constant("C3 Hours",r"ConstantC3","8760"),
    ]   
    
    thisDesignSpace = DesignSpace('Test Design Space',designSpaceList)

    #systemName = 'Test System'
    #mutationProbabilityReal = 0.05
    #mutationProbabilityString = 0.05
    #crossoverDistributionIndex = 5
    #mutationDistributionIndex = 5
    #populationSize = 50 # MUST BE EVEN
    #numberOfGenerations = 20
    #outputResultsFile = r"C:\DoktoratSim\System1\results.csv"
    #systemDirectory = r"C:\DoktoratSim\System1"
    
#    thisSystem = EvolutionarySystem(
#                                systemName,
#                                thisDesignSpace,
#                                populationSize,
#                                systemDirectory,
#                                executablePath,
#                                inputTemplateFileObjects,
#                                maxProc,
#                                maxCPU,
#                                populationSize,
#                                numberOfGenerations,
#                                outputResultsFile,
#                                mutationProbabilityReal,
#                                mutationProbabilityString,
#                                crossoverDistributionIndex,
#                                mutationDistributionIndex,
#                                )

    systemSuperList = []
############################## 1
#    systemName                    = "BasicTwentyTwenty"           
#    thisDesignSpace               = thisDesignSpace   
#    populationSize                = 20                  
#    executablePath                = r"C:\\Apps\Trnsys17\\Exe\\TRNEXE.exe"                  
#    inputTemplateFileObjects      = inputTemplateFileObjects                  
#    maxProc                       = 4                  
#    maxCPU                        = 100                  
#    numGens                       = 100
#    mutationProbabilityReal       = 0.05                  
#    mutationProbabilityString     = 0.05                  
#    crossoverDistributionIndex    = 5                  
#    mutationDistributionIndex     = 5                  
#
#
#    thisSystem = EvolutionarySystem(
#                       systemName                    ,
#                       thisDesignSpace               ,
#                       populationSize                ,
#                       executablePath                ,
#                       inputTemplateFileObjects      ,
#                       maxProc                       ,
#                       maxCPU                        ,
#                       numGens                       ,
#                       mutationProbabilityReal       ,
#                       mutationProbabilityString     ,
#                       crossoverDistributionIndex    ,
#                       mutationDistributionIndex     ,
#                       )    
#    systemSuperList.append(thisSystem)
#    
############################## 2
#
#    systemName                    = "HighDistribTwentyTwenty"           
#    thisDesignSpace               = thisDesignSpace   
#    populationSize                = 20                  
#    executablePath                = r"C:\\Apps\Trnsys17\\Exe\\TRNEXE.exe"                  
#    inputTemplateFileObjects      = inputTemplateFileObjects                  
#    maxProc                       = 4                  
#    maxCPU                        = 100                  
#    numGens                       = 100       
#    mutationProbabilityReal       = 0.05                  
#    mutationProbabilityString     = 0.05                  
#    crossoverDistributionIndex    = 20                  
#    mutationDistributionIndex     = 20                  
#
#
#    thisSystem = EvolutionarySystem(
#                       systemName                    ,
#                       thisDesignSpace               ,
#                       populationSize                ,
#                       executablePath                ,
#                       inputTemplateFileObjects      ,
#                       maxProc                       ,
#                       maxCPU                        ,
#                       numGens                       ,
#                       mutationProbabilityReal       ,
#                       mutationProbabilityString     ,
#                       crossoverDistributionIndex    ,
#                       mutationDistributionIndex     ,
#                       )    
#    systemSuperList.append(thisSystem)
#    
############################## 3
#
#    systemName                    = "HighMutation"           
#    thisDesignSpace               = thisDesignSpace   
#    populationSize                = 20                  
#    executablePath                = r"C:\\Apps\Trnsys17\\Exe\\TRNEXE.exe"                  
#    inputTemplateFileObjects      = inputTemplateFileObjects                  
#    maxProc                       = 4                  
#    maxCPU                        = 100                  
#    numGens                       = 50       
#    mutationProbabilityReal       = 0.25                  
#    mutationProbabilityString     = 0.25                  
#    crossoverDistributionIndex    = 5                  
#    mutationDistributionIndex     = 5                  
#
#
#    thisSystem = EvolutionarySystem(
#                       systemName                    ,
#                       thisDesignSpace               ,
#                       populationSize                ,
#                       executablePath                ,
#                       inputTemplateFileObjects      ,
#                       maxProc                       ,
#                       maxCPU                        ,
#                       numGens                       ,
#                       mutationProbabilityReal       ,
#                       mutationProbabilityString     ,
#                       crossoverDistributionIndex    ,
#                       mutationDistributionIndex     ,
#                       )    
#    systemSuperList.append(thisSystem)
#
############################### 4
#
#    systemName                    = "LowPopulation"           
#    thisDesignSpace               = thisDesignSpace   
#    populationSize                = 6                  
#    executablePath                = r"C:\\Apps\Trnsys17\\Exe\\TRNEXE.exe"                  
#    inputTemplateFileObjects      = inputTemplateFileObjects                  
#    maxProc                       = 4                  
#    maxCPU                        = 100                  
#    numGens                       = 50       
#    mutationProbabilityReal       = 0.05                  
#    mutationProbabilityString     = 0.05                  
#    crossoverDistributionIndex    = 5                  
#    mutationDistributionIndex     = 5                  
#
#
#    thisSystem = EvolutionarySystem(
#                       systemName                    ,
#                       thisDesignSpace               ,
#                       populationSize                ,
#                       executablePath                ,
#                       inputTemplateFileObjects      ,
#                       maxProc                       ,
#                       maxCPU                        ,
#                       numGens                       ,
#                       mutationProbabilityReal       ,
#                       mutationProbabilityString     ,
#                       crossoverDistributionIndex    ,
#                       mutationDistributionIndex     ,
#                       )    
#    systemSuperList.append(thisSystem)


############################## 6
#
#    systemName                    = "HighPopHighMutate"           
#    thisDesignSpace               = thisDesignSpace   
#    populationSize                = 100                  
#    executablePath                = r"C:\\Apps\Trnsys17\\Exe\\TRNEXE.exe"                  
#    inputTemplateFileObjects      = inputTemplateFileObjects                  
#    maxProc                       = 4                  
#    maxCPU                        = 100                  
#    numGens                       = 5       
#    mutationProbabilityReal       = 0.25                  
#    mutationProbabilityString     = 0.25                  
#    crossoverDistributionIndex    = 5                  
#    mutationDistributionIndex     = 5                  
#
#
#    thisSystem = EvolutionarySystem(
#                       systemName                    ,
#                       thisDesignSpace               ,
#                       populationSize                ,
#                       executablePath                ,
#                       inputTemplateFileObjects      ,
#                       maxProc                       ,
#                       maxCPU                        ,
#                       numGens                       ,
#                       mutationProbabilityReal       ,
#                       mutationProbabilityString     ,
#                       crossoverDistributionIndex    ,
#                       mutationDistributionIndex     ,
#                       )    
#    systemSuperList.append(thisSystem)
#    
############################## 7
#
#    systemName                    = "ReallyHighMutation"           
#    thisDesignSpace               = thisDesignSpace   
#    populationSize                = 20                  
#    executablePath                = r"C:\\Apps\Trnsys17\\Exe\\TRNEXE.exe"                  
#    inputTemplateFileObjects      = inputTemplateFileObjects                  
#    maxProc                       = 4                  
#    maxCPU                        = 100                  
#    numGens                       = 50       
#    mutationProbabilityReal       = 0.75                  
#    mutationProbabilityString     = 0.75                  
#    crossoverDistributionIndex    = 5                  
#    mutationDistributionIndex     = 5                  
#
#
#    thisSystem = EvolutionarySystem(
#                       systemName                    ,
#                       thisDesignSpace               ,
#                       populationSize                ,
#                       executablePath                ,
#                       inputTemplateFileObjects      ,
#                       maxProc                       ,
#                       maxCPU                        ,
#                       numGens                       ,
#                       mutationProbabilityReal       ,
#                       mutationProbabilityString     ,
#                       crossoverDistributionIndex    ,
#                       mutationDistributionIndex     ,
#                       )    
#    systemSuperList.append(thisSystem)   

############################## 5

    systemName                    = "HighPopulation"           
    thisDesignSpace               = thisDesignSpace   
    populationSize                = 100                  
    executablePath                = r"C:\\Apps\Trnsys17\\Exe\\TRNEXE.exe"                  
    inputTemplateFileObjects      = inputTemplateFileObjects                  
    maxProc                       = 4                  
    maxCPU                        = 100                  
    numGens                       = 100       
    mutationProbabilityReal       = 0.05                  
    mutationProbabilityString     = 0.05                  
    crossoverDistributionIndex    = 5                  
    mutationDistributionIndex     = 5                  


    thisSystem = EvolutionarySystem(
                       systemName                    ,
                       thisDesignSpace               ,
                       populationSize                ,
                       executablePath                ,
                       inputTemplateFileObjects      ,
                       maxProc                       ,
                       maxCPU                        ,
                       numGens                       ,
                       mutationProbabilityReal       ,
                       mutationProbabilityString     ,
                       crossoverDistributionIndex    ,
                       mutationDistributionIndex     ,
                       )    
    systemSuperList.append(thisSystem)

    
############################## 9
#
#    systemName                    = "Test3"           
#    thisDesignSpace               = thisDesignSpace   
#    populationSize                = 20                  
#    executablePath                = r"C:\\Apps\Trnsys17\\Exe\\TRNEXE.exe"                  
#    inputTemplateFileObjects      = inputTemplateFileObjects                  
#    maxProc                       = 4                  
#    maxCPU                        = 100                  
#    numGens                       = 50       
#    mutationProbabilityReal       = 0.05                  
#    mutationProbabilityString     = 0.05                  
#    crossoverDistributionIndex    = 5                  
#    mutationDistributionIndex     = 5                  
#
#
#    thisSystem = EvolutionarySystem(
#                       systemName                    ,
#                       thisDesignSpace               ,
#                       populationSize                ,
#                       executablePath                ,
#                       inputTemplateFileObjects      ,
#                       maxProc                       ,
#                       maxCPU                        ,
#                       numGens                       ,
#                       mutationProbabilityReal       ,
#                       mutationProbabilityString     ,
#                       crossoverDistributionIndex    ,
#                       mutationDistributionIndex     ,
#                       )    
#    systemSuperList.append(thisSystem)

############################## 10
#
#    systemName                    = "Test"           
#    thisDesignSpace               = thisDesignSpace   
#    populationSize                = 20                  
#    executablePath                = r"C:\\Apps\Trnsys17\\Exe\\TRNEXE.exe"                  
#    inputTemplateFileObjects      = inputTemplateFileObjects                  
#    maxProc                       = 4                  
#    maxCPU                        = 100                  
#    numGens                       = 50       
#    mutationProbabilityReal       = 0.05                  
#    mutationProbabilityString     = 0.05                  
#    crossoverDistributionIndex    = 5                  
#    mutationDistributionIndex     = 5                  
#
#
#    thisSystem = EvolutionarySystem(
#                       systemName                    ,
#                       thisDesignSpace               ,
#                       populationSize                ,
#                       executablePath                ,
#                       inputTemplateFileObjects      ,
#                       maxProc                       ,
#                       maxCPU                        ,
#                       numGens                       ,
#                       mutationProbabilityReal       ,
#                       mutationProbabilityString     ,
#                       crossoverDistributionIndex    ,
#                       mutationDistributionIndex     ,
#                       )    
#    systemSuperList.append(thisSystem)

    for system in systemSuperList:
        for generation in system:
            pass

    logging.info("Ended Evolutionary System test script")
    
def _mathExecute():
    logging.info("Math execute test script")
    
    pass 

if __name__ == "__main__":

    # Load the logging configuration
    logging.config.fileConfig('..\\LoggingConfig\\loggingNofile.conf')
    _mathExecute()