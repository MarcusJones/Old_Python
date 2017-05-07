


#def converKJH_kW(numpyFrame):
#    unitsMask = np.array(numpyFrame.headersDef[:,0] == "units")
#    kJh_mask = np.array(numpyFrame.headersArray[unitsMask,:][0] == "[kJ/hr]")
#    
#    numpyFrame.headersArray[unitsMask,kJh_mask] = "[kW]"
#    numpyFrame.dataArray[:,kJh_mask] = numpyFrame.dataArray[:,kJh_mask] / 3600
#    
#    numConversions = np.shape(numpyFrame.dataArray[:,kJh_mask])[1]
#    logging.info("Made {} conversions from kJ_h to kW".format(numConversions))

#===============================================================================
# Unit testing
#======================================

    @property
    def string_summary(self):

        #print numItems
        #raise
        #print len(self.headersArray)
        #print self.get_num_cols()
        allStrLens = list()
        for col in self.headersArray:
            for item in col:
                allStrLens.append(len(item))
        columnWidth = max(allStrLens) + 2
        
        
        
        for row in zip(self.headersDef, self.headersArray):
            print "{:10} {}".format(row[0],row[1:][0])
            
        
        
        self.checkTimeExists()

        indexedArray = zip(self.timeArray, self.dataArray)

        print "{:<10} {}".format(indexedArray[0][0],indexedArray[0][1:][0])
        print "{:<10} {}".format(":",":")
        print "{:<10} {}".format(indexedArray[-2][0],indexedArray[-2][1:][0])
        print "{:<10} {}".format(indexedArray[-1][0],indexedArray[-1][1:][0])



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

#class Node(object):
#    def __init__(self, headerDef, headerVal): 
#        self.search_pair = (headerDef, headerVal)         
#    
#    def __and__(self, other):
#        return Tree(self,"AND",other)
#    
#    def __xor__(self, other):
#        return Tree(self,"XOR",other)
#    







    def _getHeaderMask(self,searchTree):
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
        
        thisMask = np.zeros(self.get_num_cols(), dtype=np.bool)
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
 



    

    def _getHeaderMaskOLD(self,idxHeadDef,searchStr):
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
        
        thisMask = np.zeros(self.get_num_cols(), dtype=np.bool)
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
        
        #overallMask = np.zeros((self.get_num_cols(),), dtype=np.bool)
        maskList = list()
        for pair in idx_object:
            searchDef = pair[0]
            searchStr = pair[1]
            idxHeaderDef = self._getHeaderRow(searchDef)
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
        
        #overallMask = np.zeros((self.get_num_cols(),), dtype=np.bool)
        maskList = list()
        for pair in idx_object:
            searchDef = pair[0]
            searchStr = pair[1]
            idxHeaderDef = self._getHeaderRow(searchDef)
            thisMask = self._getHeaderMask(idxHeaderDef,searchStr)
            maskList.append(thisMask)
            # Union of the masks
            #overallMask = overallMask | thisMask
        overallMask = self.maskUnion(maskList)
        logging.info("Head mask, {} found ".format( sum(overallMask)))

        return overallMask





#def printLinedUpRow(row,spacing):
#
#    thisFormat = ' '.join(['%%%ds' % spacing for item in row ])
#    #print thisFormat
#    print thisFormat % tuple(row)
#    #numItems = len(row)






    def add_frame_name(self):
        raise
        self.headersDef.insert(0, "frameName")
        #print [self.name for i in range(np.shape(self.headersArray)[1])]
        self.headersArray.insert(0,[self.name for i in range(np.shape(self.headersArray)[1])])
    
    
    
    
    


           
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












def updateHeader(frame,ddddddd,d,d,d,d,d,d,newValueString):
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


#    def modifyHeader(self,headDef,searchStr,newValue):
#        idxHeaderDef = self.findHeadRow(headDef)
#        #self._getHeaderDefMask
#        headMask = self._getHeaderMask(idxHeaderDef,searchStr)
#        print self.headersArray[idxHeaderDef][headMask]
#        
    
    
    
    
    
    

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

    
    
    
    
    
        
    def OLDtest02_getColumnMask(self):
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
    
    def OLDtest04_changeHeadNumpyArray(self):
        print "**** TEST {} ****".format(whoami())

        searchIdx = Idx("Attrib1","alp") + Idx("Xpos","2")
        resultMask = self.testFrame.overWriteHeadersDirect(searchIdx,"NEW!")
        
        #print self.testFrame.displayArray()
        
        resultMask = self.testFrame.getHeadMaskUnion(Idx("Attrib1","NEW!"))
        assert(sum(resultMask)==1)

    def OLDtest05_getTimeMask(self):
        print "**** TEST {} ****".format(whoami())
        print type(self.testFrame.timeArray)

        timeMask = self.testFrame.timeArray > 2
        
        assert(sum(timeMask)==2)
        
        assert(sum(self.testFrame.allTimeMask)== 5)

    def OLDtest06_getView(self):
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
        
    def OLDtest07_addAverageColumn(self):
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
    def OLDtest08_addSumColumn(self):
        print "**** TEST {} ****".format(whoami())
        frame = self.testFrame
        
        thisHeadMask = self.testFrame.getHeadMaskUnion(Idx("Xpos",".") )
        thisTimeMask = frame.timeArray > 2
        
        def getSum(array):
            return np.sum(array,1)
        
        frame.addNewVector(None,thisHeadMask,getSum,"Sum for Xpos = .")
        
        #print frame.displayArray()
        
    def OLDtest09_changeInPlace(self):
        print "**** TEST {} ****".format(whoami())
        frame = self.testFrame
        
        thisHeadMask = self.testFrame.getHeadMaskUnion(Idx("Xpos","2") )
        thisTimeMask = frame.timeArray > 2
        
        def makeNegative(array):
            return array * -1
        
        frame.modifySubArray(thisTimeMask,thisHeadMask,makeNegative)
        frame.overWriteHeadersDirect(Idx("Xpos","2"),"Cheesed")
        
        
        
        print frame.displayArray()
        
    def OLDtest10_changeInPlace2(self):
        print "**** TEST {} ****".format(whoami())
        frame = self.testFrame
        
        def makeNegative(array):
            return array * -1
        
        def getMean(array):
            return np.mean(array,0)
              
        frame.updateColumns(frame.allTimeMask,Idx("Xpos","2"),getMean,"Cheesed")  
        print frame.displayArray()
        
        
        
        
        
                
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
            
    