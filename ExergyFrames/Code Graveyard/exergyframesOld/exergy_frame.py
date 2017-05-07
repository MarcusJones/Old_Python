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
import logging
from UtilityInspect import whoami, whosdaddy
from UtilityFile import FileObject
from UtilityPathsAndDirs import getFilesByExtRecurse
import os
import re
import numpy as np
import scipy
from scipy.io import savemat
from datetime import timedelta, datetime
import pprint 
import unittest
import random
import csv
#from __future__ import print_function

#===============================================================================
# Code
#===============================================================================




class DataFile(FileObject):
    # TODO: Don't need this class! Just use functions! See illum loader
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
    def __init__(self, fullFilePath,descriptions): 
        #timeVector = None
        #dataMatrix = None
        #headers = None
        #units = None
        self.descriptions = descriptions
        super(DataFile,self).__init__(fullFilePath)
    
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
        
        # TODO: This is messy
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
        number = str(number)
        [col.append(number) for col in headers]
        
        headerDef.append("description")

        pointAddress = (system, pointType, number)
        uniPointAddress = tuple([unicode(item) for item in  pointAddress])

        extraZoneDescriptions = ["", "", " Ideal Heat"," Ideal Cool", " QTSPAS"]
        try: 
            thisDesc = self.descriptions[uniPointAddress]
            if pointType == "Zone":
                for col,extraDesc in zip(headers,extraZoneDescriptions):
                    col.append(thisDesc + extraDesc)
            else:
                [col.append(thisDesc) for col in headers]
        except:
            [col.append("description") for col in headers]
        
        return DataFrameList("",data,None,headers,headerDef)


class Idx(object):
    """This class does something for someone. 
    """
    def __init__(self, headerDefs=None, headerValues=None, search_pairs=None): 
        if not search_pairs:
            self.search_pairs = [[headerDefs, headerValues]]
        elif search_pairs:
            self.search_pairs = search_pairs
        else:
            raise Exception("ERROR")
        #print "New IDX",self.searchPairs
        self.index = 0
    @classmethod
    def fromTuple(cls, pairs):
        #cls.searchPairs = pairs
        return cls(None,None,pairs)
        
    def __str__(self):
        return str(self.search_pairs)
    
    def __add__(self, other):
        totalPairs = self.search_pairs + other.search_pairs
        return self.__class__.fromTuple(totalPairs)
    
    def __iter__(self):
        return self
        
    def next(self):
        try:
            result = self.search_pairs[self.index]
        except IndexError:
            # Reset for next time!
            self.index = 0
            raise StopIteration
        self.index+=1
        return result
 
#class DataFrameList(object):
#    """
#    AnalysisData consists of a matrix of size n-timeStepRows and m-DataColumns
#    Also has a n-length timeVector, and m-length headers and units
#    """
#    def __init__(self, 
#                 name,
#                 dataArray, 
#                 timeSeriesArray, 
#                 headersArray, 
#                 headersDef,
#                 ):
#        self.name = name
#        self.dataArray       = dataArray      
#        self.timeSeriesArray = timeSeriesArray
#        self.headersArray    = headersArray
#        self.headersDef = headersDef
#        
#        logging.info("{} Data: {} Time: {} Headers: {}".format(self.name, self.dataStr(),
#                                       self.timeStr(),
#                                       self.headStr(),
#                                       ))
#    def dataStr(self):
#        return np.shape(self.dataArray)
#    
#    def timeStr(self):
#        return np.shape(self.timeSeriesArray)
#    
#    def headStr(self):
#        return np.shape(self.headersArray)

