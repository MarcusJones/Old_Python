#===============================================================================
# Title of this Module
# Authors; MJones, Other
#
#Matlab plotd
#===============================================================================
from __future__ import print_function
"""This module does stuff
Etc.
"""

#===============================================================================
# Set up
#===============================================================================
from config import *
import logging.config
import unittest

from utility_inspect import whoami
from UtilityFile import FileObject

import os, re, csv, random
import numpy as np
from scipy.io import savemat, loadmat
from utility_excel import excelWriteTable,excelWriteTableXLSX


#---Working with header masks---------------------------------------------------------------------------


def force_rows_to_string(rows):
    newTable = list()
    for row in rows:
#        newRow = list()
#        for item in row:
#            try:
#                item.
#            except:
#                pass
#            newRow.append(item)
        newTable.append(map(str, row))
    #print newTable
    #raise
    return newTable

def print_mask_str(theMask):
    maskList = [str(item) for item in theMask.astype(np.int)]
    maskStr = "".join(maskList)
    return maskStr

def get_mask(frame,headerDef,searchStr,flg_verbose = True):
    # Get the row number of the header
    idxHeadDef = findHeadRow(frame,headerDef)

    # Get this entire row
    header_line = frame.headersArray[idxHeadDef]

    # Init a blank mask
    thisMask = np.zeros(frame.num_cols, dtype=np.bool)

    # Loop over each element in this row
    idx = 0
    for head in header_line:
        head = str(head)
        try:
            assert(type(searchStr) == type(head))
        except:
            print("type(searchStr)", type(searchStr))
            print("type(head)", type(head))
            raise

        #print (searchStr,head)

        if re.search(searchStr,head):
            thisMask[idx] = True
        idx +=1
    if flg_verbose:
        if not thisMask.any():
            #print "Header line:", header_line
            logging.debug("*** WARNING *** " + "Search {}={}, not found on row {}".format(headerDef, searchStr, idxHeadDef))

            #print
            #raise Exception("Search {}={}, not found on row {}".format(headerDef, searchStr, idxHeadDef))

        logging.debug("Search {}={}: {} ".format(headerDef, searchStr, print_mask_str(thisMask), ))

    return thisMask

def getFullMask(frame,flg_verbose = True):
    onesMask = np.ones(frame.num_cols, dtype=np.bool)
    if flg_verbose:
        logging.debug("Full mask with {} elements ".format(sum(onesMask)))

    return onesMask

def maskUnion(leftMask, rightMask):
    resultMask = leftMask | rightMask

    logging.debug("{} Union {} = {}".format(print_mask_str(leftMask),
                                       print_mask_str(rightMask),
                                       print_mask_str(resultMask)))
    return resultMask

def maskIntersect(leftMask, rightMask):
    resultMask = leftMask & rightMask

    logging.debug("{} Interesect {} = {}".format(print_mask_str(leftMask),
                                       print_mask_str(rightMask),
                                       print_mask_str(resultMask)))
    return resultMask

def findHeadRow(frame,searchDef):
    """Given a regex, search the array of header definitions
    Return the index number corresponding to the matched value
    Now, must match beginning and end
    If multiple header defs with same name (should never happen!), returns 1st only

    """
    # TODO: Add check for duplicate header defs
    searchDef = "^" + searchDef + "$"
    rowIndexNumber = 0
    flgFound = False

    for foundHeaderDef in frame.headersDef:
        if re.search(searchDef,foundHeaderDef):
            flgFound = True
            break
        rowIndexNumber +=1
    if flgFound:
        pass
        #print idxHeaderDef,headerDef
    else:
        raise Exception, "{} not found in header definitions".format(searchDef)
    return rowIndexNumber

#---Frame utils---------------------------------------------------------------------------

def mergeFrames(newFrameName, frames, flgMergeHeads = False):
    """frames - the list of frames
    Creates a new array object
    """
    firstHeaderDef = frames[0].headersDef
    for frame in frames:
        if all(frame.headersDef != frames[0].headersDef) and not flgMergeHeads:
            for frame in frames:
                print(frame.headersDef)
            raise Exception("Header definitions are not all equal?")

    firstDataShape = np.shape(frames[0].dataArray)
    for frame in frames:
        if np.shape(frame.dataArray)[0] != firstDataShape[0]:
            print(np.shape(frame.dataArray), firstDataShape)
            raise Exception("Not currently supported - data arrays must have same time axis length! You tried to merge {} rows into {}".format(
                    np.shape(frame.dataArray)[0], firstDataShape[0]))


    # First, create the arrays
    frameNumRows = 0
    frameNumCols = 0
    for frame in frames:
        frameNumRows = np.shape(frame.dataArray)[0]
        frameNumCols += np.shape(frame.headersArray)[1]
        #frameNumHeaders = np.shape(frame.headersArray)[0]

    allHeaderDefs = list()
    combinedHeader = list()
    for frame in frames:
        for headerDef in frame.headersDef:
            if headerDef not in allHeaderDefs:
                allHeaderDefs.append(headerDef)
                #headRow = findHeadRow(frame,headerDef)
                #thisHeadRow = frame.headersArray[headRow]
                #print "FOUND",thisHeadRow
                #combinedHeader.append(thisHeadRow)
    #print allHeaderDefs

    #print np.array(combinedHeader)

    frameNumHeaders = len(allHeaderDefs)

    # Pre-allocate for speed
    mergedDataArray = np.empty((frameNumRows,frameNumCols),dtype = 'float64')
    mergedDataArray[:] = np.NaN

    mergedHeaderArray = np.empty((frameNumHeaders,frameNumCols),dtype = 'object')
    mergedHeaderArray[:] = "UNDEFINED"




    logging.info("Preallocated blocks; data: {} head: {}".format(np.shape(mergedDataArray),np.shape(mergedHeaderArray)))




    startCol = 0
    for frame in frames:
        frameNumCols = np.shape(frame.headersArray)[1]
        endCol = startCol + frameNumCols

        logging.debug("Merging; {}".format(frame))

        for hdrDef in frame.headersDef:
                headRow = findHeadRow(frame,hdrDef)
                thisHeadRow = frame.headersArray[headRow]
                targetHeadRow = allHeaderDefs.index(hdrDef)

