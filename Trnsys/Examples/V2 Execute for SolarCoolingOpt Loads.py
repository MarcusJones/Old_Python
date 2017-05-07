'''
Created on Mar 22, 2011

@author: UserXP
'''

from Batch2 import Batch2, DesignSpace
import Variables
import Utilities
import csv
import datetime
import time
import os
import logging.config
import FileObject

logging.config.fileConfig('..\\LoggingConfig\\logging.conf')

logging.info('Starting the script')

#===============================================================================
# Parameters
#===============================================================================

executablePath = r"C:\\Apps\Trnsys17\\Exe\\TRNEXE.exe"                  

#systemDirectory = r"D:\DoktoratSim\System1"
#outputResultsFile = r"D:\DoktoratSim\System1\results.csv"

inputProjFolder = r"C:\SolarCoolOpt"

inputTemplateFileObjects = [
                            FileObject.FileObject(r"C:\\Freelance\\088_SolarCoolingOpt\\TPF\\Template_r03.dck"),
                            ]

maxProcesses = 4
maxCPUtime = 100


#===============================================================================
# BUI Files
#===============================================================================

BUIFilePathsList = list()

rootFilePath = r"C:\\Freelance\\088_SolarCoolingOpt\\BUI\\buifiles_afrohner\\"

buiFiles = [
    "ME_MEE_L_30.b17",
    "ME_MEE_L_50.b17",
    "ME_MEE_S_30.b17",
    "ME_MEE_S_50.b17",
    "ME_NEE_L_30.b17",
    "ME_NEE_L_50.b17",
    "ME_NEE_S_30.b17",
    "ME_NEE_S_50.b17",
    "ME_VEE_L_30.b17",
    "ME_VEE_L_50.b17",
    "ME_VEE_S_30.b17",
    "ME_VEE_S_50.b17",
    "SE_MEE_L_30.b17",
    "SE_MEE_L_50.b17",
    "SE_MEE_S_30.b17",
    "SE_MEE_S_50.b17",
    "SE_NEE_L_30.b17",
    "SE_NEE_L_50.b17",
    "SE_NEE_S_30.b17",
    "SE_NEE_S_50.b17",
    "SE_VEE_L_30.b17",
    "SE_VEE_L_50.b17",
    "SE_VEE_S_30.b17",
    "SE_VEE_S_50.b17",
    ]

for file in buiFiles:
    BUIFilePathsList.append(os.path.normpath(rootFilePath + file))

#===============================================================================
# WEATHER FILES
#===============================================================================

weatherFilePathsList = list()

weatherrootFilePath = r"C:\\Freelance\\088_SolarCoolingOpt\\WEA\\"


weatherFiles = [
    "AT-Wien-Hohe-Warte-110350.tm2",
    "GR-Athinai-Hellenkion-167160.tm2",
    "EG-Cairo-623660.tm2",
    "us-hi-honolulu-22521.tm2",
    ]

for file in weatherFiles:
    weatherFilePathsList.append(os.path.normpath(weatherrootFilePath + file))


#===============================================================================
# LOADS FILES
#===============================================================================
loadsFilePathsList = list()

loadsrootFilePath = r"C:\\Freelance\\088_SolarCoolingOpt\LOADS\\"

loadsFiles = [
    "Wohnung.csv",
    "Buro.csv",
    "Hotel.csv",
    "Krankenhaus.csv",
    ]

for file in loadsFiles:
    loadsFilePathsList.append(os.path.normpath(loadsrootFilePath + file))


#===============================================================================
# Design space
#===============================================================================

# Define the design space
designSpaceList = [
    #__init__(self,name,regexTarget,list)
    Variables.SequentialStringList("BUI Path",r"VarX1-BUI",BUIFilePathsList),
    Variables.SequentialStringList("Weather Path",r"VarX2-Weather",weatherFilePathsList),
    Variables.SequentialStringList("Loads File Path",r"VarX3-Loads",loadsFilePathsList),
    ]
   
myDesignSpace = DesignSpace('Test Design Space',designSpaceList)


myBatch = Batch2(
                             "MyBatch",
                             inputProjFolder,
                             executablePath,
                             inputTemplateFileObjects,
                             maxProcesses,
                             maxCPUtime
                             )

myBatch.loadDesignSpace(myDesignSpace)

print myBatch


myBatch.createGlobalSearchRunList()


runListFilePath = inputProjFolder + "\\thisRunList.txt"

fileObj = open(runListFilePath,"w")

runCnt = 0
for run in myBatch.runList:
    print >>fileObj, "{0:3d},".format(runCnt),
    for thing in run:
        print >>fileObj, thing,
    print >>fileObj
    runCnt += 1
fileObj.close()


myBatch.finishRunDefinitions()


myBatch.createIndividuals()


myBatch.executeParallel()

#Q_0.createRandomRuns(self.popSize)
#self.generationList.append(Q_0)




#print A[0]
#print len(A[0])

# Create the batch
#batch = Batch.Batch(A,projDirectory,executablePath,inputFilePath,maxProc,maxCPU)
# Execute the batch
#batch.execute2()