class ExergyFrame(object):
    """
    AnalysisData consists of a matrix of size n-timeStepRows and m-DataColumns
    n-length timeVector, 
    for each m column, there is a list of p attributes, a p-m header array
    header definitions are in a p-length array
    
    EXAMPLE;
    
       | alp   bet   char
       | a     b     c
    ---------------------    
    1  | 1     3     5
    2  | 1     3     5
    3  | 1     3     5
    4  | 1     3     5
    
    headerDef = ["name","letter"]
    
    m = 4
    n = 3
    p = 2
    
    
    INPUTS
    name           String, seen as output struct variable name for Matlab
    dataArray      n x m numerical 2D list OR 2D Numpy array
    timeArray      n x 1 numerical 1D list OR 1D Numpy array
    headersArray   1 x m string 1D list OR 1D Numpy array
    headersDey     p x 1 string 1D list OR 1D Numpy array
    
    """
    
    
    def __init__(self, 
                 name,
                 dataArray, 
                 timeArray, 
                 headersArray, 
                 headersDef,
                 ):
        self.name = name
        self.dataArray       = dataArray      
        self.timeArray = timeArray
        self.headersArray    = headersArray
        self.headersDef     = headersDef
        
        self._convert_to_ndarray()
        #self.add_frame_name()
        
        logging.info("FRAME - {} Data: {} Time: {} Headers: {} Def: {}".format(self.name, self.dataStr(),
                                       self.timeStr(),
                                       self.headStr(),
                                       self.headerDefStr(),
                                       ))
    def num_cols(self):
        return np.shape(self.dataArray)[1]
    
    
    def add_frame_name(self):
        raise
        self.headersDef.insert(0, "frameName")
        #print [self.name for i in range(np.shape(self.headersArray)[1])]
        self.headersArray.insert(0,[self.name for i in range(np.shape(self.headersArray)[1])])
    
    def add_simple_time(self):
        num_rows = np.shape(self.dataArray)[0]
        self.timeArray = range(num_rows)
        self._convert_to_ndarray()
        
    def checkTimeExists(self):
        try:
            if not self.timeArray.any():
                raise Exception("No time array!")
        except:
            if self.timeArray == [False]*len(self.timeArray):
                raise Exception("No time array!")
    
    def displayArray(self):
        
        for row in zip(self.headersDef, self.headersArray):
            print "{:10} {}".format(row[0],row[1:][0])
        
        self.checkTimeExists()

        indexedArray = zip(self.timeArray, self.dataArray)

        print "{:<10} {}".format(indexedArray[0][0],indexedArray[0][1:][0])
        print "{:<10} {}".format(":",":")
        print "{:<10} {}".format(indexedArray[-2][0],indexedArray[-2][1:][0])
        print "{:<10} {}".format(indexedArray[-1][0],indexedArray[-1][1:][0])

    
    def _convert_to_ndarray(self):
        self.dataArray = np.array(self.dataArray)
        self.timeArray = np.array(self.timeArray)
        self.headersArray = np.array(self.headersArray)
        self.headersDef  = np.array(self.headersDef)  
        
        logging.info("Converted to ndarray".format())    


    def findHeadRow(self,searchDef):
        """Given a regex, search the array of header definitions
        Return the index number corresponding to the matched value
        Now, must match beginning and end
        If multiple header defs with same name (should never happen!), returns 1st only
        
        """
        # TODO: Add check for duplicate header defs
        searchDef = "^" + searchDef + "$"
        idx = 0
        flgFound = False

        for foundHeaderDef in self.headersDef:
            if re.search(searchDef,foundHeaderDef):
                flgFound = True
                break
            idx +=1
        if flgFound:
            pass 
            #print idxHeaderDef,headerDef
        else:
            raise Exception, "{} not found in header definitions".format(searchDef)
        return idx
    

    def _getHeaderMask(self,idxHeadDef,searchStr):
        """Given the index row of a header, search all headers in that row
        If match, add this column to a mask
        Returns an array of dtype .bool which is used as a mask 
        Must find at least one match!
        """
        
        # Get header line
        header_def = self.headersDef[idxHeadDef]
        
        header_line = self.headersArray[idxHeadDef]
        #idxHeaderLine = 0

        #flgFound = False
        
        thisMask = np.zeros(self.num_cols(), dtype=np.bool)
        idx = 0
        for head in header_line:
            head = str(head)
            
            try:
                assert(type(searchStr) == type(head))
            except:
                
                #unicode(searchStr)
                print "type(searchStr)", type(searchStr)
                print "type(head)", type(head)
                raise
            if re.search(searchStr,head):
                thisMask[idx] = True
                foundHead = head
            idx +=1
        
        #print thisMask
        #raise
        
        if thisMask.any():
            pass 
        else:
            raise Exception, "FAILED HEAD LINE:\n {} \n {} not found in header, along header row {}, {} def".format(header_line,searchStr,idxHeadDef,header_def)
        
        logging.debug("Head {}={},  {} found ".format(header_def, searchStr, sum(thisMask), ))
        
        return thisMask
    
    def updateHeader(self,idx_object,targetHeadDef,newValueString):
        """
        
        """
        thisSearchTotalStr = list()
        #thisMergedmask = 
        maskList = list()
        
        for pair in idx_object:
            searchDef = pair[0]
            searchStr = pair[1]
            thisPairStr = "{}={}".format(searchDef,searchStr)
            thisSearchTotalStr.append(thisPairStr)
            idxRow = self.findHeadRow(searchDef)
            try:
                thisMask = self._getHeaderMask(idxRow,searchStr)
                maskList.append(thisMask)
                
            except:
                raise Exception, "Failed to match header '{}' = '{}'".format(searchDef, searchStr)

        overallMask = self.maskIntersection(maskList)

        #print idxHeaderDef
        headRow = self.headersArray[idxRow]
        idxCol = 0
        for head in headRow:
            if overallMask[idxCol]:
                #print self.headersArray[idxRow][idxCol]
                idxTargetRow = self.findHeadRow(targetHeadDef)
                targetHeaderDef = self.headersDef[idxTargetRow]
                self.headersArray[idxTargetRow][idxCol] = newValueString
                numberUpdates = np.sum(overallMask)
            idxCol += 1
        
        logging.info("Updated criteria {} {} times;  to {}, in {}, ".format(thisSearchTotalStr,numberUpdates,newValueString,targetHeaderDef))

    def updateHeaderConcat(self,idx_object,targetHeadDef,newValueString):
        """
        
        """
        thisSearchTotalStr = list()
        #thisMergedmask = 
        maskList = list()
        
        for pair in idx_object:
            searchDef = pair[0]
            searchStr = pair[1]
            thisPairStr = "{}={}".format(searchDef,searchStr)
            thisSearchTotalStr.append(thisPairStr)
            idxRow = self.findHeadRow(searchDef)
            try:
                thisMask = self._getHeaderMask(idxRow,searchStr)
                maskList.append(thisMask)
            except:
                raise Exception, "Failed to match header '{}' = '{}'".format(searchDef, searchStr)

        overallMask = self.maskIntersection(maskList)
        
        #print idxHeaderDef

        
        headRow = self.headersArray[idxRow]
        idxCol = 0
        for head in headRow:
            if overallMask[idxCol]:
                #print self.headersArray[idxRow][idxCol]
                idxTargetRow = self.findHeadRow(targetHeadDef)
                targetHeaderDef = self.headersDef[idxTargetRow]
                oldValueString = self.headersArray[idxTargetRow][idxCol]
                #newValueString = newValueString + " " + oldValueString
                self.headersArray[idxTargetRow][idxCol] = newValueString + oldValueString
                numberUpdates = np.sum(overallMask)
            idxCol += 1
        
        logging.info("Updated criteria {} {} times;  to {}, in {}, ".format(thisSearchTotalStr,numberUpdates,newValueString,targetHeaderDef))
    
    def overWriteHeadersDirect(self,idx_object,newValueString):
        for pair in idx_object:
            searchDef = pair[0]
            searchStr = pair[1]
            idxRow = self.findHeadRow(searchDef)
            thisMask = self._getHeaderMask(idxRow,searchStr)
            #print idxHeaderDef
            headRow = self.headersArray[idxRow]
            idxCol = 0
            for head in headRow:
                if thisMask[idxCol]:
                    #print self.headersArray[idxRow][idxCol]
                    self.headersArray[idxRow][idxCol] = newValueString
                idxCol += 1
            #print self.headersArray[idxHeaderDef,]
            
        logging.info("Direct head ".format())

    @property
    def allTimeMask(self):
        return self.timeArray == self.timeArray  