#                logging.debug("Write header; {} into slice {},{} of merged {}, at row {}".format(
#                                   np.shape(thisFrame.headersArray),
#                                   startCol,
#                                   endCol,
#                                   np.shape(mergedHeaderArray),
#                                   targetHeadRow
#                                   ))
                try:
                    mergedHeaderArray[targetHeadRow,startCol:endCol] = thisHeadRow
                except:
                    print(startCol, endCol)
                    print(thisHeadRow)
                    print(mergedHeaderArray[targetHeadRow,startCol:endCol])
                    raise

        logging.debug("Write header; {} into slice {},{} of merged {}".format(
                           np.shape(frame.headersArray),
                           startCol,
                           endCol,
                           np.shape(mergedHeaderArray),
                           ))

        logging.info("Write data; {} into slice {},{} of merged {}".format(
                                   np.shape(frame.dataArray),
                                   startCol,
                                   endCol,
                                   np.shape(mergedDataArray),
                                   ))

        mergedDataArray[:,startCol:endCol] = frame.dataArray
        startCol += frameNumCols

    logging.info("New data frame {}: head {}, data {}".format(
                    newFrameName,
                    np.shape(mergedHeaderArray),
                    np.shape(mergedDataArray)
                    )
                 )
    #raise
    #pickHeaderDef = frames[0].headersDef

    return ExergyFrame(newFrameName,mergedDataArray,0,mergedHeaderArray,allHeaderDefs)

def renameHeader(frame,searchTree,headerDef,newValue,flgConcatenate = False, flgReplace = False, regex = "."):
    """
    Modifies array IN-PLACE
    Complex header renaming
    headerDef - Specify the headerDef row by name
    searchTree - Specify the search mask
    *** Can be ANY search tree!
    newValue - Specify new string to replace (default)
    or set flgConcatenate
    or set flgReplace, and specify the regex
    """
    # Make a new header, otherwise the space is restricted!

    replaceMask = evaluateSearchTree(frame,searchTree)
    idxHeadDef = findHeadRow(frame,headerDef)

    headRow = frame.headersArray[idxHeadDef]
    idxCol = 0
    numberUpdates = 0
    for head in headRow:
        if replaceMask[idxCol]:
            originalHeadStr = frame.headersArray[idxHeadDef][idxCol]
            if flgConcatenate and originalHeadStr:
                if originalHeadStr:
                    try:
                        frame.headersArray[idxHeadDef][idxCol] = originalHeadStr + " " + newValue
                    except:
                        print(originalHeadStr, newValue)
                        raise
            elif flgReplace and originalHeadStr:
                if originalHeadStr:
                    #re.sub(pattern, repl, string, count=0, flags=0)
                    try:
                        assert re.search(regex,originalHeadStr), "{} not found in {}".format(regex,originalHeadStr)
                        frame.headersArray[idxHeadDef][idxCol] = re.sub(regex,newValue,originalHeadStr)
                        #frame.headersArray[idxHeadDef][idxCol] = "test"
                    except:
                        print(originalHeadStr, newValue)
                        raise
            else:
                frame.headersArray[idxHeadDef][idxCol] = newValue
            numberUpdates = numberUpdates + 1
        idxCol += 1

    logging.info("Updated {} {} times with {}".format(headerDef,numberUpdates,newValue))

def add_simple_time(frame):
    num_rows = np.shape(frame.dataArray)[0]
    frame.timeArray = range(num_rows)
    frame._convert_to_ndarray()
    logging.info("Added time vector over {} rows".format(num_rows))

    return frame


def extractSubFrame(frame,searchTree,timeMask=None):
    """
    Extract a sub-frame given the masking values
    """
    try:
        if not timeMask.any():
            timeMask = frame.allTimeMask
    except:
        if not timeMask:
            timeMask = frame.allTimeMask

    headmask = evalIdx(frame,searchTree)

    newData = frame.dataArray[timeMask][:,headmask]


    newTime = frame.timeArray[timeMask]
    newHeads = frame.headersArray[:,headmask]
    newHeadDef = frame.headersDef

    logging.debug("new sub array returned, shape: {} ".format( np.shape(newData)))

    return ExergyFrame("",newData,newTime,newHeads,newHeadDef)

def columnWiseFunction(frame,searchTree,passedFunc,timeMask=None):
    if not timeMask:
        timeMask = frame.allTimeMask
    #headmask = evalIdx(frame,searchTree)

    #selectedData = frame.dataArray[timeMask][:,headmask]
    # Get a copy! Safer!


    # Doesn't matter, Fancy indexing ALWAYS returns copy, not view!!!
    selectedData = extractSubFrame(frame,searchTree,timeMask)

    logging.debug("Column wise: {}".format(passedFunc.__name__,))

    return passedFunc(selectedData.dataArray)

def inPlaceFunction(frame,searchTree,passedFunc,timeMask=None):
    """
    In place function, elementwise
    """

    if not timeMask:
        timeMask = frame.allTimeMask

    headmask = evalIdx(frame,searchTree)

    logging.debug("In-place function: {}".format(passedFunc.__name__,))


    # This is the in place loop!

    for row in range(len(frame.dataArray)):
        if timeMask[row]:
            for col in range(len(frame.dataArray[row])):
                if headmask[col]:
                    frame.dataArray[row][col] = passedFunc(frame.dataArray[row][col])


def rowWiseAdvanced():
    pass
    # TODO:
    # This function should operate using a more advanced passed function,
    # One which can check the headers of the data! Maybe it operates on a whole extracted array, instead of just the .dataArray!


