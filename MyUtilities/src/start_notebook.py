#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

""". 
http://www.libertypages.com/clarktech/?p=4963
http://www.randalolson.com/2012/05/12/a-short-demo-on-how-to-use-ipython-notebook-as-a-research-notebook/
http://blog.fperez.org/2012/09/blogging-with-ipython-notebook.html
https://github.com/ipython/ipython/issues/2672
"""

#===============================================================================
# Set up
#===============================================================================
from __future__ import division    
import logging.config
from utility_inspect import whoami, whosdaddy
import unittest
from config import *


import subprocess as subprocess
from subprocess import PIPE


#import subprocess
import os

def runNotebook():
    #profilesDir = os.getcwd() + "\..\IpythonNotebook\Profiles"
    
    myIPythonDir = os.getcwd() + "\..\IpythonNotebook\myIPythonDir"
    
    
    #os.getcwd() + "\..\IpythonNotebook\Profiles"
    
    arguments = [
                 "notebook", 

                 "--ipython-dir=\"{}\"".format(myIPythonDir),
                 "--notebook-dir=\"{}\"".format(myIPythonDir),
                 "--profile=myHomeProfile",
                 #"--pylab=inline"
                 ]
    wholeCommand = ["ipython"] + arguments
    
    wholeCommandString = " ".join(wholeCommand)
    
    print(wholeCommandString)
    
    #p = subprocess.Popen(wholeCommandString, stdout=PIPE, stderr=PIPE, stdin=PIPE,shell=True).wait()
    p = subprocess.Popen(wholeCommandString,shell=True)
    
    
    #p.call()
    #print p
    #output = p.stdout.read()
    #print output
    #p.stdin.write(input)


    #os.system("start " + wholeCommandString)

#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print(ABSOLUTE_LOGGING_PATH)
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())
    
    #print FREELANCE_DIR
    
    runNotebook()
    
    logging.debug("Finished _main".format())
    