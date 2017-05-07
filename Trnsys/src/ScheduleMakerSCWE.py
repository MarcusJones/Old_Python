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
import unittest
from utility_excel import ExcelBookRead
import numpy as np
import os
from config import *
import re

def makeSched(schedBookPath,simulationDirPath):
    """Return the something to the something."""
    schedBook = ExcelBookRead(schedBookPath)
    
    sheetList = schedBook.get_sheet_names()
    
    # Filter
    sheetList = [name for name in sheetList if not re.match("^<.*.>$",name,)]
    
    logging.debug("Working on sheets {}".format(sheetList))
    flgFirst = True
    
    for sheet in sheetList:
        logging.debug("Working on sheet {}".format(sheet))
        
        rawTable = schedBook.getTable(sheet,0,None,0)
        rawTable = np.array(rawTable)
        
        #print rawTable
        #print 
        variantColIdxs = list()
        for item in rawTable[0,:]:
            #print item
            #
            #print itemIndex
            if item:
                #print item
                itemIndex=np.where(rawTable[0,:]==item)
                #print itemIndex
                variantColIdxs.append(int(itemIndex[0]))
                
        logging.debug("Found schedule columns; {} ".format(variantColIdxs))
                
        if flgFirst:
            lastVariantColIdxs = None
        else:
            if len(variantColIdxs) != len(lastVariantColIdxs):
                #print variantColIdxs
                #print lastVariantColIdxs
                print rawTable
                raise Exception("Mismatch in number of schedules per sheet. Last number; {}, this num; {}".format(len(lastVariantColIdxs),len(variantColIdxs)))
            
        if len(variantColIdxs) > 1:
            #print len(variantColIdxs)
            scheduleWidth = variantColIdxs[1] - variantColIdxs[0]
            for i in range(2, len(variantColIdxs)):
                thisDiff = variantColIdxs[i] - variantColIdxs[i-1]
                if thisDiff != scheduleWidth: 
                    raise Exception("All variants must be {} wide, found one with {}".format(scheduleWidth,thisDiff))
        else:
            scheduleWidth = len(rawTable[0,1:])
            #print scheduleWidth
            
        ### 
        schedules = list()
        for marker in variantColIdxs:
            # slice the array, no first column, no headers
            schedName = rawTable[0,marker]
            thisSchedTable = rawTable[2:-1,marker:marker + scheduleWidth]
            firstRow = thisSchedTable[0,:]
            
            firstRow = firstRow[np.newaxis, :]

            # Repeat the first row!!!
            thisSchedTable = np.concatenate((firstRow, thisSchedTable), axis=0)
            thisSchedTable = thisSchedTable.astype(np.float)
            finalScheduleShape = np.shape(thisSchedTable)
            
            logging.debug("Schedule created {} rows {} cols".format(finalScheduleShape[0],finalScheduleShape[1]))
            
            schedules.append((schedName,thisSchedTable))

        for schedule in schedules:
            thisName = schedule[0]
            thisSched = schedule[1]

            thisVariantDir = os.path.join(simulationDirPath, thisName)
            thisVariantPath = os.path.join(thisVariantDir, sheet + ".csv")
            try:
                os.makedirs(thisVariantDir)
            except OSError:
                pass

            np.savetxt(thisVariantPath, thisSched, delimiter=",",fmt="%10.5f")
            logging.debug("Schedule successfully saved to {}".format(thisVariantPath))
            
            lastVariantColIdxs = variantColIdxs
            logging.debug("MAKE SCHED IS LOSING THE FIRST ROW - FIXXXX".format())
            
            flgFirst = False
            logging.debug("MAKE SCHED IS LOSING THE FIRST ROW - FIXXXX".format())


def dohaMetroProj():
    schedBookPath = FREELANCE_DIR + r"\101_DohaMetro\Input\Schedules r00.xlsx"
    simulationDirPath = FREELANCE_DIR + r"tempSim\\"
    
    makeSched(schedBookPath,simulationDirPath)
    

#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    logging.config.fileConfig('..\\..\\MyUtilities\\LoggingConfig\\loggingNofile.conf')
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())


    dohaMetroProj()
    #makeSched()
        
    logging.debug("Finished _main".format())
    