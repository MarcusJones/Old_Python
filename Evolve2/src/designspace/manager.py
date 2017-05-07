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

from utility_inspect import whoami
from utility_inspect import whoami, whosdaddy

import os

from utility_excel import ExcelBookRead
from variable import Variable as Variable
from design_space import DesignSpace
import controllers as controllers
import evaluators
import operators as operators

#import UtilityXML as util_xml 
import UtilityJSON as util_json
from pprint import pprint 
import utility_path as util_file
import time


#===============================================================================
# Code
#===============================================================================

def loadProjectFromJSON(settings):
    pprint(settings)
    
    settings = settings["project"]
    logging.debug("Loading project {}".format(settings["name"]))
    
    #print settings['algorithm']['controller']

    
    controllerClass = getattr(controllers, settings['algorithm']['controller'])
    controllerSettings = settings['algorithm']['settings']
    controller = controllerClass(controllerSettings)
    
    
    
    #- Variables ----------
    vList = list()
    vNames = list()
    for varDef in settings['designspace']['variables']:

            
        if varDef['ordered'] == 'True': ordered = True
        else: ordered = False
        
        
        if 'val' in varDef:
            try: 
                print varDef
                if varDef['type'] == 'int': 
                    varDef['val'] = [int(i) for i in varDef['val']]
                elif varDef['type'] == 'float': 
                    #print varDef['val']
                    varDef['val'] = [float(i) for i in varDef['val']]
                elif varDef['type'] == 'string': 
                    pass
                else: raise Exception("Test")
                thisVar = Variable(varDef['name'], 
                                         varDef['val'], 
                                         ordered, 
                                         )
            except:
                raise
        else:
            
            thisVar = Variable.from_range(varDef['name'], 
                                     varDef['min'], 
                                     varDef['step'], 
                                     varDef['max'],)
        vNames.append(varDef['name'])
        vList.append(thisVar)
    logging.debug("Loaded {} variables from settings".format(vNames))
    
    #- Objectives ------------
    objectives = settings['objective_space']['objectives']
    logging.debug("Loaded {} objectives from settings".format(settings['objective_space']['objectives']))
    
    #- Design space ----------
    thisDspace = DesignSpace(vList,objectives)
    logging.debug("Created design space from settings".format())
    
    controller.registerDSpace(thisDspace)
    
    #- Register operators ----
    opList = list()
    opNames = list()
    if 'algorithm' in settings:
        if 'operators' in settings['algorithm']:
            for op in settings['algorithm']['operators']:
                #print getattr(operator, 'test')
                
                logging.debug("Creating {}".format(op['name']))
                if 'parameters' in op:
                    logging.debug("Creating parameters for {}; {}".format(op['name'], op['parameters']))
                #parameters
                opNames.append(op['name'])
                ThisOperator = getattr(operators, op['name'])
                opList.append(ThisOperator(op))
    logging.debug("Created {} operators from settings".format(opNames))

    controller.registerOperators(opList)

            
    #- Register the evaluator ------
    theEvaluator = getattr(evaluators, settings['algorithm']['evaluator'])
    logging.debug("Created {} evaluator from settings".format(settings['algorithm']['evaluator']))

    controller.registerEvaluator(theEvaluator)


    #- Create the directory root ----
    #print path_exists(settings['projectPath'])
    
    #raise
    #print splitUpPath(settings['projectPath'])
    #print 
    print util_file.getNewDirectoryRev(settings['projectPath'])
    
    #raise
    if util_file.path_exists(settings['projectPath']):
        #print path_exists(settings['projectPath'])
        if util_file.query_yes_no("Overwrite this project? {}".format(settings['projectPath'])):
            util_file.erase_dir(settings['projectPath'])
            util_file.create_dir(settings['projectPath'])
    else: 
        util_file.create_dir(settings['projectPath'])

    
    #- Create the DB ---------------
    logging.debug("Creating database: {}".format(settings["databasePath"]))
    start = time.time()
    
    
    controller.createDatabase(settings["databasePath"])
    end = time.time()
    logging.info("Created DB over {:.2f} seconds".format(end - start))

    #- Finished! -------------
    
    logging.debug("SUMMARY:".format())
    controller.print_summary()    
    
    raise 
    return controller
    




    
def runProject(projectPath):
    settings = util_json.loadSettingsFile(projectPath)
    controller = loadProjectFromJSON(settings)
    controller.execute()
    controller.postProc()
    
    
    
