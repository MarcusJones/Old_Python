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
from utility_path import split_up_path
from Utilities import idStr

import lxml
#from lxml import etree

from IDF import IDF
from IDF import printXML,xmlTextReplace
from IDF import treeGetClass, xpathRE,cleanOutObject,keptClassesDict
from IDF import idfGetZoneNameList,applyTemplate
#loadTemplates

from copy import deepcopy
#xmlTextReplace, 


from UtilityLogger import loggerCritical

import re


#===============================================================================
# Code
#===============================================================================

#--- ADD


def processZoneHVAC(IDFobj, zoneName):
    # Get the matching zone definition for this zone
    zoneHVACdef = getZoneHVACdef(IDFobj, zoneName)
    
    if not zoneHVACdef["outlet"]:
        className = "ZoneHVAC:EquipmentConnections"
        position = 1
        xpathSearch = r"OBJECT/CLASS[text() = '{}']/../ATTR[{}][text()='{}']/..".format(className,position,zoneName)
        zoneHvacs =  xpathRE(IDFobj.XML, xpathSearch)
        #printXML()
        theZHVAC = zoneHvacs[0]
    

        xpathSearch = "ATTR[4]".format(zoneName,)
        thisAttr = theZHVAC.xpath(xpathSearch)[0]
        #formerNode = thisAttr.text 
        thisAttr.text = zoneName + "Exhaust"
        
    #raise
    
    return zoneHVACdef
    
     