#    def modifyHeader(self,headDef,searchStr,newValue):
#        idxHeaderDef = self.findHeadRow(headDef)
#        #self._getHeaderDefMask
#        headMask = self._getHeaderMask(idxHeaderDef,searchStr)
#        print self.headersArray[idxHeaderDef][headMask]
#        

    def maskIntersection(self,maskList):
        overallMask = maskList[0]
        for mask in maskList:
            overallMask = overallMask & mask

        if not sum(overallMask) > 0:
            raise Exception("No elements found in intersection!")

        logging.info("Found {} elements in intersected overall mask".format(sum(overallMask)))
        

        
        return overallMask
            
    def maskUnion(self,maskList):
        overallMask = maskList[0]
        for mask in maskList:
            overallMask = overallMask | mask
        return overallMask
    
    def getHeadMaskIntersect(self,idx_object):
        """Get a mask based on a single Idx
        """
        
        #overallMask = np.zeros((self.num_cols(),), dtype=np.bool)
        maskList = list()
        for pair in idx_object:
            searchDef = pair[0]
            searchStr = pair[1]
            idxHeaderDef = self.findHeadRow(searchDef)
            thisMask = self._getHeaderMask(idxHeaderDef,searchStr)
            maskList.append(thisMask)
            # Union of the masks
            #overallMask = overallMask | thisMask
        overallMask = self.maskIntersection(maskList)
        logging.info("Head mask, {} found ".format( sum(overallMask)))

        return overallMask
    
    def getHeadMaskUnion(self,idx_object):
        """Get a mask based on a single Idx
        """
        
        #overallMask = np.zeros((self.num_cols(),), dtype=np.bool)
        maskList = list()
        for pair in idx_object:
            searchDef = pair[0]
            searchStr = pair[1]
            idxHeaderDef = self.findHeadRow(searchDef)
            thisMask = self._getHeaderMask(idxHeaderDef,searchStr)
            maskList.append(thisMask)
            # Union of the masks
            #overallMask = overallMask | thisMask
        overallMask = self.maskUnion(maskList)
        logging.info("Head mask, {} found ".format( sum(overallMask)))

        return overallMask

    def dataStr(self):
        return np.shape(self.dataArray)
    
    def timeStr(self):
        return np.shape(self.timeArray)
    
    def headStr(self):
        return np.shape(self.headersArray)
    
    def headerDefStr(self):
        return str(self.headersDef)
    
    def saveToMat(self,matFullPath):

        # Assemble dict from headersArray
        idxDef = 0
        headerDict = {}
        for headerDef in self.headersDef:
            idxDef += 1
            #print headerDict
            headerDict["{}".format(headerDef)] =idxDef
        
        headerDefList = headerDict.items()        
        
        sortedHeaderDefList = sorted(headerDefList, key=lambda tup: tup[1])
        headerCellArray = np.array(sortedHeaderDefList, dtype="object")
        #self.headersDef = headerCellArray

        thisDict = {self.name:{
                    "headers":self.headersArray,
                    "headerDef":headerCellArray,
                    "data":self.dataArray,
                    "time":self.timeArray,
                    }
                    }
        
        savemat(matFullPath, thisDict, oned_as='row')
        logging.info("Saved objects into {} ".format( matFullPath))
    
    def inPlaceFunction(self,timeMask,idx_object,passedFunction,newLabel):
        logging.debug("Updating cols  ".format())
        thisHeadMask = self.getHeadMaskUnion(idx_object)
        thisTimeMask = timeMask
        
        self.modifySubArray(thisTimeMask,thisHeadMask,passedFunction)
        self.overWriteHeadersDirect(idx_object,newLabel)
        
        
    
    def modifySubArray(self,timeMask,headmask,passedFunction):

        if timeMask == None:
            timeMask = self.allTimeMask
        else:
            # TODO:
            raise Exception("Time masking not yet supported!")
        
        matrixMask = np.outer(timeMask,headmask)

        #print np.shape(matrixMask)
        #print np.shape(self.dataArray)
        #print np.shape(self.dataArray[matrixMask])
        #raise
        self.dataArray[matrixMask] = passedFunction(self.dataArray[matrixMask])
        
        logging.debug("Sub array selection modified by {}, shape: {} ".format(passedFunction, np.shape(self.dataArray[matrixMask])))

    def extractSubFrame(self,timeMask,headmask):

        newData = self.dataArray[timeMask][:,headmask]
        
        newTime = self.timeArray[timeMask]
        newHeads = self.headersArray[:,headmask]
        newHeadDef = self.headersDef
        
        logging.debug("new sub array returned, shape: {} ".format( np.shape(newData)))
        
        return ExergyFrame("",newData,newTime,newHeads,newHeadDef)
    
    def addNewVector(self,timeMask,headmask,passedFunction,newHeadText):
        if timeMask == None:
            timeMask = self.allTimeMask
        else:
            # TODO:
            raise Exception("Time masking not yet supported!")
        
        logging.debug("Adding new column based on " +
            "{} rows, {} columns, using {}, header is {}".format(
                                                     sum(timeMask),
                                                     sum(headmask),
                                                     passedFunction,
                                                     newHeadText
                                                     ))

        
        subArray = self.extractSubFrame(timeMask,headmask)

        newData = passedFunction(subArray.dataArray)

        oldHead = subArray.headersArray[:,0]
        newHead = oldHead
        newHead[-1] = newHeadText

        self.dataArray = np.column_stack( [ self.dataArray , newData ] )
        self.headersArray = np.column_stack( [self.headersArray,newHead])
        logging.debug("{} Data columns now in this frame".format(np.shape(self.dataArray)[1]))
        
    def saveToCSV(self,csvFullPath):

        self.checkTimeExists()
        indexedArray = zip(self.timeArray, self.dataArray)
        
        myfile = open(csvFullPath, 'wb')
        wr = csv.writer(myfile)
        

        
        #f_handle = open(csvFullPath, 'w')
        #open (csvFullPath, 'a') as f 
        for row in zip(self.headersDef, self.headersArray):
            
            thisRow = [row[0]] + list(row[1:][0])
            wr.writerow(thisRow)
            #np.savetxt(f_handle,row,"%s",delimiter=',')
           
            #print map(list,row)
            #np.savetxt(f_handle,row,"%s",delimiter=',')
            #f_handle.write ("{:10} {}\n".format(row[0],row[1:][0])   )     
        
        for row in indexedArray:
            thisRow = [row[0]] + list(row[1:][0])       
            wr.writerow(thisRow)

        logging.info("Saved objects into {} ".format( csvFullPath))


