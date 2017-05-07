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
import os
import logging
import distutils
import logging.config
import Utilities
import Variables
import numpy
#log = logging.getLogger(__name__)

class SimulationRun(object):
#    runID = 0
#    runDirectory = ''   
#    executablePath = ''
#    executableArguments  = ''
#    inputFileTemplate = ''  
#    inputTranslationList = ()
#    fullExecutableCommand = ''
#    
    def __init__(   self,
                    runID, 
                    runDirectory,
                    executablePath,
                    #inputFileTemplates,
                    inputTemplateFileObjects,
                    variableVector
                    ):
        """
        self                   
        runID
        runDirectory            Directory for the project
        executablePath          Full path string

        inputFileTemplate  
        inputTranslationList   
        """   
        
        self.fitness = None

        
        #############################################################
        # ID and status
        #############################################################        
        # The ID, used for directory and file naming, and identity
        self.runID               = runID     
        
        self.name = str(self.runID)
        
        # Possible status 
        self.status = {
               "execution":"Pending",
               "errors":"Pending",
               "runStartTime":"Pending"
            }
        # The pOpen process object
        self.process = 0
                
        #############################################################
        # File input & output
        #############################################################
        # Head directory of the run
        self.runDirectory       = runDirectory
        # The full path of the input file
        self.inputFilePath = "UNDEFINED" 
        # The path for output files
        self.outputFilesPath = ""
        # Path to 'simulationProgram'.exe
        self.executablePath      = executablePath
        # The template file      
        self.inputTemplateFileObjects   = inputTemplateFileObjects
        # The translations for this file   
        self.variableVector    = variableVector   
        # The complete translated file
        self.translatedFileTemplates = list()
        
        #############################################################
        # Timing variables
        #############################################################
        self.runStartTime = 0
        self.runStopTime = 0
        
        variableNameList = list()
        variableValueList = list()
        #prin self.variableVector
#        for variable in self.variableVector:
#            logging.info("This variable: {0}".format(variable))
#            variableNameList.append(variable.name)
#            variableValueList.append(variable.value)

        for variable in self.variableVector:
            logging.info("This variable: {0}".format(variable))
            variableNameList.append(variable[0])
            variableValueList.append(variable[1])

        logging.info("Created {0}".format(self))

      
    def loadTemplates(self):
        
        for inputFileObject in self.inputTemplateFileObjects:
            inputFileObject.loadData()
#        self.inputFileTemplatePath = inputFileTemplatePath

#        #prin 'reading:', self.inputFileTemplatePath
#        fIn = open(self.inputFileTemplatePath,'r')
#        # Don't read unicode... inputFileTemplate=unicode(fIn.read(),'utf-8')
#        self.inputFileTemplate=fIn.read()
#        fIn.close()
        logString = "Template files loaded from into {0}".format(self)
        logging.info(logString)
        
    def translateInputFiles(self): 
        logString = 'Translating run ID; ' + str(self.runID)
        #prin log.__dict__
        logging.info(logString)
        # Loop each translation pair
        # Each translation contains one search Regex, and a replacement value
        # E.g. (re.compile(ur'''MySearchRegex''', re.U|re.M), ur'''MyNewString''') 
        #translations = [ (re.compile(ur'''MySearchRegex''', re.U|re.M), ur'''MyNewString'''), 
        #               # more regex pairs here
        #               ]
        
        self.loadTemplates()

        
        for inputFileObject in self.inputTemplateFileObjects:
            
            #logging.debug("Translating {0} for variable - {1}".format(inputFileTemplate))
            #print len(inputFileTemplate)
            #print len(self.inputFileTemplates)
            #self.translatedFiles = inputFileTemplate
            for variable in self.variableVector:
                # Do the translation on the copy
                #self.translatedFile = re.sub(translationPair[0],translationPair[1], self.translatedFile)
                #self.translatedFile = re.sub(translationPair[0],translationPair[1], self.translatedFile)
                #self.translatedFile = re.sub(variable.value,variable.regexTarget, self.translatedFile)
                #re.sub(pattern, repl, string[, count, flags])
                thisVarTarget = variable[0]
                thisVarValue =  variable[1]
                # This is an ugly hack to get rid of the escape \0= NULL, etc.
                # For some reason variable[1] changes from \\ to single \ 
                thisVarValue = "\\\\".join(thisVarValue.split("\\"))
                
