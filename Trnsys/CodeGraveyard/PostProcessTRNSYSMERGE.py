#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 
#Matlab plotd
#===============================================================================

"""This module does stuff
Etc.
"""

#===============================================================================
# Set up
#===================================d============================================
import logging.config
from UtilityInspect import whoami, whosdaddy
from UtilityFile import FileObject
import os
import re
import numpy
import scipy
from scipy.io import savemat
from datetime import timedelta, datetime
import pprint 
from UtilityExcel import ExcelBook
import unittest

#===============================================================================
# Code
#===============================================================================
class AnalysisFile(FileObject):
    """This class does something for someone. 
    """
    def __init__(self, fullFilePath): 
        #timeVector = None
        #dataMatrix = None
        #headers = None
        #units = None
        super(AnalysisFile,self).__init__(fullFilePath)
        
    def returnAnalysisData_BAL(self):
        thisBalDataList = list()
        lineCount = 0
        for line in self.fileData.split('\n'):
            #print line

            if line: 
                line = re.sub("\|"," ",line)


                # Get rid of the |
                #print thisLineSplit
                if lineCount == 0:
                    line = re.sub("="," ",line)
                    line = re.sub("\+"," ",line)
                    line = re.sub("\-"," ",line)  
                    thisLineSplit = re.compile("\s+").split(line.lstrip().rstrip())
                    headers = numpy.array(thisLineSplit,dtype=object)
                elif lineCount == 1:
                    line = re.sub("="," ",line)
                    line = re.sub("\+"," ",line)
                    line = re.sub("\-"," ",line)    
                    thisLineSplit = re.compile("\s+").split(line.lstrip().rstrip())
                    
                    units = numpy.array(thisLineSplit,dtype=object)
                else:
                    thisLineSplit = re.compile("\s+").split(line.lstrip().rstrip())
                    # DO NOT Skip the first 3 (Time, Percent, Pipe)
                    #thisLineSplit = thisLineSplit[0:]
                    #print thisLineSplit
                    floatDataList = [float(num) for num in thisLineSplit]
                    thisBalDataList.append(floatDataList)
                lineCount = lineCount + 1
            
        balDataArry = numpy.array(thisBalDataList)
        #print balDataArry
        timeVector = balDataArry[:,0]
        
        
        pureFileName = os.path.splitext(os.path.split(self.filePath)[1])[0]
        #print pureFileName

        thisData = AnalysisData(dataColumns= balDataArry,
                                
                        sourceFilePath=self.filePath,
                        headers = headers,
                        units=units,
                        timeVector=timeVector,
                        system=pureFileName,
                        pointType="Building",
                        number=0,
                        description="description"
                        )        
        
        
        #thisData.forceConsistency()
        logging.debug("Returning the Analysis Data {}".format(thisData))
        return thisData
    
    def returnAnalysisData_OUT(self):
        thisDataList = list()
        lineCount = 0
        for line in self.fileData.split('\n'):
            #print line
            if line: 
                #print thisLineSplit
                if lineCount == 0:
                    thisLineSplit = re.compile("\s+").split(line.lstrip().rstrip())
                    headers = numpy.array(thisLineSplit,dtype=object)
                elif lineCount == 1:
                    thisLineSplit = re.compile("\s+").split(line.lstrip().rstrip())
                    units = numpy.array(thisLineSplit,dtype=object)
                else:
                    thisLineSplit = re.compile("\s+").split(line.lstrip().rstrip())
                    floatDataList = [float(num) for num in thisLineSplit]
                    thisDataList.append(floatDataList)
                lineCount = lineCount + 1
            
        dataArry = numpy.array(thisDataList)
        #print dataArry
        timeVector = dataArry[:,0]
        
        dataArry = dataArry[:,1:]
        headers = headers[1:]
        units = units[1:]

        pureFileName = os.path.splitext(os.path.split(self.filePath)[1])[0]
        splitFileName = re.split("_",pureFileName)
        system = splitFileName[0]
        pointType = splitFileName[1]
        number = splitFileName[2]
        number = int(number)
        
        thisData = AnalysisData(dataColumns= dataArry,
                                
                        sourceFilePath=self.filePath,
                        headers = headers,
                        units=units,
                        timeVector=timeVector,
                        system=system,
                        pointType=pointType,
                        number=number,
                        description="description"
                        )
        
        #headers=None, units=None, timeVector=None, system=None, pointType=None, number=None,description = None
        #thisData.forceConsistency()
        logging.debug("Returning the Analysis Data {}".format(thisData))
          
        return thisData    
    
    
    def returnAnalysisData_EPW(self):
        #lineCount = 0
        epwArray = list()
        for line in self.fileData.split('\n')[8:20]:
            #print line.split(",")
            thisLine = line.split(",")
            thisLine.pop(5)
            #print thisLine
            epwArray.append(thisLine)
        
        timeVector = [line[0:4] for line in epwArray]
        timeVector = numpy.array(timeVector, dtype=float)
        epwNumpyArray = numpy.array(epwArray, dtype=float)
        
        #print timeVector
        #headers = ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Dry Bulb Temperature (C)', 'Dew Point Temperature (C)', 'Relative Humidity', 'Atmospheric Station Pressure (Pa)', 'Extraterrestrial Horizontal Radiation (Wh/m2)', 'Extraterrestrial Direct Normal Radiation (Wh/m2)', 'Horizontal Infrared Radiation from Sky (Wh/m2)', 'Global Horizontal Radiation (Wh/m2)', 'Direct Normal Radiation (Wh/m2)', 'Diffuse Horizontal Radiation (Wh/m2)', 'Global Horizontal Illuminance (lux)', 'Direct Normal Illuminance (lux)', 'Diffuse Horizontal Illuminance (lux)', 'Zenith Illuminance (lux)', 'Wind Direction (deg)', 'Wind Speed (m/s)', 'Total Sky Cover', 'Opaque Sky Cover', 'Visibility (km)', 'Ceiling Height (m)', 'Present Weather Ovservation', 'Present Weather Codes', 'Precipitable Water (mm)', 'Aerosol Optical Depth (thousandths)', 'Snow Depth (cm)', 'Days Since Last Snowfall']
        headerString = "Year, Month, Day, Hour, Minute,Datasource, DryBulb {C},DewPoint {C},RelHum {%},Atmos Pressure {Pa},ExtHorzRad {Wh/m2},ExtDirRad {Wh/m2},HorzIRSky {Wh/m2},GloHorzRad {Wh/m2},DirNormRad {Wh/m2},DifHorzRad {Wh/m2},GloHorzIllum {lux},DirNormIllum {lux},DifHorzIllum {lux},ZenLum {Cd/m2},WindDir {deg},WindSpd {m/s},TotSkyCvr {.1},OpaqSkyCvr {.1},Visibility {km},Ceiling Hgt {m},PresWeathObs,PresWeathCodes,Precip Wtr {mm},Aerosol Opt Depth {.001},SnowDepth {cm},Days Last Snow,Albedo {.01},Rain {mm},Rain Quantity {hr}"
        headers = headerString.split(",")
        #print headers
        #print len(headers)
        headers = numpy.array(headers, dtype = object)
        units = ["-" for i in range(34)]
        units = numpy.array(units, dtype = object)
        headers = numpy.array(units, dtype = object)
        
        thisData = AnalysisData(dataColumns= epwNumpyArray,
                                sourceFilePath=self.filePath,
                                headers = headers,
                                units=units,
                                timeVector=timeVector,
                                system="Weather",
                                pointType="All",
                                number="0",
                                description="Weather"
                                )
        
        
        #logging.debug("Returning the Analysis Data {}".format(thisData))

        
        
        return thisData
            
