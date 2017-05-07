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
class DataFile(FileObject):
    """Receives the full path to a: 
        BAL file
        OUT file
        EPW file
    Returns 2 2D lists:
        headers
        data 
    
    """
    def __init__(self, fullFilePath): 
        #timeVector = None
        #dataMatrix = None
        #headers = None
        #units = None
        super(DataFile,self).__init__(fullFilePath)
        
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
        
        print headers
        print units
        raise
        
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
        for line in self.fileData.split('\n')[8:]:
            #print line.split(",")
            thisLine = line.split(",")
            try:
                thisLine.pop(5)
            except:
                pass
                #print "No pop"
                
            #print thisLine
            epwArray.append(thisLine)
        
        epwArray.pop()
        
        timeVector = [line[0:4] for line in epwArray]
#        for line in timeVector:
#            #pass
#            #print line
#            if len(line) is not 4:
#                raise
#            #print line == True
#        
        timeVector = numpy.array(timeVector, dtype=float)
        
        #for line in epwArray[8000:]:
            #pass
        #    print line
            #if len(line) is not 4:
            #    raise
                    
        #print epwArray[]
        epwNumpyArray = numpy.array(epwArray, dtype=float)
        
        #print timeVector
        #headers = ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Dry Bulb Temperature (C)', 'Dew Point Temperature (C)', 'Relative Humidity', 'Atmospheric Station Pressure (Pa)', 'Extraterrestrial Horizontal Radiation (Wh/m2)', 'Extraterrestrial Direct Normal Radiation (Wh/m2)', 'Horizontal Infrared Radiation from Sky (Wh/m2)', 'Global Horizontal Radiation (Wh/m2)', 'Direct Normal Radiation (Wh/m2)', 'Diffuse Horizontal Radiation (Wh/m2)', 'Global Horizontal Illuminance (lux)', 'Direct Normal Illuminance (lux)', 'Diffuse Horizontal Illuminance (lux)', 'Zenith Illuminance (lux)', 'Wind Direction (deg)', 'Wind Speed (m/s)', 'Total Sky Cover', 'Opaque Sky Cover', 'Visibility (km)', 'Ceiling Height (m)', 'Present Weather Ovservation', 'Present Weather Codes', 'Precipitable Water (mm)', 'Aerosol Optical Depth (thousandths)', 'Snow Depth (cm)', 'Days Since Last Snowfall']
        headerString = "Year, Month, Day, Hour, Minute, DryBulb,DewPoint ,RelHum ,Atmos Pressure ,ExtHorzRad ,ExtDirRad ,HorzIRSky ,GloHorzRad ,DirNormRad ,DifHorzRad ,GloHorzIllum ,DirNormIllum ,DifHorzIllum ,ZenLum ,WindDir ,WindSpd ,TotSkyCvr ,OpaqSkyCvr ,Visibility ,Ceiling Hgt ,PresWeathObs,PresWeathCodes,Precip Wtr ,Aerosol Opt Depth ,SnowDepth ,Days Last Snow,Albedo , Rain,Rain Quantity"
        headers = headerString.split(",")

        unitString = ", , , , , {C}, {C}, {%},{Pa},{Wh/m2},{Wh/m2},{Wh/m2},{Wh/m2}, {Wh/m2}, {Wh/m2}, {lux}, {lux}, {lux}, {Cd/m2}, {deg}, {m/s}, {.1}, {.1}, {km},  {m},,,  {mm},   {.001}, {cm},  , {.01},{mm},{hr}"
        units = unitString.split(",")
        
        #print headers
        #print len(headers)
        headers = numpy.array(headers, dtype = object)
        units = numpy.array(units, dtype = object)

        #units = ["-" for i in range(34)]
        
        #headers = numpy.array(units, dtype = object)
        
        
        sourceFileBaseName = os.path.basename(self.filePath)
        
        thisData = AnalysisData(dataColumns= epwNumpyArray,
                                sourceFilePath=self.filePath,
                                headers = headers,
                                units=units,
                                timeVector=timeVector,
                                system=sourceFileBaseName,
                                pointType="All",
                                number="0",
                                description="Weather"
                                )
        
        
        #logging.debug("Returning the Analysis Data {}".format(thisData))

        return thisData

