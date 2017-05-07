'''
Created on 2012-12-11

@author: mjones
'''
import subprocess
from datetime import datetime
from config import *
from UtilityFile import FileObject


#currentCPU = self.computerResources.current_CPU()

def getTRNSYScommand(fullFilePath, flgSuppress = False):
    assert FileObject(fullFilePath).exists(), "Can't find {}".format(fullFilePath)
    assert FileObject(TRNSYS_EXEC).exists(), "Can't find trnsys.exe at {}".format(TRNSYS_EXEC)
    
    executionCommand = TRNSYS_EXEC + ' "' + fullFilePath + '" '
    #print executionCommand
    if flgSuppress:
         executionCommand += r" /h"
    #print "Running the following command;\n", executionCommand
    return executionCommand

def runTRNSYS(fullFilePath, flgSuppress = False):
    
    #getTRNSYScommand(fullFilePath, flgSuppress = False
                     
                     

    executionCommand = TRNSYS_EXEC + ' "' + fullFilePath + '" '
    print executionCommand
    if flgSuppress:
         executionCommand += r" /h"
    print "Running the following command;\n", executionCommand

    process = subprocess.Popen(executionCommand, shell=True)
    #PID = process.pid
    #runStartTime = datetime.now()
    
    
    
if __name__ == "__main__":
    allDCKfiles = [r"D:\apps\Trnsys17\Examples\Begin\Begin.dck",
                   r"D:\apps\Trnsys17\Examples\Cooling Tower\Type51CoolingTower.dck"
                   ]
    
    allOutputDirects = [r"D:\apps\Trnsys17\Examples\Cooling Tower"]
    
    for deckFile in allDCKfiles:
        #print deckFile
        runTRNSYS(deckFile, True)
    
    for outputDir in allOutputDirects:
        print outputDir
        outputDir = outputDir + r"\Type51CoolingTower.lst"
        print outputDir
        
        fh = open(outputDir, "r")
        print fh
        
        for line in fh:
            print line
