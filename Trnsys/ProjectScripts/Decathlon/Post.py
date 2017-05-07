from exergyframes import exergy_frame as xrg
from exergyframes import meta_table as metaTab
import logging
import os
from config import *
import datetime
import UtilityPathsAndDirs as utilPath
import re 
import numpy as np

def _create():
    # Input
    projectDir = FREELANCE_DIR + r"\DecathlonSim"
    descriptionsFilePath = projectDir + r"\INPUT\Descriptions_r00.xlsx"
    zoneNamesFilePath = projectDir + r"\INPUT\ZoneNames.xlsx"
    
    #balDir = FREELANCE_DIR + r"\086_SmartCampus1\TRNSYS"
    
    # Output
    fileName = "ZerothRun"
    csvOutDir = projectDir + r"\Analysis\\"
    matfileOutDir = projectDir + r"\Analysis\\"

    now = datetime.datetime.now()
    nowStr = "{}-{}-{} {}-{}-{} ".format(now.year,
                     now.month,now.day, now.hour,now.minute,now.second)
    csvFileFullPath = os.path.join(csvOutDir,nowStr + fileName + ".csvIGNORED")
    matFileFullPath = os.path.join(matfileOutDir, nowStr + fileName + ".mat")
    
    #===========================================================================
    # Loop each variant
    #===========================================================================
    # Get the var dirs
    
    #variantDirs = projectDir
    
    #fullVariantPaths =  [os.path.join(projectDir,d) for d in variantDirs]
   # fullVariantPaths =  [d for d in fullVariantPaths if os.path.isdir(d)]
    
    #fullOutPaths = [os.path.join(d,"OUT") for d in fullVariantPaths]
    
    #variantPathPairs = zip(variantDirs,fullOutPaths)
    variantPathPairs = [["Main",projectDir]]


    
    #===========================================================================
    # # Get OUT files ----------------------------------------------------------
    #===========================================================================
    superFrameList = list()

    for pair in variantPathPairs:
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
                logging.info("(Skipping '{}')".format(os.path.split(pureFileName)[1]))        
            frameList.append(thisFrame)
        superFrameList += frameList
        #superFrameList.append(frameList)
        
    #print superFrameList
    #xrg.displayFrame(thisFrame)
    logging.info("Found '{}' OUT frames over all variants)".format(len(superFrameList)))      

    #===========================================================================
    # # Get BAL files ----------------------------------------------------------
    #===========================================================================
    for pair in variantPathPairs:
    #for pair in [variantPathPairs[0]]:
        print pair
        
        thisDir = pair[1]
        inputFiles = utilPath.getFilesByExtRecurse(thisDir, "bal")
        inputFiles = [item for item in inputFiles if not re.search("SUMMARY", item )] 
        frameList = list()
        #for filePath in inputFiles[20:25]:
        for filePath in inputFiles:
            # Skip unless 3 elements in file name!
            pureFileName = os.path.splitext(os.path.split(filePath)[1])[0]
            splitFileName = re.split("_",pureFileName)
            #if len(splitFileName)==3:
            thisFrame = xrg.load_single_bal_file(filePath)
            #else:
            #    logging.info("(Skipping '{}')".format(os.path.split(pureFileName)[1]))        
            frameList.append(thisFrame)
        superFrameList += frameList
        #superFrameList.append(frameList)
        
    #print superFrameList
    logging.info("Found '{}' BAL files over all variants)".format(len(superFrameList)))      

    #===========================================================================
    # Merge frames
    #===========================================================================
    frameName = "dataFrame"
    
    finalFrame = xrg.mergeFrames(frameName, superFrameList,True)
    
    finalFrame = xrg.add_simple_time(finalFrame)
    
    #finalFrame._convert_to_ndarray()
    
    #xrg.displayFrame(finalFrame)
    
    
    #===========================================================================
    # # Add descriptions -------------------------------------------------------
    #===========================================================================
    
    descriptions = metaTab.getDescriptionsOut(descriptionsFilePath)
    
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
    # # Convert kJ/hr to W -----------------------------------------------------
    #===========================================================================
    
    def convertKJHtokW(array):
        array = array / 3600
        return array
    
    thisMask = xrg.idx("units",r"kJ/hr")
    xrg.inPlaceFunction(finalFrame,thisMask,convertKJHtokW)
    xrg.renameHeader(finalFrame,thisMask,"units","kW")
    
    
    
    #----------------------------------------------------------------- Save data
    
        
    #xrg.displayFrame(finalFrame)
    
    
    finalFrame.saveToCSV(csvFileFullPath)
    finalFrame.saveToMat(matFileFullPath)    

def _decathLoad():
    logging.debug("Load".format())
    loadMatPath = FREELANCE_DIR + r"\DecathlonSim\Analysis\\2012-10-31 13-28-14 ZerothRun.mat"
    thisFrame = xrg.load_from_mat(loadMatPath)
    
    
    print thisFrame.headersArray
    
    
if __name__ == "__main__":
    
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")
    logging.debug("Started _main".format())

    _create()
    #_decathLoad()
    
    
    logging.debug("Finished _main".format())
    