class AnalysisFile2(FileObject):
    """Receives the full path to a: 
        BAL file
        OUT file
        EPW file
    Returns 2 2D lists:
        headers
        data 
    And 1 list, with the types of data in the header 
    (data, headers, headerDef)
    """
    def __init__(self, fullFilePath): 
        #timeVector = None
        #dataMatrix = None
        #headers = None
        #units = None
        super(AnalysisFile2,self).__init__(fullFilePath)

    def returnAnalysisData_OUT(self):
        data = list()
        headers = list()
        headerDef = ["labels","units"]
        lineCount = 0
        for line in self.fileData.split('\n'):
            #print line
            if line: 
                theseItems = re.compile("\s+").split(line.lstrip().rstrip())
                if lineCount == 0:
                    headers.append(list(theseItems[1:]))
                elif lineCount == 1:
                    headers.append(list(theseItems[1:]))
                else:
                    # Skip the first item, the time vector!
                    theseFloats = [float(num) for num in theseItems[1:]]
                    data.append(theseFloats)

                lineCount = lineCount + 1
        
        # This is messy
        headers = zip(*headers) # Transpose
        headers = [list(col) for col in headers] # Force list!?

        headerDef.append("source")
        pureFileName = os.path.splitext(os.path.split(self.filePath)[1])[0]
        [col.append(pureFileName) for col in headers]

        splitFileName = re.split("_",pureFileName)
        
        headerDef.append("system")
        system = splitFileName[0]
        [col.append(system) for col in headers]

        headerDef.append("pointType")
        pointType = splitFileName[1]
        [col.append(pointType) for col in headers]

        headerDef.append("number")
        number = splitFileName[2]
        number = int(number)
        [col.append(number) for col in headers]
        
        
        return DataFrameList("",data,None,headers,headerDef)

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
        
        logging.debug("Returning dictionary from {}".format(self))

class DataFrameList(object):
    """
    AnalysisData consists of a matrix of size n-timeStepRows and m-DataColumns
    Also has a n-length timeVector, and m-length headers and units
    """
    def __init__(self, 
                 name,
                 dataArray, 
                 timeSeriesArray, 
                 headersArray, 
                 headersDef,
                 ):
        self.name = name
        self.dataArray       = dataArray      
        self.timeSeriesArray = timeSeriesArray
        self.headersArray    = headersArray
        self.headersDef = headersDef
        
        logging.info("{} Data: {} Time: {} Headers: {}".format(self.name, self.dataStr(),
                                       self.timeStr(),
                                       self.headStr(),
                                       ))
    def dataStr(self):
        return numpy.shape(self.dataArray)
    
    def timeStr(self):
        return numpy.shape(self.timeSeriesArray)
    
    def headStr(self):
        return numpy.shape(self.headersArray)
    
    
    
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
        thisEpwFileObj = DataFile(outFilePath)
        thisEpwFileObj.loadAllText()
        thisEPWdata = thisEpwFileObj.returnAnalysisData_EPW()
        fileDataObjects.append(thisEPWdata)
        
    return fileDataObjects

def load_OUT_files(pathProj):
    logging.debug("Loading OUT files from {}".format(pathProj))
    
    # Walk the project dir
    allFilePathList = list()
    for root, dirs, files in os.walk(pathProj):
        for name in files:       
            thisFilePath = os.path.join(root, name)
            allFilePathList.append(thisFilePath)
    
    # Filter for the BAL files
    outFilePaths = list()

    outFilePaths = [filePath for filePath in allFilePathList if 
                    os.path.splitext(filePath)[1].lower() == ".OUT".lower()
                    ]
   
    logging.info("Found {} .OUT files in {}".format(len(outFilePaths),pathProj))
    
    # Process the files
    outFileDataObjects = list()
    for outFilePath in outFilePaths:
        pureFileName = os.path.splitext(os.path.split(outFilePath)[1])[0]
        splitFileName = re.split("_",pureFileName)
        if len(splitFileName)==3:
            #print splitFileName
            thisOutFileObj = AnalysisFile2(outFilePath)
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
        thisBalFileObj = DataFile(balFilePath)
        thisBalFileObj.loadAllText()
        #print thisBalFileObj.fileData
        thsiAnalysisData = thisBalFileObj.returnAnalysisData_BAL()
        balFileDataObjects.append(thsiAnalysisData)

    logging.info("Loaded and  {} AnalysisData objects".format(len(balFileDataObjects)))
    
    #print balFileDataObjects
    
    return balFileDataObjects

def getTime(resultFiles):
    forceTime(resultFiles)
    
    try:
        iterator = iter(resultFiles)
    except TypeError:
        return resultFiles.timeVector  
    else:
        firstFileTimeVec = resultFiles[0].timeVector 
        logging.info("Returning time vec: {}".format(firstFileTimeVec))        
        return firstFileTimeVec

            
    
     

