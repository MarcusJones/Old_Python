from __future__ import division    
'''
Created on 2013-08-01

@author: Anonymous2
'''
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
FLG_PRE = 0
FLG_EXEC = 0
FLG_POST1 = 0
FLG_POST_SUM = 0
FLG_POST_ZONESUM = 0
from config import *

import logging.config
import unittest
import re
from utility_inspect import whoami, whosdaddy, listObject
import UtilityFile as utilFile
import utility_path as utilDir
from UtilityFile import FileObject

from RunTRNSYS import getTRNSYScommand
from UtilityExecutor import ExecuteParallel
import exergyframes.exergy_frame as xrg
import pandas as pd
#print x
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
    
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        
    @unittest.skipIf(not FLG_PRE,"")
    def test010_SimpleCreation(self):
        print "**** TEST {} ****".format(whoami())
        
        #=======================================================================
        # Paths
        #=======================================================================
        SOLARCOOLING_PROJECT_DIR = r"C:\Projects2\100_SolarCooling"
        pathToBuiTemplate = os.path.join(SOLARCOOLING_PROJECT_DIR, "Model", "building.b17")
        pathToDCK = os.path.join(SOLARCOOLING_PROJECT_DIR, "Model", "Main r10_imported.dck")
        schedules_dir = os.path.join(SOLARCOOLING_PROJECT_DIR, "Model")
        weatherPath = os.path.join(SOLARCOOLING_PROJECT_DIR, "WEA")
        weatherUnzipPath = PROJECT_DIR + r"\tempWeatherUnzip"
        mainProjectDir = PROJECT_DIR
        
        #=======================================================================
        # Error checking
        #=======================================================================
        assert os.path.exists(pathToBuiTemplate), "{} not found".format(pathToBuiTemplate)
        assert os.path.exists(pathToDCK), "{} not found".format(pathToDCK)
        assert os.path.exists(weatherPath), "{} not found".format(weatherPath)
        if not os.path.exists(mainProjectDir):
            utilDir.create_dir(mainProjectDir)
        if not os.path.exists(weatherUnzipPath):
            utilDir.create_dir(mainProjectDir)

                
        #=======================================================================
        # Get the weather
        #=======================================================================
        file_list = ["AUT_Vienna.Schwechat.110360_IWEC","AUT_Innsbruck.111200_IWEC"]
        weaFiles = utilDir.get_files_by_ext_recurse(weatherPath,"zip")
        for filePath in weaFiles:
            #print filePath
            flg_found = False
            for file_name in file_list:
                if re.search(file_name, filePath):
                    flg_found = True
                    break
            if not flg_found:
                continue
            logging.info("\n\nProcessing {}".format(filePath))
            # Unzip the weather
            utilFile.unzip(filePath,weatherUnzipPath)
            
            
            # Get the climate zone
            statPath = utilDir.get_file_by_ext_one(weatherUnzipPath,"stat")[0]
            statFile = utilFile.FileObject(statPath)
            CZline = statFile.getMatch("^\s*-\s*Climate\stype\s\"\S+\"\s\(ASHRAE")
            # - Climate type "1A" (ASHRAE Standards 90.1-2004 and 90.2-2004 Climate Zone)**
            #- Climate type "1B" (ASHRAE Standards 90.1-2004 and 90.2-2004 Climate Zone)**
            
            try: 
                CZquoted = re.search("\"\S+\"",CZline).group()
                CZnumber = re.search("\d",CZquoted).group()
            except:
                #CZquoted = re.search("\"\w\w\"",CZline).group()
                CZnumber = "-1"
                print "Couldn't find climate zone in line {} in file {}".format(CZline,statPath)
                
                continue
                #raise Exception()
            
            
            # Create the directory
            fileName = utilDir.split_up_path(statFile.filePath)[-2]
            projName = "{}--{}".format(CZnumber,fileName)
            projDir = os.path.join(mainProjectDir,projName)
            utilDir.create_dir(projDir)
            utilDir.create_dir(projDir+r"\out")
            
            # Move in the WEA
            thisWeaPath = utilDir.get_file_by_ext_one(weatherUnzipPath,"epw")[0]
            targetWeatherPath = os.path.join(projDir,"weather.epw")
            utilDir.copy_file(thisWeaPath, targetWeatherPath)
            
            # Move in the STAT
            this_stat_path = utilDir.get_file_by_ext_one(weatherUnzipPath,"stat")[0]
            target_stat_path  = os.path.join(projDir,"weather.stat")
            utilDir.copy_file(this_stat_path, target_stat_path)
            
            
            # Clean up weather temp dir
            utilDir.erase_dir_contents(weatherUnzipPath)
            
            # Read the weather file for information
            thisWeather = FileObject(targetWeatherPath)
            thisWeather.loadLines()
            firstLine = thisWeather.lines[0].strip().split(",")
            
            # Get the basic information from the EPW file
            descriptions = ["Skip1","City","State", "Country", "Source", "Station", "Latitude", "Longitude", "Timezone", "Elevation"]
            thisWeathDesc = dict(zip(descriptions,firstLine))
            logging.info("\t\tCity {}, Zone {}, Lat {}, Long {}".format(thisWeathDesc["City"],CZnumber,thisWeathDesc["Latitude"],thisWeathDesc["Longitude"]))
            
            #===================================================================
            # Copy all CSV schedules
            #===================================================================
            for schedFile in utilDir.get_file_by_ext_one(schedules_dir,"csv"):
                schedList = utilDir.split_up_path(schedFile)
                ext = schedList.pop()
                fileName = schedList.pop()
                
                utilDir.copy_file(schedFile,os.path.join(projDir,fileName + ext) )

            #=======================================================================
            # B17 File
            #=======================================================================
            templateB17 = FileObject(pathToBuiTemplate)

            # Parameterize the BUI
            replacements = [
                            # The original constructions are replaced with unused names
                            [r"^WALL EXT_WALL$",        "WALL REPLACED_WALL"],
                            [r"^WALL EXT_ROOF$",     "WALL REPLACED_ROOF"],
                            [r"^WALL EXT_FLOOR$",    "WALL REPLACED_FLOOR"],
                            [r"^WINDOW EXT_WINDOW1$",    "WINDOW REPLACED_WINDOW"],
    
                            # The CZ are renamed to replace the missing constructions
                            [r"^WALL ROOF_CZ{}$".format(CZnumber), "WALL EXT_ROOF"],
                            [r"^WALL EXT_WALL_CZ{}$".format(CZnumber), "WALL EXT_WALL"],
                            [r"^WALL FLOOR_TG_CZ{}$".format(CZnumber),    "WALL EXT_FLOOR"],
                            [r"^WINDOW WIND_CZ{}$".format(CZnumber), "WINDOW EXT_WINDOW1"],
                            
                            ]
            
            templateB17.loadLines()
            templateB17.makeReplacements(replacements)
            templateB17.writeFile(os.path.join(projDir,"building.b17"))
            # Copy it over
            utilDir.copy_file(pathToDCK,os.path.join(projDir,"deckfile.dck") )

    
    @unittest.skipIf(not FLG_EXEC, "")
    def test020_execute(self):
        print "**** TEST {} ****".format(whoami())
        
        commands = [getTRNSYScommand(dck,True) for dck in utilDir.get_files_by_ext_recurse(PROJECT_DIR,"dck")]