#                while 1:
#                    print thisVarValue
                matches = re.findall(thisVarTarget, inputFileObject.fileData)
                #print re.sub(variable.regexTarget, str(variable.value), inputFileObject.fileData)
                inputFileObject.fileData = re.sub(thisVarTarget, thisVarValue, inputFileObject.fileData)
                #self.translatedFileTemplates.append(translatedFileTemplate)
                logging.debug("Translate matches: {0}, variable: {1}, input file: {2}".format(len(matches),variable,inputFileObject))
            
            #inputFileObject.fileData = translatedInputFileObject
        
#    def createProject(self): 
#        pass

    def writeTranslatedInputFile(self):
        #for line in self.translatedFile:
        #    prin (line)
        #prin repr(self.inputFileTemplate)
        #prin repr(self.translatedFile)
        
        for inputFileObject in self.inputTemplateFileObjects:
            inputFileObject.writeData()
        logging.info("Created input file for Run {0} in {1}".format(self.runID,self.inputFilePath))
        
        
    def execute(self): 
        logString = 'Executing run, ID number; ' + str(self.runID)
        logging.info(logString)
        #prin "Executing " + self.executionCommand
        self.process = subprocess.Popen(self.executionCommand, shell=True)
        self.PID = self.process.pid
        self.runStartTime = datetime.now()
        #prin "Finished executing"

    def update(self):
        if self.process:
            retcode = self.process.poll()
            if retcode is None:
                self.status["execution"] = "Running"
            else:
                self.status["execution"] = "Finished"
        else:
            pass
        #prin "Run ", self.runID, "is", self.status["execution"], "."
        #prin "Run ", self.ID["runID"], self.status["execution"], "execution.", "PID:", self.ID["PID"] 

    def __str__(self):

#      str_list = []
#      for num in xrange(loop_count):
#        str_list.append(`num`)

        varStringList = list()
        #varStringList.append("(")
        for variable in self.variableVector:
            try:
            #prin variable.value
                varStringList.append(str(round(variable.value,1)))
            except:
                pass
            
            try:
                varStringList.append(variable.value)
            except:
                varStringList.append("Broken xx!1")
            
#            if Utilities.iter_islast(self.variableVector):
#                prin "END"
                
        #varStringList.append(")")
        
        varString = ', '.join(varStringList)
        varString = "(" + varString + ")"
        return "Run ID: {0}, {1} variables: {2}, input path: {3}, num input files {4}".format(str(self.runID), len(self.variableVector), varString, self.inputFilePath, len(self.inputTemplateFileObjects))  

    def printOutResult(self,targetFilePath):
        
        varStringList = list()
        #varStringList.append("(")
        for variable in self.variableVector:
            try:
            #prin variable.value
                varStringList.append(str(round(variable.value,1)))
            except:
                varStringList.append(variable.value,)

        fitnessStringList = list()
        for result in self.fitness.results:
            value = result.value
#            print value
#            print repr(value)
#            print type(value)
        
            fitnessStringList.append(str(round(value,1)))
        
        resultList = varStringList + fitnessStringList
        resultString = ','.join(resultList)
        resultString += "\n"

        resultFile = open(targetFilePath,'a')
        resultFile.write(resultString)
        resultFile.close()
        
        logString = "Wrote result to file"
        logging.info(logString)        
            
    
    
class TrnsysRun(SimulationRun):
    def __init__(self,
                    runID, 
                    runDirectory,
                    executablePath,
                    inputFileTemplate,
                    variableVector
                    ):
        # The following will call the __init__ of the parent
        super(TrnsysRun,self).__init__(
                    runID, 
                    runDirectory,
                    executablePath,
                    inputFileTemplate,
                    variableVector
                    )
        
    def createProject(self):
        # Main project directory
        if not os.path.exists(self.runDirectory): 
            os.makedirs(self.runDirectory)
            
        # The DCK file
        DCK_extension = r".dck"                                          
        DCK_directory = self.runDirectory + r"\\DCK\\"
        self.DCK_filePath = os.path.normpath(DCK_directory + str(self.runID) + DCK_extension)
        if not os.path.exists(DCK_directory): 
            os.makedirs(DCK_directory)
        
        # The B17 file
        B17_extension = r".b17"                                          
        #B17_directory = os.path.normpath(self.runDirectory + r"\\B17\\.")
        B17_directory = self.runDirectory + r"\\B17\\"
        #self.B17_filePath = r"\\" + str(self.runID) + B17_extension
        self.B17_filePath = os.path.normpath(B17_directory + "Building" + B17_extension)
        if not os.path.exists(B17_directory): 
            os.makedirs(B17_directory)
        
        # The OUT directory
        self.outputFileDir = os.path.normpath(self.runDirectory + r"\\OUT\\.")
        if not os.path.exists(self.outputFileDir): 
            os.makedirs(self.outputFileDir)    
        
        # The EXE full command
        self.executionCommand = self.executablePath + " " + self.DCK_filePath + r" /h" 

        # This needs work, not robust!
        
        # Update the FileObjects with the Output directories
        # The first one is the B17
        #self.inputTemplateFileObjects[0].outputFilePath = self.B17_filePath
        # The second is the DCK
        print "Modified here as well"
        self.inputTemplateFileObjects[0].outputFilePath = self.DCK_filePath


        
        