def rowWiseFunction(frame,searchTree,passedFunc,timeMask=None):
    """
    Creates a new data frame object!
    """

    if not timeMask:
        timeMask = frame.allTimeMask

    headmask = evalIdx(frame,searchTree)

    # Doesn't matter, Fancy indexing ALWAYS returns copy, not view!!!
    selectedData = extractSubFrame(frame,searchTree,timeMask)

    newData = passedFunc(selectedData.dataArray)

    oldHead = selectedData.headersArray[:,0]

    newHead = ["NODATA" for item in frame.headersDef]

    logging.debug("rowWiseFunction function: {}".format(passedFunc.__name__,))

    return ExergyFrame(passedFunc.__name__,
                       newData,
                       selectedData.timeArray,
                       newHead,
                       selectedData.headersDef
                       )


#def addNewVector(frame,timeMask,headmask,passedFunction,newHeadText):
#    """
#    Save the entire frame to CSV
#    """
#    if timeMask == None:
#        timeMask = frame.allTimeMask
#    else:
#        # TODO:
#        raise Exception("Time masking not yet supported!")
#
##    logging.debug("Adding new column based on " +
##        "{} rows, {} columns, using {}, header is {}".format(
##                                                 sum(timeMask),
##                                                 sum(headmask),
##                                                 passedFunction,
##                                                 newHeadText
##                                                 ))
#
#
#    subArray = extractSubFrame(timeMask,headmask)
#
#    newData = passedFunction(subArray.dataArray)
#
#    oldHead = subArray.headersArray[:,0]
#    newHead = oldHead
#    newHead[-1] = newHeadText
#
#    frame.dataArray = np.column_stack( [ frame.dataArray , newData ] )
#    frame.headersArray = np.column_stack( [frame.headersArray,newHead])
#    logging.debug("{} Data columns now in this frame".format(np.shape(frame.dataArray)[1]))
#
#    return frame
#

def displayIndexedFrame(frame, colWidthOverride = None):
    def cleanRowTuple(headDefItem,remainderArrayRow):
        cleanedRowList = [headDefItem] + list(remainderArrayRow)
        return tuple(cleanedRowList)

    headDefLenList = list()
    for headDef in frame.headersDef:
        headDefLenList.append(len(headDef))

    headerDefMaxWidth = max(headDefLenList) + 1


    if not colWidthOverride:
        allStrLens = list()
        #print frame.headersArray
        #raise
        for item in sum(frame.headersArray,[]):
         #frame.headersArray.flat:

            allStrLens.append(len(str(item)))
        columnWidth = max(allStrLens) + 1
    else:
        columnWidth = colWidthOverride

    formatItems = ["{{:>{}}}".format(columnWidth) for item in range(frame.num_cols+1)]
    formatItems.insert(1, "|")

    # Update first width!
    formatItems[0] = "{{:>{}}}".format(headerDefMaxWidth)

    thisFormat = ' '.join(formatItems)
    thisElipses = [":".format(columnWidth) for item in range(frame.num_cols+1)]


    thisSeperator = ["-"*(columnWidth-1) for item in range(frame.num_cols+1)]
    thisSeperator[0] = "-"*(headerDefMaxWidth-1)

    for row in zip(frame.headersDef, frame.headersArray):
        print(thisFormat.format(*cleanRowTuple(row[0],row[1])))

    print(thisFormat.format(*thisSeperator))

    #frame.checkTimeExists()
    indexedArray = zip(frame.indexArray, frame.dataArray)

    print(thisFormat.format(*cleanRowTuple(indexedArray[0][0],indexedArray[0][1:][0])))
    print(thisFormat.format(*thisElipses))
    print(thisFormat.format(*cleanRowTuple(indexedArray[-2][0],indexedArray[-2][1:][0])))
    print(thisFormat.format(*cleanRowTuple(indexedArray[-1][0],indexedArray[-1][1:][0])))


def displayFrame(frame, colWidthOverride = None):
    logging.debug("Displaying frame {}".format( frame))

    def cleanRowTuple(headDefItem,remainderArrayRow):
        if isinstance(headDefItem, np.datetime64):

            headDefItem = str(headDefItem).split(':')[0]
            headDefItem = headDefItem.replace('T', ' ')
            #raise


        #raise
        #print headDefItem
        #print headDefItem

        #print headDefItem
        #print headDefItem

        #logging.debug("Cleaning header {}".format(headDefItem))
        #logging.debug("Cleaning remainder {}".format(remainderArrayRow))

        cleanedRowList = [headDefItem] + list(remainderArrayRow)
        result = tuple(cleanedRowList)
        #logging.debug("Cleaning result {}".format(result))
        return result


    #===========================================================================
    # Get the column width
    #===========================================================================
    headDefLenList = list()
    for headDef in frame.headersDef:
        headDefLenList.append(len(headDef))

    headerDefMaxWidth = max(headDefLenList) + 1

    if not colWidthOverride:
        allStrLens = list()
        #print frame.headersArray
        for item in frame.headersArray.flat:

            allStrLens.append(len(str(item)))
        columnWidth = max(allStrLens) + 1
    else:
        columnWidth = colWidthOverride

    logging.debug("Maximum column width: {}, Override: {}".format(headerDefMaxWidth, colWidthOverride))

    #===========================================================================
    # Create the format string
    #===========================================================================
    formatItems = ["{{:>{}}}".format(columnWidth) for item in range(frame.num_cols+1)]
    formatItems.insert(1, "|")

    # Update first width, for the time vector and column labels
    formatItems[0] = "{{:>{}}}".format(headerDefMaxWidth)

    # Join all format items
    thisFormat = ' '.join(formatItems)
    logging.debug("Format string: {}".format(thisFormat))

    # An elipsis to represent data longer than a few rows
    thisElipses = [":".format(columnWidth) for item in range(frame.num_cols+1)]

    # The separation line between headers and data
    thisSeperator = ["-"*(columnWidth-1) for item in range(frame.num_cols+1)]
    thisSeperator[0] = "-"*(headerDefMaxWidth-1)

    #===========================================================================
    # Print the header
    #===========================================================================
    for row in zip(frame.headersDef, frame.headersArray):
        print(thisFormat.format(*cleanRowTuple(row[0],row[1])))

    print(thisFormat.format(*thisSeperator))

    assert(frame.checkTimeExists())

    #===========================================================================
    # Print the data
    #===========================================================================
    indexedArray = zip(frame.timeArray, frame.dataArray)
    #for row in indexedArray:
    #    print row
    # First row

    #print "indexedArray[0][0]: ",indexedArray[0][0]
    #print "indexedArray[0][1:][0]: ",indexedArray[0][0]
    #print
    #print "CleanRowTuple: ", cleanRowTuple(indexedArray[0][0],indexedArray[0][1:][0])
    #print "NEXT"
    print(thisFormat.format(*cleanRowTuple(indexedArray[0][0],indexedArray[0][1:][0])))
    # Elipses
    print(thisFormat.format(*thisElipses))
    # Last couple rows
    print(thisFormat.format(*cleanRowTuple(indexedArray[-2][0],indexedArray[-2][1:][0])))
    print(thisFormat.format(*cleanRowTuple(indexedArray[-1][0],indexedArray[-1][1:][0])))




