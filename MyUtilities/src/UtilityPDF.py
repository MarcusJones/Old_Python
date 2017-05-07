#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""This module does A and B. 
Etc.
"""

#===============================================================================
# Set up
#===============================================================================
from __future__ import division    
import logging.config
from utility_inspect import whoami, whosdaddy
from utility_path import listDirs, split_up_path, get_file_by_ext_one
import unittest
import reportlab as rl
import pyPdf as pdf
from config import *
import os
#===============================================================================
# Code
#===============================================================================
class MyClass(object):
    """This class does something for someone. 
    """
    def __init__(self, aVariable): 
        pass
    
class MySubClass(MyClass):
    """This class does
     
    """
    def __init__(self, aVariable): 
        super(MySubClass,self).__init__(aVariable)
    def a_method(self):
        """Return the something to the something."""
        pass

def some_function():
    """Return the something to the something."""
    pass

#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):
    def test010_SimpleCreation(self):
        print "**** TEST {} ****".format(whoami())
        
        figDirRoot = FREELANCE_DIR + r"\090_SmartCampusForsch2\Fig\\"
        SummaryPDFdir = FREELANCE_DIR + r"\090_SmartCampusForsch2\SummaryPDF\\"
        SummaryPDFfileName = "ThirdRun"
        
                
        
        
        allDirs = listDirs(figDirRoot)
        allDirs.append(figDirRoot)
        #print allDirs
        
        for direct in allDirs:
            #os.path.splitpath(direct)
            #os.path.split(p)
            outputPDF = pdf.PdfFileWriter()
            
            thisDirStem = split_up_path(direct)[-2]
            
            logging.info("Looking in {}".format(direct))
            
            pdfFiles = get_file_by_ext_one(direct,"pdf")
            
            thesePdfFileNames = [split_up_path(direct)[-2] for direct in pdfFiles]
            thisNumbering = list()
            for nameRow in thesePdfFileNames:
                thisNumbering.append(tuple(nameRow.split(" ")[:2]))
            
            print thisNumbering
            
            
            finalRows = list()
            for row in zip(thisNumbering, pdfFiles):
                finalRows.append(row)
            
            finalRows.sort()
            
            #for row in finalRows:
            #    print "fff", row
#            
#            for numbering in thisNumbering:
#                print thisNumbering.sort()
#                
            
            for row in finalRows:
                
                pdfFile = row[1]
                logging.info("Getting {}".format(pdfFile))
                thisPDF = pdf.PdfFileReader(file(pdfFile, "rb"))
                allPages = thisPDF.pages 
                for thisPage in allPages:
                    outputPDF.addPage(thisPage)
                
                #print split_up_path(pdfFile)

            overallPDFname = SummaryPDFdir + SummaryPDFfileName +" "+thisDirStem + ".pdf"
            logging.info("Writing {}".format(overallPDFname))
            outputStream = file(overallPDFname, "wb")
            outputPDF.write(outputStream)
            outputStream.close()
        
        
        
        
        print rl
        print pdf
#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    logging.config.fileConfig('..\\..\\MyUtilities\\LoggingConfig\\loggingNofile.conf')
    myLogger = logging.getLogger()
    myLogger.setLevel("INFO")

    logging.info("Started _main".format())
    #print dir(pdf.PdfFileReader)
    #raise
    
    unittest.main()
        
    logging.info("Started _main".format())
    