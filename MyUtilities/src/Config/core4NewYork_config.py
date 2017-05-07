'''
Created on 2012-09-09

@author: Anonymous
'''
import os
from UtilityFile import FileObject
PYTHON_ECLIPSE = os.getcwd() + r"\\..\..\..\\"
PYTHON_ECLIPSE = os.path.abspath(PYTHON_ECLIPSE) # Doesn't always work, not robust!! 
#PYTHON_ECLIPSE = r"D:\Eclipse"


ECLIPSE_DIR = r"C:\Eclipse"


FREELANCE_DIR =     projectOutDir = r"C:\Projects\\"
PATH_IDF_OUT = FREELANCE_DIR + r"\\IDFout\\"

TRNSYS_EXEC =  r"C:\Apps\Trnsys17\Exe\TRNExe.exe"

EXCEL_POST_PROC_TEMPLATE = "C:\Eclipse\PyIDF\ExcelTemplates\postProcessTemplateLEED r03.xlsx"


### SOLAR COOLING PAPER ###
SOLARCOOLING_WEATHER_DIR = r"C:\Projects\100_SolarCooling\WEA"
PATH_BUI_TEMPLATE = r"C:\Projects\100_SolarCooling\Model\building.b17"
PATH_DCK = r"C:\Projects\100_SolarCooling\Model\Main r10_imported.dck"
SCHEDULE_DIR = r"C:\Projects\100_SolarCooling\Model"
PROJECT_DIR = r"C:\thisProjDir"





#EXERGY_FRAME_PATH = 
#UTILITIES_PATH =  
#ExergyFrames\src
MODULE_PATHS = [PYTHON_ECLIPSE + r"\ExergyFrames\src",
                PYTHON_ECLIPSE + r"\MyUtilities\src"
                ]

logFilePath = r"C:\Eclipse\MyUtilities\LoggingConfig\loggingNofile.conf"
thisFile = FileObject(logFilePath)
if not thisFile.exists():
    raise Exception("Logging config file DNE! {}".format(logFilePath))
else:
    ABSOLUTE_LOGGING_PATH = logFilePath

SEARCH_DIRS = ["D:\Freelancing\\", "D:\Scripting\All Scripts"]
MAX_CPU_PERCENT = 80
MAX_PROCESSES= 4
UPDATE_DELAY = 5


IDF_TEMPLATE_FILE = r"C:\Projects\IDF_Library\Templates.xlsx"
IDF_TEMPLATE_PATH = r"C:\Projects\IDF_Library\\" 
IDD_PATH = r"C:\EnergyPlusV7-2-0\Energy+.idd"

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