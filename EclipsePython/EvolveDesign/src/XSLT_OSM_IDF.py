'''
Created on Apr 15, 2011

@author: UserXP
'''
'''
Created on Apr 14, 2011

@author: UserXP
'''
import re
from lxml import etree
#import StringIO
from IDF import IDF, keptClassesDict
import logging.config



def _testing():
    
    #fIn = open(r'..\\Test OSM files\BasicTest.osm', 'r')
    
    fTransform = open(r'..\\XSLT\\TutorialXSL.xsl', 'r')
    
    thisIDF = IDF(
        pathIdfInput=r"D:\EclipseSpace2\EclipsePython\EvolveDesign\Test OSM files\BasicTest.osm", 
        XML=None, 
        IDFstring = None, 
        IDstring = None, 
        description = None, 
        pathIdfOutput = None,
        )
    
    # Call the load        
    thisIDF.loadIDF()
    # Call convert
    thisIDF.parseIDFtoXML()
    thisIDF.cleanOutObject(keptClassesDict['openStudioGeom'])
    
    xslFilePath
    
    thisIDF.printToScreenXml()
    
if __name__ == "__main__":
    logging.config.fileConfig('..\\LoggingConfig\\loggingNofile.conf')
    logging.debug("Started _main".format())

    _testing()
    
    logging.debug("Started _main".format())