def load_single_illum_file(fullFilePath):
    logging.info("Loading {} ".format( fullFilePath))
    
    data = list()
    headers = list()
    headerDef = ["FullFilePath","FileName","Serial","X","Y","Z","Name"]
    
    #print fullFilePath
    pureFileName = os.path.splitext(os.path.split(fullFilePath)[1])[0]
    #print pureFileName
    
    illum_file = FileObject(fullFilePath)
    illum_file.loadAllText()
    for line in illum_file.fileData.split('\n'):
        if line: 
            splitLine = re.split("\s+",line)
            thisDataLine = splitLine[3:]
            thisDataFloatList = [float(item) for item in thisDataLine]
            data.append(thisDataFloatList)
            numCols = len(thisDataFloatList)
    
    headers = list()
    for i in range(numCols):
        headers.append([fullFilePath,pureFileName,str(i),"","","",""])
    
    headers = zip(*headers)
    thisFrame = ExergyFrame("Illum",data,None,headers,headerDef)
    thisFrame.add_simple_time()
    
    logging.info("Illum frame".format())

    #print thisFrame.headersArray
    
    return thisFrame
        

def load_single_out_file(fullFilePath):
    # Setup
    data = list()
    headers = list()
    headerDef = ["labels","units"]
    
    # Get the data
    fileObject = FileObject(fullFilePath)
    fileObject.loadAllText()
    
    lineCount = 0
    for line in fileObject.fileData.split('\n'):
        #print line
        if line: 
            theseItems = re.compile("\s+").split(line.lstrip().rstrip())
            numCols = len(theseItems[1:])
            if lineCount == 0:
                headers.append(list(theseItems[1:]))
            elif lineCount == 1:
                headers.append(list(theseItems[1:]))
            else:
                # Skip the first item, the time vector!
                theseFloats = [float(num) for num in theseItems[1:]]
                data.append(theseFloats)
            lineCount = lineCount + 1

    # Process the headers


    # Get the attribs from file name
    pureFileName = os.path.splitext(os.path.split(fullFilePath)[1])[0]
    splitFileName = re.split("_",pureFileName)
    if len(splitFileName)==3:
        thisSystem = splitFileName[0]
        thisPointType = splitFileName[1]
        thisNumber = str(splitFileName[2])
    else:
        raise

    # source
    headerDef.append("source")
    headRow = [pureFileName for col in range(numCols)]
    headers.append(headRow)
    
    #system",
    headerDef.append("system")
    headRow = [thisSystem for col in range(numCols)]
    headers.append(headRow)
        
    #"pointType",
    headerDef.append("pointType")
    headRow = [thisPointType for col in range(numCols)]
    headers.append(headRow)
        
    #"number",
    headerDef.append("number")
    headRow = [thisNumber for col in range(numCols)]
    headers.append(headRow)


    #"fullFilePath",
    headerDef.append("fullFilePath")
    headRow = [fullFilePath for col in range(numCols)]
    headers.append(headRow)
    
    
    #runDirectory
    fullFilePath = os.path.normpath(fullFilePath)
    drive,path_and_file=os.path.splitdrive(fullFilePath)
    path,file=os.path.split(path_and_file)
    folders=[]
    while 1:
        path,folder=os.path.split(path)
        if folder!="":
            folders.append(folder)
        else:
            if path!="":
                folders.append(path)
            break
    folders.reverse()
    runDirectory =  folders[-2]
    #print runDirectory
    headerDef.append("variant")
    headRow = [runDirectory for col in range(numCols)]
    headers.append(headRow)
    
    
    #"description"
    headerDef.append("description")
    headRow = [[] for col in range(numCols)]
    try: 
        if thisPointType == "Zone":
            
            headers.append(["", "", " Ideal Heat"," Ideal Cool", " QTSPAS"])
            logging.info("Zone header added".format())

        else:
            headers.append(headRow)
    except:
        raise
        #[col.append("description") for col in headers]
    


            
    # Transpose 2D list
    #headers = zip(*headers)
    #headers = [list(col) for col in headers] # Force back to list!?


    thisFrame =  ExergyFrame("trnOut",data,None,headers,headerDef)

    thisFrame.add_simple_time()
    
    return thisFrame

