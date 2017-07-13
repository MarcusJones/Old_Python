#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""This module does A and B. 
Etc.
"""


from __future__ import division    

from config import *
import logging.config
import unittest
from utility_inspect import whoami, whosdaddy, listObject

import re
from lxml import etree
import logging.config
import copy
from collections import defaultdict # Python 2.7 has a better 'Counter'
from Utilities import genID, idStr
from win32com.client import Dispatch
import os
import csv
from utility_path import split_up_path, get_files_by_ext_recurse

from UtilityPrintTable import PrettyTable
from copy import deepcopy
import json as json
import pprint as pprint
import random as random
pp = pprint.PrettyPrinter(indent=4)
pPrint = pp.pprint
from UtilityLogger import loggerCritical

from utility_excel import ExcelBookRead
from UtilityXML import printXML



#from ProjectScripts.generate_variants import *

keptClassesDict =  {
        'MoreClassesTEMP' : set([
                          # Geometry ##################
                          'Zone',                          
                          'BuildingSurface:Detailed',                            
                          'FenestrationSurface:Detailed',
                          'GlobalGeometryRules',
                          'Shading:Building:Detailed',

                          # Loads ######################
                          'People',
                          'ElectricEquipment',          
                          'Lights',
                          'Schedule:Compact',
                          'ZoneInfiltration:DesignFlowRate',
                          'ScheduleTypeLimits',
                                          
                           # Materials ##################
                          'Material:AirGap',
                          'Material:InfraredTransparent',
                          'WindowMaterial:Gas', 
                          'Material:NoMass',
                          'Material',
                          'Construction',
                          'WindowMaterial:SimpleGlazingSystem',
                          'WindowMaterial:Glazing',
                          ]),
                          
        'onlyGeometry' : set([
                          # Geometry ##################
                          'Zone',                          
                          'BuildingSurface:Detailed',                            
                          'FenestrationSurface:Detailed',
                          'Shading:Building:Detailed',
                          ]),      
        'noHVAC': set([   
                          # Control ##################
                          'Version',
                          'SimulationControl',
                          'Building',
                          'ShadowCalculation',
                          'Site:Location',
                          'SizingPeriod:DesignDay',
                          'RunPeriod',
                          'RunPeriodControl:DaylightSavingTime',
                          'Site:GroundTemperature:BuildingSurface',
                          'Site:GroundTemperature:BuildingSurface',
                          'Site:GroundTemperature:Deep',
                          'Site:GroundTemperature:Shallow',
                          'Site:GroundReflectance',
                          'Site:GroundReflectance:SnowModifier',                          
                          
                          # Schedules #################
                          'ScheduleTypeLimits',
                          'Schedule:Day:Hourly',
                          'Schedule:Week:Daily',
                          'Schedule:Compact',
               
                           # Surface Construction Elements ##################
                          'Material',
                          'Material:NoMass',
                          'Material:InfraredTransparent',
                          'Material:AirGap',
                          'WindowMaterial:Glazing',
                          'WindowMaterial:Gas', 
                          'WindowMaterial:SimpleGlazingSystem',
                          'WindowMaterial:Shade',
                          'MaterialProperty:GlazingSpectralData',
                          'Construction',
                          
                          # Surfaces
                          'Zone',
                          'BuildingSurface:Detailed',                            
                          'FenestrationSurface:Detailed',
                          'GlobalGeometryRules',
                          'WindowProperty:ShadingControl',
                          'WindowProperty:FrameAndDivider',
                          'Shading:Building:Detailed',
                          
                          # Advaced Surfaces
                          'SurfaceProperty:OtherSideCoefficients',
                          
                          # Loads ######################
                          'People',
                          'Lights',
                          'ElectricEquipment',          
                          'ZoneInfiltration:DesignFlowRate',
                        
                          # Daylighting
                          'Daylighting:Controls',
                          'OutputControl:IlluminanceMap:Style'
                          
                          # Zone Airflow
                          #'ZoneInfiltration:DesignFlowRate',
                          
                          # HVAC Design Objects
                          #'DesignSpecification:OutdoorAir',
                          #'DesignSpecification:ZoneAirDistribution',
                          #'Sizing:Zone',
                          'Sizing:System',
                          'Sizing:Plant',
                          
                          # Zone HVAC Controls and Thermostats
                          #'ZoneControl:Humidistat',
                          #'ZoneControl:Thermostat',
                          #'ZoneControl:Thermostat:OperativeTemperature',
                          #'ThermostatSetpoint:DualSetpoint',
                          
                          
                          # HVAC
                          #'ZoneHVAC:EquipmentConnections',
                          
                          ]),  
        'geometryAndSpaceLoads' : set([
                          # Geometry ##################
                          'Zone',                          
                          'BuildingSurface:Detailed',                            
                          'FenestrationSurface:Detailed',
                          'Shading:Building:Detailed',
                          'ZoneInfiltration:DesignFlowRate',
                          'ElectricEquipment',
                          'Lights',
                          'People',
                          'ZoneList',
                          'ScheduleTypeLimits',
                          'Schedule:Day:Interval',
                          'Schedule:Week:Daily',
                          'Schedule:Year',
                          ]),                          


}

#--- Manipulate Objects / CONFIRMED
def merge(objectA, objectB):
    # Start a new XML root object
    currentXML = myRootNode()

    # Create the new IDF object with this root
    mergedIDF = IDF.fromXmlObject(currentXML)

    AObjects = objectA.XML.xpath('//OBJECT')
    for object in AObjects:
        mergedIDF.XML.append(object)

    BObjects = objectB.XML.xpath('//OBJECT')
    for object in BObjects:
        mergedIDF.XML.append(object)
    
    logging.debug(idStr(
        "'{}':{} + '{}':{}  = '{}':{} Union operation".format(
                                                  objectA.ID,
                                              int(len(AObjects)), 
                                              objectB.ID,
                                              int(len(BObjects)),
                                              mergedIDF.ID,
                                              mergedIDF.numObjects,
                                              ),
        mergedIDF.ID))
    
    return mergedIDF


#--- Utilities 
def forceList(item):
    """Forces item to be a list
    """    
    if not isinstance(item, list):
        return [item]
    else:
        return item

#--- XML Utilities

def xmlTextReplace(objects, searchStr, theNewText):
    """Given a list of XML node objects, search through all ATTR elements
    Replace the "placeHolder" string with "theNewText"
    Returns the entire XML node
    """
    assert isinstance(objects,list)
    replaceCnt = 0
    for obj in objects:
        #print obj
        for attr in obj.xpath("ATTR"):
            # Replace all searchStr!
            #print attr
            if re.search(re.escape(searchStr), attr.text):
                attr.text = re.sub(re.escape(searchStr), theNewText, attr.text)
                replaceCnt = replaceCnt + 1
    logging.debug("Replaced {} with {}, {} times".format(searchStr,theNewText,replaceCnt))
    

def getPositionOfATTR(IDDobj, className, XMLattribName, XMLattribValue):
    """Given an IDD object, search for a class, an attribute, and it's value, return the
    position
    """
    classDef = treeGetClass(IDDobj.XML, className)
    assert len(classDef) == 1, "Actual length {}".format(len(classDef))
    classDef = classDef[0]
    
    position = classDef.xpath("count(./ATTR[@{}='{}']/preceding-sibling::*)+1".format(XMLattribName, XMLattribValue))
    
    return position

def myRootNode():
    # Start the XML tree
    xmlVer = "0.1"
    # Root tag
    currentXML = etree.Element("EnergyPlus_XML", XML_version=xmlVer)
    # A comment
    commentXML = etree.Comment("XML Schema for EnergyPlus version 6 'IDF' files and OpenStudio version 0.3.0 'OSM' files")
    currentXML.append(commentXML)
    # Another comment
    commentXML = etree.Comment("Schema created April. 2011 by Marcus Jones")
    currentXML.append(commentXML)
    return currentXML


    
def treeGetClass(IDFtree, classNameRegex, flgExact = True):
    """Returns a list of XML OBJECT nodes according to search of class name
    """
    
    #assert(isinstance(IDFtree,etree._ElementTree)), "Expected etree._Element, got {}".format(type(IDFtree))
    if flgExact:
        classNameRegex = "^" + classNameRegex + "$" 
    xpathSearch = "//CLASS[re:match(text(), '" + classNameRegex + "')]/.."
    queryElements = xpathRE(IDFtree,xpathSearch)
    queryElements = forceList(queryElements)

    logging.debug('Search of {} {} hits in {}'.format(classNameRegex, len(queryElements),IDFtree))
    
    return queryElements
    

def xpathRE(tree, strXpath):
    """
    This function is just an alias for the etree.xpath function,
    just to avoid having to always declare the namespace 're:'
    """
    return tree.xpath(strXpath, 
        namespaces={"re": "http://exslt.org/regular-expressions"})


#--- Introspection 

def idfGetZoneNameList(IDFobj, zoneName='.'):
    with loggerCritical():
        zoneElements = treeGetClass(IDFobj.XML, "^Zone$")
    
    names = list()
    for zoneEl in zoneElements:
        nameXml = zoneEl.xpath('ATTR') # Select ATTR
        name = nameXml[0].text # It's the first ATTR
        names.append(name)
    
    filteredNameList = [name for name in names if re.search(zoneName, name)]
    
    return filteredNameList

def printStdTable(rows):
    headers = rows.pop(0)
    alignments = rows.pop(0)
    alignments = zip(headers, alignments)
    theTable = PrettyTable(headers)
    for align in alignments:
        theTable.set_field_align(*align)
    
    for row in rows:
        theTable.add_row(row)
        
    print theTable
    
def getAllObjectsTable(IDFobj):
    """Lists all objects, and their names (first ATTR)
    """
    objects = IDFobj.XML.xpath('//OBJECT')
    
    tableHeader = [("Class", "Name")]
    tableAlign = [("r", "l")]
    tableRows = list()
    for object in objects:
        # Select the class of each object
        type = object.xpath('CLASS')
        name = object.xpath('ATTR')
        tableRows.append((type[0].text, name[0].text))

    return tableHeader + tableAlign + sorted(tableRows)

#--- Assembly
def applyDefaultConstNames(IDFobj, IDDobj):
    
    
    xpathSearch = r"OBJECT/CLASS[text() = 'BuildingSurface:Detailed']/.."
    surfaceObjs = IDFobj.XML.xpath(xpathSearch)
    for surface in surfaceObjs: 
        
        surfaceType = surface.xpath("ATTR[2]")[0].text
        surfaceBoundaryCond = surface.xpath("ATTR[5]")[0].text
        surfaceConstructionName = surface.xpath("ATTR[3]")[0]
        if surfaceBoundaryCond == "Surface":
            if surfaceType == "Ceiling":
                surfaceConstructionName.text = "Interior Ceiling"
            elif surfaceType == "Wall":
                surfaceConstructionName.text = "Interior Wall"
            elif surfaceType == "Floor":
                surfaceConstructionName.text = "Interior Floor"
            else:
                raise            
        elif surfaceBoundaryCond == "Outdoors" or surfaceBoundaryCond == "Adiabatic":
            if surfaceType == "Ceiling" or surfaceType == "Roof":
                surfaceConstructionName.text = "Exterior Roof"
            elif surfaceType == "Wall":
                surfaceConstructionName.text = "Exterior Wall"
            elif surfaceType == "Floor":
                surfaceConstructionName.text = "Exterior Floor"
            else:
                raise Exception("Surface type not found {}".format(surfaceType))
            
        elif surfaceBoundaryCond == "Ground":
            surfaceConstructionName.text = "Exterior Floor"
            
        else:
            print surfaceBoundaryCond
            raise
        
    logging.debug(idStr("Applied dummy constructions to {} surfaces".format(len(surfaceObjs)),IDFobj.ID))
        
    xpathSearch = r"OBJECT/CLASS[text() = 'FenestrationSurface:Detailed']/.."
    surfaceObjs = IDFobj.XML.xpath(xpathSearch)
    for surface in surfaceObjs: 
        surfaceType = surface.xpath("ATTR[2]")[0].text
        surfaceBoundaryCond = surface.xpath("ATTR[5]")[0].text
        surfaceConstructionName = surface.xpath("ATTR[3]")[0]
        surfaceConstructionName.text = r"Exterior Window"
        #print surface.xpath("ATTR[3]")[0].text
    #xpathSearch = r"OBJECT/CLASS[text() = 'BuildingSurface:Detailed']/.."
    #surfaceObjs = IDFobj.XML.xpath(xpathSearch)[0]
    #printXML(surfaceObjs)
    #raise 
    #raise
    logging.debug(idStr("Applied dummy constructions to {} windows".format(len(surfaceObjs)),IDFobj.ID))

    #pass

def applyChange(IDFobj, IDDobj, change):
    
    with loggerCritical():
        targetSelection = treeGetClass(IDDobj.XML, change['class'], True)
        #printXML(targetSelection[0])
    assert targetSelection
    
    with loggerCritical():
        position = IDDgetMatchedPosition(targetSelection[0],"field",change['attr'])
        
    assert position
    
    with loggerCritical():
        targetSelection = treeGetClass(IDFobj.XML, change['class'], True)
    
    # Match the NAME
    if len(targetSelection) > 1:
        #print targetSelection
        filteredSelection = list()
        #targetSelection = list()
        
        
        
        
        
        for cl in targetSelection:
            
            # Set the name in the tree to Upper Case
            original_name = cl[1].text
            cl[1].text = original_name.upper()
            
            change["objName"] = change["objName"].upper()
            #raise
            xpathSearch = "ATTR[re:match(text(), '" + change["objName"] + "')]/.."
            
            matchedClass = xpathRE(cl,xpathSearch)
            #print matchedClass
            if matchedClass:
                filteredSelection.append(matchedClass[0])

            # Reset the name back to original
            cl[1].text = original_name

                
            #print thisClass
        #printXML(cl)
        #print xpathSearch
        targetSelection = filteredSelection          
        assert targetSelection, "Couldn't find {} - {} - {}".format(change['class'],
                                                                    change['attr'],
                                                                    change["objName"]
                                                                    )
            #printXML(cl)
        #print targetSelection
        #raise
    
    numChanges = 0
    for thisClass in targetSelection:
        targetAttr = thisClass.xpath("ATTR[{}]".format(position))
        assert targetAttr
        #printXML(targetAttr[0])
        #logging.debug(idStr("Changing {} in {}, position {}".format(change['attr'],change['class'], position).format(change),IDFobj.ID))
        
        
        targetAttr = targetAttr[0]
        if not isinstance(change['newVal'],str):
            change['newVal'] = str(change['newVal'])
        targetAttr.text = change['newVal']
        numChanges += 1
        
    
    logging.debug(idStr("Changed {} times: {} ".format(numChanges,change,),IDFobj.ID))
    
    
    return IDFobj


def applyTemplate(IDFobj,IDDobj,IDFtemplate,zoneNames = ".", templateName = "No name", uniqueName = None):
    """ Template is a regular IDF object
    """
    logging.debug(idStr("Processing template *** {} ***: {}".format(templateName,IDFtemplate),IDFobj.ID)) 
    
    # Loop over each class of the template
    objectCnt = 0
    
    allObjsList = IDFtemplate.XML.xpath('//OBJECT')
    
    #replacement = random.randint(0, 1000000)
    #replacement = "{}".format(replacement)
    xmlTextReplace(allObjsList, "*SYSTEM NUMBER*",  uniqueName)
    #print allObjsList
    
    #raise 
    for thisClass in IDFtemplate.XML.xpath('//CLASS'):
        
        objectParent = thisClass.xpath("..")[0]
        # Inspect the DEFINITION of this thisClass
        objectClassName =  thisClass.text
        with loggerCritical():
            classDef = treeGetClass(IDDobj.XML, objectClassName)
        assert len(classDef) >= 1, "Couldn't any {} in IDD".format(objectClassName)
        assert len(classDef) == 1, "Found {} in IDD {} times".format(objectClassName,len(classDef))
        classDef = classDef[0]

        # This thisClass is multiplied over zones! 
        if (
            (
             IDDboolMatchField(classDef,"object-list","ZoneNames") 
             or 
             IDDboolMatchField(classDef,"object-list","ZoneAndZoneListNames")
             ) 
                and   
            (
             IDDboolMatchField(classDef,"field","Zone Name")
             or
             IDDboolMatchField(classDef,"field","Zone or ZoneList Name") 
             )
            
            and
            (objectClassName not in ("Pump:VariableSpeed","WaterUse:Equipment"))
            ):
            # Get the position of the zone name
            
            #print objectClassName, 
            #(objectClassName not in ["Pump:VariableSpeed",])
            
            #raise 
            
            #raise
            with loggerCritical():
                try:
                    position = IDDgetMatchedPosition(classDef,"object-list","ZoneNames")
                except:
                    position = IDDgetMatchedPosition(classDef,"object-list","ZoneAndZoneListNames")

            #print position
            if IDDboolMatchField(classDef,"field","Name"):
                # Get the position of the zone name
                with loggerCritical():
                    namePosition = IDDgetMatchedPosition(classDef,"field","Name")
            else:
                namePosition = -1
            #print IDDboolMatchField(classDef,"field","Name")
            #print namePosition
            #raise
            # Loop over zones            
            for zoneName in idfGetZoneNameList(IDFobj,zoneNames):
                #print zoneName
                thisMultiplyObject = deepcopy(objectParent)
                
                if namePosition != -1:
                    uniqueNameAttr = thisMultiplyObject.xpath("//ATTR[{}]".format(int(namePosition)))
                    uniqueNameAttr[0].text = uniqueNameAttr[0].text + zoneName
                #print namePosition
                #xmlTextReplace([thisMultiplyObject], r"\*ZONENAME\*",zoneName)
                
                # Update pointer to zone name
                targetNameAttr = thisMultiplyObject.xpath("//ATTR[{}]".format(int(position)))
                #printXML(targetNameAttr[0])
                try:
                    targetNameAttr[0].text = zoneName
                except:
                    print "Should {} really be multiplied?".format(objectClassName)
                    print "Position: {}".format(position)
                    print "zoneName: {}".format(zoneName)
                    print "namePosition: {}".format(namePosition)
                    printXML( classDef)
                    raise
                #print targetNameAttr[0].text
                #printXML(thisMultiplyObject)
                IDFobj.XML.append(thisMultiplyObject)
                #logging.debug(idStr("Zonename updated, position {}".format(int(position)),IDFobj.ID))

            logging.debug(idStr("\tMerged {} into {} over {} zones matching '{}'".format(objectClassName, IDFobj.ID, len(idfGetZoneNameList(IDFobj)),zoneNames),IDFobj.ID))

        # Otherwise, just merge it straight in
        else:
            
            # BUT: Check for any possible unique names
            IDFobj.XML.append(objectParent)
            objectCnt += 1
            
    logging.debug(idStr("\tMerged {} static objects from {}".format(objectCnt, templateName, IDFobj.ID,),IDFobj.ID)) 
    return IDFobj



def IDDboolMatchField(IDDclass, label, value):
    #printXML(IDDclass)
    #print IDDclass.xpath("//ATTR[@{}='{}']".format(label,value))
    
    #logging.debug("{}".format(IDDclass) )
    
    if IDDclass.xpath("ATTR[@{}='{}']".format(label,value)):
        return True
    else:
        return False

def IDDboolHasField(IDDclass, label):
    if IDDclass.xpath("ATTR[@{}]".format(label)):
        return True
    else:
        return False 


def IDDgetMatchedPosition(IDDclass,label,value):
    #search = IDDclass.xpath("ATTR[@{}='{}']".format(label,value))
    #objectName = IDDclass.xpath("CLASS")
    #assert len(search) == 1, "Object {}, {} = {}, {} hits".format(objectName[0].text, label,value,len(search))
    
    #print printXML(IDDclass)
    
    #position  = IDDclass.xpath("count(./ATTR[@{}='{}']/preceding-sibling::*)".format(label,value))
    
    
    matchList = list()
    for attrMatch in IDDclass.xpath("./ATTR[@{}='{}']".format(label,value)):
        thePosition = attrMatch.xpath("count(preceding-sibling::ATTR)")
        matchList.append(int(thePosition)+1)
        
    #allMatches = 
    #print allMatches
    #print allMatches[0].xpath("count(preceding-sibling::ATTR)")
    #print IDDclass.xpath("./ATTR[@{}='{}']/preceding-sibling::ATTR)".format(label,value))[0]
    #print position
    
    #print matchList
    #raise

    logging.debug("{} {}={} positions {}".format(IDDclass,label,value,matchList))
     
    #assert matchList, 
    try:
        matchList[0]
    except:
        #print logging.debug("Couldn't find {}={} in {}".format(label,value, IDDclass))
        #printXML(IDDclass)
        #raise Exception()
        print "Couldn't find {}={} in {} ".format(label,value, IDDclass[0].text )
        raise
    
    return matchList[0]





def assembleVariants(variants,IDDobj):
    """
    zoneClass - This is the target class which will be multiplied
    template - this is the template IDF Object
    """
    raise Exception("SEE VARIANTS IN CENTRAL FOR RECENT")


def getTemplatePath(templatePath, filterRegExString = ".", flgExact = True):
    if flgExact:
        filterRegExString= "^" + filterRegExString + "$"
        
    for root, dirs, files in os.walk(templatePath):
        for name in files:
            splitName = os.path.splitext(name)
            if splitName[1] == ".idf":
                if re.search(filterRegExString,splitName[0]):
                    return os.path.join(root, name)
#    raise
#
#    for path in get_files_by_ext_recurse(templatePath, "idf"):
#            base=os.path.basename(path)
#            fileName = os.path.splitext(base)[0]
#            if  re.search(filterRegExString,fileName):
#                #print path
#                #templatePath=IDF.fromIdfFile(path,fileName)
#                print os.path.abspath(fileName)
#                print fileName
#                raise
#                return fileName
#                ##template.getTemplateInfo()
#                #templates.append(template)
#                
    raise Exception("Template {} not found in {}".format(filterRegExString,templatePath))

def getTemplates(templatePath, filterRegExString = ".", flgExact = True):
    raise
# This is just a filter for file names now...
    """Given a path, return a list of matching IDF files, and load into IDF objects
    """ 

    templates = list()
    if flgExact:
        filterRegExString= "^" + filterRegExString + "$"

    with loggerCritical():
        for path in get_files_by_ext_recurse(templatePath, "idf"):
            base=os.path.basename(path)
            fileName = os.path.splitext(base)[0]
            if  re.search(filterRegExString,fileName):
                #print path
                template=IDF.fromIdfFile(path,fileName)
                #template.getTemplateInfo()
                templates.append(template)
    
    # No duplicates!
    assert(len(templates) == len(set(templates)))
    assert len(templates)
    
#    assert(len(thisTemplate) == 1), "Template; {} found {} matches {}".format(templateDef['templateName'],
#                    len(thisTemplate),thisTemplate)
#    thisTemplate = thisTemplate[0]    
        
    
    logging.debug("Found {} templates in {} filtered {}".format(len(templates),IDF_TEMPLATE_PATH, filterRegExString))
    
    return templates


def cleanOutObject(IDFobj,keptClassNames, flgExact = True):
    objectTable = getObjectCountTable(IDFobj)
    
    #print objectTable
    objectTable.pop(0) # Eject the header
    currentClasses = set([item[0] for item in objectTable])
    # List comprehension to create set
    deletedClasses = currentClasses - set(keptClassNames)
    
    myLogger = logging.getLogger()
    myLogger.setLevel("CRITICAL")
    
    IDFobj = deleteClasses(IDFobj,list(deletedClasses),flgExact)
    
    myLogger.setLevel("DEBUG")
    
    
    logging.debug(idStr(
        "Out of {0} classes in this IDF, {1} are deleted".format(
           len(currentClasses),
           len(deletedClasses),
           len(keptClassNames),
           ),IDFobj.ID))   
    return IDFobj


def deleteClasses(IDFobj, classNames, flgExact = True):

    for className in classNames:
        className = "^" + className + "$"
        
        queryElements = treeGetClass(IDFobj.XML,className)

        for object in queryElements:
            IDFobj.XML.remove(object)

        logging.debug(idStr(
            'Deleted {0} {1} objects'.format(len(queryElements), className),
            IDFobj.ID))
    return IDFobj


def deleteClassesFromExcel(IDFobj, IDDobj, delete):
    
    logging.debug(idStr("Deleting: {}".format(delete),IDFobj.ID))
    #[{'class': u'TestClass', 'Name': u'TestName'}]
    #raise
    with loggerCritical():
        targetSelection = treeGetClass(IDDobj.XML, delete['class'], True)
        #printXML(targetSelection[0])
    assert targetSelection
    #"Name"
    #with loggerCritical():
    #    position = IDDgetMatchedPosition(targetSelection[0],"field",change['attr'])
    #    
    #assert position
    
    with loggerCritical():
        targetSelection = treeGetClass(IDFobj.XML, delete['class'], True)
    
    # Match the NAME
    if len(targetSelection) > 1:
        #print targetSelection
        filteredSelection = list()
        #targetSelection = list()
        for cl in targetSelection:
            xpathSearch = "ATTR[re:match(text(), '" + delete["objName"] + "')]/.."
            
            matchedClass = xpathRE(cl,xpathSearch)
            #print matchedClass
            if matchedClass:
                filteredSelection.append(matchedClass[0])
            #print thisClass
        #printXML(cl)
        #print xpathSearch
        targetSelection = filteredSelection          
        assert targetSelection, "No {}".format(delete['class'])
            #printXML(cl)
        #print targetSelection
        #raise
    
    for object in targetSelection:
        IDFobj.XML.remove(object)    

    logging.debug(idStr("Deleted: {} objects".format(len(targetSelection)),IDFobj.ID))

def loadVariants(inputExcelPath,path_idf_base):
    
    logging.debug("Loading variants from {0}".format(inputExcelPath))
    
    # Attach the book
    book = ExcelBookRead(inputExcelPath)

    # Select the sheet
    variantsTable = book.getTable("(Variants)", startRow = 0, endRow=None, startCol=0, endCol=None)
    try:
        variantBlockLimits = [variantsTable.index(row) for row in variantsTable if row[0]]
    except:
        print(variantsTable)
        raise
    
    variants = dict()
    while len(variantBlockLimits) > 1:
        startRow = variantBlockLimits[0]
        endRow = variantBlockLimits[1]

        #print "This variant table", 
        variantBlockLimits.pop(0)
        #print variantsTable
        variantName = variantsTable[startRow][0]
        logging.debug("Working on {} table, rows {} to {}".format(variantName,startRow, endRow))
        
        if variantName in variants:
            raise Exception("Duplicate variant name {}".format(variantsTable[startRow][0]))
        
        rawTable = variantsTable[startRow:endRow]
        description = rawTable[0][2]
        
        # Process source path
        sourcePathDefinition = rawTable[0][3]
        sourcePath = path_idf_base + sourcePathDefinition
        
        # Flags
        flagIndices = [rawTable.index(row) for row in rawTable if row[1].strip() == "flag"]
        flagDefs =  [{"flag":rawTable[ind][2],
                "argument":rawTable[ind][3]}
                for ind in flagIndices]
                
        # Deletes
        deleteIndices = [rawTable.index(row) for row in rawTable if row[1].strip() == "del"]
        deleteDefs =  [{"class":rawTable[ind][2],
                "objName":rawTable[ind][3]}
                for ind in deleteIndices]
        
        # Templates
        templateIndices = [rawTable.index(row) for row in rawTable if row[1] == "tp"] 
        templateDefs =  [{"templateName":rawTable[ind][2],
                "zones":rawTable[ind][3],
                "uniqueName":"{}".format(rawTable[ind][4])} 
                for ind in templateIndices]
        # Changes
        changeIndices = [rawTable.index(row) for row in rawTable if row[1] == "ch"] 
        changeDefs = [{"class":rawTable[ind][2],
                "objName":rawTable[ind][3],
                "attr":rawTable[ind][4],
                "newVal":rawTable[ind][5],
                } 
                for ind in changeIndices]
        
              
        variants[variantName] = {
                                 "flags" : flagDefs,
                                 "deletes" : deleteDefs,
                                 "templates" : templateDefs,
                                 "changes" : changeDefs,
                                 "source" : sourcePath,
                                 "description" : description,
                                 
                                 }
    #print variants
    for var in variants:
        thisVar = variants[var]
        logging.debug("      *** {:>5} - {:<50} *** ".format("Variant",var))
        
        logging.debug("{:>20} : {:<50}".format("templates",len(thisVar["templates"])))

        logging.debug("{:>20} : {:<50}".format("flags",len(thisVar["flags"])))
                      
        logging.debug("{:>20} : {:<50}".format("deletes",len(thisVar["deletes"])))
        logging.debug("{:>20} : {:<50}".format("changes",len(thisVar["changes"])))
        logging.debug("{:>20} : {:<50}".format("description",thisVar["description"]))
        logging.debug("{:>20} : {:<50}".format("source",thisVar["source"]))

   
    #print variants
    logging.debug("Loaded {} variants from {}".format(len(variants),inputExcelPath))
    
    
    
    
    return variants

def shortStr(theStr, length = 30):
    if len(theStr)<=length:
        return theStr
    else:
        return theStr[0:length-3] + "..."

def deleteOrphanedZones(IDFobj):

    ### GET SPACES ###
    xpathSearch = "//CLASS[re:match(text(), '^OS:Space$')]/.."
    #xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]/"
    spaces = xpathRE(IDFobj.XML,xpathSearch)
    logging.debug("Found {} OS:Space".format(len(spaces)))

    
    ### GET ZONES ###
    xpathSearch = "//CLASS[re:match(text(), '^OS:ThermalZone')]/.."
    #xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]/"
    zones = xpathRE(IDFobj.XML,xpathSearch)
    logging.debug("Found {} OS:ThermalZone".format(len(zones)))
        
    
    ### LOOP Both REVERSE ###
    notFound = 0
    for zone in zones:    
        zoneName = zone.xpath("ATTR")[0].text
        found = False
        for space in spaces:    
        
            thisSpaceName = space.xpath("ATTR")[0].text
            thisSpacePointsToZoneName = space.xpath("ATTR")[9].text                    
            #zoneName = zone.xpath("ATTR")[0].text
            if re.search("^"+zoneName+"$",thisSpacePointsToZoneName):
                #print 
                #print "Match"
                #print "Space: {}, Space points to {}, Zone exists here: {}".format(thisSpaceName,thisSpacePointsToZoneName,zoneName)
                #newZoneName =  "ZONE " + thisSpaceName
                
                #print "New name:" + newZoneName
                found = True
                #space.xpath("ATTR")[9].text = newZoneName
                #zone.xpath("ATTR")[0].text =  newZoneName
        if not found:
                IDFobj.XML.remove(zone)
                notFound += 1
            
    logging.debug("Checked {} zones over {} spaces, deleted {} zones.".format(len(zones),len(spaces),notFound))


class IDF(object):
    '''
    The IDF class holds the IDF data
    '''
    
    #--- Creation
    #def __init__(self, pathIdfInput=None, XML=None, IDDstring = None, pathIdfOutput = None):
    def __init__(self, pathIdfInput=None, ID = None):
        # The path to source file
        self.pathIdfInput = pathIdfInput

        # Generate a random ID
        if not ID:
            self.ID = genID()
        
        # Created later
        #self.XML = None


    @classmethod
    def fromIdfFile(cls, pathIdfInput, ID = None):
        # First start a blank object
        thisClass = IDF(pathIdfInput=pathIdfInput, ID=ID)
        if not ID:
            thisClass.ID = genID()
        else: 
            thisClass.ID = ID
        
        # Assign the path object
        # Call the load
        thisClass.loadIDF()
        # Call convert
        thisClass.parseIDFtoXML()
        # Return this class

        logging.debug(idStr('Created an IDF object named {}, with {} objects'.format(
                                                                               thisClass.ID,
                                                                               thisClass.numObjects,
                                                                               ), thisClass.ID))
        return thisClass

    @classmethod
    def fromIDDFile(cls, pathIdfInput, ID = None):
        # First start a blank object
        thisClass = IDF(pathIdfInput=pathIdfInput, ID=ID)
        thisClass.ID = ID
        
        # Assign the path object
        # Call the load
        thisClass.loadIDF()
        # Call convert
        thisClass.parseIDFtoXML2()
        # Return this class

        logging.debug(idStr('Created an IDD (DEFINITION) object named {}, with {} objects'.format(
                                                                               thisClass.ID,
                                                                               thisClass.numObjects,
                                                                               ), thisClass.ID))
        return thisClass


    @classmethod
    def fromXmlFile(cls, pathXmlFile):
        
        # First start a blank object
        thisClass = IDF()
        
        thisClass.loadXML(pathXmlFile)

        #this
        #raise Exception("UNSUPPORTED")
        #thisClass = IDF()
        #thisClass.ID = genID() 
        #logging.debug(idStr('NOT IMPLEMENTED Creating IDF object from XML file', thisClass.ID))
        #cls.loadIDF(cls)
        return thisClass
    
    @classmethod
    def fromXmlObject(cls, XML):
        # First start a blank object
        thisClass = IDF()
        #thisClass.ID = genID() 
        # Assign the XML object
        thisClass.XML = XML
        # Return this class
        #logging.debug(idStr('Created IDF object from XML object', thisClass.ID))
#        logging.debug(idStr('Created an IDF object named {}, with {} objects'.format(
#                                                                               thisClass.ID,
#                                                                               thisClass.numObjects,
#                                                                               ), thisClass.ID))
#        
        return thisClass

    #--- Introspection
    def __str__(self):
        return "IDF:{}, IDF Lines:{}, XML Objects:{}, XML_root:{}".format(
                             self.ID,
                             self.numLines,
                             self.numObjects,
                             self.XML,
                             )
            #'Loaded IDF {0} with {1} lines'.format(self.pathIdfInput,countLines),
            #sxself.ID))
    
    @property
    def numLines(self):
        try: 
            self.IDFstring
            return(len(self.IDFstring))
        except:
            return 0
    
    @property
    def numObjects(self):
        if self.XML is not None:
            objects = self.XML.xpath('OBJECT')
            return(int(len(objects)))
        else:
            return 0 

    def printTemplateDef(self):
        try:
            print self.templateDef
        except:
            raise Exception("Template not defined")
        
        
    #--- Load data
    def loadXML(self,XMLpath):
        #print XMLpath
        self.XML = etree.parse(XMLpath)
        
        logging.debug(idStr(
            'Loaded XML from {}, {} objects'.format(
                                                 XMLpath, self.numObjects
                                                 ),self.ID))

    def loadIDF(self):
        # Define input and output full file paths
        fIn = open(self.pathIdfInput, 'r')
       
        # Calls the readlines method of object which returns a list object of lines
        #self.IDFlines = fIn.readlines()
        
        self.IDDstring = fIn.read()
        
        countLines = 0
        for line in self.IDDstring.split('\n'):
            countLines += 1

        logging.debug(idStr(
            'Loaded IDF {} with {} lines'.format(
                                                 self.pathIdfInput,
                                                 countLines,
                                                 ),self.ID))
        
        fIn.close()
    #--- Convert data

    def convertXMLtoIDF(self):
       
        stringTransform = """<?xml version="1.0" ?>
            <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
            <xsl:output method="text" indent="no"/>
            
            <xsl:template match="EnergyPlus_XML">
            <ROOT>
            <!-- New line, and select all OBJECTS -->
            <xsl:text>&#xa;</xsl:text>
            <xsl:apply-templates select="OBJECT"/>
            </ROOT>
            
            </xsl:template>
            
            <xsl:template match="OBJECT">
                <!-- Select NAME and newline -->
                <xsl:apply-templates select="CLASS"/>
                <xsl:text>&#xa;</xsl:text>
                <!-- Then select ATTR and newline -->
                <xsl:apply-templates select="ATTR"/>
                <xsl:text>&#xa;</xsl:text>
            </xsl:template>
            
            <!-- Write the class name and a comma -->
            <xsl:template match="CLASS"><xsl:value-of select="." />
                <xsl:text>,</xsl:text>
                <!-- Tab, !, and comment -->
                <xsl:text>&#9;</xsl:text>    
                <xsl:text>!</xsl:text>
                <xsl:value-of select="@Comment"/>
            </xsl:template>
            
                
            <!-- Add a tab, then attribute -->
            <xsl:template match="ATTR"><xsl:text>&#9;</xsl:text><xsl:value-of select="." />
                
                <!-- Add either a comma or a semi colon -->
                <xsl:if test="position() != last()">
                    <xsl:text>,</xsl:text>
                </xsl:if>
                <xsl:if test="position() = last()">
                    <xsl:text>;</xsl:text>
                </xsl:if>
                
                <!-- Tab, !, and comment -->
                <xsl:text>&#9;</xsl:text>    
                <xsl:text>!</xsl:text>
                <xsl:value-of select="@Comment"/>
                
                <!-- New line -->
                <xsl:text>&#xa;</xsl:text>
            </xsl:template>
            
            </xsl:stylesheet>
            """
        
        # Load the XSLT string into an etree
        xmlTransformXML = etree.XML(stringTransform)
        
        # Convert the XML into an XSLT transform object
        transform = etree.XSLT(xmlTransformXML)
        
        # Write a new IDF file from the current XML
        newIdfXml = transform(self.XML)
     
        self.IDDstring = newIdfXml.__str__()
        
        logging.debug(idStr(
            'Converted XML to IDF, {} objects'.format(self.numObjects),
            self.ID))
        
    def getTemplateInfo(self):
        # NOT NEEDED ANYMORE ! ?
        raise
        lines = list()
        
        # Get all lines
        for line in self.IDDstring.split('\n'):
            lines.append(line)
        
        # Look for !!!
        lineIndex = 0
        jsonDefLines = list()
        while (lineIndex < len(lines)) :
            thisLine = lines[lineIndex]
            if re.search(r"^!!!", thisLine,re.VERBOSE):
                jsonDefLines.append(re.sub(r'!!!', '', thisLine))
            lineIndex += 1
        jsonDefString = "\n".join(jsonDefLines)
        data = None
#        if jsonDefLines:
#            try:
#                data = json.loads(jsonDefString)
#            except:
#                print jsonDefString
#                raise
#            # Split the name def! 
#            try:
#                nameDef = data["uniqueName"]
#            except:
#                print lines
#                raise
#            nameDef = re.split('=', nameDef)
#            data["uniqueNameLoc"] =  nameDef[0].strip()
#            data["uniqueName"] =  nameDef[1].strip()
        self.templateDef = data
    
    def tokenize(self,thisLine):
        tokens = dict()
        
        splitDict = {
             "splitFld"                 : re.compile(r"\\ \w+",re.VERBOSE),
             "splitComma"   : re.compile(r",",re.VERBOSE),
                 }
        pattDict = {
                    "Object"          : re.compile(r"^\s*[\w:]+\s*[,;]",re.VERBOSE),
                    "Field"                 : re.compile(r"\\ \S+",re.VERBOSE),
                    "splitSemi"   : re.compile(r";",re.VERBOSE),
                    
                    }    
        
        # Check for field, strip it off
        if re.search(pattDict["Field"], thisLine):
            
            thisLine = str(thisLine.encode('utf-8').decode('ascii', 'ignore'))
            # Get field name
            fieldNameToken = re.findall(pattDict["Field"],thisLine)
            
            assert len(fieldNameToken) == 1, Exception("ERROR on this line\n {}".format(thisLine))
            
            fieldNameFirst = fieldNameToken[0][1:]
            fieldNameFirst=re.sub(r">","_GT",fieldNameFirst)
            fieldNameFirst=re.sub(r"<","_LT",fieldNameFirst)
            fieldNameFirst=re.sub(r":","_",fieldNameFirst)

            tokens["fldName"] = fieldNameFirst
            
            
            
            # Split the line on the field
            splitLine = re.split(pattDict["Field"],thisLine)
            assert len(splitLine) == 2
            # Left side is the new line to process
            thisLine = splitLine[0]  
            # Right side is the field text
            tokens["fldText"] = splitLine[1].strip()
            
        # Check for object(s)
        if re.search(pattDict["Object"], thisLine):
            if re.search(pattDict["splitSemi"], thisLine):
                # This signals the end of an object
                tokens["flgEnd"] = True
                
            # Found at least one object
            # Split the line on the seperators
            splitLine = re.split(r"[,;]", thisLine)
            if type(splitLine) is  not list: 
            #instance(splitLine, str):
                splitLine = [splitLine]
            
            
            attribs = list()
            attribs = attribs + [attrib for attrib in splitLine if re.search("\S+",attrib)]
            if attribs:
                tokens["attribs"] = [attrib.strip() for attrib in attribs]

            
        return tokens
    
    def parseIDFtoXML2(self):
        """Currently used for IDD object, but could be used for IDF??
        """
        currentXML = myRootNode()
        
        pattDict = {
                    "Comment line"          : re.compile(r"^!",re.VERBOSE),
                    "Blank"                 : re.compile(r"^\s*$",re.VERBOSE),
                    "EmptyGroup"            : re.compile(r"^\s* [\S \s]+ ;$",re.VERBOSE),
#                    "Start Object"          : re.compile(r"[,;]$",re.VERBOSE),
#                    "Inside Object"         : re.compile(r",",re.VERBOSE),                    
#                    "End Object"            : re.compile(r";",re.VERBOSE),
#                    "Field"                 : re.compile(r"\\ \S+",re.VERBOSE),
#                    
                    }
        
        lines = list()
        for line in self.IDDstring.split('\n'):
            lines.append(line)   
        
        lineIndex = 0 
        
        flgObject = False
        
        
        while (lineIndex < len(lines)) :
            thisLine = lines[lineIndex]
            #print thisLine
            
            # Skip
            if re.search(pattDict["Comment line"], thisLine):
                pass
            # Skip
            elif re.search(pattDict["Blank"], thisLine):
                pass
            elif re.search(pattDict["EmptyGroup"], thisLine):
                pass
                        
            else:
                tokens = self.tokenize(thisLine)
                if "attribs" in tokens:
                    if (flgObject==False):
                        #print "Start",
                        flgObject = True
                        thisObjectXML = etree.SubElement(currentXML, "OBJECT")
                        
                        for attrib in tokens["attribs"]:
                            tokens["attribs"].remove(attrib)
                            thisATTRXML = etree.SubElement(thisObjectXML, "CLASS")
                            thisATTRXML.text = attrib
                            
                    if (flgObject==True):
                        for attrib in tokens["attribs"]:
                            tokens["attribs"].remove(attrib)
                            thisATTRXML = etree.SubElement(thisObjectXML, "ATTR")
                            thisATTRXML.text = attrib
                            
                if "fldName" in tokens and flgObject:
                    #print tokens["fldName"],
                    #thisATTRXML[tokens["fldName"]] = tokens["fldText"]
                    if thisATTRXML.get(tokens["fldName"]):
                        oldText = thisATTRXML.get(tokens["fldName"])
                        newText = oldText +" " + tokens["fldText"]
                        thisATTRXML.set(tokens["fldName"], newText)
                    else:
                        try:
                            thisATTRXML.set(tokens["fldName"], tokens["fldText"])
                        except:
                            print tokens
                            raise
                    
                if "flgEnd" in tokens:
                    flgObject = False
                    #print "End",                    
                    
                if "fldName" in tokens and not flgObject:                    
                    try:
                        thisATTRXML.set(tokens["fldName"], tokens["fldText"])
                    except:
                        pass
                    

                #print "{:50} {:30}".format(tokens, thisLine)
                
                
                
                
            lineIndex += 1
        
        #print currentXML.text
        
        self.XML = currentXML

        logging.debug(idStr(
            'Converted IDD to XML:{} {}, {} objects'.format( 
                                                       type(self.XML),
                                                       self.XML,
                                                       self.numObjects,
                                                       ),self.ID))    
    def parseIDFtoXML(self):
        
        #=======================================================================
        # This is the updated version, with the capability to handle OSM files!
        #=======================================================================
        
        
        
         # create a local copy
        lines = []
        
        for line in self.IDDstring.split('\n'):
            lines.append(line)

        currentXML = myRootNode()
        lineIndex = 0
        #zoneNameIndex = 0
        
        #print len(lines)
        
        flagStart = False
        flagEnd = False
        
        
        # Loop over each line
        while (lineIndex < len(lines)) :
            
            thisLine = lines[lineIndex]
            
            # Strip the comment
            comment = "No comment"
            # ANOTHER HACK! Just blanking a full comment line, handled later in scipt!
            if re.search(r"^!", thisLine,re.VERBOSE):
                #print "SKIP"
                thisLine = ""     
            elif re.search(r"!", thisLine,re.VERBOSE):
                # Update to only split ONCE
                try: 
                    values,comment = re.split(r"!", thisLine,re.VERBOSE, 1)
                except:
                    print re.split(r"!", thisLine,re.VERBOSE)
                    raise Exception("Maybe a line with 2 ! ? Try to catch these before")
                comment = comment.rstrip()
                comment = comment.lstrip()                
                #print values
                thisLine = values
            # And strip any white space
            thisLine = thisLine.rstrip()
            thisLine = thisLine.lstrip()

            
            #print thisLine
            
            # If it has no , or ;, completely skip the line
            # Otherwise do this:
            if re.search(r"[,;]", thisLine,re.VERBOSE):
                
                #print "2"
                #print thisLine
                
                # This is a HACK
                appendThis = ""
                if re.search(r";", thisLine,re.VERBOSE):
                    appendThis = ";"
                
                items = re.split(r"[,;]", thisLine,re.VERBOSE)
                
                #print items
                # re.split annoyingly returns an extra entry at the end 
                # REMOVE IT
                items = items[0:-1]
                #print items
                
                # More HACK
                items[-1] = items[-1] + appendThis
                #print items
                
                for item in items:
                    item.rstrip()
                    item.lstrip()
                    
                    if not item and not flagStart:
                        #print ""
                        raise "Blank - Should NEVER see thsi!"

                    # Found a ;, END
                    # Create an ATTR
                    elif re.search(r";", item,re.VERBOSE) and flagStart: 
                        flagStart = False
                        #print "END", item
                        item = item.replace(r";","")
                        thisAttrXML = etree.SubElement(thisObjectXML, "ATTR")
                        thisAttrXML.text = item
                        thisAttrXML.set("Comment", comment)
                        
                    
                    # Found a START
                    # Create a CLASS
                    elif not flagStart:
                        flagStart = True
                        #print "START", item
    
                        # Start an Object
                        thisObjectXML = etree.SubElement(currentXML, "OBJECT")
                        # An object always has a Class
                        thisClassXML = etree.SubElement(thisObjectXML, "CLASS")
                        thisClassXML.text = item
                    
                    # Found a INSIDE
                    # Create an ATTR         
                    elif flagStart: 
                        #print "INSIDE", item
                        thisAttrXML = etree.SubElement(thisObjectXML, "ATTR")
                        thisAttrXML.text = item
                        thisAttrXML.set("Comment", comment)
                        
    
                 
            lineIndex += 1
            # END WHILE 
        # END IF
        
        # The XML is saved
        self.XML = currentXML

        logging.debug(idStr(
            'Converted IDF to XML:{} {}, {} objects'.format( 
                                                       type(self.XML),
                                                       self.XML,
                                                       self.numObjects,
                                                       ),self.ID))
    #--- Write data
    def writeIdf(self, pathIdfOutput):
        
        # Ensure conversion to XML
        self.convertXMLtoIDF()
        
        self.pathIdfOutput = pathIdfOutput
        
        #XMLstring = (etree.tostring(self.XML, pretty_print=True))
        
        
        #if not os.path.exists(pathIdfOutput):
        #    os.makedirs(pathIdfOutput)

        fOut = open(self.pathIdfOutput, 'w')
        
        fOut.write(self.IDDstring)
        
        fOut.close()

        logging.debug(idStr(
            'Wrote IDF {}, {} objects'.format(pathIdfOutput,self.numObjects, self.numLines),
            self.ID))
        
    def writeXml(self,pathXmlOutput):

        self.pathXmlOutput = pathXmlOutput

        fOut = open(self.pathXmlOutput, 'w')

        resultXML = (etree.tostring(self.XML, pretty_print=True))

        fOut.write(resultXML)
        fOut.close
        
        #pathIdfOutput
        
        logging.debug(idStr(
            'Wrote XML {0}'.format(self.pathXmlOutput),
            self.ID))
    
    
    
    
    #--- Utility
    def __add__(self,other):
        return merge(self, other)
    


#===============================================================================
# Unit testing
#===============================================================================

@unittest.skip("")
class IDDTests(unittest.TestCase):
    
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        currentPath = split_up_path(__file__)
        projectRootPath = currentPath[:-4]
        sampleFileDir = ["SampleIDFs"]
        sampleFile1 = ["Energy+.iddSAMPLE"]  
        pathIDDsample1 = projectRootPath + sampleFileDir + sampleFile1
        self.pathIDDsample  = os.path.join(*pathIDDsample1)
        
        sampleFile2 = ["Energy+.idd"]  
        pathIDDsample2 = projectRootPath + sampleFileDir + sampleFile2
        self.pathIDDfull = os.path.join(*pathIDDsample2)
        
    @unittest.skip("")
    def test010_IDDSample(self):
        print "**** TEST {} ****".format(whoami())
        testIDD = IDF.fromIDDFile(self.pathIDDsample)
        printXML(testIDD.XML)
        
    def test020_IDD_FULL(self):
        print "**** TEST {} ****".format(whoami())

        testIDD = IDF.fromIDDFile(self.pathIDDfull)

        testIDD.writeXml(r"c:\\temp\\test.xml")
        
        for item in treeGetClass(testIDD.XML,"Vers",False):
            printXML(item)


@unittest.skip("")
class IDFtests(unittest.TestCase):
    
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        currentPath = split_up_path(__file__)

        thisProjRoot = split_up_path(os.getcwd())[:4] 
        thisTestExcelProj = "\\".join(thisProjRoot) + r"\ExcelTemplates\Input Data Tower SO03 r06.xlsx"
        self.thisTestExcelProj = thisTestExcelProj
        #projectFile = r"C:\Eclipse\PyIDF\ExcelTemplates\Input Data Tower SO03 r06.xlsx"
        projectRootPath = currentPath[:-4]
        sampleFileDir = ["SampleIDFs"]
        sampleFile1 = ["5ZoneFPIU.idf"]  
        sampleFile2 = ["r00 MainIDF.idf"]
        path_5Zone = projectRootPath + sampleFileDir + sampleFile1
        self.path_5Zone  = os.path.join(*path_5Zone)
        path_CentralTower = projectRootPath + sampleFileDir + sampleFile2
        self.path_CentralTower = os.path.join(*path_CentralTower)



        
    def test010_SimpleCreation(self):
        print "**** TEST {} ****".format(whoami())
        
        testIDF = IDF.fromIdfFile(self.path_5Zone)
        #print testIDF
        #print listZones(testIDF)
        #countAllClasses(testIDF, printFlag = 1)
        
        objTable = getAllObjectsTable(testIDF)
        #printStdTable(objTable)
        cntTable = getObjectCountTable(testIDF)
        print testIDF.numObjects
        newIDF = testIDF + testIDF

        #print testIDF.numObjects
        #print newIDF.numObjects
        #print testIDF.numObjects
        
        #assert(newIDF.numObjects == testIDF.numObjects)
        #printStdTable(cntTable)
        

    #@unittest.skip("")
    def test020_checkTemplates(self):
        print "**** TEST {} ****".format(whoami())

        templates = loadTemplates(IDF_TEMPLATE_PATH)
        
        testIDF = IDF.fromIdfFile(self.path_5Zone)
        with loggerCritical():
            for template in templates:
                testIDF = testIDF + template

        print "{} templates passed addition test".format(len(templates))

        #pp = pprint.PrettyPrinter(indent=4)
        #lastTemplate = templates.pop()
        #print lastTemplate
        #print pp.pprint(lastTemplate.templateDef)
        
    def test030_getVariants(self):
        #weatherFilePath = FREELANCE_DIR + r"\WEA\ARE_Abu.Dhabi.412170_IWEC.epw"
        #outputDirPath = FREELANCE_DIR + r"\Simulation"    
        #groupName = "00myGroup"
        #===========================================================================
        # Assemble!
        #===========================================================================
        #idfAssembly(projectFile,weatherFilePath,outputDirPath,groupName)
        variants = loadVariants(self.thisTestExcelProj)
        
    def test040_cleanObjects(self):
        print "**** TEST {} ****".format(whoami())
        myIDF = IDF.fromIdfFile(self.path_CentralTower)
        #printStdTable(getObjectCountTable(myIDF))
        
        #zoneObjs = treeGetClass(myIDF.XML, "Zone")
        #print idfGetZoneNameList(myIDF)
        #printStdTable(getObjectCountTable(myIDF))
        #print keptClassesDict['onlyGeometry']
        #print myIDF.numObjects
        cleanOutObject(myIDF, keptClassesDict['onlyGeometry'])
        #print myIDF.numObjects
        assert(myIDF.numObjects == 224)
        #printStdTable(getObjectCountTable(myIDF))


        
    def test050_applyTemplates(self):
        print "**** TEST {} ****".format(whoami())
        variants = loadVariants(self.thisTestExcelProj)
        
        # Customize for test
        myVariant = variants.itervalues().next()
        #pPrint(myVariant)
        myVariant["source"] = self.path_CentralTower
        myVariant["templates"] = [{'templateName': u'Generic lights', 'zones': u'.'}]
        myVariants = [myVariant]
        
        #assembleVariants(myVariants)
        
        
        #print myVariant
            
        #finalIDF = applyTemplates(testIDF, templates)
        
        #print finalIDF

        

    def test0X0_XXX(self):
        print "**** TEST {} ****".format(whoami())

@unittest.skip("")
class TemplateTtests(unittest.TestCase):
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        #currentPath = split_up_path(__file__)
        thisProjRoot = split_up_path(os.getcwd())[:4] 
        
        
        # Path to XLS definition 
        thisTestExcelProj = "\\".join(thisProjRoot) + r"\ExcelTemplates\Input Data Tower SO03 r06.xlsx"
        self.thisTestExcelProj = thisTestExcelProj
        
        # Path to full IDD
        pathIDDsample2 = thisProjRoot + ["SampleIDFs"] + ["Energy+.idd"]  
        self.pathIDDfull = os.path.join(*pathIDDsample2)
        
        # Path to an actual model file
        path_CentralTower = thisProjRoot + ["SampleIDFs"] + ["r00 MainIDF.idf"]
        self.path_CentralTower = os.path.join(*path_CentralTower)
        
        # Path to IDD XML
        path_IDD_XML = thisProjRoot + ["SampleIDFs"] + ["Energy+idd.xml"]
        self.path_IDD_XML = os.path.join(*path_IDD_XML)
        
    def test050_applyTemplates(self):
        print "**** TEST {} ****".format(whoami())
        
        IDDobj = IDF.fromXmlFile(self.path_IDD_XML)
        print IDDobj
        variants = loadVariants(self.thisTestExcelProj)

        # Customize for test
        myVariant = variants.itervalues().next() # Get one variant
        #pPrint(myVariant)#
        myVariant["source"] = self.path_CentralTower # Update source
        myVariant["templates"] = [{'templateName': u'Generic lights', 'zones': u'.'}] # Only one template
        myVariants = [myVariant]
        

        
        assembleVariants(myVariants,IDDobj)
@unittest.skip("")
class MyTest(unittest.TestCase):
    def test050_applyTemplates(self):
        print "**** TEST {} ****".format(whoami())
        testPath = r"C:\Users\Anonymous2\Desktop\TestIDF.txt"
        testPathOUT = r"C:\Users\Anonymous2\Desktop\TestIDF.xml"
        IDFobj = IDF.fromIdfFile(testPath)
        IDFobj.writeXml(testPathOUT)
        
        raise
        print IDDobj
        variants = loadVariants(self.thisTestExcelProj)

        # Customize for test
        myVariant = variants.itervalues().next() # Get one variant
        #pPrint(myVariant)#
        myVariant["source"] = self.path_CentralTower # Update source
        myVariant["templates"] = [{'templateName': u'Generic lights', 'zones': u'.'}] # Only one template
        myVariants = [myVariant]        
         

class JustForCentralDELETEORPHANS(unittest.TestCase):
    def test050_applyTemplates(self):
        print "**** TEST {} ****".format(whoami())
        osmFilePath = r"C:\Users\Anonymous2\Desktop\SKPOSM\Main r04.osm"
        osmFileOut = r"C:\Users\Anonymous2\Desktop\SKPOSM\Cleaned.osm"
        IDFobj = IDF.fromIdfFile(osmFilePath) 
        deleteOrphanedZones(IDFobj)
        IDFobj.writeIdf(osmFileOut)
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
    






    
