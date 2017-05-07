from exergyframes import exergy_frame as xrg
import logging
import os
from config import *
import datetime
import UtilityPathsAndDirs as utilPath
import re 
import numpy as np

def _SCWEFORSCH():
    # Input
    projectOutDir = FREELANCE_DIR + r"\SCWEsim1"
    descriptionsFilePath = FREELANCE_DIR + r"\090_SmartCampusForsch2\Input\Descriptions r01.xlsx"
    #balDir = FREELANCE_DIR + r"\086_SmartCampus1\TRNSYS"
    
    # Output
    fileName = "SevenRun"
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
    #for pair in [variantPathPairs[0]]:
        print pair
        
        thisDir = pair[1]
        inputFiles = utilPath.getFilesByExtRecurse(thisDir, "out") 
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
    
    finalFrame = xrg.add_simple_time(finalFrame)
    
    finalFrame._convert_to_ndarray()
    
    finalFrame.displayArray()
    
    #===========================================================================
    # Add descriptions
    #===========================================================================
    descriptions = getDescriptions(descriptionsFilePath)
    
    for desc in descriptions:
        searchSys = desc[0][0]
        searchPointType = desc[0][1]
        searchNum = desc[0][2]
        #print desc
        searchIdx = (xrg.idx("system",searchSys) &
                      xrg.idx("pointType",searchPointType) & 
                      xrg.idx("number",searchNum))
        
        #print searchIdx,        type(searchIdx)

        descValue = desc[1]
        
        # IN PLACE
        xrg.renameHeader(finalFrame,searchIdx,"description",descValue,True)
        
    
    #===========================================================================
    # Convert kJ/hr to W
    #===========================================================================
    
    def convertKJHtokW(array):
        array = array / 3600
        return array
    thisMask = xrg.idx("units",r"kJ/hr")
    xrg.columnWiseFunction(finalFrame, thisMask, convertKJHtokW)
    print "DOES NOT WORK USE IN PLACE FUNCTION"
    raise 
    xrg.renameHeader(finalFrame,thisMask,"units","kW")
    
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
            searchIdx = xrg.idx("description","Buero Mitte") + xrg.idx("variant",thisVariant)
            finalFrame = xrg.addNewVector(finalFrame,None,searchIdx,convertSpecific,thisNewDesc)
            finalFrame.updateHeader(xrg.idx("description",thisNewDesc),"units",thisUnit)
    
        thisNewDesc = "Specific cooling"
        thisUnit = r"kW/m2"
        
        for thisVariant in variantRowValues:
            searchIdx = xrg.idx("description","Buero Mitte") + xrg.idx("variant",thisVariant)
            finalFrame = xrg.addNewVector(finalFrame,None,searchIdx,convertSpecific,thisNewDesc)
            
            finalFrame.updateHeader(xrg.idx("description",thisNewDesc),"units",thisUnit)
        
        
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

if __name__ == "__main__":
    
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")
    logging.debug("Started _main".format())

    _SCWEFORSCH()
    
    logging.debug("Finished _main".format())
    