def addOneVRVterminal(IDDobj, IDFobj, zoneName):
    # Get template
    with loggerCritical():
        thisProjRoot = split_up_path(os.getcwd())[:4]
        path_VRV_terminal_template = thisProjRoot + ["VRV Templates"] + ["VRV Terminal.idf"]
        path_VRV_terminal_template = os.path.join(*path_VRV_terminal_template)
        VRV_terminal_template=IDF.fromIdfFile(path_VRV_terminal_template,)
        #VRV_terminal_template.getTemplateInfo()

    # Update the terminal object to be unique
    objects = [obj for obj in VRV_terminal_template.XML.xpath("./OBJECT")]
    # Get template
    with loggerCritical():
        xmlTextReplace(objects, r"*ZONENAME*",zoneName)
    
    zoneHVACdef = processZoneHVAC(IDFobj, zoneName)
    
    # Check if the inlets is a NODE LIST!
    xpathSearch = "./OBJECT/CLASS[text()='NodeList']/../ATTR[1][text() = '{}']".format(zoneHVACdef['inlet'],)
    thisZL = IDFobj.XML.xpath(xpathSearch)
    zoneInletName = "{} VRV inlet".format(zoneName)
    zoneOutletName = "{} VRV outlet".format(zoneName)
    
    if thisZL:
        assert(len(thisZL) == 1)
        thisZL = thisZL[0]
        #Get parent!
        thisZLobj = thisZL.xpath("..")[0]
        appendElem(thisZLobj, "ATTR", zoneInletName)
    else: 
        raise "This should be a NODE LIST"
        zoneInletName = zoneHVACdef['inlet']
    
    # Check if the exhaust is also a node list! 
    xpathSearch = "./OBJECT/CLASS[text()='NodeList']/../ATTR[1][text() = '{}']".format(zoneHVACdef['outlet'],)
    thisNL = IDFobj.XML.xpath(xpathSearch)
    if thisNL:
        # Create a new node name in the NL
        thisNL = thisNL[0]
    else:
        # Create a new NL, add the old node to it
        #from random import choice
        #from Utilities import  genID
        
        #randomStr = ''.join([choice(chars) for i in range(length)])
        #NLname = "{} Exhaust NL {}".format(zoneName, genID(length=4))
        
        NLname = "{} Exhaust NL".format(zoneName)
        thisPath = thisProjRoot + ["VRV Templates"] + ["NodeList.idf"]
        thisPath = os.path.join(*thisPath)
        with loggerCritical():
            template=IDF.fromIdfFile(thisPath)
        # HACK
        thisNLobj = template.XML.xpath("OBJECT")[0]
        thisNLobj.remove(thisNLobj.xpath("ATTR")[0])
        appendElem(thisNLobj, "ATTR", NLname)
        appendElem(thisNLobj, "ATTR", zoneOutletName)
        
        #print thisNLobj
        #printXML(thisNLobj)        
        #raise 
        #print thisNLobj
        #printXML(thisNLobj)
          #<ATTR>8NPCafe:OpenPlanOffice VRV outlet</ATTR>
          #<ATTR>8NPCafe:OpenPlanOffice1 VRV outlet</ATTR>
        # Update the ZHVAC object to point to the new NL
        xpathSearch = "./OBJECT/CLASS[text()='ZoneHVAC:EquipmentConnections']/../ATTR[1][text() = '{}']/..".format(zoneName,)
        theZHVAC = IDFobj.XML.xpath(xpathSearch)[0]
        xpathSearch = "ATTR[4]".format(zoneName,)
        thisAttr = theZHVAC.xpath(xpathSearch)[0]
        formerNode = thisAttr.text 
        thisAttr.text = NLname
        
        # Finally, add the former node name to the new list to keep links
        appendElem(thisNLobj, "ATTR", formerNode)
        if formerNode:
            printXML(thisNLobj)
            # Add the NL
            IDFobj.XML.append(thisNLobj)
        

    zoneHVACdef = getZoneHVACdef(IDFobj, zoneName)

    #===========================================================================
    # Connect nodes
    #===========================================================================
    # Connect the TerminalUnit
    theTerminalObj = VRV_terminal_template.XML.xpath("./OBJECT/CLASS[text()='ZoneHVAC:TerminalUnit:VariableRefrigerantFlow']/..")
    # The terminal inlet is the zone outlet
    xmlModifyAttrAtIDDdef(IDDobj, theTerminalObj, 
                          "field", "Terminal Unit Air Inlet Node Name", 
                          zoneOutletName)
    
    # The terminal outlet is the zone inlet
    xmlModifyAttrAtIDDdef(IDDobj, theTerminalObj, 
                          "field", "Terminal Unit Air Outlet Node Name", 
                          zoneInletName)
    

    # Connect the Fan
    # The fan outlet is the zone inlet
    theFanObj = VRV_terminal_template.XML.xpath("./OBJECT/CLASS[text()='Fan:ConstantVolume']/..")
    xmlModifyAttrAtIDDdef(IDDobj, theFanObj, 
                          "field", "Air Outlet Node Name", 
                          zoneInletName)
    
    # Connect the coil 
    # The coil inlet should is the zone outlet
    theCCoilObj = VRV_terminal_template.XML.xpath("./OBJECT/CLASS[text()='Coil:Cooling:DX:VariableRefrigerantFlow']/..")
    xmlModifyAttrAtIDDdef(IDDobj, theCCoilObj, 
                          "field", "Coil Air Inlet Node", 
                          zoneOutletName)   
    
    
    #===========================================================================
    # Add to equipmentList
    #===========================================================================
    equipListObj =getEquiplist(IDFobj, zoneHVACdef["equipListName"]) 
    #print equipListObj.xpath("ATTR")
    
    terminalName = theTerminalObj[0].xpath("ATTR[1]")[0].text
    
    #attr = etree.SubElement(equipListObj, #)
    
    numChildren = len(equipListObj)
    numEquipments, remaindar =  divmod((numChildren - 2), 4)
    assert remaindar == 0
    
    appendElem(equipListObj, "ATTR", "ZoneHVAC:TerminalUnit:VariableRefrigerantFlow")
    appendElem(equipListObj, "ATTR", terminalName)
    appendElem(equipListObj, "ATTR", str(numEquipments + 1))
    appendElem(equipListObj, "ATTR", str(numEquipments + 1))    
    
    #===========================================================================
    # Add to IDF
    #===========================================================================
    [IDFobj.XML.append(obj) for obj in VRV_terminal_template.XML.xpath("./OBJECT")]
    logging.debug(idStr("Added terminal {} to zone {}".format(terminalName,zoneName),IDFobj.ID))
    
    return terminalName

def add_curves_scheds(IDDobj,IDFobj):
    # Get template
    logging.debug(idStr("Adding curves".format(),IDFobj.ID))

    thisProjRoot = split_up_path(os.getcwd())[:4]
    with loggerCritical():
        treeGetClass(IDDobj.XML, "Curve:Biquadratic", flgExact = True)
    
    #raise
    thisPath = thisProjRoot + ["VRV Templates"] + ["VRV_curves.idf"]
    thisPath = os.path.join(*thisPath)
    with loggerCritical():
        template=IDF.fromIdfFile(thisPath,)
    applyTemplate(IDFobj,IDDobj,template)
    
    thisPath = thisProjRoot + ["VRV Templates"] + ["VRV_availSched.idf"]
    thisPath = os.path.join(*thisPath)
    with loggerCritical():
        template=IDF.fromIdfFile(thisPath)
    applyTemplate(IDFobj,IDDobj,template)
   
    logging.debug(idStr("Added curves".format(),IDFobj.ID))
    