#    headers = list()
#    for i in range(numCols):
#        headers.append([fullFilePath,pureFileName,str(i),"","","",""])
#    
#    headers = zip(*headers)
#    thisFrame = ExergyFrame("Illum",data,None,headers,headerDef)
#    thisFrame.add_simple_time()
#    


           
def load_OUT_files(pathProj,descriptionsFilePath):
    """From a directory, collect all OUT files
    Load them into DataFrameList objects
    Return as an unmerged list
    """ 
    logging.debug("Loading OUT files from {}".format(pathProj))

    descriptions = getDescriptions(descriptionsFilePath)
    
    # Walk the project dir
    allFilePathList = list()
    for root, dirs, files in os.walk(pathProj):
        for name in files:       
            thisFilePath = os.path.join(root, name)
            allFilePathList.append(thisFilePath)
    
    # Filter for the BAL files
    outFilePaths = [filePath for filePath in allFilePathList if 
                    os.path.splitext(filePath)[1].lower() == ".OUT".lower()
                    ]
   
    logging.info("Found {} .OUT files in {}".format(len(outFilePaths),pathProj))
    
    # Process the files
    outFileDataFrames = list()
    for outFilePath in outFilePaths:
        pureFileName = os.path.splitext(os.path.split(outFilePath)[1])[0]
        splitFileName = re.split("_",pureFileName)
        if len(splitFileName)==3:
            #print splitFileName
            thisOutFileObj = DataFile(outFilePath,descriptions)
            thisOutFileObj.loadAllText()
            #print thisBalFileObj.fileData
            thisDataFrame = thisOutFileObj.returnAnalysisData_OUT()
            outFileDataFrames.append(thisDataFrame)
            #thisBalFileObj.loadAllText()
        else:
            logging.info("(Skipping '{}')".format(os.path.split(outFilePath)[1]))
    
    assert isinstance(outFileDataFrames, type(list()))
    
    logging.info("Loaded and {} AnalysisData objects".format(len(outFileDataFrames)))
    
    return outFileDataFrames

