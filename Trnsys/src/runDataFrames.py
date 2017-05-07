from exergyframesOld import exergy_frame as xrg
import logging
import os
from config import *
import datetime
import utility_path as utilPath
import re 
from utility_excel import ExcelBookAPI
import numpy as np

def getDescriptions(descriptionsFilePath):
    # descriptionsFilePath is an excel file with a proper "Descriptions" sheet
    parametersBook = ExcelBookAPI(descriptionsFilePath)
    descriptionsTable = parametersBook.getTable("Descriptions",1,200,1,4)
    #print descriptionsTable
    descriptions = list()
    for row in descriptionsTable[1:]:

        if row[0] and row[3]:
            try:
                row[2] = int(row[2])
                row[2] = str(row[2])
            except:
                print "This row fails", row
                raise
            row = [str(item) for item in row]
            #print row
            descriptions.append((tuple(row[:3]), row[3]))
    
    
    logging.info("Descriptions added for {} points".format(len(descriptions)))

    #descriptions = dict(descriptions)
    return descriptions


def _SCWE2():
    # Input
    projectOutDir = FREELANCE_DIR + r"\090_SmartCampusForsch2\TRNSYS\OUT"
    descriptionsFilePath = FREELANCE_DIR + r"\090_SmartCampusForsch2\Input\Descriptions r00.xlsx"
    #balDir = FREELANCE_DIR + r"\086_SmartCampus1\TRNSYS"
    
    # Output
    fileName = "Limited"
    csvOutDir = FREELANCE_DIR + r"\090_SmartCampusForsch2\Analysis\\"
    matfileOutDir = FREELANCE_DIR + r"\090_SmartCampusForsch2\Analysis\\"
    
    
    now = datetime.datetime.now()
    nowStr = "{}-{}-{} {}-{}-{} ".format(now.year,
                     now.month,now.day,now.hour,now.minute,now.second)
    csvFileFullPath = os.path.join(csvOutDir,nowStr + fileName + ".csv")
    matFileFullPath = os.path.join(matfileOutDir, nowStr + fileName + ".mat")
    
    #===========================================================================
    # Get files 
    #===========================================================================
    inputFiles = utilPath.get_files_by_ext_recurse(projectOutDir, "out") 
    frameList = list()
    #for filePath in inputFiles[20:25]:
    for filePath in inputFiles:
        # Skip unless 3 elements in file name!
        pureFileName = os.path.splitext(os.path.split(filePath)[1])[0]
        splitFileName = re.split("_",pureFileName)
        if len(splitFileName)==3:
            thisFrame = xrg.load_single_out_file(filePath)
        else:
            raise        
            logging.info("(Skipping '{}')".format(os.path.split(pureFileName)[1]))        
        frameList.append(thisFrame)
    
    
    #===========================================================================
    # Merge frames
    #===========================================================================
    frameName = "dataFrame"

    finalFrame = xrg.mergeFrames(frameName, frameList)
    finalFrame.add_simple_time()
    
    finalFrame._convert_to_ndarray()


    #finalFrame.string_summary()
    
    
    #===========================================================================
    # Add descriptions
    #===========================================================================
    descriptions = getDescriptions(descriptionsFilePath)
    
    for desc in descriptions:
        searchSys = desc[0][0]
        searchPointType = desc[0][1]
        searchNum = desc[0][2]
        #print desc
        searchIdx = (xrg.Idx("system",searchSys) + 
                      xrg.Idx("pointType",searchPointType) + 
                      xrg.Idx("number",searchNum))
        
        #print searchIdx,        type(searchIdx)

        descValue = desc[1]

        finalFrame.updateHeaderConcat(searchIdx,"description",descValue)
    
    #===========================================================================
    # Convert kJ/hr to W
    #===========================================================================
    
    def convertKJH(array):
        array = array / 3.6
        return array
    
    searchIdx = xrg.Idx("units",r"kJ/hr")
    headMaskKJH = finalFrame.getHeadMaskUnion(searchIdx)
    
    finalFrame.modifySubArray(None, 
                        headMaskKJH, convertKJH)
    
    finalFrame.updateHeader(searchIdx,"units","W")
        
    #===========================================================================
    # Get sums and means
    #===========================================================================
    def getSum(array):
        return np.sum(array,1)
    thisUnit = r"kW"
    
    thisNewDesc = "Buero heating sum"
    searchIdx = (xrg.Idx("description","Buero") + 
                 xrg.Idx("description","Ideal Heat"))
    finalFrame = addNewVectorSimple(finalFrame,searchIdx,getSum,thisNewDesc)
    finalFrame.updateHeader(xrg.Idx("description",thisNewDesc),"units",thisUnit)
    
    thisNewDesc = "Buero cooling sum"
    searchIdx = (xrg.Idx("description","Buero") + 
                 xrg.Idx("description","Ideal Cool"))
    finalFrame = addNewVectorSimple(finalFrame,searchIdx,getSum,thisNewDesc)
    finalFrame.updateHeader(xrg.Idx("description",thisNewDesc),"units",thisUnit)