def forceTime(thisDataList):
    try:
        iterator = iter(thisDataList)
    except TypeError:
        logging.info("Only 1 data object no need to check time consistency".format())        
        return
    else:
        lastTimeVector = thisDataList[0].timeVector
        for dataObj in thisDataList:
            #assert dataObj.timeVector.all() == lastTimeVector.all()
            assert dataObj.timeVector.all() is lastTimeVector.all()
    
        logging.info("Time checked over {} AnalysisData objects - OK".format(len(thisDataList)))

def arrangeDataFlat(thisDataList):
    
    try:
        iterator = iter(thisDataList)
    except TypeError:
        thisDataList = [thisDataList]
    else: 
        pass
    #objCount = 0
    headersList = list()
    dataList = list()
    
    for dataObj in thisDataList:
        numCols = dataObj.dataColumns.shape[1]
        extraZoneDescriptions = ["", "", " Ideal Heat"," Ideal Cool", " QTSPAS"]
        if dataObj.pointType == "Zone":
            #print dataObj.description, "ZONE"
            #print dataObj.pointType
            theseDescriptions = [dataObj.description + extraZoneDescriptions[i] for i in range(0,numCols)]
        else:
            #print dataObj.description 
            theseDescriptions = [dataObj.description for i in range(0,numCols)]
        #print theseDescriptions
        for iCols in range(0,numCols):
            #print theseDescriptions[iCols]
            #print iCols
            #objCount += 1
            
            
            #systemRow           = 1
            #pointTypeRow        = 2
            #numberRow           = 3
            #headersRow          = 4                    
            #descriptionRow      = 5
            #unitsRow            = 6
            #sourceFilePathRow   = 7
            
            headList =                   [dataObj.system,
                                    dataObj.pointType,
                                    dataObj.number,
                                    dataObj.headers[iCols],                     
                                    theseDescriptions[iCols],
                                    dataObj.units[iCols],
                                    dataObj.sourceFilePath,]
            
            #print len(headList)
            
            headersList.append(headList)
            
            dataList.append(dataObj.dataColumns[:,iCols])
    
    #print len(headersList)
    headersArray = numpy.array(headersList,dtype=object )
    #print headersArray
    #print headersArray.shape
    
    headersArray = headersArray.transpose()
    dataArray = numpy.array(dataList)
    dataArray = dataArray.transpose()
    
    #### GET THE TIME ####
    # Always customize the time when comparing different sources
    #timeVector = getTime(thisDataList)
    #timeColumns = [(2013,0,0,hour,0,0) for hour in timeVector]
    #timeArray = numpy.array(timeColumns)
    #timeDict = {"timeColumns":timeArray}
    
    #print len(dataList)
    
    arrangedDict = {"data":dataArray,"headers":headersArray}
    
    return arrangedDict
    
 
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
                #logging.debug("Description for {}: {}".format(thisPointTuple, desc[1]))
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
    count = 0
    for point in anlaysisObjects:
        
        #print list(point.units)
        itemIndex=numpy.where(point.units==r"[kJ/hr]")[0]
        #print itemIndex
        #print "empty?", itemIndex
        #print itemIndex, itemIndex == True
        if itemIndex.size:
            count = count + 1
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
    logging.info("Converted {} entries to kW ".format( count))


def _wienWeather():
    weatherDir = r"D:\Freelance\086_SmartCampus1\WEA\Study"
    epwObjects = load_EPW_file(weatherDir)
    timeArray = getTime(epwObjects)
    
    arrangedDictionary = arrangeDataFlat(epwObjects)
    
    timeDict = {"timeColumns":timeArray}

    exportDict = {}
    exportDict["theData"] = arrangedDictionary
    exportDict["time"] = timeDict

    saveToMat(exportDict, r'D:\Freelance\086_SmartCampus1\WEA\Study\compare.out')    

def _SCWE1():
    projectOutDir = r"D:\Freelance\086_SmartCampus1\TRNSYS\OUT"
    descriptionsFilePath = r"D:\Freelance\086_SmartCampus1\Input\Parameters r15.xlsx"
    
    matfileOutDir = r"D:\Freelance\086_SmartCampus1\FIG\\"
    matFileName = r"MainLoadsLowerSP.mat"
    
    matFileFullPath = os.path.join(matfileOutDir,matFileName)
    
    outFiles = load_OUT_files(projectOutDir)
    convertKJHtoKW(outFiles)
    augmentDescriptions(outFiles,descriptionsFilePath)
    timeArray = getTime(outFiles)
    
    arrangedDictionary = arrangeDataFlat(outFiles)
    
    timeDict = {"timeColumns":timeArray}

    exportDict = {}
    exportDict["theData"] = arrangedDictionary
    exportDict["time"] = timeDict
    
    thisName = "Test frame"
    thisFrame = DataFrame(thisName,arrangedDictionary["data"],timeArray,arrangedDictionary["headers"])
    
    #saveToMat(exportDict, matFileFullPath)    