def mergeFrames(newFrameName, frames):
    """frames - the list of frames
    return DataFrameNPArray
    """
#    
#    print "got frames;"
#    for frame in frames:
#        print np.shape(frame.dataArray)
#    
    # First, create the arrays
    frameNumRows = 0
    frameNumCols = 0
    for frame in frames:
        frameNumRows = np.shape(frame.dataArray)[0]
        frameNumCols += np.shape(frame.headersArray)[1]
        frameNumHeaders = np.shape(frame.headersArray)[0]

    # Pre-allocate
    mergedDataArray = np.empty((frameNumRows,frameNumCols),dtype = 'float64')
    mergedDataArray[:] = np.NaN
    
    mergedHeaderArray = np.empty((frameNumHeaders,frameNumCols),dtype = 'object')
    mergedHeaderArray[:] = np.NaN

    logging.info("Preallocated blocks; data: {} head: {}".format(np.shape(mergedDataArray),np.shape(mergedHeaderArray)))
    
    startCol = 0
    for thisFrame in frames:
        frameNumCols = np.shape(thisFrame.headersArray)[1]
        endCol = startCol + frameNumCols
        
        logging.info("Write header; {} into slice {},{} of merged {}".format(
                           np.shape(thisFrame.headersArray),
                           startCol,
                           endCol,
                           np.shape(mergedHeaderArray),
                           ))
        mergedHeaderArray[:,startCol:endCol] = thisFrame.headersArray 

        logging.info("Write data; {} into slice {},{} of merged {}".format(
                                   np.shape(thisFrame.dataArray),
                                   startCol,
                                   endCol,
                                   np.shape(mergedDataArray),
                                   ))

        mergedDataArray[:,startCol:endCol] = thisFrame.dataArray 
        startCol += frameNumCols
    
    logging.info("New data frame {}: head {}, data {}".format(
                    newFrameName,
                    np.shape(mergedHeaderArray),
                    np.shape(mergedDataArray)
                    )
                 )
    pickHeaderDef = frames[0].headersDef
    
    return ExergyFrame(newFrameName,mergedDataArray,0,mergedHeaderArray,pickHeaderDef)


