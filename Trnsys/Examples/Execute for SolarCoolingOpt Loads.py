'''
Created on Mar 22, 2011

@author: UserXP
'''
import Batch
import Variables
import Utilities
import csv
import datetime
import time
import os
import logging.config

logging.config.fileConfig('..\\LoggingConfig\\logging.conf')

atWork = 0
atHome = 1
if atWork :
    executablePath = "C:\Programme\Trnsys17\Trnsys17\Exe\TRNEXE.exe"
    projDirectory = r"C:\testProjDir\Batch1"
    inputFilePath = r"C:\testProjDir\TestTrnsysProject\Begin.dck"
elif atHome:
    executablePath = r"C:\Program Files\Trnsys16_1\Exe\TRNEXE.exe"
    projDirectory = r"C:\SolarCoolOptTemp\Batch1"
    inputFilePath = r"C:\Freelance\088_SolarCoolingOpt\TPF\Test1.dck"
    #print os.path.exists(inputFilePath)
elif 0 :
    executablePath = "C:\Apps\Trnsys17\Exe\TRNEXE.exe"
    projDirectory = r"C:\testProjDir\Batch1"
    inputFilePath = r"C:\testProjDir\TestTrnsysProject\Begin.dck"

logging.info('Starting the script')

# Define some attributes
runID                 = 1
executableArguments   = r"\n"
#inputTranslationList      = ((r'START','MyValue'), ('STOP','MyValue'))
inputTranslationList      = ()

inputProjFolder = r"C:\SolarCoolOptTemp"

# Configure the batch
maxProc = 4
maxCPU = 100

# Define the design space
A = [
    #__init__(self,name,regexTarget,list)
    Variables.SequentialStringList("A3",r"DefaultMaterial",("Wood","Steel","Cheese")),
    Variables.SequentialStringList("A3",r"DefaultMaterial",("Wood","Steel","Cheese")),
    Variables.SequentialStringList("A3",r"DefaultMaterial",("Wood","Steel","Cheese")),
    ]

#print A[0]
#print len(A[0])

# Create the batch
batch = Batch.Batch(A,projDirectory,executablePath,inputFilePath,maxProc,maxCPU)
# Execute the batch
batch.execute2()

