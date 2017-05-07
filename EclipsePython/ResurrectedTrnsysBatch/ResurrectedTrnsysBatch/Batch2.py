'''
Created on Mar 24, 2011

@author: UserXP
'''
#import Plotting
import Variables
#import Utilities
import SimulationRuns
#import psutil
import datetime
import time
import logging.config
import random
from copy import deepcopy


#log = logging.getLogger(__name__)



class DesignSpace(object):
    
    def __init__(self, name, variableList): 
        self.name = name
        self.variableList = variableList
        
        logString = "Created DesignSpace '{0}' with {1} variables:".format(self.name, len(self.variableList))
        
        logging.info(logString)

        count = 0
        for designVariable in self.variableList:
            logging.info("{0} Variable {1}: {2}".format(self,count,designVariable))
            count += 1
#            logging.info("   Variable: {0}, a {1} of magnitude {2} targeting '{3}', = {4}".format(
#                                                       designVariable.name,
#                                                       designVariable.type,
#                                                       thisVarLen,
#                                                       designVariable.regexTarget.pattern,
#                                                       round(designVariable.value,2)
#                                                       ))
    def __len__(self):
        return len(self.variableList)
    
    def __iter__(self):
        self.iterIndex = 0
        return self
    
    def __str__(self):
        return self.name
    
    # Custom iterator, the variable will return the target Regex with 
    # the current variable
    def next(self):
        if self.iterIndex < len(self):
            current = self.variableList[self.iterIndex]
        else: 
            raise StopIteration
        self.iterIndex += 1
        return (current)    
    
class Batch2(object):
    '''
    classdocs
    '''

    def __init__(self,
                 name,
                 batchPath,
                 executablePath,
                 inputTemplateFileObjects,
                 maxProcesses,
                 maxCPUtime
                 ):
        '''
        Constructor
        '''
        self.executionDelay = 5
        
        # Assign from arguments
        self.name = name
        self.batchPath = batchPath
        self.executablePath = executablePath
        self.inputTemplateFileObjects = inputTemplateFileObjects
        
        # The three lists
        self.runList = list()
        self.individualRunList = list()
        self.liveQueue = list()
        self.pendingQueue = list()
        self.finishedQueue = list()
        self.postProcessingQueue = list()
        
        # Computer resources
        self.maxProcesses = maxProcesses
        self.maxCPUtime = maxCPUtime
        self.computerResources = ComputerResources()
        
        # Timing
        self.startTime = 0
        self.endTime = 0

        logString = "Created {0}".format(self)
        logging.info(logString)
        
        # Initialize the batch 
#        self.loadTemplate()
#        self.createGlobalSearchRunList()
#        self.createIndividuals()

#    def loadFileObjects(self, inputFileTemplatePaths):

    def loadTemplatePaths(self, inputFileTemplatePaths):
        
        if isinstance(inputFileTemplatePaths, basestring):
            inputFileTemplatePaths = [inputFileTemplatePaths]

        self.inputFileTemplatePaths = inputFileTemplatePaths
        
        for inputFileTemplatePath in self.inputFileTemplatePaths:
            #prin 'reading:', self.inputFileTemplatePath
            fIn = open(inputFileTemplatePath,'r')
            # Don't read unicode... inputFileTemplate=unicode(fIn.read(),'utf-8')
            # Add this template file
            self.inputFileTemplates.append(fIn.read())
            fIn.close()
            logString = "{0} loaded into Batch '{1}'".format(inputFileTemplatePath, self.name)
            logging.info(logString)

        logString = "{0} Template files loaded into Batch '{1}'".format(len(self.inputFileTemplatePaths), self.name)
        #print self.inputFileTemplatePaths
        logging.info(logString)

    def loadDesignSpace(self, designSpace):
        self.designSpace = designSpace
        
        logString = "Loaded the '{0}' design space into '{1}'".format(self.designSpace.name, self.name)
        logging.info(logString)
        
    def createRandomRuns(self, popSize):
        runID = 0
        logging.info("Creating random runs for {0}".format(self))
        
        for runNumber in xrange(0,popSize):
#            
#            for run in self.individualRunList:
#                logging.info("Top of FOR: {0}".format(run))
#            
            # create a new random variable list 
            thisVariableVector = list()
            