#---Main object---------------------------------------------------------------------------
class ExergyFrameIndexed(object):
    """
    AnalysisData consists of a matrix of size n-timeStepRows and m-DataColumns
    n-length indexVector,
    for each m column, there is a list of p attributes, a p-m header array
    header definitions are in a p-length array

    EXAMPLE;

           | alp   bet   char
           | a     b     c
    ---------------------
    zone1  | 1     3     5
    zone2  | 1     3     5
    zone3  | 1     3     5
    totals | 1     3     5

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

    ExergyFrameIndx(name,
                 dataArray,
                 indexArray,
                 headersArray,
                 headersDef,)
    """

    def __init__(self,
                 name,
                 dataArray,
                 indexArray,
                 headersArray,
                 headersDef,
                 ):
        self.name = name
        self.dataArray       = dataArray
        self.indexArray = indexArray
        self.headersArray    = headersArray
        self.headersDef     = headersDef


        logging.info(self.summary_string)

    @property
    def summary_string(self):
        return "FRAME - {} Data: {} Index: {} Headers: {} Def: {}".format(self.name, self.dataStr(),
                                       self.indexStr(),
                                       self.headStr(),
                                   self.headerDefStr())

    def dataStr(self):
        return np.shape(self.dataArray)

    def indexStr(self):
        return np.shape(self.indexArray)

    def headStr(self):
        return np.shape(self.headersArray)

    def headerDefStr(self):
        return str(self.headersDef)
    @property
    def num_cols(self):
        return np.shape(self.dataArray)[1]


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
        self.forceShapesTwoAxis()
        self.forceShapes()
        logging.info(self.summary_string)

    #-Strings & printing ----------------------------------------------------------------------

    @property
    def summary_string(self):
        return "FRAME - {} Data: {} Time: {} Headers: {} Def: {}".format(self.name, self.dataStr(),
                                       self.timeStr(),
                                       self.headStr(),
                                   self.headerDefStr())

    def __str__(self):
        return self.summary_string

#     def displayArray(self):
#         raise Exception("This is obselete, use the utility function in meta_table!")
#         def cleanRowTuple(headDefItem,remainderArrayRow):
#             cleanedRowList = [headDefItem] + list(remainderArrayRow)
#             return tuple(cleanedRowList)
#
#         allStrLens = list()
#         for col in self.headersArray:
#             try:
#                 for rowItem in col:
#                     allStrLens.append(len(rowItem))
#             except:
#                 allStrLens.append(col)
#         try:
#             columnWidth = max(allStrLens) + 2
#         except:
#             columnWidth = 5
#
#         formatItems = ["{{:>{}}}".format(columnWidth) for item in range(self.num_cols+1)]
#         formatItems.insert(1, "|")
#         thisFormat = ' '.join(formatItems)
#
#         thisElipses = [":".format(columnWidth) for item in range(self.num_cols+1)]
#         thisSeperator = ["-"*columnWidth for item in range(self.num_cols+1)]
#
#         for row in zip(self.headersDef, self.headersArray):
#             print(thisFormat.format(*cleanRowTuple(row[0],row[1])))
#
#         print thisFormat.format(*thisSeperator)
#
#         self.checkTimeExists()
#         indexedArray = zip(self.timeArray, self.dataArray)
#
#         print thisFormat.format(*cleanRowTuple(indexedArray[0][0],indexedArray[0][1:][0]))
#         print thisFormat.format(*thisElipses)
#         print thisFormat.format(*cleanRowTuple(indexedArray[-2][0],indexedArray[-2][1:][0]))
#         print thisFormat.format(*cleanRowTuple(indexedArray[-1][0],indexedArray[-1][1:][0]))

    def string_summary_onlyHeader(self):
        def cleanRowTuple(headDefItem,remainderArrayRow):
            cleanedRowList = [headDefItem] + list(remainderArrayRow)
            return tuple(cleanedRowList)

        allStrLens = list()
        for col in self.headersArray:
            for item in col:
                allStrLens.append(len(item))
        columnWidth = max(allStrLens) + 2

        formatItems = ["{{:>{}}}".format(columnWidth) for item in range(self.num_cols+1)]
        formatItems.insert(1, "|")
        thisFormat = ' '.join(formatItems)

        thisElipses = [":".format(columnWidth) for item in range(self.num_cols+1)]
        thisSeperator = ["-"*columnWidth for item in range(self.num_cols+1)]

        for row in zip(self.headersDef, self.headersArray):
            print(thisFormat.format(*cleanRowTuple(row[0],row[1])))


    def dataStr(self):
        return np.shape(self.dataArray)

    def timeStr(self):
        return np.shape(self.timeArray)

    def headStr(self):
        return np.shape(self.headersArray)

    def headerDefStr(self):
        return str(self.headersDef)

    #-Basic properties ----------------------------------------------------------------------
    @property
    def num_cols(self):
        return np.shape(self.dataArray)[1]

    @property
    def allTimeMask(self):
        return self.timeArray == self.timeArray

    #-Self diagnostics ----------------------------------------------------------------------
    def checkTimeExists(self):

        if self.timeArray == None:
            raise
        return True