def add_head(IDDobj, IDFobj, name, masterZoneName):
    # Applies the head template
    # Updates head name, and master zone name
    # Returns the ZoneTerminalUnitList
    
    logging.debug(idStr("Adding VRV head {} with master zone {}".format(name,masterZoneName),IDFobj.ID))
    
    with loggerCritical():
        thisProjRoot = split_up_path(os.getcwd())[:4]
        path_VRV_head_template = thisProjRoot + ["VRV Templates"] + ["VRV_head.idf"]
        path_VRV_head_template = os.path.join(*path_VRV_head_template)
        VRV_head_template=IDF.fromIdfFile(path_VRV_head_template,)
    #VRV_head_template.getTemplateInfo()
    
    
 
    
    objects = VRV_head_template.XML.xpath("OBJECT")
    #print objects
    

#printXML(VRV_head_template.XML)        

    
    xmlModifyAttrAtIDDdef(IDDobj, objects, "field", "Heat Pump Name",name)
    xmlModifyAttrAtIDDdef(IDDobj, objects, "field", "Zone Name for Master Thermostat Location",masterZoneName)
    #(IDDobj, objects, label, value, updateVal)

    xmlTextReplace(objects, r"*TERMINAL UNIT AA*",name)
    
    #for obj in objects:
    #    printXML(obj)
    
    with loggerCritical():
        terminalUnitList = treeGetClass(VRV_head_template.XML,"ZoneTerminalUnitList")
    
    
    
    [IDFobj.XML.append(obj) for obj in VRV_head_template.XML.xpath("./OBJECT")]
    
    logging.debug(idStr("Added terminal head {}, master zone is {}".format(name,masterZoneName),IDFobj.ID))
    
   
    return terminalUnitList

def addTerminals(IDDobj, IDFobj, zoneNameRegex = "."):
    # Get the zone list
    thisZoneList = idfGetZoneNameList(IDFobj,zoneNameRegex)
    logging.debug(idStr("Adding VRV system into {} zones matching {}".format(len(thisZoneList),zoneNameRegex),IDFobj.ID))
    logging.debug(idStr("Zones: {}".format(thisZoneList),IDFobj.ID))

    # Create a head
    # Get number of existing condenser units:
    with loggerCritical():
        if treeGetClass(IDFobj.XML, "AirConditioner:VariableRefrigerantFlow"):
            num = len(treeGetClass(IDFobj.XML, "AirConditioner:VariableRefrigerantFlow"))
        else:
            num = 0
    
    # The first zone will contain the master thermostat
    theFirstMatchedZone = thisZoneList[0]
    
    terminalUnitList = add_head(IDDobj,IDFobj,"VRF Condenser {}".format(num+1),theFirstMatchedZone)

    logging.debug(idStr("Added a head, got it's terminal list {}".format(terminalUnitList),IDFobj.ID))
    
    assert len(terminalUnitList) == 1
    terminalUnitList = terminalUnitList[0]
    
    # For each zone, add a terminal
    for zoneName in thisZoneList:
        terminalUnitName = addOneVRVterminal(IDDobj,IDFobj, zoneName)
        appendElem(terminalUnitList, "ATTR", terminalUnitName)

    logging.debug(idStr("Added terminal objects into {}, len = {}".format(IDFobj.ID, IDFobj.numObjects),IDFobj.ID))

#--- XML Utils
def appendElem(tree, name, text):
    tree.append(createElem(name,text))

def createElem(name, text):
    elem = lxml.etree.Element(name)
    elem.text = text
    return elem

def XMLsearchResult(obj,xpath):
    res = obj.xpath(xpath)
    print "'{}' = {}".format(xpath, res)
    