#    thisNewDesc = "Werkstatt heating sum"
#    searchIdx = (xrg.Idx("description","(Tischlerei)|(Schlosserei)") + 
#                 xrg.Idx("description","Ideal Heat"))
#    finalFrame = addNewVectorSimple(finalFrame,searchIdx,getSum,thisNewDesc)
#    finalFrame.updateHeader(xrg.Idx("description",thisNewDesc),"units",thisUnit)
#
#    thisNewDesc = "Werkstatt cooling sum"
#    searchIdx = (xrg.Idx("description","(Tischlerei)|(Schlosserei)") + 
#                 xrg.Idx("description","Ideal Cool"))
#    finalFrame = addNewVectorSimple(finalFrame,searchIdx,getSum,thisNewDesc)
#    finalFrame.updateHeader(xrg.Idx("description",thisNewDesc),"units",thisUnit)

    #===========================================================================
    # Get the specific power requirements
    #===========================================================================
    def getSpecOffice(array):
        array = array / 178.9473684
        return array
    
#    def getSpecWS(array):
#        array = array / 2810.53
#        return array

    thisUnit = r"kW/m2"

    thisNewDesc = "Specific Buero heating sum"
    searchIdx = xrg.Idx("description","Buero heating sum")
    finalFrame = addNewVectorSimple(finalFrame,searchIdx,getSpecOffice,thisNewDesc)
    finalFrame.updateHeader(xrg.Idx("description",thisNewDesc),"units",thisUnit)
    
    thisNewDesc = "Specific Buero cooling sum"
    searchIdx = xrg.Idx("description","Buero cooling sum")
    finalFrame = addNewVectorSimple(finalFrame,searchIdx,getSpecOffice,thisNewDesc)
    finalFrame.updateHeader(xrg.Idx("description",thisNewDesc),"units",thisUnit)
    
#    thisNewDesc = "Specific Werkstatt heating sum"
#    searchIdx = xrg.Idx("description","Werkstatt heating sum")
#    finalFrame = addNewVectorSimple(finalFrame,searchIdx,getSpecWS,thisNewDesc)
#    finalFrame.updateHeader(xrg.Idx("description",thisNewDesc),"units",thisUnit)
#    
#    thisNewDesc = "Specific Werkstatt cooling sum"
#    searchIdx = xrg.Idx("description","Werkstatt cooling sum")
#    finalFrame = addNewVectorSimple(finalFrame,searchIdx,getSpecWS,thisNewDesc)
#    finalFrame.updateHeader(xrg.Idx("description",thisNewDesc),"units",thisUnit)

    #===========================================================================
    # Save 
    #===========================================================================
    #finalFrame.saveToCSV(csvFileFullPath)
    finalFrame.saveToMat(matFileFullPath)
    