#        try:
#            print self.timeArray
#            print "any", self.timeArray.any()
#
#            if not self.timeArray.any():
#                raise Exception("No time array (any)!")
#        except:
#
#            if self.timeArray == [None]*len(self.timeArray):
#                print self.timeArray
#                raise Exception("No time array! (empty)")

    def checkShapes(self):
        print("Time array ", np.shape(self.timeArray))
        print("Data array ", np.shape(self.dataArray))
        #print self.dataArray.ndim
        print("Header array ", np.shape(self.headersArray))
        #print self.headersArray.ndim

        print("Header definitions array ", np.shape(self.headersDef))

    def forceShapesTwoAxis(self):
        if self.dataArray.ndim is 1:
            self.dataArray = self.dataArray[np.newaxis].T
        elif self.dataArray.ndim is 2:
            pass
        else:
            raise

        if self.headersArray.ndim is 1:
            self.headersArray = self.headersArray[np.newaxis].T
        elif self.headersArray.ndim is 2:
            pass
        else:
            raise

    def forceAllShapes(self):
        timeRows = np.shape(self.timeArray) [0]
        assert(len(np.shape(self.timeArray)) == 1)
        #timeCols = np.shape(self.timeArray) [1]

        dataRows = np.shape(self.dataArray)[0]
        dataCols = np.shape(self.dataArray)[1]

        headRows = np.shape(self.headersArray)[0]
        headCols = np.shape(self.headersArray)[1]

        headerDefRows = np.shape(self.headersDef)[0]

        assert(dataRows == timeRows),"{} Data rows NOT EQUAL {} time rows".format(dataRows,timeRows)
        assert(dataCols == headCols),"{} data Cols NOT EQUAL {} head Cols".format(dataCols,headCols)
        assert(headerDefRows == headRows),"{} headerDef Rows NOT EQUAL {} head Rows".format(headerDefRows,headRows)


    def forceShapes(self):

        dataRows = np.shape(self.dataArray)[0]
        dataCols = np.shape(self.dataArray)[1]

        headRows = np.shape(self.headersArray)[0]

        headCols = np.shape(self.headersArray)[1]

        headerDefRows = np.shape(self.headersDef)[0]

        assert(dataCols == headCols), "Shape data: {} shape headers: {}, shape headerdef: {}".format(np.shape(self.dataArray),
                                                                                                  np.shape(self.headersArray),
                                                                                                  np.shape(self.headersDef))
        #"{} data Cols NOT EQUAL {} head Cols".format(dataCols,headCols)
        assert(headerDefRows == headRows), "Shape data: {} shape headers: {}, shape headerdef:".format(np.shape(self.dataArray),
                                                                                                  np.shape(self.headersArray),
                                                                                                  np.shape(self.headersDef))
        #"{} headerDef Rows NOT EQUAL {} head Rows".format(headerDefRows,headRows)






    #-Convert----------------------------------------------------------------------

    def _convert_to_ndarray(self):
        """
        Convert the entire frame to the Numpy array structure
        Called on INIT
        """
        self.dataArray = np.array(self.dataArray)
        self.timeArray = np.array(self.timeArray)

        #print self.headersArray

        #print len(self.headersArray)


        #print len(self.headersArray[0])




        self.headersArray = np.array(self.headersArray, dtype="object")

        #print self.headersArray
        #print np.shape(self.headersArray)

        #raise



        self.headersDef  = np.array(self.headersDef,dtype="object")
        if 0:
            logging.info("Data {}".format(np.shape(self.dataArray)))
            logging.info("Time {}".format(np.shape(self.timeArray)))
            logging.info("Heads {}".format(np.shape(self.headersArray)))
            logging.info("Def {}".format(np.shape(self.headersDef)))

        logging.info("Converted to ndarray".format())
        #raise
    def _convert_to_utf8(self):

        """
        In place function, elementwise
        """
        #print self.headersArray
        raise Exception("This is not needed?s")
        for row in self.headersArray:
            for item in row:
                #item = unicode(item, "utf-8")
                item = item.decode('utf-8')

        #print self.headersArray

        for item in self.headersDef:
            item = unicode(item, "utf-8")

        #raise

    #-Saving the frame----------------------------------------------------------------------
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


#    def saveToExcelXLS(self,fullPath,sheetName, flgTranspose = False):
#        excelWriteTable(fullPath,sheetName,self.getTableAsRows(flgTranspose))
#
#    def saveToExcelXLSX(self,fullPath,sheetName, flgTranspose = False):
#        excelWriteTableXLSX(fullPath,sheetName,self.getTableAsRows())
    
    
    def return_rows(self, flgTranspose = False):
        return force_rows_to_string(self.getTableAsRows(flgTranspose))
    
    def saveToExcelAPI(self,ExcelAPI, sheetName, flgTranspose = False):
        rows = force_rows_to_string(self.getTableAsRows(flgTranspose))
        ExcelAPI.write(sheetName,rows)



    def getTableAsRows(self,flgTranspose = False):
        self.checkTimeExists()
        indexedArray = zip(self.timeArray, self.dataArray)
        #f_handle = open(csvFullPath, 'w')
        #open (csvFullPath, 'a') as f
        allRows = list()
        for row in zip(self.headersDef, self.headersArray):

            thisRow = [row[0]] + list(row[1:][0])
            allRows.append(thisRow)
            #wr.writerow(thisRow)
            #np.savetxt(f_handle,row,"%s",delimiter=',')

            #print map(list,row)
            #np.savetxt(f_handle,row,"%s",delimiter=',')
            #f_handle.write ("{:10} {}\n".format(row[0],row[1:][0])   )

        for row in indexedArray:
            thisRow = [row[0]] + list(row[1:][0])
            allRows.append(thisRow)

        if flgTranspose:
            allRows = zip(*allRows)

        logging.info("Got table {} rows tranpose = {}  ".format(len(allRows),flgTranspose))

        return allRows

    def saveToCSV(self, csvFullPath, flgTranspose = False):
        """
        Save the entire frame to CSV
        """


        myfile = open(csvFullPath, 'wb')
        wr = csv.writer(myfile)

        allRows = self.getTableAsRows(flgTranspose)

        for row in allRows:
            wr.writerow(row)

        logging.info("Saved objects into {} ".format( csvFullPath))



