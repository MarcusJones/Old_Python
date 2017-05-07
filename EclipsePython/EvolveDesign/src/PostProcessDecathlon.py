
import os
import scipy.io as sio
import re
import csv
import fnmatch 

import logging.config


class MyClass(object):
    
    def __init__(self, aVariable): 
        pass
    
def _test1():
    logging.debug("Started _test1".format())
    
    
    projectDir = os.path.normpath(r"D:\Freelancing\Project Expansion Test Dir")
    
    #loadsFiles = list()
    #[loadsFiles.append(os.path.join(projectDir, name, "OUT", "loads.out")) 
    #    for name in os.listdir(projectDir) 
    #    if os.path.isdir(os.path.join(projectDir, name)) ]
    
    #print os.listdir(projectDir)
    
    #for item in os.listdir(projectDir):
    #    if fnmatch.fnmatch("qxx", "[a-z]xx")
    #print fnmatch.fnmatch("qxx", "[a-z]xx")

    for root, dirs, files in os.walk(projectDir):
        for filename in fnmatch.filter(files, '*.eso'):
            print filename

    
    
    logging.debug("Finished _test1".format())
    pass 

if __name__ == "__main__":
    logging.config.fileConfig('..\\LoggingConfig\\loggingNofile.conf')
    logging.debug("Started _main".format())


    _test1()
    
    logging.debug("Started _main".format())
    