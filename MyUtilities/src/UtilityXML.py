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
import lxml as lxml
from utility_inspect import whoami, whosdaddy, listObject

import pprint
#===============================================================================
# Code
#===============================================================================

from lxml import etree


#- -------------

#- -------------

def loadSettingsFile(projectFilePath):
        tree = etree.parse(projectFilePath)
        root = tree.getroot()        
        
        settings = elementtree_to_dict(root)
        return settings
    
def createTextEl(root, tagName, text):
    element = etree.SubElement(root, tagName)
    #if isinstance(text, unicode):
    #    text = text.encode("utf-8")
    #text = text.encode("utf-8")
    #text = text.encode("windows-1252")
    text = unicode(text)
    try: 
            element.text = text
    except:
        print "Problem string:", text
        print "Problem string:", repr(text)
        print "Unicode?", type(text) is unicode
        raise
        


def printXML(theXMLtree):
    print(etree.tostring(theXMLtree, pretty_print=True))
    
    
def elementtree_to_dict(element):
    #print "start {} ". format(element.tag)
#    if element.getparent() is not None:
#        listDesignate = element.getparent().get("list")
#    else:
#        listDesignate = None
#    # The parent will tell the child if it should be listed
#    if listDesignate == element.tag:
#        #print element
#        flgList = True
#    else:
#        flgList = False
    node = dict()

    #print "\t tag: {:10}, text:{:10}, parent:{:30}, list designate:{:10}, flgList:{}".format(element.tag, repr(element.text), element.getparent(), listDesignate, flgList)
    
    text = getattr(element, 'text', None)
    if text is not None and len(element) == 0:
        return text

    child_nodes = {}
    for child in element: # element's children
        child_nodes.setdefault(child.tag, []).append( elementtree_to_dict(child) )

    # convert all single-element lists into non-lists
    #print "Convert {} ". format(element.tag)
    
    for key, value in child_nodes.items():
        # Unless they are designated as a list type!
        if not(element.get("list") == key):
            #print element.get("list")
            if len(value) == 1:
                child_nodes[key] = value[0] 

    node.update(child_nodes.items())
    #print "end {} ". format(element.tag)
    return node


#===============================================================================
# Unit testing
#===============================================================================

class XMLcatalog(unittest.TestCase):


    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        self.testString1 = """
<?xml version="1.0" encoding="ISO-8859-1"?>

<bookstore>
  <book>
    <title lang="en">Harry Potter</title>
    <author>J K. Rowling</author>
    <year>2005</year>
    <price>29.99</price>
  </book>
</bookstore> 
"""
        self.testString2 = """
  <OBJECT>
    <CLASS unique-object="" required-object="" min-fields="8">Building</CLASS>
    <ATTR field="Name" required-field="" retaincase="" default="NONE">A1</ATTR>
    <ATTR field="North Axis" note="degrees from true North" units="deg" type="real" default="0.0">N1</ATTR>
    <ATTR field="Terrain" note="Country=FlatOpenCountry | Suburbs=CountryTownsSuburbs | City=CityCenter | Ocean=body of water (5km) | Urban=Urban-Industrial-Forest" type="choice" key="Country Suburbs City Ocean Urban" default="Suburbs">A2</ATTR>
    <ATTR field="Loads Convergence Tolerance Value" note="Loads Convergence Tolerance Value is a fraction of load" type="real" minimum_GT="0.0" maximum=".5" default=".04">N2</ATTR>
    <ATTR field="Temperature Convergence Tolerance Value" units="deltaC" type="real" minimum_GT="0.0" maximum=".5" default=".4">N3</ATTR>
    <ATTR field="Solar Distribution" note="MinimalShadowing | FullExterior | FullInteriorAndExterior | FullExteriorWithReflections | FullInteriorAndExteriorWithReflections" type="choice" key="MinimalShadowing FullExterior FullInteriorAndExterior FullExteriorWithReflections FullInteriorAndExteriorWithReflections" default="FullExterior">A3</ATTR>
    <ATTR field="Maximum Number of Warmup Days" note="EnergyPlus will only use as many warmup days as needed to reach convergence tolerance. This field's value should NOT be set less than 25." type="integer" minimum_GT="0" default="25">N4</ATTR>
    <ATTR field="Minimum Number of Warmup Days" note="Warmup days will be set to be the value you entered when it is less than the default 6." type="integer" minimum_GT="0" default="6">N5</ATTR>
  </OBJECT>
"""
    #test1 = 
    def test010(self):
        print "**** TEST {} ****".format(whoami())
        projectFile = r"C:\EclipseWorkspace\Evolve2\Config\simple1.xml"
        
        """Simple1
        {project: {a: 1, b:2    }}
        """
        
        tree = lxml.etree.parse(self.testString1)
        tree = etree.parse(projectFile)
        root = tree.getroot()        
        
        settings = elementtree_to_dict(root)
        