def converKJH_kW(numpyFrame):
    unitsMask = np.array(numpyFrame.headersDef[:,0] == "units")
    kJh_mask = np.array(numpyFrame.headersArray[unitsMask,:][0] == "[kJ/hr]")
    
    numpyFrame.headersArray[unitsMask,kJh_mask] = "[kW]"
    numpyFrame.dataArray[:,kJh_mask] = numpyFrame.dataArray[:,kJh_mask] / 3600
    
    numConversions = np.shape(numpyFrame.dataArray[:,kJh_mask])[1]
    logging.info("Made {} conversions from kJ_h to kW".format(numConversions))

#===============================================================================
# Unit testing
#===============================================================================
   

    
class allTests(unittest.TestCase):
    def setUp(self):
        print "**** {} ****".format(whoami())
        data_2d = list() 
        for i in range(5):
            row = [random.randint(0,10) for i in xrange(4)]
            data_2d.append(row)
            
#        for row in data_2d:
#            print row
            
        headerDef = ["Attrib1","Xpos","Ypos"]
        
        headers = [
                   ["alpha","beta","charlie","delta"],
                   ["0","2","2","4"],
                   ["0","1","1","6"],
                   ]

        
        thisFrame = ExergyFrame("test frame",
                                data_2d,
                                None,
                                headers,
                                headerDef,
                                )
        
        thisFrame.add_simple_time()
        
        
        
        #print thisFrame.displayArray()
        
        self.testFrame = thisFrame
