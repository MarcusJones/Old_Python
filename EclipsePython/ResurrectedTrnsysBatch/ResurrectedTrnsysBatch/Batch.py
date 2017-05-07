'''
Created on Mar 24, 2011

@author: UserXP
'''

import Variables
import Utilities
import SimulationRuns
import psutil
import datetime
import time
import logging.config
#log = logging.getLogger(__name__)

class Batch(object):
    '''
    classdocs
    '''

    def __init__(self,
                 designSpace,
                 batchPath,
                 executablePath,
                 inputFileTemplatePath,
                 maxProcesses,
                 maxCPUtime
                 ):
        '''
        Constructor
        '''
        
        
        # Assign from arguments
        self.designSpace = designSpace
        self.batchPath = batchPath
        self.executablePath = executablePath
        self.inputFileTemplatePath = inputFileTemplatePath
        
        # The three lists
        self.runList = list()
        self.individualRunList = list()
        self.liveQueue = list()
        self.pendingQueue = list()
        self.finishedQueue = list()
        self.maxProcesses = maxProcesses
        self.maxCPUtime = maxCPUtime
        self.computerResources = ComputerResources()
        self.startTime = 0
        self.endTime = 0
        
        #        
        self.loadTemplate()
        self.createRunList()
        self.createIndividuals()

        logString = "Created Batch 001 with", len(self.runList), "runs."
        logging.info(logString)


    def loadTemplate(self):
            #print 'reading:', self.inputFileTemplatePath
            fIn = open(self.inputFileTemplatePath,'r')
            # Don't read unicode... inputFileTemplate=unicode(fIn.read(),'utf-8')
            self.inputFileTemplate=fIn.read()
            fIn.close()
            print "Template file loaded from", self.inputFileTemplatePath
                
    def createRunList(self):
        i = 0
        evalValueStr = "("
        evalForStr = ""
        for variable in self.designSpace:
            evalValueStr += "v" + str(i) + ","
            evalForStr += "\t"*i + "for v" + str(i) + " in self.designSpace[" + str(i) + "]:\n" 
            i += 1
        evalValueStr = "\t"*i + " runList.append(" + evalValueStr + "))\n"
        evalStr = evalForStr + evalValueStr
        runList = [] 
        logging.info("Create list eval string:\n{0}".format(evalStr))
        #print self.designSpace[0]
        exec(evalStr)
        #print runList
        self.runList = runList
        logging.info("Created runlist: {0}".format(runList))
        logging.info("Length of runlist: {0}".format(len(runList)))

    def createIndividuals(self):
        runID = 0
        for run in self.runList:
            logging.info("Creating run {0}".format(run))
            self.individualRunList.append(
                        SimulationRuns.TrnsysRun(
                            runID, 
                            self.batchPath + "\\Run_" + str(runID),
                            self.executablePath,
                            self.inputFileTemplate,
                            run
                            )
                        ) 
            runID += 1 
    
    def execute(self):

        for run in self.individualRunList:
            run.createProject()
            run.translateInputFile()
            run.writeTranslatedInputFile()
            
    def execute2(self):
               
        self.startTime = datetime.datetime.now()
        self.pendingQueue = self.individualRunList

        print "Executing runs at", self.startTime  
        # Loop continuously if there are still pending runs
        while len(self.pendingQueue) or len(self.liveQueue):
            time.sleep(2)
            
            currentCPU = self.computerResources.current_CPU()
            
            # Update the Live
            for run in self.liveQueue:
                run.update()
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
                    print "Trying to run: ", run
                    print run
                    run.createProject()
                    run.translateInputFile()
                    run.writeTranslatedInputFile()
                    run.execute()
                    # Break out of the Pending loop
                    break
            
            print ["CPU:", str(currentCPU), "Pending:", 
                len(self.pendingQueue), "Live:", len(self.liveQueue), 
                "Finished", len(self.finishedQueue)]
        self.endTime = datetime.datetime.now()
        self.deltaTime = self.endTime - self.startTime
        print ("Finished execution of runs with", self.maxProcesses, "parallel threads and a",
               self.maxCPUtime, "CPU limit")
        print "Total real execution time:", self.deltaTime
        print ("MaxThread", self.maxProcesses, "CPU limit",
               self.maxCPUtime, "Time",self.deltaTime )

       
        
    def __len__(self):
        piSigma = 1
        for variable in self.designSpace:
            piSigma = piSigma * len(variable) 
        return piSigma   

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
    
if __name__ == "__main__":

    # Load the logging configuration
    
    logging.config.fileConfig('..\\LoggingConfig\\loggingNofile.conf')
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")
    #myLogger.setLevel("INFO")    
    logging.info("Started BATCH test script")
    
    logging.info("Stopped BATCH test script")
    

    # Configure the batch
    executablePath = "C:\Apps\Trnsys17\Exe\TRNEXE.exe"
    projDirectory = r"D:\TestTemp"
    inputFilePath = r"D:\Doktorat\Phase3\TestTrnsysProject\Begin.dck"
    maxProc = 4
    maxCPU = 100
    
    # Define the design space
    A = [
        # Solar collector slope
        Variables.FloatList("A1",r"VarX1",0,30,60),
        # Solar collector area
        Variables.FloatList("A2",r"VarX2",0,1,3),
        # Tank material
        Variables.RandomStringList("A3",r"DefaultMaterial",("Wood","Steel","Cheese")),
        ]
    
    # Create the batch
    batch = Batch(A,projDirectory,executablePath,inputFilePath,maxProc,maxCPU)
    # Execute the batch
    #batch.execute2()

    
    
