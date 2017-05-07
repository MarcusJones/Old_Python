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
# Standard:
from __future__ import division    

from config import *

import logging.config
import unittest

from utility_inspect import whoami, whosdaddy, listObject

import matplotlib.pyplot as plt

import numpy as np
#===============================================================================
# Code
#===============================================================================

def startGenerationsFigure():
    thisFig = plt.figure()
    
    #print listObject(plt.figure())
    
    ax1 = thisFig.add_subplot(111)
    
    return thisFig

def updateGenerationsPlot(genStats, theFig):
    
    
    print genStats
    if genStats["genNum"] == 0:
        #theFig.axes[0].fill_between(genStats["genNum"], genStats["min"], genStats["max"], where=None, interpolate=False, alpha = 0.2)
        points1 = theFig.axes[0].plot(genStats["genNum"], genStats["avg"], 'ro')
    else:
        thisAx = theFig.axes[0]
        thisAx.set_xdata(np.append(thisAx.get_xdata(), genStats["genNum"]))
        thisAx.set_ydata(np.append(thisAx.get_xdata(), genStats["avg"]))
        thisAx.draw()
    print "Figure:", theFig.get_children()
    
    print "Axis 0:", theFig.axes[0].get_children()
    
#    for item in dir(theFig.axes[0]):
#        print item
        
    theFig.show()
    raw_input("Press Enter to continue...")
    return theFig

def plotAllGens(results):
    
    plt.plot(results["genNum"], results["avg"], 'ro')
            
    #plt.errorbar(results["genNum"], results["avg"], yerr=[results["min"], results["max"]], fmt='--o')
    
    #numObjs = len(results["names"])
    #print numObjs
    
    for objIndx in range(len(results["names"])):
        #print results["genNum"][objIndx]
        #print results["min"][objIndx]
        #print results["max"][objIndx]
        mins = zip(*results["min"])
        max = zip(*results["max"])
        plt.fill_between(results["genNum"], mins[objIndx], max[objIndx], where=None, interpolate=False, alpha = 0.2)
        #print mins, max
    
    
    plt.show()

#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):
    
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
            
    def test010_SimpleCreation(self):
        print "**** TEST {} ****".format(whoami())
        thisFig =  startGenerationsFigure()
        
        #print type(thisFig)
        
        printObj = thisFig.axes[0]
        print "********"
        print type(printObj)
        for item in dir(printObj):
            print item
            
        
        #thisFig.axes[0].([1,1,1,])
        
        
        
        #matplotlib.figure.Figure
        #matplotlib.axes.AxesSubplot
        
#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print ABSOLUTE_LOGGING_PATH
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())
    
    #print FREELANCE_DIR
    
    unittest.main()
        
    logging.debug("Finished _main".format())
    