class AnalysisData(object):
    """
    AnalysisData consists of a matrix of size n-timeStepRows and m-DataColumns
    Also has a n-length timeVector, and m-length headers and units
    """
    def __init__(self, 
                 dataColumns, 
                 sourceFilePath, 
                 headers=None, 
                 units=None, 
                 timeVector=None, 
                 system=None, 
                 pointType=None, 
                 number=None,
                 description = None,
                 ):
        
        self.dataColumns = dataColumns    
        self.headers = headers   
        self.units = units
        self.timeVector = timeVector
        self.sourceFilePath = sourceFilePath
        self.sourceFileBaseName = os.path.basename(self.sourceFilePath)
        self.system=system
        self.pointType=pointType
        self.number =number
        self.description=description

        logging.debug("Created AnalysisData object ".format())
        self.get_dimensions()
        self.printConsistency()
        
    def __str__(self):
        return "{}:{}:{} '{}' from {}".format(
                                    self.system,
                                    self.pointType,
                                    self.number,
                                    self.description,
                                    self.getConsistency()
                                    )
    def get_dimensions(self):
        self.nTimeStepRows = self.dataColumns.shape[0]
        
        self.mDataColumns = self.dataColumns.shape[1]
               
        try: self.mHeaders = len(self.headers)
        except: self.mHeaders = 0
        
        try: self.mUnits = len(self.units)
        except: self.mUnits = 0
        
        try: self.nTimes = len(self.timeVector)
        except: self.nTimes = 0 

    def fakeHeaders(self):
        self.headers = ['-']*self.mDataColumns

    def fakeUnits(self):
        self.units = ['-']*self.mDataColumns
    
    def getConsistency(self):
        return "[cols heads units] [{} {} {}] [timeRows timeSteps] [{} {}] in {}".format(self.mDataColumns, 
                                                                                                  self.mHeaders, 
                                                                                                  self.mUnits,
                                                                                                  self.nTimeStepRows, 
                                                                                                  self.nTimes, 
                                                                                                  self.sourceFileBaseName
                                                                                                  )
    def printConsistency(self):
        self.get_dimensions()
        logging.info(self.getConsistency())
        #logging.debug("".format())

    def print_first_4(self):
        colWidth = 15
        templateString = "{:15}  " * len(self.headers)
        print templateString.format(*self.headers)
        templateString = "{:15}  " * len(self.units)
        print templateString.format(*self.units)
        templateString = "{:<15}  " * self.mDataColumns
        
        
        for line in self.dataColumns[:4]:
            print templateString.format(*line)
            
    def forceConsistency(self):
        nTimeStepRows = self.dataColumns.shape[0]
        mDataColumns = self.dataColumns.shape[1]
     
        try: mHeaders = len(self.headers)
        except: mHeaders = 0
        try: mUnits = len(self.units)
        except: mUnits = 0
        try: nTimes = len(self.timeVector)
        except: nTimes = 0 
        
        #print "assert", mDataColumns == mHeaders == mUnits
        assert mDataColumns == mHeaders == mUnits, "Must have headers and units for all columns!"
    
        assert nTimeStepRows == nTimes, "Must have a time step for all points!"
    def forceDataTypes(self):
        #print self.dataColumns.dtype.kind
        #print self.headers.dtype.kind
        assert self.dataColumns.dtype.kind == "f" 
        #isinstance(self.dataColumns,type(numpy.array()))
        assert isinstance(self.sourceFilePath, type(""))
        assert self.headers.dtype.kind == "O" 
        #isinstance(self.headers, type(list()))
        assert self.units.dtype.kind == "O"  
        #isinstance(self.units, type(list()))
        assert self.timeVector.dtype.kind == "f" 
        #isinstance(self.timeVector, type(numpy.array())) 
        assert isinstance(self.system, type(""))
        assert isinstance(self.pointType, type(""))
        assert isinstance(self.number, type(int()))
        assert isinstance(self.description, type(""))
        
        
    def returnDataDictionary(self):
        self.forceConsistency()
        self.forceDataTypes()
        
        # This is a single statepoint
        