#        for dckFile in utilDir.get_files_by_ext_recurse(PROJECT_DIR,"dck"):
#            #print utilDir.split_up_path(dckFile)
#            print getTRNSYScommand(dckFile)
#
#            #runTRNSYS(dckFile)
#            #raise
        ExecuteParallel(commands)

    @unittest.skipIf(not FLG_POST1, "")
    def test030_post(self):
        print "**** TEST {} ****".format(whoami())
        for dckFile in utilDir.get_files_by_ext_recurse(PROJECT_DIR,"dck"):
            projDir = os.path.join(*utilDir.split_up_path(dckFile)[:-2])
            summaryFile = FileObject(os.path.join(projDir, "SUMMARY.BAL"))
            solarFile = FileObject(os.path.join(projDir, "SOLAR_TOT.BAL"))
            outDir = os.path.join(projDir, "out")
            outFiles = utilDir.get_files_by_ext_recurse(outDir, "out")
            frameList = list()
            for filePath in outFiles:
                # Skip unless 3 elements in file name!
                pureFileName = os.path.splitext(os.path.split(filePath)[1])[0]
                splitFileName = re.split("_",pureFileName)
                if len(splitFileName)==3:
                    thisFrame = xrg.load_single_out_file(filePath)
                else:
                    raise        
                    logging.info("(Skipping '{}')".format(os.path.split(pureFileName)[1]))        
                frameList.append(thisFrame)
            
            new_frame = xrg.mergeFrames("dataFrame", frameList, flgMergeHeads = True)
            new_frame.saveToMat(os.path.join(projDir, "result.mat"))
            new_frame = xrg.add_simple_time(new_frame)
            new_frame.saveToCSV(os.path.join(projDir, "result.csv"))

    @unittest.skipIf(not FLG_POST_SUM, "")
    def test040_post_summary(self):
        print "**** TEST {} ****".format(whoami())
        frames = list()
        for dckFile in utilDir.get_files_by_ext_recurse(PROJECT_DIR,"dck"):
            
            # Get each individual project directory
            projDir = os.path.join(*utilDir.split_up_path(dckFile)[:-2])
            summaryFile = FileObject(os.path.join(projDir, "SUMMARY.BAL"))
            
            #===================================================================
            # STAT file
            #===================================================================
            # Get the climate zone from the STAT
            stat_file = FileObject(os.path.join(projDir, "weather.stat"))
            stat_file.loadLines()
            CZline = stat_file.getMatch("^\s-\sClimate\stype\s\"\w\w\"\s\(ASHRAE")
            # Make sure we can find a climate zone
            try:
                CZquoted = re.search("\"\w\w\"",CZline).group()
                CZnumber = re.search("\d",CZquoted).group()
                CZletter = re.search("\w+",CZquoted).group()[1]
            except:
                CZnumber = 'UNK'
                CZletter = 'UNK'              
            kop_line = stat_file.getMatch(u"^\s-\sClimate\stype\s\"\w\w+\"\s\(K")
            kop_letter = re.search("\"\w+\"",kop_line).group()
            kop_letter = re.search("\w+",kop_letter).group()


            #===================================================================
            # Get weather descriptions
            #===================================================================
            # Read the weather file for information
            thisWeather = FileObject(os.path.join(projDir, "weather.epw"))
            thisWeather.loadLines()
            firstLine = thisWeather.lines[0].strip().split(",")
            firstLine += [CZnumber,CZletter,kop_letter]
            # The first line of the weather file contains the info
            descriptions = ["Skip1","City","State", "Country", "Source", "Station", "Latitude", "Longitude", "Timezone", "Elevation","CZnumber","CZletter","Koppen Class"]
            description = dict(zip(descriptions,firstLine))
            
            #===================================================================
            # Energy_TOT into aggregated file
            #===================================================================
            # Clean up the Energy_TOT.BAL file, save it as version 2
            energy_total = FileObject(os.path.join(projDir, "ENERGY_TOT.BAL"))
            energy_total.makeReplacements([["\|", ""],["=", " "],["\+", " "],["-", " "]])
            new_path = energy_total.filePath + "2"
            energy_total.writeFile(new_path)
            energy_total = FileObject(new_path)
            # Load it in
            df = pd.read_csv(energy_total.filePath, header=[0,1], delimiter=r"\s+")

            # Sum it up and flip it
            df_sum_energy = pd.DataFrame(df.sum()).transpose()
            
            #===================================================================
            # Solar_TOT into aggregated file
            #===================================================================
            # Clean up the Energy_TOT.BAL file, save it as version 2
            solar_total = FileObject(os.path.join(projDir, "SOLAR_TOT.BAL"))
            solar_total.makeReplacements([["\|", ""],["=", " "],["\+", " "],["-", " "]])
            new_path = solar_total.filePath + "2"
            solar_total.writeFile(new_path)
            solar_total = FileObject(new_path)
            # Load it in
            df = pd.read_csv(solar_total.filePath, header=[0,1], delimiter=r"\s+")

            # Sum it up and flip it
            df_sum_solar = pd.DataFrame(df.sum()).transpose()
            
            
            #print df_sum_energy
            #print df_sum_solar
            total_sum = pd.merge(df_sum_energy, df_sum_solar)
            #print df_sum_solar[:][:6]
            #print total_sum[:][1:6]
            #raise
            
            #===================================================================
            # Compile the location info 
            #===================================================================
            total_sum['City']        =  description['City']       
            total_sum['Elevation']   =  description['Elevation']  
            total_sum['Country']     =  description['Country']    
            total_sum['Longitude']   =  description['Longitude']  
            total_sum['Latitude']    =  description['Latitude']   
            total_sum['State']       =  description['State']      
            total_sum['filename'] = energy_total.filePath
            total_sum["CZnumber"]         =  description["CZnumber"]     
            total_sum["CZletter"]         =  description["CZletter"]     
            total_sum["Koppen Class"]     =  description["Koppen Class"]
             
            #print total_sum
            frames.append(total_sum)         
        
        # Concat defaults to 0 axis (rows)
        df_aggregated = pd.concat(frames)
        
        #print df_aggregated.iloc[:,2:4]
        #raise
        
        result_path = r"C:\thisProjDir\aggregated.xls"
        writer = pd.ExcelWriter(result_path) 

        df_aggregated.to_excel(writer, 'Aggregated')
        logging.debug("Created {} ".format(result_path))
        writer.save()
        



    @unittest.skipIf(not FLG_POST_ZONESUM, "")
    def test050_post_zonal(self):
        print "**** TEST {} ****".format(whoami())
        frames = list()
        for dckFile in utilDir.get_files_by_ext_recurse(PROJECT_DIR,"dck"):
            
            # Get each individual project directory
            projDir = os.path.join(*utilDir.split_up_path(dckFile)[:-2])
           
            #===================================================================
            # Energy_zone into aggregated file
            #===================================================================
            # Clean up the Energy_TOT.BAL file, save it as version 2
            energy_total = FileObject(os.path.join(projDir, "ENERGY_zone.BAL"))
            energy_total.makeReplacements([["\|", ""],["=", " "],["\+", " "],["-", " "]])
            new_path = energy_total.filePath + "2"
            energy_total.writeFile(new_path)
            energy_total = FileObject(new_path)
            # Load it in
            df = pd.read_csv(energy_total.filePath, header=[0,1], delimiter=r"\s+")

            # Sum it up and flip it
            df_sum_energy = pd.DataFrame(df.sum()).transpose()
            
            #===================================================================
            # Solar_zone into aggregated file
            #===================================================================
            # Clean up the Energy_TOT.BAL file, save it as version 2
            solar_total = FileObject(os.path.join(projDir, "SOLAR_ZONES.BAL"))
            solar_total.makeReplacements([["\|", ""],["=", " "],["\+", " "],["-", " "]])
            new_path = solar_total.filePath + "2"
            solar_total.writeFile(new_path)
            solar_total = FileObject(new_path)
            # Load it in
            df = pd.read_csv(solar_total.filePath, header=[0,1], delimiter=r"\s+")

            # Sum it up and flip it
            df_sum_solar = pd.DataFrame(df.sum()).transpose()
            
            
            for col in df_sum_solar.columns:
                new = col[0] + 'SOL'
                col = (new, col[1])
            print df_sum_solar.columns    
            raise
            print df_sum_energy

            # Merge the two
            total_sum = pd.merge(df_sum_energy, df_sum_solar,'outer')
            print total_sum

            #print total_sum
            frames.append(total_sum)         
            
        #=======================================================================
        # write
        #=======================================================================
        # Concat defaults to 0 axis (rows)
        df_aggregated = pd.concat(frames)
        
        #print df_aggregated.iloc[:,2:4]
        #raise
        
        result_path = r"C:\thisProjDir\aggregated_zones.xls"
        writer = pd.ExcelWriter(result_path) 

        df_aggregated.to_excel(writer, 'Aggregated')
        logging.debug("Created {} ".format(result_path))
        writer.save()








                
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
    