'''
Created on 2012-09-09

@author: Anonymous
'''
import os

PYTHON_ECLIPSE = os.getcwd() + r"\\..\..\..\\"
PYTHON_ECLIPSE = os.path.abspath(PYTHON_ECLIPSE) # Doesn't always work, not robust!! 
PYTHON_ECLIPSE = r"D:\EclipseSpace2"

FREELANCE_DIR =     projectOutDir = r"C:\Projects\\"
TRNSYS_EXEC =  r"D:\Apps\Trnsys17_1\Exe\TRNexe.exe"

EXCEL_POST_PROC_TEMPLATE = "D:\EclipsePython\PyIDF\ExcelTemplates\postProcessTemplateLEED r03.xlsx"



#EXERGY_FRAME_PATH = 
#UTILITIES_PATH =  
#ExergyFrames\src
MODULE_PATHS = [PYTHON_ECLIPSE + r"\ExergyFrames\src",
                PYTHON_ECLIPSE + r"\MyUtilities\src"
                ]


ABSOLUTE_LOGGING_PATH = r"C:\Eclipse\MyUtilities\LoggingConfig\loggingNofile.conf"

SEARCH_DIRS = ["D:\Freelancing\\", "D:\Scripting\All Scripts"]
MAX_CPU_PERCENT = 80
MAX_PROCESSES= 4
UPDATE_DELAY = 5


SQL_TEST_PATH = "C:\EclipseWorkspace\Evolve2\TestOutput\update_r228.sql"

IDF_TEMPLATE_FILE = FREELANCE_DIR + r"\IDF_Library\Templates.xlsx"
IDF_TEMPLATE_PATH = FREELANCE_DIR + r"\IDF_Library\\" 

IST_STATS_DIR = r"C:\Dropbox\04 School\IST Statistics"

if __name__ == "__main__":
    print PYTHON_ECLIPSE
    #print MODULE_PATHS
    
    
    cmdList = list()
    cmdList.append("import sys")

    for modulePth in MODULE_PATHS:
        cmdList.append("sys.path.append(\"{}\")".format(modulePth)) 
    
    cmdList.append("import exergy_frame as xrg")
    cmdList.append("import subprocess")
    
    for pth in  cmdList:
        print pth