#        statePoint  = {self.pointType:{
#                  "data":self.dataColumns,
#                  "headers":self.headers,
#                  "time":self.timeVector,
#                  "units":self.units,
#                    self.number =number
#                    self.description=description                      
#                  }}
        
    
        
        #nameOfStruct = "data" + os.path.splitext(self.sourceFileBaseName)[0]
#        structure = {self.system:{
#                  "data":self.dataColumns,
#                  "headers":self.headers,
#                  "time":self.timeVector,
#                  "units":self.units,
#                  }}
#        structure = {nameOfStruct:{
#                     
#                  "data":self.dataColumns,
#                  "headers":self.headers,
#
#                  }}
        #print structure
        #matFilePath = os.path.join(filePath,self.sourceFileBaseName + ".mat")
        #print matFilePath
        
        #print matFilePath
        #print structure
        #savemat(matFilePath, {"tt" : self.dataColumns}, oned_as='row')
        
        logging.debug("Returning dictionary from {}".format(self))
        

def datetime2matlabdn(dt):
    mdn = dt + timedelta(days = 366)
    frac_seconds = (dt-datetime.datetime(dt.year,dt.month,dt.day,0,0,0)).seconds / (24.0 * 60.0 * 60.0)
    frac_microseconds = dt.microsecond / (24.0 * 60.0 * 60.0 * 1000000.0)
    return mdn.toordinal() + frac_seconds + frac_microseconds