#---Search index code---------------------------------------------------------------------------

class Node(object):
    def __init__(self,leftChild,rightChild,search_pair,nodeFunc):
        #self.nodeType     = nodeType
        self.leftChild    = leftChild
        self.rightChild   = rightChild
        self.search_pair = search_pair
        self.nodeFunc    = nodeFunc

    def __and__(self,other):
        """
        This is a bitwise intersection
        """
        return Node(self,other,None,maskIntersect)

    def __or__(self,other):
        """
        This is a bitwise union
        """
        return Node(self,other,None,maskUnion)

def idx(headerDef,searchStr):
    # Simple helper function to streamline leaf Node creation
    searchPair = (headerDef,searchStr)
    return Node(None,None,searchPair,None)

def printSearch(node,X=None):
    # Given a search tree, print the search tree
    if not X:
        X = ""
    if not node.nodeFunc:
        pairStr = "{}={}".format(node.search_pair[0],node.search_pair[1])
        return( pairStr )
    else:
        return  "{} *{}* {}".format(printSearch(node.leftChild,X),
            str(node.nodeFunc.__name__),
            printSearch(node.rightChild,X))

def evaluateSearchTree(frame,node,X=None):
    # Given a search tree, recurse evaluate the search tree
    if X == None:
        X = getFullMask(frame)

    if not node.nodeFunc:
        return get_mask(frame,node.search_pair[0],node.search_pair[1])
    else:
        return node.nodeFunc(evaluateSearchTree(frame,node.leftChild,X),
                      evaluateSearchTree(frame,node.rightChild,X))

evalIdx = evaluateSearchTree

#---Frame creation scripts---------------------------------------------------------------------------

def load_from_mat(fullFilePath):
    logging.info("Loading {} ".format( fullFilePath))
    allData = loadmat(fullFilePath)

    for key in allData.keys():
        #print key, re.search("__.*__",key)
        if not re.search("__.*__",key):
            frameName = key
    #print frameName
    #print frameName
    #print allData[frameName]
    #headers = allData[frameName]["headers"]
    #headerDef = allData[frameName]["headerDef"]
    #data = allData[frameName]["data"]
    #time = allData[frameName]["time"]

    #raise

    data = allData[frameName][0][0][1]

    headerDef =  allData[frameName][0][0][2]
    headerDef = [row[0] for row in headerDef]
    headerDef = [item.astype("str") for item in headerDef ]
    headerDef = [item.tostring() for item in headerDef ]

    headers = allData[frameName][0][0][0]
    cleanHeaders = list()
    for row in headers:
        #print row
        #row = [item.astype("str") for item in row]
        row = [item.tostring() for item in row]
        #.encode('utf-8')
        #print row
        cleanHeaders.append(row)
    headers = cleanHeaders

    time = allData[frameName][0][0][3][0]

    #print time
    #raise
    thisFrame = ExergyFrame(frameName,data,time,headers,headerDef)



    return thisFrame


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
    #thisFrame.add_simple_time()

    logging.info("Illum frame".format())

    #print thisFrame.headersArray

    return thisFrame


def load_single_bal_file(fullFilePath):

    fileObject = FileObject(fullFilePath)
    fileObject.loadLines()

    headerDef = ["labels","units"]

    thisBalDataList = list()
    lineCount = 0
    for line in fileObject.lines:
        #print line

        if line:
            line = re.sub("\|"," ",line)
            # Get rid of the |
            if lineCount == 0:
                line = re.sub("="," ",line)
                line = re.sub("\+"," ",line)
                line = re.sub("\-"," ",line)
                thisLineSplit = re.compile("\s+").split(line.lstrip().rstrip())
                labels = np.array(thisLineSplit,dtype=object)
            elif lineCount == 1:
                line = re.sub("="," ",line)
                line = re.sub("\+"," ",line)
                line = re.sub("\-"," ",line)
                thisLineSplit = re.compile("\s+").split(line.lstrip().rstrip())
                units = np.array(thisLineSplit,dtype=object)
            else:
                thisLineSplit = re.compile("\s+").split(line.lstrip().rstrip())
                # DO NOT Skip the first 3 (Time, Percent, Pipe)
                #thisLineSplit = thisLineSplit[0:]
                #print thisLineSplit
                floatDataList = [float(num) for num in thisLineSplit]
                thisBalDataList.append(floatDataList)
            lineCount = lineCount + 1

    #print headers
    #print units
    zoneNumbers = list()
    balanceNumber = list()
    balanceLabel = list()
    headerDef = headerDef + ["Zone number","Balance","Balance Label"]

    for label in labels:
        splitLabel = label.split("_")
        if len(splitLabel) == 3 and re.match( "\d+",splitLabel[0]  ) :
            zoneNumbers.append(splitLabel[0])
            balanceNumber.append(splitLabel[1])
            balanceLabel.append(splitLabel[2])
            #print splitLabel
        else:
            zoneNumbers.append(0)
            balanceNumber.append("NONE")
            balanceLabel.append("NONE")

    zoneNumbers = np.array(zoneNumbers,dtype=object)
    balanceNumber = np.array(balanceNumber,dtype=object)
    balanceLabel = np.array(balanceLabel,dtype=object)

    headers = [labels, units, zoneNumbers, balanceNumber, balanceLabel]
    #print headers

    #raise

    headersArray = np.array(headers)

    balDataArray = np.array(thisBalDataList)
    #print balDataArry

    # Remove the time column
    timeVector = balDataArray[:,0]
    balDataArray = balDataArray[:,1:]
    headersArray = headersArray[:,1:]


    pureFileName = os.path.splitext(os.path.split(fullFilePath)[1])[0]
    #print pureFileName

    thisFrame = ExergyFrame("BalData",balDataArray,timeVector,headersArray,headerDef)
    #thisFrame.checkShapes()
    #thisFrame.forceShapes2D()
