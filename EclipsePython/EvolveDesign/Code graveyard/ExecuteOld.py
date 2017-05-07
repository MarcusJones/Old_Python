'''
Created on Feb 27, 2011

@author: UserXP
'''
#!/usr/bin/python
import sys
import time
import subprocess
import psutil
from datetime import datetime
from collections import deque
import re
import csv
import FindReplace


# Instantiate the logger
import logging
logger = logging.getLogger('execute')
hdlr = logging.FileHandler('..\\Log files\\execute.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)

# Insantiate the CSV file

csvFile = open('..\\Log files\\runLog.csv', 'wb')
csvFile.close()
csvFile = open('..\\Log files\\runLog.csv', 'a')
csvLog = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

csvLog.writerow(["Time",
                    "Number Pending", 
                    "Number Running",
                    "Average CPU", 
                    "Instant CPU",
                    "Total Phys Mem",
                    "Total Avail Mem",
                    "Total Virtual Mem",
                    "Total available virtual mem"
                    ])

csvFile.close()

logger.info('Starting the script')


class TrnsysRun(object):
    def __init__(self,projectPath,trnEXEPath,runID):
        super(TrnsysRun, self).__init__()
        logString = 'Created a TrnsysRun object, ID ' + str(runID)
        logger.info(logString)
        
        # The pOpen process object
        self.process = 0
        
        # Store the identity of the run
        self.ID = {
                   "generation":"Pending",
                   "runID":runID,
                   "PID":"Pending"
                   }
        
        # The input, output, execution paths
        self.fileIO = {
                       "projectPath":projectPath,
                       "trnEXEPath":trnEXEPath,
                       # Relative directories
                       "projDCK":"\\DCK\\Begin.dck",
                       "projOutputDir":"\\OUT\\",
                       "projWeatherFile":"\\WEA\\",
                       "projListFile":"Pending"
                       }
        self.fileIO["trnExeCmd"] = self.fileIO["trnEXEPath"] + " " + self.fileIO["projectPath"] + self.fileIO["projDCK"] + " /n"
        
        # The current status of the run
        self.status = {
                       "execution":"Pending",
                       "errors":"Pending",
                       "runStartTime":"Pending"
                    }
        
        # Characteristics of the run
        self.character = {
                          "runStartTime":"Pending",
                          "runStopTime":"Pending",
                          "runErrors":"Pending"
                          }

class GATrnsysRun(TrnsysRun):
    def __init__(self):
        super(GATrnsysRun, self).__init__()
        self.empnum = "abc123"


    def execute(self):
        logString = 'Executing ID ' + str(self.ID["runID"])
        logger.info(logString)
        self.process = subprocess.Popen(self.fileIO["trnExeCmd"], shell=True)
        self.ID["PID"] = self.process.pid 
        self.runStartTime = datetime.now()
        
    def update(self):
        if self.process:
            retcode = self.process.poll()
            if retcode is None:
                self.status["execution"] = "Running"
            else:
                self.status["execution"] = "Finished"
        else:
            pass
        #print "Run ", self.ID["runID"], self.status["execution"], "execution.", "PID:", self.ID["PID"] 

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

class Manager:
        def __init__(self):
            self.liveQueue = list()
            self.pendingQueue = list()
            self.finishedQueue = list()
            self.maxProcesses = 8
        
class Generation:
    def __init__(self):
        self.liveQueue = list()
        self.pendingQueue = list()
        self.finishedQueue = list()
        self.maxProcesses = 8
        self.computerResources = ComputerResources()
        
    def create_copies_for_testing(self):
        
        atWork = 1
        
        # Load local configuration libraries
        if atWork :
            projectPath = "D:\Doktorat\Phase2"
            trnEXEPath = "C:\Programme\Trnsys17\Trnsys17\Exe\TRNEXE.exe"
        else :
            projectPath = "C:\Doktorat\Phase2"
            trnEXEPath = "C:\Apps\Trnsys17\Exe\TRNEXE.exe"
            
        totalRuns = 50
        runID = -1
        for _ in range(0,totalRuns):
            runID += 1
            self.pendingQueue.append(TrnsysRun(projectPath,trnEXEPath,runID))

    def execute(self): 
        # Loop continuously if there are still pending runs
        while len(self.pendingQueue) or len(self.liveQueue):
            time.sleep(2)
            currentCPU = self.computerResources.current_CPU()
            print "Step"
            
            # Update the Live
            for trnRun in self.liveQueue:
                trnRun.update()
                # Move off the live queue if finished
                # Could use Filter here! Replace for loop!!!!!
                # Actually, LIST COMPREHENSION would be better
                if trnRun.status["execution"] == "Finished":
                    self.finishedQueue.append(trnRun)
                    self.liveQueue.remove(trnRun)
            
            # Update the Pending 
            for trnRun in self.pendingQueue:
                trnRun.update()
                # Execute if resources available
                if currentCPU <= 80:
                    # Move the run into live queue
                    self.liveQueue.append(trnRun)
                    self.pendingQueue.remove(trnRun)
                    trnRun.execute()
                    # Break out of the Pending loop
                    break
            print ["CPU:", str(currentCPU), "Pending:", 
                len(self.pendingQueue), "Live:", len(self.liveQueue), 
                "Finished", len(self.finishedQueue)]

class Batch:
    def __init__(self):
        self.liveQueue = list()
        self.pendingQueue = list()
        self.finishedQueue = list()
        self.maxProcesses = 8
        self.computerResources = ComputerResources()
        
    def execute(self): 
        # Loop continuously if there are still pending runs
        while len(self.pendingQueue) or len(self.liveQueue):
            time.sleep(2)
            currentCPU = self.computerResources.current_CPU()
            print "Step"
            
            # Update the Live
            for trnRun in self.liveQueue:
                trnRun.update()
                # Move off the live queue if finished
                # Could use Filter here! Replace for loop!!!!!
                # Actually, LIST COMPREHENSION would be better
                if trnRun.status["execution"] == "Finished":
                    self.finishedQueue.append(trnRun)
                    self.liveQueue.remove(trnRun)
            
            # Update the Pending 
            for trnRun in self.pendingQueue:
                trnRun.update()
                # Execute if resources available
                if currentCPU <= 80:
                    # Move the run into live queue
                    self.liveQueue.append(trnRun)
                    self.pendingQueue.remove(trnRun)
                    trnRun.execute()
                    # Break out of the Pending loop
                    break
            print ["CPU:", str(currentCPU), "Pending:", 
                len(self.pendingQueue), "Live:", len(self.liveQueue), 
                "Finished", len(self.finishedQueue)]

    def create_copies_for_testing(self):
        
        atWork = 1
        
        # Load local configuration libraries
        if atWork :
            projectPath = "D:\Doktorat\Phase2"
            trnEXEPath = "C:\Programme\Trnsys17\Trnsys17\Exe\TRNEXE.exe"
        else :
            projectPath = "C:\Doktorat\Phase2"
            trnEXEPath = "C:\Apps\Trnsys17\Exe\TRNEXE.exe"
            
        totalRuns = 50
        runID = -1
        for _ in range(0,totalRuns):
            runID += 1
            self.pendingQueue.append(TrnsysRun(projectPath,trnEXEPath,runID))
        
##        for trnRun in trnRunQueue:
##                if (trnRun.status["execution"] == "Pending") and (cpuAveragePercent <= 80): 
#
#              # Check for finished processes in the live Queue
#                
#                if trnRun.status["execution"] == "Finished":
#                   
#                elif trnRun.status["execution"] == "Pending":
#
#                    trnRun.execute()
#                    break
#                elif trnRun.status["execution"] == "Running":
#                    pass
#                print trnRun.status["execution"]
#                    
#            if len(self.liveQueue) < self.maxProcesses: 
#                pass
#            print self.pendingQueue
#            print self.liveQueue
#            print self.finishedQueue
#            break

print "Creating generation"
testGeneration = Generation()
#print testGeneration
testGeneration.create_copies_for_testing()
#print testGeneration.liveQueue
#print len(testGeneration.pendingQueue)
testGeneration.execute()

print testGeneration.pendingQueue

print "Finished"

#trnRunQueue = list()
#runID = -1
#totalRuns = 50
#for i in range(0,totalRuns):
#    runID += 1
#    trnRunQueue.append(TrnsysRun(projectPath,trnEXEPath,runID))
#
#pendingRuns = 1
#liveRuns = 0
#startLoop = 0
#updateInterval = 1 # In seconds
#totalStartTime = datetime.now()
#
## Could instead have two lists, one for Pending, one for Live, one for Completed!!!
#
#while not(pendingRuns):
#    # Check the current time elapsed
#    deltaTotalTime = datetime.now() - totalStartTime
#    if deltaTotalTime.seconds > 5*60:
#        break 
#    
#    # Reset the main loop timer
#    if not(startLoop):
#        startLoop = datetime.now()
#    deltaTime = datetime.now() - startLoop
#
#    # This is the main loop, executed every updateInterval seconds
#    if deltaTime.seconds > updateInterval:
#        
#        # Reset the loop timer
#        startLoop = 0
#        
#        # Reset the runs counts
#        pendingRuns = 0
#        liveRuns = 0
#
#        # Count current live or pending runs from all runs in queue
#        # Could instead update counter using each object?
#        # But this method should be more robust?
#        # Because we can't test when the simulation is completed??
#
#        # Execute a single additional run if CPU resources available
#        for trnRun in trnRunQueue:
#                if (trnRun.status["execution"] == "Pending") and (cpuAveragePercent <= 80): 
#                    trnRun.execute()
#                    break
#
#        csvFile = open('..\\Log files\\runLog.csv', 'a')
#        csvLog = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#       
#        csvLog.writerow([str(datetime.now()),
#                        pendingRuns,
#                        liveRuns,
#                        cpuAveragePercent,
#                        psutil.cpu_percent(),
#                        psutil.TOTAL_PHYMEM,
#                        psutil.avail_phymem(),
#                        psutil.total_virtmem(),
#                        psutil.avail_virtmem()
#                        ])
#        csvFile.close()
#   
#logger.info('Finished the script')
#print "Finished executing"
#   