def xmlBreakdown(obj):
    print "*****************BREAKDOWN"
    
    print "obj = {}".format(obj)
    print "Full object:"
    printXML(obj)

    XMLsearchResult(obj, "OBJECT")

    XMLsearchResult(obj, "/OBJECT")
    
    XMLsearchResult(obj, "//OBJECT")
    
    XMLsearchResult(obj, ".")
    
    XMLsearchResult(obj, "..")
    
    XMLsearchResult(obj, "../OBJECT")
    
    XMLsearchResult(obj, "ATTR")
    
    XMLsearchResult(obj, "./ATTR")
    
    XMLsearchResult(obj, "./ATTR[1]")
    print "*****************BREAKDOWN"
    
    
def xmlModifyAttrAtPosition(objects):
    raise
    """objects is a list of etree._Element node references. 
    Node are always a reference!
    """
    
    assert isinstance(objects, list)
    #print type(objects[0])
    assert isinstance(objects[0],lxml.etree._Element)
    
    #xmlBreakdown(objects[0])
    #assert 
    
def xmlModifyAttrAtIDDdef(IDDobj, objects, label, value, updateVal):
    """objects is a list of etree._Element node references. 
    Node are always a reference!
    """
    
    assert isinstance(objects, list)
    #print type(objects[0])
    assert isinstance(objects[0],lxml.etree._Element)
    
    #xmlBreakdown(objects[0])
    flgFound = False
    for obj in objects:
        # Get name of this object
        objName = obj.xpath("CLASS/text()")[0]
        
        # Get the IDD class
        with loggerCritical():
            IDDclass = treeGetClass(IDDobj.XML,objName)[0]
        
        #printXML(IDDclass)
        
        matches = IDDclass.xpath("./ATTR[@{}='{}']".format(label,value))
        if matches:
            assert len(matches) == 1, "Found {}".format(matches)
            flgFound = True
            position = IDDclass.xpath("count(./ATTR[@{}='{}']/preceding-sibling::*)".format(label,value))
            
            targetAttr = obj.xpath("./ATTR[{}]".format(position))[0]
            
            targetAttr.text = updateVal
        
    assert flgFound

#--- HVAC definition modifications
def clearEquipList(IDFobj, equipList,):
    equipList = getEquiplist(IDFobj, equipList)
    #assert len(equipList) == 1
    #equipList = equipList[0]
    
    #print equipList
    allAttribs = equipList.xpath("ATTR")
    firstAttr = allAttribs.pop(0)
    [equipList.remove(attrib) for attrib in allAttribs]
    #printXML(equipList)
    logging.debug(idStr("Emptied equipment list".format(),IDFobj.ID)) 
    
    return equipList

def addToEquipList(equipList,objType,name):

    return equipList

def getEquiplist(IDFobj, listName):
    className = "ZoneHVAC:EquipmentList"
    position = 1
    #xpathSearch = r"OBJECT/CLASS[re:match(text(), '{}')]/../ATTR[{}]/..".format(className,0)
    #xpathSearch = r"OBJECT/CLASS[re:match(text(), '{}')]/../ATTR[{}]/..".format(className,position)
    xpathSearch = r"OBJECT/CLASS[text() = '{}']/../ATTR[{}][text()='{}']/..".format(className,position,listName)

    equipList = xpathRE(IDFobj.XML, xpathSearch)
    assert len(equipList) == 1

    return equipList[0]

def getZoneHVACdef(IDFobj, zoneName):

    className = "ZoneHVAC:EquipmentConnections"
    position = 1
    xpathSearch = r"OBJECT/CLASS[text() = '{}']/../ATTR[{}][text()='{}']/..".format(className,position,zoneName)
    zoneHvacs =  xpathRE(IDFobj.XML, xpathSearch)
    #printXML( zoneHvacs[0])
    #printXML( zoneHvacs[1])
    assert len(zoneHvacs) >= 1, "No ZoneHVAC! zoneName = {} gives {}".format(zoneName,zoneHvacs)
    assert len(zoneHvacs) == 1, "Too many matches! zoneName = {} gives {}".format(zoneName,zoneHvacs)
    zoneHvac = zoneHvacs[0]

    attribs = zoneHvac.xpath("ATTR")

    zhvacDef = dict()
    zhvacDef["name"] = attribs.pop(0).text
    zhvacDef["equipListName"] = attribs.pop(0).text
    zhvacDef["inlet"] = attribs.pop(0).text
    zhvacDef["outlet"] = attribs.pop(0).text
    zhvacDef["air"] = attribs.pop(0).text
    zhvacDef["return"] = attribs.pop(0).text

    logging.debug(idStr("ZoneHVAC Name:{}".format(zhvacDef["name"]),IDFobj.ID))
    for k,v in zhvacDef.iteritems():
        print "{:>30} - {}".format(k,v) 


    return zhvacDef