#    thisData = AnalysisData(dataColumns= balDataArry,
#
#                    sourceFilePath=self.filePath,
#                    headers = headers,
#                    units=units,
#                    timeVector=timeVector,
#                    system=pureFileName,
#                    pointType="Building",
#                    number=0,
#                    description="description"
#                    )


    #thisData.forceConsistency()
    #logging.debug("Returning the Analysis Data {}".format(thisData))
    return thisFrame


def load_single_out_file(fullFilePath):
    # Setup
    data = list()
    headers = list()
    headerDef = ["labels","units"]

    # Get the data
    fileObject = FileObject(fullFilePath)
    fileObject.loadLines()

    lineCount = 0
    for line in fileObject.lines:
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
    assert(len(headRow) == numCols )

    #"fullFilePath",
    headerDef.append("fullFilePath")
    headRow = [fullFilePath for col in range(numCols)]
    headers.append(headRow)
    assert(len(headRow) == numCols )

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
    print(headRow)
    assert(len(headRow) == numCols )
    headers.append(headRow)



    #"description"
    headerDef.append("description")
    headRow = ["" for col in range(numCols)] # Create an empty description first
    assert(len(headRow) == numCols )
    headers.append(headRow)

    # TODO: THis is broken
    if 0:
        try:
            if 0:
            #if thisPointType == "Zone":

                headers.append(["", "", " Ideal Heat"," Ideal Cool", " QTSPAS"])
                logging.info("Zone header added".format())

            else:
                pass
                #headers.append(headRow)
        except:
            raise
            #[col.append("description") for col in headers]




    # Transpose 2D list
    #headers = zip(*headers)
    #headers = [list(col) for col in headers] # Force back to list!?


    #print len(data), data
    #print len(headers), headers
    #print len(headerDef), headerDef

    #print "Data {} by {}".format(len(data), len(data[0]))
    #print "headers {} by {}".format(len(headers), len(headers[0]))
    #print "headerDef {} by {}".format(len(headerDef), len(headerDef[0]))
    #headers2 = headers[:]
    #print len(headers2[0])
    #print np.array(headers2)
    #print np.shape(np.array(headers2))
    #print headerDef
    #raise
    thisFrame =  ExergyFrame("trnOut",data,None,headers,headerDef)

    #thisFrame = add_simple_time(thisFrame)

    logging.info("OUT file ".format())
    #raise
    return thisFrame

#    headers = list()
#    for i in range(numCols):
#        headers.append([fullFilePath,pureFileName,str(i),"","","",""])
#
#    headers = zip(*headers)
#    thisFrame = ExergyFrame("Illum",data,None,headers,headerDef)
#    thisFrame.add_simple_time()
#



#---Testing---------------------------------------------------------------------------
#===============================================================================
# Unit testing
#===============================================================================
#@unittest.skip("Skipping the basic testing")
class testBALfiles(unittest.TestCase):
#class testFrame(unittest.TestCase)
    def setUp(self):
        print("**** {} ****".format(whoami()))

    def test01_getBal(self):
        print("**** TEST {} ****".format(whoami()))
        testBalFilePath = r"..\..\test files\SOLAR_ZONES.bal"

        thisFrame = load_single_bal_file(testBalFilePath)

        thisFrame.checkShapes()

        #thisFrame.forceShapes()
        displayFrame(thisFrame)

        thisFrame.saveToCSV(r"C:\TEST\test2.csv")

        #fh = open(testBalFilePath)
        #fh.close()

@unittest.skip("")
class testIndexedFrame(unittest.TestCase):
    def setUp(self):
        print("**** {} ****".format(whoami()))

        # This is random
        data_2d = list()

        for i in range(5):
            row = [random.randint(0,10) for i in xrange(4)]
            data_2d.append(row)

        # This is fixed
        data_2d = [[1, 10, 0, 6], [6, 2, 5, 3], [0, 8, 10, 7], [10, 6, 6, 8], [8, 2, 2, 0]]
         #        for row in data_2d:
#            print row
        indexes = ["A zone", "B zone","C zone","D zone","Ezone"]
        headerDef = ["Attrib1","Xpos","Ypos"]

        headerDefOther = ["Attrib1","QQQAAAAAAAAAAAAAAAAAAAA","ZZZ"]

        headers = [
                   ["alpha","beta","charlie","delta"],
                   ["0","2","2","4"],
                   ["0","1","1","6"],
                   ]


        thisFrame = ExergyFrameIndexed("test frame",
                                data_2d,
                                indexes,
                                headers,
                                headerDef,
                                )
        self.testFrame = thisFrame
    def test01_(self):
        print("**** TEST {} ****".format(whoami()))
        displayIndexedFrame(self.testFrame)

@unittest.skip("")
class testFrame(unittest.TestCase):
#class testFrame(unittest.TestCase):
    def setUp(self):
        print("**** {} ****".format(whoami()))

        # This is random
        data_2d = list()

        for i in range(5):
            row = [random.randint(0,10) for i in xrange(4)]
            data_2d.append(row)

        # This is fixed
        data_2d = [[1, 10, 0, 6], [6, 2, 5, 3], [0, 8, 10, 7], [10, 6, 6, 8], [8, 2, 2, 0]]
         #        for row in data_2d:
