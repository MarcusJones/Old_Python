from exergyframes import exergy_frame as xrg
from exergyframes import meta_table as metaTab
from exergyframes.psychro import enthalpy, enthalpyFlow

import logging
import os
from config import *
import datetime
import UtilityPathsAndDirs as utilPath
import re 
import numpy as np

def _create():
    # Input
    projectDir = FREELANCE_DIR + r"\101_DohaMetro"
    descriptionsFilePath = projectDir + r"\Input\Descriptions_r00.xlsx"
    
    
    # Output
    fileName = "AlQadeem Twenty NoSolar "
    csvOutDir = projectDir + r"\Analysis\\"
    matfileOutDir = projectDir + r"\Analysis\\"

    now = datetime.datetime.now()
    nowStr = "{}-{}-{} {}-{}-{} ".format(now.year,
                     now.month,now.day, now.hour,now.minute,now.second)
    csvFileFullPath = os.path.join(csvOutDir,nowStr + fileName + ".csv")
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
    variantPathPairs = [["Main","D:\Freelancing\DohaMetroSim\QadeemFullNoSolar"]]


    
    #===========================================================================
    # Get OUT files 
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
    # Merge frames
    #===========================================================================
    frameName = "dataFrame"
    
    finalFrame = xrg.mergeFrames(frameName, superFrameList,True)
    
    finalFrame = xrg.add_simple_time(finalFrame)
    
    #finalFrame._convert_to_ndarray()
    
    #xrg.displayFrame(finalFrame)
    
    
    #===========================================================================
    # Add descriptions
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
    # Convert kJ/hr to W
    #===========================================================================
    
    def convertKJHtokW(array):
        #print "Before", sum(array)
        array = array / 3600
        #print "After:", sum(array)
        return array
    
    thisMask = xrg.idx("units",r"kJ/hr")
    #finalFrame.headersArray()
    #xrg.columnWiseFunction(finalFrame, thisMask, convertKJHtokW)
    xrg.inPlaceFunction(finalFrame,thisMask,convertKJHtokW)
    xrg.renameHeader(finalFrame,thisMask,"units","kW")
    
    #===========================================================================
    # Expand moist air state points
    #===========================================================================
    
    # Get the statepoints
    thisMask = xrg.idx("pointType",r"MoistAir")
    thisMask = xrg.evalIdx(finalFrame,thisMask)
    
    systemRow = xrg.findHeadRow(finalFrame,"system")
    numberRow = xrg.findHeadRow(finalFrame,"number")
    
    systemNames = finalFrame.headersArray[systemRow,thisMask]
    numbers =  finalFrame.headersArray[numberRow,thisMask]
    
    uniqueMoaPoints = set(zip(systemNames,numbers))
    
    def calculateEnthalpyFlow(tripleColumn):
        #print tripleColumn
        return enthalpyFlow(tripleColumn[:,0],tripleColumn[:,1],tripleColumn[:,2])
    
    enthalpyCols = list()
    for moaPoint in uniqueMoaPoints:
        fullMask = (
         xrg.idx("pointType",r"MoistAir") & 
         xrg.idx("system",moaPoint[0]) &
         xrg.idx("number",moaPoint[1])
         )
        thisEnthalpyCol = xrg.rowWiseFunction(finalFrame,fullMask,calculateEnthalpyFlow)
        #print thisEnthalpyCol.headersArray
        thisEnthalpyCol.headersArray = np.array(
                                                [
                    ["hf"],
                    ["[kW]"],
                    [""],
                    [moaPoint[0]],
                    ["MoistAir"],
                    [str(moaPoint[1])],
                    [""],
                    [""],
                    [""],
                ])
        
        enthalpyCols.append(thisEnthalpyCol)
        #print xrg.evalIdx(finalFrame,fullMask)


    finalFrame = xrg.mergeFrames(frameName, [finalFrame] + enthalpyCols,True)
    
    finalFrame = xrg.add_simple_time(finalFrame)
    
    xrg.displayFrame(finalFrame,20)
            
    
    
    #===========================================================================
    # Save data
    #===========================================================================
        
    #finalFrame.saveToCSV(csvFileFullPath)
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
    