def getFilesByExt(rootPath,ext):
    ext = "." + ext
    
    # Walk the project dir
    allFilePathList = list()
    for root, dirs, files in os.walk(rootPath):
        for name in files:       
            thisFilePath = os.path.join(root, name)
            allFilePathList.append(thisFilePath)
    
    
    # Filter 
    resultFilePaths = list()

    resultFilePaths = [filePath for filePath in allFilePathList if 
                    os.path.splitext(filePath)[1].lower() == ext.lower()
                    ]
   
    logging.info("Found {} {} files in {}".format(len(resultFilePaths),ext,rootPath))
    
    return resultFilePaths

def load_EPW_file(rootPath):

    outFilePaths = getFilesByExt(rootPath, "EPW")
    
    
    fileDataObjects = list()
    for outFilePath in outFilePaths:
        #print outFilePath
        thisEpwFileObj = AnalysisFile(outFilePath)
        thisEpwFileObj.loadAllText()
        thisEPWdata = thisEpwFileObj.returnAnalysisData_EPW()
        fileDataObjects.append(thisEPWdata)
        
    return fileDataObjects

def load_OUT_files(rootPath):
    logging.debug("Loading OUT files from {}".format(rootPath))
    
    outFilePaths = getFilesByExt(rootPath, "OUT")

    # Process the BAL files
    outFileDataObjects = list()
    for outFilePath in outFilePaths:
        pureFileName = os.path.splitext(os.path.split(outFilePath)[1])[0]
        splitFileName = re.split("_",pureFileName)
        if len(splitFileName)==3:
            #print splitFileName
            thisOutFileObj = AnalysisFile(outFilePath)
            thisOutFileObj.loadAllText()
            #print thisBalFileObj.fileData
            thisAnlysisData = thisOutFileObj.returnAnalysisData_OUT()
            outFileDataObjects.append(thisAnlysisData)
            #thisBalFileObj.loadAllText()
        else:
            logging.info("(Skipping '{}')".format(os.path.split(outFilePath)[1]))
    
    assert isinstance(outFileDataObjects, type(list()))
    
    logging.info("Loaded and {} AnalysisData objects".format(len(outFileDataObjects)))
       
    return outFileDataObjects
  