#        # The B17 file
#        self.B17Directory = os.path.normpath(self.runDirectory + r"\B17")
#                        
#        self.inputFilePath = os.path.normpath(inputFileDir + inputFileName)        
#                  
        # Sub dir for output file
            
        logging.info("Created project directory for Run {0} in {1}".format(self.runID,self.runDirectory))
        # Sub dir for 

    def postProcess(self):
        
        self.fitness = None
        self.fitness = Fitness("Fitness for run " + self.name)
        
        logging.info("Post processing for run {0}, current Fitness vector: {1}".format(self.name,self.fitness))
        
        logging.info("Post processing in {0}".format(self.outputFileDir))
        dirList=os.listdir(self.outputFileDir)
        
        for outputFileName in dirList:
            
            outputFullFilePath = self.outputFileDir + "\\" + outputFileName
            #outputFullFilePath = os.path.abspath(outputFileName)
            outputFile = open (outputFullFilePath)
            theseOutputLines = outputFile.readlines()
            lastLine = theseOutputLines[-1]
            
            if outputFileName == "IntQcool.out":
                #print re.split("[\s]+",lastLine)
                #print re.split("[*-]*[\d.]+",lastLine)
                value = re.split("[\s]+",lastLine)[2]
                value = numpy.float(value)
                value = value /3600
                value = value /1000
                thisResult = NumericalResult("Cooling",value,"MWh")
                logging.info("Adding result to {0}".format(self))
                self.fitness.addResult(thisResult)
                
                
            if outputFileName == "IntQheat.out":
                #print re.split("[\s]+",lastLine)
                #print re.split("[*-]*[\d.]+",lastLine)
                value = re.split("[\s]+",lastLine)[2]
                value = numpy.float(value)
                value = value /3600
                value = value /1000
                thisResult = NumericalResult("Heating",value,"MWh")
                logging.info("Adding result to {0}".format(self))                
                self.fitness.addResult(thisResult)
                                    
        #logging.info("Post processed run {0}".format(self))
        logging.info("Run name: {0}, fitness name: {1}, ".format(self.name, self.fitness.name))
        for result in self.fitness.results:
            logging.info("    Result: {0}".format(result))
        dirList=os.listdir(self.outputFileDir)
        

    def dominates(self,otherIndividual):
        """        
        To determine if a point in the search is dominates another, 
        a vector whose components are the values of the objective functions 
        in the point is defined. A vector A dominates another vector B iif 
        the values for each of the components of A are at least equal to the 
        values of B, and at least a value from A is strictly greater than 
        the corresponding value from B.         
        """        
        individual_p = self
        individual_q = otherIndividual
        
        results_p = list()
        for result in individual_p.fitness.results:
            results_p.append(result.value)
            
        results_q = list()
        for result in individual_q.fitness.results:
            results_q.append(result.value)
            
        #print "Compare:"
        #print "Indiv p, ID:",individual_p.runID, results_p
        #print "Indiv q, ID:", individual_q.runID, results_q
                
        pDominatesCount = 0   
        qDominatesCount = 0             
        for resultNumber in range(len(results_p)):
            if results_p[resultNumber] <= results_q[resultNumber]:
                #print "P Dominates in result {0}".format(resultNumber)
                pDominatesCount += 1
            else:
                #print "Q Dominates in result {0}".format(resultNumber)
                qDominatesCount += 1

#        if qDominatesCount 
#        if pDominatesCount and qDominatesCount:
#            print "No dominance"

        #print "pDominateCount = {0}".format(pDominatesCount)                     
        #print "qDominateCount = {0}".format(qDominatesCount)
                        
        if qDominatesCount == len(results_q):
            #print "Dominates=FALSE; p does not dominate q"
            return False
        else:
            #print "Dominates=TRUE; p dominates q"
            return True
            
#        prin "Created run", self.runID, "with translations:", self.inputTranslationList
  