def addOneZoneHVAC(IDFobj, zoneName):
    
    thisProjRoot = split_up_path(os.getcwd())[:4]
    
    path_Template = thisProjRoot + ["VRV Templates"] + ["ZONE_HVAC.idf"]
    path_Template = os.path.join(*path_Template)
    with loggerCritical():
        template=IDF.fromIdfFile(path_Template,)
    #template.getTemplateInfo()
    
    objects = [obj for obj in template.XML.xpath("./OBJECT")]
    xmlTextReplace(objects, r"*ZONENAME*",zoneName)
        
    [IDFobj.XML.append(obj) for obj in template.XML.xpath("./OBJECT")]
    logging.debug(idStr("Added ZONEhvac to {}".format(zoneName),IDFobj.ID)) 

def addZoneHVACs(IDFobj, zoneNameRegex = "."):
    logging.debug(idStr("Adding ZONEhvac objects into {}, len = {}".format(IDFobj.ID, IDFobj.numObjects),IDFobj.ID)) 
    #for thisObject in template.XML.xpath('//CLASS'):
        #objectParent = thisObject.xpath("..")[0]
        # Inspect the DEFINITION of this thisObject
        #objectClassName =  thisObject.text
        #classDef = treeGetClass(IDDobj.XML, objectClassName)
        #assert len(classDef) == 1
        #classDef = classDef[0]    
        
    for zoneName in idfGetZoneNameList(IDFobj,zoneNameRegex):
        addOneZoneHVAC(IDFobj, zoneName)

        #thisMultiplyObject = deepcopy(objectParent)
        #xmlTextReplace(thisMultiplyObject, placeHolder,zoneName)
        #print thisMultiplyObject.XML
        #IDFobj.XML.append(thisMultiplyObject)
        #print "Added zoneHVAC"
        #objectCnt += 1
    #template = xmlTextReplace(template)
    #logging.debug(idStr("Merged {} ZONEhvac objects into {}, len = {}".format(objectCnt,IDFobj.ID, IDFobj.numObjects),IDFobj.ID)) 
    #return IDFobj    
    
    #clearEquipList(IDFobj)


#===============================================================================
# Unit testing
#===============================================================================
@unittest.skip("")
class allTests(unittest.TestCase):
    
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        
        with loggerCritical():
            #currentPath = split_up_path(__file__)
            thisProjRoot = split_up_path(os.getcwd())[:4] 
    
            # Path to test IDF
            path_VRV = thisProjRoot + ["VRV Templates"] + [r"VRV Terminal.idf"]
            self.path_VRV = os.path.join(*path_VRV)
            
            # Path to IDD XML
            path_IDD_XML = thisProjRoot + ["SampleIDFs"] + ["Energy+idd.xml"]
            self.path_IDD_XML = os.path.join(*path_IDD_XML)
    
            self.IDDobj = IDF.fromXmlFile(self.path_IDD_XML)
            
            self.IDFobj = IDF.fromIdfFile(self.path_VRV)        
            
    def test010_SimpleCreation(self):
        print "**** TEST {} ****".format(whoami())
                
        anObjectList = treeGetClass(self.IDFobj.XML,"ZoneHVAC:TerminalUnit:VariableRefrigerantFlow")
        
        anObjectList = treeGetClass(self.IDFobj.XML,"Coil",False)
        print anObjectList
        xmlBreakdown(anObjectList[0])
        
        #xmlModifyAttrAtPosition(anObjectList)
        
    def test020_SimpleCreation(self):
        print "**** TEST {} ****".format(whoami())
        
        anObjectList = treeGetClass(self.IDFobj.XML,"Coil",False)
        
        xmlModifyAttrAtIDDdef(self.IDDobj,anObjectList,"field","Name", "TESTING")
        
        for obj in anObjectList:
            printXML(obj)