@unittest.skip("")
class allTests(unittest.TestCase):
    
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
    
    def test010(self):
        print "**** TEST {} ****".format(whoami())
        projectFile = r"C:\EclipseWorkspace\Evolve2\Config\simple1.xml"
        
        """Simple1
        {project: {a: 1, b:2    }}
        """
        tree = etree.parse(projectFile)
        root = tree.getroot()        
        
        settings = elementtree_to_dict(root)
        
        

    def test020(self):
        print "**** TEST {} ****".format(whoami())
        projectFile = r"C:\EclipseWorkspace\Evolve2\Config\simple2.xml"
        
        """Simple1
        {project: {a: 1, b:2    }}
        """
        tree = etree.parse(projectFile)
        root = tree.getroot()        
        
        settings = elementtree_to_dict(root)
        

    def test030(self):
        print "**** TEST {} ****".format(whoami())
        projectFile = r"C:\EclipseWorkspace\Evolve2\Config\testProject2.xml"
        
        """Simple1
        {project: {a: 1, b:2    }}
        """
        tree = etree.parse(projectFile)
        root = tree.getroot()        
        
        settings = elementtree_to_dict(root)
        

        pprint.pprint(settings)
        for operator in settings['algorithm']['operators']:
            print operator
        for variable in settings['designspace']['variables']:
            print variable

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






"""


# Find a CLASS object with the name matching className, and return it's PARENT
xpathSearch = "//OBJECT/CLASS[re:match(text(), '{}')]/.."

# Parent : .. 
 

# Find a CLASS object with the name matching className, and return it's PARENT
# Then match all with the first attribute matchting
xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]/../ATTR[re:match(text(), '{1}')]"


xpathSearch = "".join([
    "//OBJECT/CLASS[re:match(text(), '" + className + "')]/..", # Select all class names
    "/ATTR[re:match(text(), '" + objectInstanceName + "')]/..", # Match the name
    "/ATTR/@Comment[re:match(.,'" + attributeComment+ "')]/..", # Same as above
    ])


# Find a CLASS object with the name matching className, and return it's PARENT, 
# then select all ATTR's inside this parent
xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]/../ATTR"

# Same as above, then select all Comment attributes, then select all which match the REGEX, 
# then return the PARENT of this comment attribute (an ATTR tag)
xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]/../ATTR/@Comment[re:match(.,'Nominal')]/.."

# Same as above, broken out into variables
className = 'HVACTemplate:Plant:Chiller'
attributeWithComment = 'Nominal COP'
xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]/../ATTR[@Comment='- Nominal COP {W/W}']"
xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]/../ATTR/@Comment[re:match(.,'" + attributeWithComment+ "')]/.."

# Select all CLASS nodes which text node = ^Zone$
# Go back up to the parent, the OBJECT
# Select all ATTR which are in the 2nd postion (index 1) AND which have a text node matching zoneName
xpathSearch = "//CLASS[re:match(text(), '{0}')]/../ATTR[re:match(text(), '{1}')]/..".format('^Zone$',zoneName)


# Select all class objects which have Zone in the name and return it's Parent (Object)
xpathSearch = "//CLASS[re:match(text(), '^Zone$')]/.."
zones = self.XML.xpath(xpathSearch,
            namespaces={"re": "http://exslt.org/regular-expressions"})

# Select all attributes with a comment containing ^[-]*[/s]*Name$
xpathSearch = "//OBJECT/ATTR[1]/@Comment[re:match(.,'^[-]*[/s]*Name$')]/.."
objects = self.XML.xpath(xpathSearch,
        namespaces={"re": "http://exslt.org/regular-expressions"})
#

# Then print out the class and name
for zone in zones:
     #print zone.text
     type = zone.xpath('CLASS')
     name = zone.xpath('ATTR')


# Use the .format method for string variables!
xpathSearch = "//CLASS[re:match(text(), '{0}')]/..".format(zoneClass)
multiplyObject = template.XML.xpath(xpathSearch,
   namespaces={"re": "http://exslt.org/regular-expressions"})
     
        
        

#//OBJECT                                               # Select all OBJECT 
#/CLASS[re:match(text(), 'IdealLoadsAirSystem')]        # Select all CLASS that match
# /..                                                   # Select the parent of it     
#/ATTR[1]                                               # Select the first ATTR         
        
targetRegXpathReplace = (
    "//OBJECT/CLASS[re:match(text(), 'IdealLoadsAirSystem')]/../ATTR[1]")
   
"""