def load_BAL_files(pathBUIproj):
    logging.debug("Loading BAL files from {}".format(pathBUIproj))
    
    # Walk the project dir
    allFilePathList = list()
    for root, dirs, files in os.walk(pathBUIproj):
        for name in files:       
            thisFilePath = os.path.join(root, name)
            allFilePathList.append(thisFilePath)
            
    # Filter for the BAL files
    balFilePaths = [
                    filePath for filePath in allFilePathList 
                    if 
                    os.path.splitext(filePath)[1].lower() == ".BAL".lower() and 
                    not os.path.splitext(os.path.basename(filePath))[0] == "SUMMARY"
                    ]
                    #os.path.splitext(os.path.basename(filePath))[0] == "Energy_zone"]
   
    logging.info("Found {} .BAL files in {}".format(len(balFilePaths),pathBUIproj))
    
    # Process the BAL files
    balFileDataObjects = list()
    for balFilePath in balFilePaths:
        thisBalFileObj = AnalysisFile(balFilePath)
        thisBalFileObj.loadAllText()
        #print thisBalFileObj.fileData
        thsiAnalysisData = thisBalFileObj.returnAnalysisData_BAL()
        balFileDataObjects.append(thsiAnalysisData)

    logging.info("Loaded and  {} AnalysisData objects".format(len(balFileDataObjects)))
    
    #print balFileDataObjects
    
    return balFileDataObjects

def getTimeColArray(resultFiles):
    forceTime(resultFiles)
    timeVector = resultFiles[0].timeVector
    timeColumns = [(2013,0,0,hour,0,0) for hour in timeVector]
    timeArray = numpy.array(timeColumns)  
    
    logging.info("Time columns created".format())
    
    return timeArray

def forceTime(thisDataList):
    #print thisDataList
    lastTimeVector = thisDataList[0].timeVector
    for dataObj in thisDataList:
        #assert dataObj.timeVector.all() == lastTimeVector.all()
        assert dataObj.timeVector.all() is lastTimeVector.all() 
    logging.info("Time checked over {} AnalysisData objects - OK".format(len(thisDataList)))
        


def show1line(string):
    #print len(string.split("/n")[0])
    #print repr(string)
    return str(string).split("\n")[0]


def augmentDescriptions(anlaysisObjects,descriptionsFilePath):
    # descriptionsFilePath is an excel file with a proper "Descriptions" sheet
    parametersBook = ExcelBook(descriptionsFilePath)
    descriptionsTable = parametersBook.getTable("Descriptions",1,200,1,4)
    #print descriptionsTable
    descriptions = list()
    for row in descriptionsTable[1:]:
        if row[0] and row[3]:
            try:
                row[2] = int(row[2])
            except:
                print "This row fails", row
                raise
            descriptions.append((tuple(row[:3]), row[3]))

    #for desc in descriptions:
    #    print desc[0]
    

    for point in anlaysisObjects:
        thisPointTuple = (point.system.encode("utf-8"), point.pointType.encode("utf-8"), point.number)
        #print thisPointTuple
        matchFound = False
        for desc in descriptions:
            if desc[0] == thisPointTuple:
                logging.debug("Description for {}: {}".format(thisPointTuple, desc[1]))
                point.description = desc[1]
                matchFound = True
        if not matchFound:
            raise Exception("No description match for {}".format(thisPointTuple))
        
    logging.info("Descriptions added for {} points".format(len(anlaysisObjects)))



def saveToMat(thisDictionary, matFilePath):
    
    #print thisDataList
    
    # Get the overall dictionary structure
    
#    for thisData in thisDataList:
#        #print thisData
#        thisData.returnDataDictionary()
#        #thisFile.
#        #thisFile.save_mat(dirPath)
        
        
    savemat(matFilePath, thisDictionary, oned_as='row')

    logging.info("Saved objects into {} ".format( matFilePath))
    