class allTests2(unittest.TestCase):
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        
        with loggerCritical():
            #currentPath = split_up_path(__file__)
            thisProjRoot = split_up_path(os.getcwd())[:4] 
    
            # Path to test IDF
            # Path to a simple IDF
            sampleFileDir = ["SampleIDFs"]
            sampleFile1 = ["5ZoneElectricBaseboard.idf"]  
            path_5Zone = thisProjRoot + sampleFileDir + sampleFile1    
            path_5Zone  = os.path.join(*path_5Zone)
            
            # Path to IDD XML
            path_IDD_XML = thisProjRoot + ["SampleIDFs"] + ["Energy+idd.xml"]
            self.path_IDD_XML = os.path.join(*path_IDD_XML)
    
            self.IDDobj = IDF.fromXmlFile(self.path_IDD_XML)
            
            self.IDFobj = IDF.fromIdfFile(path_5Zone)        
            
            self.IDFobj = cleanOutObject(self.IDFobj,keptClassesDict['onlyGeometry'])
            
            
            pathDOAS = thisProjRoot + ["SampleIDFs"] + ["EXPANDED-5ZoneFanCoil-DOAS.idf"]
            pathDOAS = os.path.join(*pathDOAS)
            self.IDF_DOAS = IDF.fromIdfFile(pathDOAS)
            

    @unittest.skip("")
    def test_01_Start(self):
 
        print "**** TEST {} ****".format(whoami())
        thisOutputPath = r"c:\temp\{}.idf".format(whoami()) 
        
        IDFobj = self.IDFobj
        print IDFobj

        IDFobj.writeIdf(thisOutputPath)
        
    @unittest.skip("")
    def test_02_AddedBlankEquipLists(self):
 
        print "**** TEST {} ****".format(whoami())

        thisOutputPath = r"c:\temp\{}.idf".format(whoami()) 
        
        IDFobj = self.IDFobj
        
        addZoneHVACs(IDFobj)
        
        IDFobj.writeIdf(thisOutputPath)

    @unittest.skip("")
    def test_03_ConnectedTerminalUnits(self):
 
        print "**** TEST {} ****".format(whoami())

        thisOutputPath = r"c:\temp\{}.idf".format(whoami()) 
        
        self.IDFobj
        
        addZoneHVACs(self.IDFobj)

        addTerminals(self.IDDobj,self.IDFobj)
        add_curves_scheds(self.IDDobj,self.IDFobj)

        self.IDFobj.writeIdf(thisOutputPath)
    
    def test_04_AddVRVtoExisting(self):
 
        print "**** TEST {} ****".format(whoami())

        thisOutputPath = r"c:\temp\{}.idf".format(whoami()) 
        
        theIDF = self.IDF_DOAS
        
        zoneMatch = "SPACE"
        addTerminals(self.IDDobj,theIDF,zoneMatch)
        add_curves_scheds(self.IDDobj,theIDF)
        theIDF.writeIdf(thisOutputPath)

#===============================================================================
# Main
#===============================================================================
def test_05_VRVtoCentral():
    pathIDF = r"C:\Projects\IDFout\As Designed.idf"
    
    #thisOutputPath = r"c:\temp\{}.idf".format(whoami()) 
    #thisOutputPath = r"C:\Projects\IDFout\{}.idf".format("As Designed With VRV")
    thisOutputPath = pathIDF
    IDFobj = IDF.fromIdfFile(pathIDF)

    # Path to IDD XML
    thisProjRoot = split_up_path(os.getcwd())[:4] 
    path_IDD_XML = thisProjRoot + ["SampleIDFs"] + ["Energy+idd.xml"]
    path_IDD_XML = os.path.join(*path_IDD_XML)
    IDDobj = IDF.fromXmlFile(path_IDD_XML)
    floors = [
    "412NPWthtNP8",
    "8NPCafe",
    "20NP",
    "1319NP",
    ]
    spaces = ["Cafeteria", "OpenPlanOffice"]
    
    searches = list()
    for floor in floors:
        reStr = floor
        reStr+= ".+"
        reStr+="(" + "|".join(spaces) + ")"
        searches.append(reStr)
        #for space in spaces:
       
    print searches
        
    
    for srch in searches:
        thisZoneList = idfGetZoneNameList(IDFobj,srch)
        print 
        print 
        print thisZoneList

        addTerminals(IDDobj, IDFobj, zoneNameRegex = srch)
    
    add_curves_scheds(IDDobj,IDFobj)
    
    #import os
    os.remove(pathIDF)
    
    IDFobj.writeIdf(thisOutputPath)
        


if __name__ == "__main__":
    print ABSOLUTE_LOGGING_PATH
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())
    
    #print FREELANCE_DIR
    
    #unittest.main()
    test_05_VRVtoCentral()
    
    logging.debug("Finished _main".format())
    