#            print row

        headerDef = ["Attrib1","Xpos","Ypos"]

        headerDefOther = ["Attrib1","QQQAAAAAAAAAAAAAAAAAAAA","ZZZ"]

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

        add_simple_time(thisFrame)

        self.testFrame = thisFrame

        self.testFrameOther = ExergyFrame("test frame",
                                data_2d,
                                None,
                                headers,
                                headerDefOther,
                                )
        add_simple_time(self.testFrameOther)

    def test01_Printing(self):
        print("**** TEST {} ****".format(whoami()))
        displayFrame(self.testFrame)
        self.testFrame.checkShapes()

    def test02_HeaderSelectionSimple(self):
        print("**** TEST {} ****".format(whoami()))
        n = idx("Attrib1","alpha")
        print(print_mask_str(evalIdx(self.testFrame,n)))
        n = idx("Attrib1","beta")
        print(print_mask_str(evalIdx(self.testFrame,n)))
        n = idx("Xpos","2")
        print(print_mask_str(evalIdx(self.testFrame,n)))


    def test03_HeaderSelectionComplex(self):
        print("**** TEST {} ****".format(whoami()))
        n2 = idx("Attrib1","alpha")
        n3 = idx("Attrib1","beta")
        n4 = idx("Xpos","2")

        n1 = n2 | n3 & n4
        print("Search:", printSearch(n1))
#        print "Result of search: {}".format(
#                    print_mask_str(evaluateSearchTree(self.testFrame,n1))
#                    )
        assert(print_mask_str(evaluateSearchTree(self.testFrame,n1)) == "1100")

    def test04_HeaderModificationOverwrite(self):
        print("**** TEST {} ****".format(whoami()))
        searchTree = idx("Attrib1","alpha")
        newValue = "sss77777UUU"
        renameHeader(self.testFrame,searchTree,"Attrib1",newValue)

        self.testFrame.string_summary_onlyHeader()
        assert(self.testFrame.headersArray[0,0] == newValue)

    def test05_HeaderModificationConcat(self):
        print("**** TEST {} ****".format(whoami()))
        searchTree = idx("Attrib1",".")
        newValue = "abcdef"

        oldValue = self.testFrame.headersArray[0,0]

        renameHeader(self.testFrame,searchTree,"Attrib1",newValue,True)
        self.testFrame.string_summary_onlyHeader()
        print(self.testFrame.headersArray[0,0])
        print(oldValue + newValue)

        assert(self.testFrame.headersArray[0,0] == oldValue + " " + newValue)



    def test06_extractNewArray2Cols(self):
        print("**** TEST {} ****".format(whoami()))
        searchTree = idx("Attrib1","alpha|charlie")

        newFrame = extractSubFrame(self.testFrame,searchTree)

        assert(newFrame.dataStr() == (5, 2))

    def test07_columnWiseSum(self):
        print("**** TEST {} ****".format(whoami()))

        def getColSums(dataArray):
            return sum(dataArray)

        searchTree = idx("Attrib1","alpha|charlie")

        sums = columnWiseFunction(self.testFrame,searchTree,getColSums)

        print(sums)

        assert(sum(sums) == 25 + 23)

    def test08_ModifyDataColumInPlace(self):
        print("**** TEST {} ****".format(whoami()))

        def makeNegative(array):
            return array * -1

        def getColSums(dataArray):
            return sum(dataArray)

        searchTree = idx("Attrib1","alpha|charlie")

        inPlaceFunction(self.testFrame,searchTree,makeNegative)

        sums = columnWiseFunction(self.testFrame,searchTree,getColSums)

        #self.testFrame.displayArray()

        assert(sum(sums) == -25 + -23)

    def test09_AddNewCol(self):
        print("**** TEST {} ****".format(whoami()))

        def sumOverRows(dataArray):
            return np.sum(dataArray,axis=1)

        def getColSums(dataArray):
            return sum(dataArray)

        searchTree = idx("Attrib1","alpha|charlie")


        summedColFrame = rowWiseFunction(self.testFrame,searchTree,sumOverRows)

        displayFrame(summedColFrame)

        searchTree = idx("Attrib1",".")

        sums = columnWiseFunction(summedColFrame,searchTree,getColSums)

        assert(sum(sums) == 48)

    def test10_MergeFrames(self):
        print("**** TEST {} ****".format(whoami()))

        #mergedFrame = , )
        #mergedFrame = add_simple_time(mergedFrame)

        self.assertRaises(Exception,mergeFrames,"Frame name",[self.testFrame, self.testFrameOther])

        mergedFrame = mergeFrames("Frame name",[self.testFrame, self.testFrameOther],True)
        mergedFrame = add_simple_time(mergedFrame)

        totalUndefs = sum(1 for i in mergedFrame.headersArray.flat if i=="UNDEFINED")
        assert(totalUndefs == 16)
        displayFrame(mergedFrame)

    #@unittest.skip("Skip")
    def test11_Load(self):
        print("**** TEST {} ****".format(whoami()))
        matFilePath = os.getcwd() + r"\\..\\..\\test files\loading\test2.mat"

        thisFrame = load_from_mat(matFilePath)

        displayFrame(thisFrame)

    @unittest.skip("Skip")
    def test12_write(self):
        print("**** TEST {} ****".format(whoami()))
        self.testFrame._convert_to_ndarray()

        self.testFrame.saveToCSV(r"c:\test2")
        self.testFrame.saveToMat(r"c:\test2")


    def test13_writeExcel(self):
        print("**** TEST {} ****".format(whoami()))


        #thisBook = ExcelBookWrite(r"C:\TEST\test2.xls")
        self.testFrame.saveToExcel(r"C:\TEST\test2.xls",'testSheetName')



#---Main---------------------------------------------------------------------------

#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    #logging.config.fileConfig('..\\..\\LoggingConfig\\loggingNofile.conf')
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)

    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")
    #myLogger.setLevel("INFO")
    logging.debug("Started _main".format())

    unittest.main()

    logging.debug("Finished _main".format())