def convertKJHtoKW(anlaysisObjects):
    for point in anlaysisObjects:
        
        #print list(point.units)
        itemIndex=numpy.where(point.units==r"[kJ/hr]")[0]
        #print itemIndex
        #print "empty?", itemIndex
        #print itemIndex, itemIndex == True
        if itemIndex.size:
            #print point.units[itemIndex]
            point.units[itemIndex] = "[kW]"
            point.dataColumns[:,itemIndex] = point.dataColumns[:,itemIndex] / 3600
            #print point.dataColumns
            #print point.dataColumns[itemIndex] 
        #print point.units[itemIndex] / 3600
        #for unit in point.units:
        #    print unit,
        #print 
    #raise

def _loadEPW():
    pathEPW = r'D:\Dropbox\00 Decathlon Development\Weather\EPW'    
    #epwData = load_EPW_file()
    
    epwFiles = load_EPW_file(pathEPW)
    print getTimeColArray(epwFiles)
    #showSimplerStructure(epwFiles)
    

def _load_decathlon():
    #epwData = load_EPW_file(r'D:\Dropbox\00 Decathlon Development\Weather\EPW\CZ08RV2.epw')
    #print epwData
    #saveToMat([epwData],r"D:\Dropbox\00 Decathlon Development\02 Modeling update (shades)")
    #epwData.save_mat()
    
    #### LOAD THE FILES ####
    #projectDir = r"D:\Dropbox\00 Decathlon Development\02 Modeling update (shades)\Variants\00 TEST project only\OUT"
    projectDir = r"C:\DropBox\00 Decathlon Development\02 Modeling update (shades)\Variants\00 Open Open"
    outputMatDir = r"C:\Dropbox\00 Decathlon Development\02 Modeling update (shades)\output.mat"
    descriptionsFilePath = r"C:\DropBox\00 Decathlon Development\02 Modeling update (shades)\Input Data\Parameters r02.xlsx"
    resultFiles = load_BAL_files(projectDir) + load_OUT_files(projectDir)
    
    # Augment with descriptsion
    augmentDescriptions(resultFiles,descriptionsFilePath)
    
    convertKJHtoKW(resultFiles)
    
    #### ARRANGE THE FILES ####
    #arrangedDictionary = arrangeData(resultFiles)
    #showStructure(arrangedDictionary)
    #showSimplerStructure(arrangedDictionary)
    
    #### GET THE TIME ####
    # Always customize the time when comparing different sources

    timeDict = {"timeColumns":timeArray}
    #arrangedDictionary["time"] = timeDict
    
    exportDict = {}
    exportDict["trnData"] = arrangedDictionary
    exportDict["time"] = timeDict
    
    
    #### SAVE ####
    saveToMat(exportDict,outputMatDir)
    
    logging.info("Finished {}".format(whoami()))


#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):
    def test010_SimpleCreation(self):
        print "**** TEST {} ****".format(whoami())
    
    def testLoadEPW(self):
        pass
    
    def testLoadAll(self):
        projectDir = r"D:\Dropbox\00 Decathlon Development\02 Modeling update (shades)"
        outputMatDir = r"D:\Dropbox\00 Decathlon Development\02 Modeling update (shades)\output.mat"
        projectDir = r"C:\Dropbox\00 Decathlon Development\02 Modeling update (shades)"
        outputMatDir = r"C:\Dropbox\00 Decathlon Development\02 Modeling update (shades)\output.mat"    
        #balFiles = load_BAL_files(projectDir)
        outFiles = load_OUT_files(projectDir)
        #saveToMat([outFiles])
    
    def testLoadOut(self):
        outFiles = load_OUT_files(r"D:\Dropbox\00 Decathlon Development\02 Modeling update (shades)\Variants\00 Open Open")
    
    


#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    logging.config.fileConfig('..\\LoggingConfig\\loggingNofile.conf')
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")
    #myLogger.setLevel("INFO")
    logging.debug("Started _main".format())
    
    #_testing()
    #_load_decathlon()
    #_testLoadAll()
    _loadEPW()

    #unittest.main()

    
    

    logging.debug("Finished _main".format())
    