'''
Created on Aug 3, 2011

@author: UserXP
'''

import logging.config
import os
import sys
sys.path.insert(0, "c:\EclipsePython\EvolveDesign\src")
import IDF
import csv

# Load the logging configuration
logging.config.fileConfig('..\\LoggingConfig\\logging.conf')

logging.info("Started IDF test script")

#===============================================================================
# Template file, weather, group, variants
#===============================================================================
templatesFile = r"C:\Freelance\IDF_Library\Templates.xlsx"
templatesFileAbsPath = os.path.abspath(templatesFile)
templatesFileDirStem = r"C:\Freelance\IDF_Library\\" 
templatesList = IDF.loadTemplates(templatesFileAbsPath, templatesFileDirStem)

# Weather file
weatherFilePath = r"C:\Freelance\055_ACECustomsHousing\WEA\ARE_Abu.Dhabi.412170_IWEC.epw"

# Group file
groupFilePath = r"C:\Freelance\Simulation\\00thisGroupFile.epg"

# The variants
#variantsFile = r"C:\Freelance\062_RasGhurabMos\RunControl\\062 AllCredits r02.xlsx"
#variantsFile = r"C:\Freelance\090_DewanVilla\RunControl\AllCredits6.xlsx"
#variantsFile = r"C:\Freelance\055_ACECustomsHousing\Runcontrol\Variants r03.xlsx"
#variantsFile = r"C:\Freelance\091_AceCustomsCommunity\Input Data\091 Input data r02.xlsx"
#variantsFile = r"C:\Freelance\073_ACE_Bachelor\Runcontrol\Variants r03.xlsx"
#variantsFile = r"C:\Freelance\090_DewanVilla\Input Data\090 Input data r03.xlsx"
variantsFile = r"C:\Freelance\096_AlBateen\Al Bateen Control r07.xlsx"

#===============================================================================
# Load variants
#===============================================================================
variantFileAbsPath = os.path.abspath(variantsFile)
#inputFilesAbsDir = os.path.normpath(inputFileDir)
outputTargetAbsDir = os.path.normpath(r"C:\Freelance\Simulation\\")
variantsList = IDF.loadVariants(inputExcelPath=variantFileAbsPath,
                         targetAbsDirStem=outputTargetAbsDir,
                         )


for variant in variantsList:
    
    #===========================================================================
    # Create a new IDF from the variant
    #===========================================================================
   
    thisIDF = IDF.IDF(
        pathIdfInput=variant.sourceFileAbsPath, 
        XML=None, 
        IDFstring = None, 
        IDstring = None, 
        description = None, 
        pathIdfOutput = variant.targetDirAbsPath
        )
    
    # Call the load        
    thisIDF.loadIDF()
    # Call convert
    thisIDF.convertIDFtoXML()
    #thisIDF.cleanOutObject()
    thisIDF.cleanOutObject(IDF.keptClassesDict['onlyGeometry'])
    
    # Apply standard templates
    #        thisIDF.applyTemplate(runControlType)
    #        thisIDF.applyTemplate('SizingParams')
    #        thisIDF.applyTemplate(outputType)
    #        thisIDF.selectCommentedAttrAndChange(["^Building$","Name",variant.ID])
    #        
    # Apply unique templates
    for template in variant.templateDescriptions:
        #print template
    
        thisIDF.applyTemplateNewStyle(template,templatesList)
        
    # Apply changes
    if variant.changesList:
        for change in variant.changesList:
            #print change
            #try:  
            #thisIDF.selectCommentedAttrAndChange(change)
            thisIDF.selectCommentedAttrInNamedObjectAndChange(change)
            #except:
            #    pass
                #raise NameError("{0},{1}".format(change,variant.name))
                
    
    thisIDF.convertXMLtoIDF()
    
    thisIDF.writeIdf(thisIDF.pathIdfOutput)
    
    #print thisIDF.listZonesWithName('Gym')
    
    #thisIDF.makeUniqueNames()

#csvout = open(groupFilePath,"w")

#csvout = csv.writer(open(groupFilePath, 'wb'))

#===============================================================================
# Write the group file
#===============================================================================

#groupSimFilePath = 'C:\Freelance\Simulation\00eggs.epg'

csvout = csv.writer(open(groupFilePath, 'wb'))

for variant in variantsList:
    thisRow = [variant.targetDirAbsPath,weatherFilePath,variant.targetDirAbsPath,"1"]
    csvout.writerow(thisRow)
    
logging.info("Wrote the {0} variants to the group simulation file at: {1}".format(len(variantsList),groupFilePath))     

logging.info("Finished IDF test script")                
        