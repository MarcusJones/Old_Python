'''
Created on 2012-09-09

@author: Anonymous
'''
import os

#===============================================================================
# E+ Projects
#===============================================================================

PROJ_SHOPPPING = {
                  'path_proj_excel' : r'D:\Projects\081_Central_Shopping_New\06 Project\\',
                  'idf_base' : r'D:\Projects\081_Central_Shopping_New\07 IDF\\',  
                  }

PROJ_ECOPOINT = {
                  'path_proj_excel' : r'D:\Projects\095_Ecopoint\Project\\',
                  'idf_base' : r'D:\Projects\095_Ecopoint\IDF\\',  
                  }

#===============================================================================
# 
#===============================================================================
PYTHON_ECLIPSE = os.getcwd() + r"\\..\..\..\\"
PYTHON_ECLIPSE = os.path.abspath(PYTHON_ECLIPSE) # Doesn't always work, not robust!! 
PYTHON_ECLIPSE = r"C:\EclipseWorkspace"

ECLIPSE_DIR = r"C:\EclipseWorkspace"

SAMPLE_SQL = r"C:\Projects\IDF_Library\Sample SQL"

FREELANCE_DIR =     projectOutDir = r"D:\Projects\\"
PATH_IDF_OUT = FREELANCE_DIR + r"\\IDFout\\"


TRNSYS_EXEC =  r"D:\Apps\Trnsys17_1\Exe\TRNexe.exe"
NUMBER_PARALLEL = 4

EXCEL_POST_PROC_TEMPLATE = "D:\EclipsePython\PyIDF\ExcelTemplates\postProcessTemplateLEED r03.xlsx"



#EXERGY_FRAME_PATH = 
#UTILITIES_PATH =  
#ExergyFrames\src
MODULE_PATHS = [PYTHON_ECLIPSE + r"\ExergyFrames\src",
                PYTHON_ECLIPSE + r"\MyUtilities\src"
                ]


ABSOLUTE_LOGGING_PATH = r"C:\EclipseWorkspace\MyUtilities\LoggingConfig\loggingNofile.conf"
LOGGING_ROOT_PATH = r"C:\EclipseWorkspace\MyUtilities\LoggingConfig\\"

SEARCH_DIRS = ["D:\Freelancing\\", "D:\Scripting\All Scripts"]
MAX_CPU_PERCENT = 80
MAX_PROCESSES= 4
UPDATE_DELAY = 2


SQL_TEST_PATH = "C:\EclipseWorkspace\Evolve2\TestOutput\update_r228.sql"

IDF_TEMPLATE_FILE = FREELANCE_DIR + r"\IDF_Library\Templates.xlsx"
IDF_TEMPLATE_PATH = FREELANCE_DIR + r"\IDF_Library\\" 

IST_STATS_DIR = r"C:\Dropbox\04 School\IST Statistics"

### SOLAR COOLING PAPER ###
SOLARCOOLING_PROJECT_DIR = r"C:\Projects2\100_SolarCooling"
#SOLARCOOLING_WEATHER_DIR = r"C:\Projects2\100_SolarCooling\WEA"
#PATH_BUI_TEMPLATE = r"C:\Projects2\100_SolarCooling\B17\Main_r11.b17"
#PATH_DCK = r"C:\Projects2\100_SolarCooling\Model\Main r10_imported.dck"
#SCHEDULE_DIR = r"C:\Projects2\100_SolarCooling\Model"
PROJECT_DIR = r"C:\thisProjDir"


#===============================================================================
# 
#===============================================================================
TRNSYS_EXEC = r"C:\Apps\Trnsys17\Exe\TRNExe.exe"
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