#-OLD--------------------------------
def getVariables(definitionBookPath):
    
    thisBook = ExcelBookRead(definitionBookPath)
    allData = thisBook.getTable("Variables")
    variableDefRows = [row for row in allData[2:] if row[0]]
    
    vList = list()
    for varDef in variableDefRows:
        varDef[0] = str(varDef[0])
        if varDef[1] == "Yes": # Ordered
            if varDef[2] == "Range": # Range
                thisVar = Variable.from_range(varDef[0], str(varDef[3]), str(varDef[4]), str(varDef[5]))
                vList.append(thisVar)
            elif varDef[2] == "List": # List
                values = tuple([var for var in varDef[3:] if var])
                thisVar = Variable.ordered(varDef[0],values)
                vList.append(thisVar)
            else: raise
            
        elif varDef[1] == "No":
            if varDef[2] == "Range": # 
                raise
            elif varDef[2] == "List": #
                values = tuple([var for var in varDef[3:] if var])
                thisVar = Variable.ordered(varDef[0],values)
                vList.append(thisVar)
            else: raise
            
        else: raise
    return vList

def getObjectives(definitionBookPath):

    thisBook = ExcelBookRead(definitionBookPath)
    allData = thisBook.getTable("Objectives")
    objectiveDefRows = [row for row in allData[1:] if row[0]]
    
    objList = list()
    for objDef in objectiveDefRows:
        objList.append(objDef[0])

    return objList

def getDesignSpace(definitionBookPath):
        basisVariables = getVariables(definitionBookPath)
        objectives = getObjectives(definitionBookPath)
        thisDspace = DesignSpace(basisVariables,objectives)
        
        return thisDspace

def getProjectDef(definitionBookPath):
    thisBook = ExcelBookRead(definitionBookPath)
    allData = thisBook.getTable("Project")
    dictionaryRows = [row for row in allData[1:] if row[0]]

    settings = dict(dictionaryRows)
    
    if settings["Type"] == "Global Search":
        settings["Controller"] = cntrl_globalSearch

    elif settings["Type"] == "Random Search":
        settings["Controller"] = Controller_randomSearch
        
    elif settings["Type"] == "Basic Evolution":
        settings["Controller"] = cntrl_basicEvolutionary
        
    else:
        raise Exception("Project type {} does not exist".format(settings["Type"]))
    
    #if settings["Individual"] == "Math":
    #    settings["evaluator"] = sumMaxFitness
    #print repr(settings["Type"])
    #print repr(str(settings["Type"]))

    
    return settings
 
    
def runProjectOLD(definitionBookPath):
    # Get settings
    settings = getProjectDef(definitionBookPath)
    
    # Get design space
    designSpace = getDesignSpace(definitionBookPath)
    
    # Get the database started
    DB = create_database(designSpace,settings["Database path"])
    
    # Instantiate the controller
    theController = settings["Controller"](settings,designSpace,DB)
    
    # Start the controller
    theController.execute()
    
    # End the controller
    theController.postProc()        
        
#===============================================================================
# Unit testing
#===============================================================================

class testExcelCreate(unittest.TestCase):
    def setUp(self):
        print "**** TEST {} ****".format(whoami())

    def test010_LoadDSpace(self):
        print "**** TEST {} ****".format(whoami())
        #projectPath = os.path.abspath(os.curdir + r"\..\..\\" + r"Config\testProject_LoadDSpace.xml")
        projectPath = os.path.abspath(os.curdir + r"\..\..\\" + r"Config\testProject_LoadDSpace.json")
        runProject(projectPath)
        
    @unittest.skip("")
    def test010_RandomSearch(self):
        print "**** TEST {} ****".format(whoami())
        definitionBookPath = os.path.abspath(os.curdir + r"\..\..\\" + r"Config\testingRandomSearch.xlsx")
        runProject(definitionBookPath)

        
    @unittest.skip("")
    def test020_GlobalSearch(self):
        print "**** TEST {} ****".format(whoami())
        definitionBookPath = os.path.abspath(os.curdir + r"\..\..\\" + r"Config\testingGlobalSearch.xlsx")
        designSpace = getDesignSpace(definitionBookPath)
        
        
        settings = getProjectDef(definitionBookPath)
        
        # Call the controller
        settings["Controller"](settings, designSpace)

    @unittest.skip("")
    def test030_BasicEvo(self):
        print "**** TEST {} ****".format(whoami())
        definitionBookPath = os.path.abspath(os.curdir + r"\..\..\\" + r"Config\testingBasicEvo.xlsx")
        designSpace = getDesignSpace(definitionBookPath)
        settings = getProjectDef(definitionBookPath)
        
        # Call the controller
        settings["Controller"](settings, designSpace)

    @unittest.skip("")
    def test040_OperatorEvo(self):
        print "**** TEST {} ****".format(whoami())
        definitionBookPath = os.path.abspath(os.curdir + r"\..\..\\" + r"Config\testingBasicEvoOperators.xlsx")
        designSpace = getDesignSpace(definitionBookPath)
        settings = getProjectDef(definitionBookPath)
        DB = create_database(self.D1,self.SQLtestLocationNewRev)
        
        # Call the controller
        settings["Controller"](settings, designSpace, DB)
       
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
    