def _SCWEFORSCH():
    # Input
    projectOutDir = FREELANCE_DIR + r"\SCWEsim1"
    descriptionsFilePath = FREELANCE_DIR + r"\090_SmartCampusForsch2\Input\Descriptions r00.xlsx"
    #balDir = FREELANCE_DIR + r"\086_SmartCampus1\TRNSYS"
    
    # Output
    fileName = "FourthRun"
    csvOutDir = FREELANCE_DIR + r"\090_SmartCampusForsch2\Analysis\\"
    matfileOutDir = FREELANCE_DIR + r"\090_SmartCampusForsch2\Analysis\\"
    
    
    now = datetime.datetime.now()
    nowStr = "{}-{}-{} {}-{}-{} ".format(now.year,
                     now.month,now.day, now.hour,now.minute,now.second)
    csvFileFullPath = os.path.join(csvOutDir,nowStr + fileName + ".csv")
    matFileFullPath = os.path.join(matfileOutDir, nowStr + fileName + ".mat")
    
    #===========================================================================
    # Loop each variant
    #===========================================================================
    # Get the var dirs
    
    variantDirs=[d for d in os.listdir(projectOutDir) if d != 'WEA']
    
    fullVariantPaths =  [os.path.join(projectOutDir,d) for d in variantDirs]
    fullVariantPaths =  [d for d in fullVariantPaths if os.path.isdir(d)]
    
    fullOutPaths = [os.path.join(d,"OUT") for d in fullVariantPaths]

    variantPathPairs = zip(variantDirs,fullOutPaths)
    for pair in variantPathPairs:
        print pair    

    #===========================================================================
    # Get files 
    #===========================================================================
    superFrameList = list()
    #for pair in variantPathPairs:
    #print variantPathPairs[:2]
    #raise
    for pair in variantPathPairs:
        print pair
        
        thisDir = pair[1]
        inputFiles = utilPath.get_files_by_ext_recurse(thisDir, "out") 
        frameList = list()
        #for filePath in inputFiles[20:25]:
        for filePath in inputFiles:
            # Skip unless 3 elements in file name!
            pureFileName = os.path.splitext(os.path.split(filePath)[1])[0]
            splitFileName = re.split("_",pureFileName)
            if len(splitFileName)==3:
                thisFrame = xrg.load_single_out_file(filePath)
            else:
                raise        
                logging.info("(Skipping '{}')".format(os.path.split(pureFileName)[1]))        
            frameList.append(thisFrame)
        superFrameList += frameList
        #superFrameList.append(frameList)
        
    print superFrameList
    logging.info("Found '{}' frames total)".format(len(superFrameList)))        
    
    #===========================================================================
    # Merge frames
    #===========================================================================
    frameName = "dataFrame"

    finalFrame = xrg.mergeFrames(frameName, superFrameList)
    finalFrame.add_simple_time()
    
    finalFrame._convert_to_ndarray()

    #===========================================================================
    # Add descriptions
    #===========================================================================
    descriptions = getDescriptions(descriptionsFilePath)
    
    for desc in descriptions:
        searchSys = desc[0][0]
        searchPointType = desc[0][1]
        searchNum = desc[0][2]
        #print desc
        searchIdx = (xrg.Idx("system",searchSys) + 
                      xrg.Idx("pointType",searchPointType) + 
                      xrg.Idx("number",searchNum))
        
        #print searchIdx,        type(searchIdx)

        descValue = desc[1]

        finalFrame.updateHeaderConcat(searchIdx,"description",descValue)
    
    #===========================================================================
    # Convert kJ/hr to W
    #===========================================================================
    
    def convertKJHtokW(array):
        array = array / 3600
        return array
    
    searchIdx = xrg.Idx("units",r"kJ/hr")
    headMaskKJH = finalFrame.getHeadMaskUnion(searchIdx)
    
    finalFrame.modifySubArray(None, 
                        headMaskKJH, convertKJHtokW)
    
    finalFrame.updateHeader(searchIdx,"units","kW")
    
    #===========================================================================
    # Add specific cooling and htg powers
    #===========================================================================
    if 0:
        def convertSpecific(array):
            array = array / 30.5
            return array    
        
        # Get the variants
        variantRow = finalFrame.findHeadRow("variant")
        
        #    print set(finalFrame.headersArray[sensorNameRow])
        variantRowValues = set(finalFrame.headersArray[variantRow])    
        
        print variantRowValues
        
        thisNewDesc = "Specific heating"
        thisUnit = r"kW/m2"
    
        for thisVariant in variantRowValues:
            searchIdx = xrg.Idx("description","Buero Mitte") + xrg.Idx("variant",thisVariant)
            finalFrame = addNewVectorSimple(finalFrame,searchIdx,convertSpecific,thisNewDesc)
            finalFrame.updateHeader(xrg.Idx("description",thisNewDesc),"units",thisUnit)
    
        thisNewDesc = "Specific cooling"
        thisUnit = r"kW/m2"
        
        for thisVariant in variantRowValues:
            searchIdx = xrg.Idx("description","Buero Mitte") + xrg.Idx("variant",thisVariant)
            finalFrame = addNewVectorSimple(finalFrame,searchIdx,convertSpecific,thisNewDesc)
            finalFrame.updateHeader(xrg.Idx("description",thisNewDesc),"units",thisUnit)
        
        
        #finalFrame = addNewVectorSimple(finalFrame,searchIdx,convertSpecific,SpecificHeating)
        #finalFrame.updateHeader(xrg.Idx("description",thisNewDesc),"units",thisUnit)
            
        

    #===========================================================================
    # Update the file path to variant name
    #===========================================================================
    # Get the unique fullFilePaths
    #finalFrame.headersArray
    #fullFileRow = finalFrame.findHeadRow("fullFilePath")
    
    #print set(finalFrame.headersArray[fullFileRow])
    #finalFrame.updateHeader(xrg.Idx("description",thisNewDesc),"units",thisUnit)
    
    #===========================================================================
    # Save 
    #===========================================================================
    #finalFrame.saveToCSV(csvFileFullPath)
    finalFrame.saveToMat(matFileFullPath)
    
def addNewVectorSimple(frame,searchIdx,func,newName):
    headMask = frame.getHeadMaskIntersect(searchIdx)
    frame.addNewVector(None, 
                    headMask, func, newName)
    return frame


if __name__ == "__main__":
    
    
    logging.config.fileConfig('..\\LoggingConfig\\loggingNofile.conf')
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")
    logging.debug("Started _main".format())

    #_SCWE2()
    _SCWEFORSCH()
    
    logging.debug("Finished _main".format())
    