#    def createProject(self):
#        inputFileExtension = r".dck"                                          
#        inputFileName = r"\\" + str(self.runID) + inputFileExtension     
#        inputFileDir = os.path.normpath(self.runDirectory + "\DCK")                                              
#        self.inputFilePath = os.path.normpath(inputFileDir + inputFileName)
#        self.executionCommand = self.executablePath + " " + self.inputFilePath + r" /n" 
#        # Main project directory
#        if not os.path.exists(self.runDirectory): 
#            os.makedirs(self.runDirectory)
#        # Sub dir for input file
#        if not os.path.exists(inputFileDir): 
#            os.makedirs(inputFileDir)
#        # Sub dir for 
#        


class TrnsysRunGA(TrnsysRun):
    def __init__(self,
                    runID, 
                    runDirectory,
                    executablePath,
                    inputFileTemplate,
                    variableVector
                    ):
        # The following will call the __init__ of the parent
        super(TrnsysRunGA,self).__init__(
                    runID, 
                    runDirectory,
                    executablePath,
                    inputFileTemplate,
                    variableVector
                    )

class NumericalResult():
    def __init__(self, name, value, unit):
        self.name = name
        self.value = value
        self.unit = unit
    
    def __str__(self):
        return "Numerical result, {0} = {1} [{2}]".format(self.name, self.value, self.unit)

class Fitness():
    def __init__(self, name):
        self.name = name
        self.results = list()
        logging.info("Created a new Fitness, name: {0}".format(self.name))

    def __str__(self):
        try: 
            return "Fitness {0} with {1} results".format(self.name, len(self.results))
        except:
            return "Fitness {0} with 0 results".format(self.name)
        
    def __len__(self):
        return len(self.results)
    
    def showTextResultVector(self):
#        print "SHOW RESULTS"
#        print "inside", self
#        print "Number of results: ", len(self.results)
        resultStringList = list()
        for result in self.results:
            resultStringList.append(str(result))
            
        resultString = ', '.join(resultStringList)
        resultString = "(" + resultString + ")"
        return resultString
            
    def addResult(self, result):
        self.results.append(result)
        logging.info("Added 1 result to {0}, length is now {1}".format(self.name, len(self.results)))

        
        

if __name__ == "__main__":
    """
    Test code for TrnsysRunGA
    """
    
    # Load the logging configuration
    logging.config.fileConfig('..\\Log files\\logging.conf')
    logging.info("STARTED SimulationsRuns test script")


    if 1: # At work
        runID = 999
        batchPath = r"D:\DoktoratSim\System1"
        executablePath = r"D:\Programme\Trnsys17\Exe\TRNEXE.exe"
        inputFileTemplate = r"UNDEFINED"
        inputFileTemplatePath = r"D:\Doktorat\Phase4\TestTrnsysProject\Begin.dck"
        
    if 0: # At home
        runID = 999
        batchPath = r"C:\DoktoratSim\System1"
        executablePath = r"C:\Apps\Trnsys17\Exe\TRNEXE.exe"
        inputFileTemplate = r"UNDEFINED"
        inputFileTemplatePath = r"C:\Doktorat\Phase4\TestTrnsysProject\Begin.dck"
    
#    genome = [0.5, 0.5, 0.5]
#    
#
#    variableVector = []
#    count = 0 
#    for gene in genome:
#        searchString = 'VarX' + str(count) + '_Test .+'
#        replaceString = 'VarX' + str(count) + '_Test = ' + str(gene)
#        prin searchString, replaceString
#        pair = (re.compile(searchString, re.U|re.M), replaceString)
#        variableVector.append(pair)
#        count += 1
#    
#    prin variableVector
#        
##    inputTranslationList = [(re.compile(ur'''VarX1_Test .+''', re.U|re.M), ur'''VarX1_Test = '''), 
##                       # more regex pairs here
##                       ]
#    

    # Some variables
    v1 = Variables.RandomFloat("A1",r"VarX1",0,60)
    v2 = Variables.RandomFloat("A2",r"VarX2",0,3)        
    v3 = Variables.RandomStringList("A3",r"DefaultMaterial",("Wood","Steel","Cheese"))

    variableVector = [v1,v2,v3]

    # The variables are unitialized, because they are RANDOM type
    #print "Before initialization"
#    for variable in variableVector:
#        print variable
    
    #print "After initialization"
    # Initialize the random variables
    for variable in variableVector:
        variable.new()
        #print variable
    
    oneIndividual = TrnsysRunGA(
                            runID, 
                            batchPath + "\\Run_" + str(runID),
                            executablePath,
                            inputFileTemplate,
                            variableVector
                            )
    
    oneIndividual.createProject()
    
    oneIndividual.loadTemplate(inputFileTemplatePath)
    
    oneIndividual.translateInputFile()
    
    oneIndividual.writeTranslatedInputFile()
    
    oneIndividual.execute()
    
    
    
    logging.info("FINISHED SimulationsRuns test script")    