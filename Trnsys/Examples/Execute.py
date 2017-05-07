'''
Created on Mar 22, 2011

@author: UserXP
'''
import Batch
import Variables
import Utilities
import logging            
import csv
import datetime
import time
import os


atWork = 0
atOther = 0
if atWork :
    executablePath = "C:\Programme\Trnsys17\Trnsys17\Exe\TRNEXE.exe"
    projDirectory = r"C:\testProjDir\Batch1"
    inputFilePath = r"C:\testProjDir\TestTrnsysProject\Begin.dck"
elif atOther:
    executablePath = "C:\Trnsys17\Exe\TRNEXE.exe"
    projDirectory = "D://Temp//Phase3//Batch1"
    inputFilePath = "D://Temp//Phase3//TestTrnsysProject//Begin.dck"
    #print os.path.exists(inputFilePath)
elif 0 :
    executablePath = "C:\Apps\Trnsys17\Exe\TRNEXE.exe"
    projDirectory = r"C:\testProjDir\Batch1"
    inputFilePath = r"C:\testProjDir\TestTrnsysProject\Begin.dck"

# Instantiate the logger
log = logging.getLogger(__name__)
hdlr = logging.FileHandler('..\\Log files\\executeLog.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
hdlr.setFormatter(formatter)
log.addHandler(hdlr) 
log.setLevel(logging.DEBUG)

# Insantiate the CSV file

#csvFile = open('..\\Log files\\runLog.csv', 'wb')
#csvFile.close()
#csvFile = open('..\\Log files\\runLog.csv', 'a')
#csvLog = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#
#csvLog.writerow(["Time",
#                    "Number Pending", 
#                    "Number Running",
#                    "Average CPU", 
#                    "Instant CPU",
#                    "Total Phys Mem",
#                    "Total Avail Mem",
#                    "Total Virtual Mem",
#                    "Total available virtual mem"
#                    ])
#
#csvFile.close()

log.info('Starting the script')

# Define some attributes
runID                 = 1
executableArguments   = r"\n"
#inputTranslationList      = ((r'START','MyValue'), ('STOP','MyValue'))
inputTranslationList      = ()

inputProjFolder = r"C:\Doktorat\Phase3"

#for maxProc in range(1,11):
#    for maxCPU in range(0,101,10): 

##createPath("C:\Python\myNewDirectory")
#myTrnsysRun = Individual.TrnsysRun(
#                    runID, 
#                    projDirectory,
#                    executablePath,
#                    inputFileTemplate,
#                    inputTranslationList
#                    )
#
#myTrnsysRun.createProject()
#myTrnsysRun.translateInputFile()
#myTrnsysRun.writeTranslatedInputFile()
#myTrnsysRun.execute()








# Configure the batch
executablePath = "C:\Apps\Trnsys17\Exe\TRNEXE.exe"
projDirectory = r"C:\Doktorat\Phase3\Batch1"
inputFilePath = r"C:\Doktorat\Phase3\TestTrnsysProject\Begin.dck"
maxProc = 4
maxCPU = 100

# Define the design space
A = [
    # Solar collector slope
    Variables.FloatList("A1",r"VarX1",0,30,60),
    # Solar collector area
    Variables.FloatList("A2",r"VarX2",0,1,3),
    # Tank material
    Variables.SequentialStringList("A3",r"DefaultMaterial",("Wood","Steel","Cheese")),
    ]

# Create the batch
batch = Batch.Batch(A,projDirectory,executablePath,inputFilePath,maxProc,maxCPU)
# Execute the batch
batch.execute2()