#            for run in self.individualRunList:
#                logging.info(": {0}".format(run))
            
            for variable in self.designSpace:
                # First, copy the uninitialized variable from the design space

                newVariable = deepcopy(variable)
                # Initialize it
                newVariable.new()
                # Append it 
                thisVariableVector.append(newVariable)
            
            #            for run in self.individualRunList:
            #                logging.info("After Reinit: {0}".format(run))
            #                        
            logging.info("Created a random variable vector: {0}".format(thisVariableVector))
            
            newRun = SimulationRuns.TrnsysRun(
                runID, 
                self.batchPath + "\\Individual_{0:03d}".format(runID),
                self.executablePath,
                self.inputTemplateFileObjects,
                thisVariableVector
                )
            
            
            # Using this random run, create an individual
            logging.info("Appending {0} to {1}".format(newRun,self))
            
            self.individualRunList.append(newRun)
#            for run in self.individualRunList:
#                logging.info("Current random run list: {0}".format(run))

            runID += 1
             
        for run in self.individualRunList:
            logging.info("Random run list summary: {0}".format(run))
                    
        
#    def createRandomIndividuals(self, popSize):
#        runID = 0
#
#        for runNumber in xrange(0,popSize):
#            # create a random variable run
#            thisRun = list()
#            for variable in self.designSpace:
#                variable.new()
#                thisRun.append(variable)
#            # Using this random run, create an individual
#            self.individualRunList.append(
#                        SimulationRuns.TrnsysRunGA(
#                            runID, 
#                            self.batchPath + "\\Run_" + str(runID),
#                            self.executablePath,
#                            self.inputFileTemplate,
#                            thisRun
#                            )
#                        ) 
#            runID += 1 

    
#    def createRandomRunList(self, popSize):
#        for runNumber in xrange(0,popSize):
#            for variable in self.designSpace:
#                variable.new()
#                prin variable.value,
#            prin 
#            #prin self.designSpace
#            #prin runNumber
        
    
    def createGlobalSearchRunList(self):
        '''
        This will create a nested for-loop on the fly, so that each
        possible combination is represented
         
        Example, for 3 variables:
        [<Variables.FloatList object at 0x00D012F0>, <Variables.FloatList object at 0x00D01990>, <Variables.StringList object at 0x00D019D0>]
        
        The exec code is:
        for v0 in self.designSpace.variableList[0]:
            for v1 in self.designSpace.variableList[1]:
                for v2 in self.designSpace[2].variableList:
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
        
        i = 0
        evalValueStr = "("
        evalForStr = ""
        #prin self.designSpace
        for variable in self.designSpace.variableList:
            evalValueStr += "v" + str(i) + ","
            evalForStr += "\t"*i + "for v" + str(i) + " in self.designSpace.variableList[" + str(i) + "]:\n" 
            i += 1
        evalValueStr = "\t"*i + " runList.append(" + evalValueStr + "))\n"
        evalStr = evalForStr + evalValueStr
        runList = [] 
        #prin evalStr   
        exec(evalStr)
        #prin runList

        self.runList = runList

        logString = "Created a run list over {0} design variables with {1} runs".format(len(self.designSpace),len(runList))
        logging.info(logString)
               
    
    def createIndividuals(self):
        logging.info("Creating individuals for {0}".format(self))
        
        runID = 0
        for run in self.runList:
            
#            thisVariableVector = list()            
#            for variable in self.designSpace:
#                newVariable = deepcopy(variable)
#                # Initialize it
#                print newVariable
#                newVariable.new()
#                # Append it 
#                thisVariableVector.append(newVariable)
#            
#            #            for run in self.individualRunList:
#            #                logging.info("After Reinit: {0}".format(run))
#            #                                    
#
#
#
            print "Here is the run, transform to name/val?:",run
            print "Here is the ds, transform to name/val?:",run
            self.individualRunList.append(
                        SimulationRuns.TrnsysRun(
                            runID, 
                            self.batchPath + "\\Run_{0:03d}".format(runID),
                            self.executablePath,
                            self.inputTemplateFileObjects,
                            run
                            )
                        ) 
            runID += 1 


    def createIndividualsFrom (self, popSize):
        runID = 0
        logging.info("Creating random runs for {0}".format(self))
        
        for runNumber in xrange(0,popSize):
#            
#            for run in self.individualRunList:
#                logging.info("Top of FOR: {0}".format(run))
#            
            # create a new random variable list 
            thisVariableVector = list()
            
#            for run in self.individualRunList:
#                logging.info(": {0}".format(run))
            
            for variable in self.designSpace:
                # First, copy the uninitialized variable from the design space

                newVariable = deepcopy(variable)
                # Initialize it
                newVariable.new()
                # Append it 
                thisVariableVector.append(newVariable)
            
            #            for run in self.individualRunList:
            #                logging.info("After Reinit: {0}".format(run))
            #                        
            logging.info("Created a random variable vector: {0}".format(thisVariableVector))
            
            newRun = SimulationRuns.TrnsysRun(
                runID, 
                self.batchPath + "\\Individual_{0:03d}".format(runID),
                self.executablePath,
                self.inputTemplateFileObjects,
                thisVariableVector
                )
            
            
            # Using this random run, create an individual
            logging.info("Appending {0} to {1}".format(newRun,self))
            
            self.individualRunList.append(newRun)
#            for run in self.individualRunList:
#                logging.info("Current random run list: {0}".format(run))

            runID += 1
             
        for run in self.individualRunList:
            logging.info("Random run list summary: {0}".format(run))

    
    def executeSerial(self):

        self.startTime = datetime.datetime.now()
        self.pendingQueue = self.individualRunList


        logString = "Executing runs at {0}".format(self.startTime  )
        logging.info(logString)
    

        for run in self.individualRunList:
            run.createProject()
            run.translateInputFile()
            run.writeTranslatedInputFile()

    def finishRunDefinitions(self):
        
        runID = 0
        for individual in self.individualRunList:
            individual.name = str(runID)
            individual.runID = runID

            individual.runDirectory = self.batchPath + "\\Run_{0:03d}".format(runID)
            individual.executablePath = self.executablePath
            individual.inputTemplateFileObjects = self.inputTemplateFileObjects
            #individual.inputTemplateFileObjects = self.inputTemplateFileObjects
            #individual.outputFilesPath
            #individual.runDirectory = self.batchPath
            runID += 1   
            
        print "Finished run defs"
            

    def executeParallel(self):
        self.startTime = datetime.datetime.now()
        
        # Move all of the runs into the pending queue
        self.pendingQueue = self.individualRunList

        logString = "Executing runs at {0}".format(self.startTime  )
        logging.info(logString)
 
        # Loop continuously if there are still pending, live, or to-be-processed runs
        while len(self.pendingQueue) or len(self.liveQueue) or len(self.postProcessingQueue):
            
            # Wait for system a little
            time.sleep(self.executionDelay)
            
            # Return the current state of the computer
            currentCPU = self.computerResources.current_CPU()

            # Check to see if another run can be executed
            for run in self.pendingQueue:
                run.update()
                # Execute if resources available
                if (currentCPU <= self.maxCPUtime) and  (len(self.liveQueue) < self.maxProcesses):
                    # Move the run into live queue
                    self.liveQueue.append(run)
                    self.pendingQueue.remove(run)
                    run.createProject()
                    run.translateInputFiles()
                    run.writeTranslatedInputFile()
                    run.execute()
                    # Break out of the Pending loop
                    break

            # Check on the live runs and move completed into post-processing
            for run in self.liveQueue:
                run.update()
                # Move off the live queue if finished
                # Could use Filter here! Replace for loop!!!!!
                # Actually, LIST COMPREHENSION would be better
                if run.status["execution"] == "Finished":
                    # The run is now finished, send to post-process
                    self.postProcessingQueue.append(run)
                    self.liveQueue.remove(run)
            
            # Do any post-processing
            for run in self.postProcessingQueue:
                run.postProcess()
                self.finishedQueue.append(run)
                self.postProcessingQueue.remove(run)
                logString = "Post-processed {0}" .format(run)
                logging.info(logString)

            logString = "CPU: {0}, Pending: {1}, Live: {2}, Pending Processing: {3}, Finished: {3}" .format(str(currentCPU), len(self.pendingQueue),len(self.liveQueue),len(self.postProcessingQueue),len(self.finishedQueue))
            logging.info(logString)
        
            
#            prin ["CPU:", , "Pending:", 
#                len(self.pendingQueue), "Live:", len(self.liveQueue), 
#                "Finished", len(self.finishedQueue)]
        self.endTime = datetime.datetime.now()
        self.deltaTime = self.endTime - self.startTime

        logString = "Finished execution of runs with {0} parallel threads and a {1} CPU limit" .format(self.maxProcesses, self.maxCPUtime)
        logging.info(logString)

        logString = "Total real execution time: {0}" .format(self.deltaTime)
        logging.info(logString)

        logString = "MaxThread {0}, CPU limit {1}, Time: {2}" .format(self.maxProcesses, self.maxCPUtime, self.deltaTime)
        logging.info(logString)
        
        #prin "Total real execution time:", self.deltaTime
#        prin ("MaxThread", , "CPU limit",
#               , "Time", )


    def executeWithoutExecuting(self):
        self.startTime = datetime.datetime.now()
        self.pendingQueue = self.individualRunList

        logString = "Executing runs at {0}".format(self.startTime  )
        logging.info(logString)
    

        #prin "Executing runs at", self.startTime  
        # Loop continuously if there are still pending runs
        while len(self.pendingQueue) or len(self.liveQueue):
            time.sleep(2)
            
            currentCPU = self.computerResources.current_CPU()
            
            # Update the Live
            for run in self.liveQueue:
                run.update()
                
                # The run is IMMEDIATELY 'Finished'
                run.status["execution"] = "Finished"
                # The run is IMMEDIATELY 'Finished'
                
                # Move off the live queue if finished
                # Could use Filter here! Replace for loop!!!!!
                # Actually, LIST COMPREHENSION would be better
                if run.status["execution"] == "Finished":
                    self.finishedQueue.append(run)
                    self.liveQueue.remove(run)
            
            # Update the Pending 
            for run in self.pendingQueue:
                run.update()
                # Execute if resources available
                if (currentCPU <= self.maxCPUtime) and  (len(self.liveQueue) < self.maxProcesses):
                    # Move the run into live queue
                    self.liveQueue.append(run)
                    self.pendingQueue.remove(run)
                    run.createProject()
                    run.translateInputFile()
                    run.writeTranslatedInputFile()
                    ### DON'T EXECUTE !!!!!!!!!!!!!! ###
                    #run.execute()
                    ### DON'T EXECUTE !!!!!!!!!!!!!! ###
                    # Break out of the Pending loop
                    break
            

            logString = "CPU: {0}, Pending: {1}, Live: {2}, Finished:" .format(str(currentCPU), len(self.pendingQueue),len(self.liveQueue),len(self.finishedQueue))
            logging.info(logString)
    
            
#            prin ["CPU:", , "Pending:", 
#                len(self.pendingQueue), "Live:", len(self.liveQueue), 
#                "Finished", len(self.finishedQueue)]
        self.endTime = datetime.datetime.now()
        self.deltaTime = self.endTime - self.startTime

        logString = "Finished execution of runs with {0} parallel threads and a {1} CPU limit" .format(self.maxProcesses, self.maxCPUtime)
        logging.info(logString)

        logString = "Total real execution time: {0}" .format(self.deltaTime)
        logging.info(logString)

        logString = "MaxThread {0}, CPU limit {1}, Time: {2}" .format(self.maxProcesses, self.maxCPUtime, self.deltaTime)
        logging.info(logString)
        
       
        
    def __len__(self):
        piSigma = 1
        for variable in self.designSpace:
            piSigma = piSigma * len(variable) 
        return piSigma   
    
    def __str__(self):
        return  "Batch name: {0}, num input templates: {1}, num Pending runs: {2}, Live: {3}, Finished: {4}, in directory: {5},".format(self.name, len(self.inputTemplateFileObjects,),len(self.pendingQueue),len(self.liveQueue),len(self.finishedQueue),self.batchPath)

class ComputerResources():
    def __init__(self): pass
        # Stores the cpu averaging list
#        self.cpuPercents = deque([0,0,0,0,0])
#        self.currentAverageCPU = 0
#        self.currentCPU = 0
#    def update(self):
#        # Update the average CPU percent
#        self.cpuPercents.pop()
#        self.cpuPercents.appendleft(psutil.cpu_percent())
#        self.currentAverageCPU = sum(self.cpuPercents)/len(self.cpuPercents)
#        self.currentCPU = psutil.cpu_percent()
    def current_CPU(self):
        return psutil.cpu_percent()

class Generation(Batch2):
    
    # Override the Batch object's INIT
    
    def __init__(
                 self,
                 name,
                 batchPath,
                 executablePath,
                 inputTemplateFileObjects,                 
                 maxProcesses,
                 maxCPUtime,
                 ):
        
        # Call the batch
        super(Generation,self).__init__(
                 name,
                 batchPath,
                 executablePath,
                 inputTemplateFileObjects,
                 maxProcesses,
                 maxCPUtime,
                 )

    def createInitialGeneration(self, popSize, designSpace, inputFilePath):
                
        self.popSize = popSize
        self.inputFilePath = inputFilePath
        self.designSpace = designSpace
        self.loadTemplate(inputFilePath)
        self.createRandomIndividuals(self.popSize)

    def listFitnesses(self):
        for run in self.finishedQueue:
            print run.fitness.showTextResultVector()

    def plotPopulation(self,systemDirectory):
        resultX = list()
        resultY = list()
        resultLabel = list()
        
        for run in self.finishedQueue:
            resultX.append(run.fitness.results[0].value)
            resultY.append(run.fitness.results[1].value)
            resultLabel.append(run.name)
#            for result in run.fitness.results:
#                results_p.append(result.value)
        #print resultX
        #print resultY
        
        savePath = systemDirectory + "\\Generation {0:03d}".format(int(self.name)) + ".pdf"
        title = "Generation {0}".format(self.name)
        Plotting.SimplePlot(resultX,resultY,title,resultLabel,False,savePath)
        #Plotting.SimplePlot([1,2,3,4], [1,4,9,16])
        #Plotting.SimplePlot([],resultY)


 

    def printResult(self,targetFilePath):
        
        #Add the title
        resultString = "Generation " + self.name
        resultString += "\n"

        resultFile = open(targetFilePath,'a')
        resultFile.write(resultString)
        resultFile.close()
        
        logString = "Wrote result to file"
        logging.info(logString)          
        
        for run in self.finishedQueue:
            run.printOutResult(targetFilePath)
       
       
if __name__ == "__main__":

    # Load the logging configuration

    logging.info("Started BATCH test script")

    # Configure the batch
    executablePath = "C:\Apps\Trnsys17\Exe\TRNEXE.exe"
    projDirectory = r"D:\Temp"
    inputFilePath = r"D:\Doktorat\Phase4\TestTrnsysProject\Begin.dck"
    maxProc = 4
    maxCPU = 100
    
    # Define the design space
#    v1 = Variables.Float("A1",r"VarX1",0,30,60)
#    v2 = Variables.Float("A2",r"VarX2",0,1,3)
#    v1 = Variables.RandomFloat("A1",r"VarX1",0,-1,60,20)
#    v2 = Variables.RandomFloat("A2",r"VarX2",0,-1,3,20)
    
    v1 = Variables.RandomFloat("A1",r"VarX1",0,60)
    v2 = Variables.RandomFloat("A2",r"VarX2",0,3)        
    v3 = Variables.RandomStringList("A3",r"DefaultMaterial",("Wood","Steel","Cheese"))
    
    thisDesignSpace = DesignSpace('Test Design Space',[v1,v2,v3])
    
    # Create the batch
    batch = Batch2('Test Batch', projDirectory, executablePath, inputFilePath, maxProc, maxCPU)
#                     name,
#                 batchPath,
#                 executablePath,
#                 inputTemplateFileObjects,
#                 maxProcesses,
#                 maxCPUtime
    batch.loadDesignSpace(thisDesignSpace)
    batch.loadTemplatePaths(inputFilePath)
    #batch.createGlobalSearchRunList()
    #batch.createRandomRunList(20)
    batch.createRandomRuns(2)
    
    print batch
    for run in batch.individualRunList:
        print run
    
    # Execute the batch
    #batch.executeParallel()
    
    

    logging.info("Stopped BATCH test script")
        
    

    if 0:
        # Load the logging configuration
        logging.config.fileConfig('..\\Log files\\logging.conf')
        
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


        