#===============================================================================
# Unit testing
#===============================================================================
def _SCWE2():
    projectOutDir = r"D:\Freelance\086_SmartCampus1\TRNSYS\OUT"
    descriptionsFilePath = r"D:\Freelance\086_SmartCampus1\Input\Parameters r15.xlsx"
    
    matfileOutDir = r"D:\Freelance\086_SmartCampus1\FIG\\"
    matFileName = r"MainLoadsLowerSP.mat"
    
    matFileFullPath = os.path.join(matfileOutDir,matFileName)
    
    outFiles = load_OUT_files(projectOutDir)
    convertKJHtoKW(outFiles)
    augmentDescriptions(outFiles,descriptionsFilePath)
    timeArray = getTime(outFiles)
    
    arrangedDictionary = arrangeDataFlat(outFiles)
    
    timeDict = {"timeColumns":timeArray}

    exportDict = {}
    exportDict["theData"] = arrangedDictionary
    exportDict["time"] = timeDict
    
    thisName = "Test frame"
    thisFrame = DataFrame(thisName,arrangedDictionary["data"],timeArray,arrangedDictionary["headers"])
    
    #saveToMat(exportDict, matFileFullPath)    

#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):
    def setUp(self):
        #### LOAD THE FILES ####
        if 0:
            self.projectDir = r"C:\DropBox\00 Decathlon Development\02 Modeling update (shades)\Variants\00 Open Open"
            self.weatherDir = r"D:\Dropbox\00 Decathlon Development\Weather\EPW"
            self.outputMatDir = r"C:\Dropbox\00 Decathlon Development\02 Modeling update (shades)\output.mat"
            self.descriptionsFilePath = r"C:\DropBox\00 Decathlon Development\02 Modeling update (shades)\Input Data\Parameters r02.xlsx"
        if 1:
            self.weatherDir = r"D:\Dropbox\00 Decathlon Development\Weather\EPW"
            self.projectDir = r"D:\DropBox\00 Decathlon Development\02 Modeling update (shades)\Variants\00 Open Open"
            self.outputMatDir = r"D:\Dropbox\00 Decathlon Development\MatlabOutput\output2.mat"
            self.descriptionsFilePath = r"D:\DropBox\00 Decathlon Development\02 Modeling update (shades)\Input Data\Parameters r02.xlsx"

        #### ARRANGE THE FILES ####
        #arrangedDictionary = arrangeData(resultFiles)
        #showStructure(arrangedDictionary)
        #showSimplerStructure(arrangedDictionary)
        
    def NOtest010_FlatData(self):
        print "**** TEST {} ****".format(whoami())
        resultFiles = load_BAL_files(self.projectDir) + load_OUT_files(self.projectDir)
        # Augment with descriptsion
        augmentDescriptions(resultFiles,self.descriptionsFilePath)
        convertKJHtoKW(resultFiles)
        arrangedDictionary = arrangeDataFlat(resultFiles)
        
        # Get the time
        # Always customize the time when comparing different sources
        timeVector = getTime(resultFiles)
        timeColumns = [(2013,0,0,hour,0,0) for hour in timeVector]
        timeArray = numpy.array(timeColumns)
        timeDict = {"timeColumns":timeArray}
        
        exportDict = {}
        exportDict["theData"] = arrangedDictionary
        exportDict["time"] = timeDict
        #print timeDict
        saveToMat(exportDict, self.outputMatDir)
        

    def test020_WeatherData(self):
        print "**** TEST {} ****".format(whoami())
        epwObjects = load_EPW_file(self.weatherDir)
        timeArray = getTime(epwObjects)
        
        arrangedDictionary = arrangeDataFlat(epwObjects)
        
        timeDict = {"timeColumns":timeArray}
    
        exportDict = {}
        exportDict["theData"] = arrangedDictionary
        exportDict["time"] = timeDict

        saveToMat(exportDict, self.outputMatDir)
        

#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    logging.config.fileConfig('..\\LoggingConfig\\loggingNofile.conf')
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")
    #myLogger.setLevel("INFO")
    logging.debug("Started _main".format())

    #_wienWeather()
    _SCWE2()
    #unittest.main()
    
    #_testing()
    #_load_decathlon()
    #_testLoadAll()
    
    

    logging.debug("Finished _main".format())
    