#    def tearDown(self):
#        print "**** {} ****".format(whoami())
#        self.testFrame = None
#        
    def test01_index(self):
        print "**** TEST {} ****".format(whoami())
        
        searchIdx = Idx("Attrib1","alp")
        searchIdx = Idx("Attrib1","alp") + Idx("dd","asdf")
        print searchIdx
        
    def test02_getColumnMask(self):
        print "**** TEST {} ****".format(whoami())
        
        #print 
        #print self.testFrame.displayArray()
        #print 
        #searchIdx = Idx("Attrib1","alp")
        
        # Single Idx
        resultMask = self.testFrame.getHeadMaskUnion(Idx("Attrib1","alp"))
        assert(sum(resultMask)==1)
        
        # Composite Idx
        resultMask = self.testFrame.getHeadMaskUnion(Idx("Attrib1","alp") + Idx("Xpos","2"))
        assert(sum(resultMask)==3)
        
        # ALL regex Idx
        resultMask = self.testFrame.getHeadMaskUnion(Idx("Attrib1","."))
        assert(sum(resultMask)==4)
        
        # Ensure error for unknown header def!
        self.assertRaises(Exception, self.testFrame.getHeadMaskUnion, 
                          Idx("afrreldklasdyuc","asdf"))
        
        # Ensure error for unknown header!
        self.assertRaises(Exception, self.testFrame.getHeadMaskUnion, 
                          Idx("Xpos","qwwuirepiophasdferljhv"))
    
    def test04_changeHeadNumpyArray(self):
        print "**** TEST {} ****".format(whoami())

        searchIdx = Idx("Attrib1","alp") + Idx("Xpos","2")
        resultMask = self.testFrame.overWriteHeadersDirect(searchIdx,"NEW!")
        
        #print self.testFrame.displayArray()
        
        resultMask = self.testFrame.getHeadMaskUnion(Idx("Attrib1","NEW!"))
        assert(sum(resultMask)==1)

    def test05_getTimeMask(self):
        print "**** TEST {} ****".format(whoami())
        print type(self.testFrame.timeArray)

        timeMask = self.testFrame.timeArray > 2
        
        assert(sum(timeMask)==2)
        
        assert(sum(self.testFrame.allTimeMask)== 5)

    def test06_getView(self):
        print "**** TEST {} ****".format(whoami())
        frame = self.testFrame
        
        #print frame.displayArray()
        betaMask = self.testFrame.getHeadMaskUnion(Idx("Attrib1","beta"))
        #print frame.allTimeMask
        
        newFrame = frame.extractSubFrame(frame.allTimeMask,betaMask)
        #assert(np.shape(newFrame.dataArray) == (5,))
        
        thisTimeMask = frame.timeArray > 2
        newFrame = frame.extractSubFrame(thisTimeMask,betaMask)
        #assert(np.shape(newFrame.dataArray) == (2,))


        thisHeadMask = self.testFrame.getHeadMaskUnion(Idx("Attrib1","alp") + Idx("Attrib1","beta"))
        thisTimeMask = frame.timeArray > 2
        newFrame = frame.extractSubFrame(thisTimeMask,thisHeadMask)
        assert(np.shape(newFrame.dataArray) == (2,2))
        
    def test07_addAverageColumn(self):
        print "**** TEST {} ****".format(whoami())
        frame = self.testFrame
        
        thisHeadMask = self.testFrame.getHeadMaskUnion(Idx("Xpos","2") )
        thisTimeMask = frame.timeArray > 2
        
        def getMean(array):
            return np.mean(array,1)
        

        frame.addNewVector(None,thisHeadMask,getMean,"Average for Xpos = 2")
        
        thisHeadMask = self.testFrame.getHeadMaskUnion(Idx("Xpos",".") )
        thisTimeMask = frame.timeArray > 2
            
        frame.addNewVector(None,thisHeadMask,getMean,"Average for Xpos = .")
        print frame.displayArray()
    def test08_addSumColumn(self):
        print "**** TEST {} ****".format(whoami())
        frame = self.testFrame
        
        thisHeadMask = self.testFrame.getHeadMaskUnion(Idx("Xpos",".") )
        thisTimeMask = frame.timeArray > 2
        
        def getSum(array):
            return np.sum(array,1)
        
        frame.addNewVector(None,thisHeadMask,getSum,"Sum for Xpos = .")
        
        #print frame.displayArray()
        
    def test09_changeInPlace(self):
        print "**** TEST {} ****".format(whoami())
        frame = self.testFrame
        
        thisHeadMask = self.testFrame.getHeadMaskUnion(Idx("Xpos","2") )
        thisTimeMask = frame.timeArray > 2
        
        def makeNegative(array):
            return array * -1
        
        frame.modifySubArray(thisTimeMask,thisHeadMask,makeNegative)
        frame.overWriteHeadersDirect(Idx("Xpos","2"),"Cheesed")
        
        
        
        print frame.displayArray()
        
    def test10_changeInPlace2(self):
        print "**** TEST {} ****".format(whoami())
        frame = self.testFrame
        
        def makeNegative(array):
            return array * -1
        
        def getMean(array):
            return np.mean(array,0)
              
        frame.inPlaceFunction(frame.allTimeMask,Idx("Xpos","2"),getMean,"Cheesed")  
        print frame.displayArray()
        
        
    def Skiptest05_write(self):
        self.testFrame._convert_to_ndarray()
        
        self.testFrame.saveToCSV(r"c:\test2.csv")
                
    def OLDsetUp(self):
        #### LOAD THE FILES ####
        projectOutDir = r"..\..\test files"
        
        projectOutFullDir = os.path.join(os.getcwd(),projectOutDir)
        
        descriptionsFilePath = r"..\..\test files\Parameters.xlsx"

        descriptionsFileFullPath = os.path.join(os.getcwd(),descriptionsFilePath)
        
        matfileOutDir = r"..\..\test files\Parameters"
        
        matFileName = r"test"
        frameName = "dataFrame"
        
        matFileFullPath = os.path.join(matfileOutDir,matFileName)
        
        outFrames = load_OUT_files(projectOutFullDir,descriptionsFileFullPath)
        
        outDataFrame = mergeFrames(frameName,outFrames)
        
        converKJH_kW(outDataFrame)
            


#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    logging.config.fileConfig('..\\..\\LoggingConfig\\loggingNofile.conf')
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")
    #myLogger.setLevel("INFO")
    logging.debug("Started _main".format())

    unittest.main()

    logging.debug("Finished _main".format())
    