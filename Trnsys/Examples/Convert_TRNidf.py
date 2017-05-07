'''
Created on Oct 31, 2011

@author: UserXP
'''

import IDF
from lxml import etree
import os
import logging.config
logging.config.fileConfig('..\\LoggingConfig\\logging.conf')

pathInputFileAbs = "..\ConvertTrnIdf\\testInput1.idf"
pathInputFileAbs = "..\ConvertTrnIdf\\testInput2.idf"

pathOutputFileAbs = "..\ConvertTrnIdf\\testOutput1.idf"
pathOutputXMLAbs = "..\ConvertTrnIdf\\testInput2.xml"

# Create a new IDF from the variant
thisIDF = IDF.IDF(
    pathIdfInput= pathInputFileAbs, 
    XML=None, 
    IDFstring = None, 
    IDstring = None, 
    description = None, 
    pathIdfOutput = pathOutputFileAbs
    )

# Call the load        
thisIDF.loadIDF()
# Call convert
thisIDF.convertIDFtoXML()
thisIDF.writeXml(pathOutputXMLAbs)

thisIDF.cleanOutObjectLeaveGeom()

thisIDF.listZonesWithName()
#thisIDF.showAllObjects()

# STEP -  Clean up the zone names #######################################################
# Find all 'Zone' objects
zoneObjects = thisIDF.xpathGetObjectByClassName("Zone")

# Change the name to have no spaces or punctuation
for zoneObject in zoneObjects:
    # Select the first ATTR node
    thisZoneAttr = zoneObject.xpath('./ATTR[1]')[0]
    # The actual zone name is
    searchVal = thisZoneAttr.text
    # We need to update all value nodes which have this string
    # First select all value nodes with this string
    updateNodes = thisIDF.XML.xpath("//ATTR[text() = \"" + searchVal + "\"]")
    # Our original name is searchVal
    # Out new filtered name is then
    filteredName = ''.join(e for e in searchVal if e.isalnum())
    # Loop over this selection
    for updateNode in updateNodes:
        # Update all nodes with the new filteredName
        updateNode.text = filteredName
        #print updateNode
        #print etree.tostring(updateNode)
    #print searchVal
    #    print thisIDF.XML.xpath("//ATTR[text() = " + searchVal + "]",
    #         namespaces={"re": "http://exslt.org/regular-expressions"})
    # Filter out anthything not alhpa numeric
    #thisZoneAttr.text = ''.join(e for e in thisZoneAttr.text if e.isalnum())

# STEP - Add two more ATTR to all CLASS = Zone ##########################################
# Find all 'Zone' objects
zoneObjects = thisIDF.xpathGetObjectByClassName("Zone")

# Change the name to have no spaces or punctuation
for zoneObject in zoneObjects:
    # Create a trnsys IDF 'Type' ATTR
    myElement = etree.Element("ATTR", Comment="Type")
    myElement.text = ""    
    zoneObject.append(myElement)
    # Create a trnsys IDF 'Zone Multiplier' ATTR
    myElement = etree.Element("ATTR", Comment="Multiplier")
    myElement.text = "1"    
    zoneObject.append(myElement)    
    #print zoneObject
    #print etree.tostring(zoneObject)
    #etree.tostring(
    #print etree.tostring(myTestNode)


# STEP - Change the 'autocalculate' of surfaces vertices, and ground view fac ##################################
# Find all objects
objects = thisIDF.xpathGetObjectByClassName("BuildingSurface:Detailed")
# A surface has this many fixed ATTR, and 3*n vertex ATTR
fixedAttrs = 10 
nodeLocationVertexCount = 10
nodeLocationViewFacGround = 9  

# Change the name to have no spaces or punctuation
for object in objects:
    #print etree.tostring(object)
    # Get all ATTR, count them
    attrCount = len(object.xpath('./ATTR'))
    #for thisAttr in object.xpath('./ATTR'):
    #    print thisAttr.text,
    vertexAttrs = attrCount - fixedAttrs
    #print vertexAttrs
    vertexCount = vertexAttrs/3.
    #print "vert count:", vertexCount
    #print "vert count % 3:", vertexAttrs%3
    #print "12% 3:", 12%3
    if not vertexAttrs%3. == 0:
        raise Exception
    #print int(vertexCount)
    autoCalcNode = object.xpath('./ATTR[' + str(nodeLocationVertexCount) + ']')[0]
    autoCalcNode.text = str(int(vertexCount))
    
    # Also delete the "autocalculate" for view factor to ground
    autoCalcNode = object.xpath('./ATTR[' + str(nodeLocationViewFacGround) + ']')[0]
    autoCalcNode.text = ""
    #print etree.tostring(object)
    
# STEP - Same as above, for Windows ##################################
# Find all objects
objects = thisIDF.xpathGetObjectByClassName("FenestrationSurface:Detailed")
# A surface has this many fixed ATTR, and 3*n vertex ATTR
fixedAttrs = 10 
nodeLocationVertexCount = 10
nodeLocationViewFacGround = 6

# Change the name to have no spaces or punctuation
for object in objects:
    #print etree.tostring(object)
    # Get all ATTR, count them
    attrCount = len(object.xpath('./ATTR'))
    #for thisAttr in object.xpath('./ATTR'):
    #    print thisAttr.text,
    vertexAttrs = attrCount - fixedAttrs
    #print vertexAttrs
    vertexCount = vertexAttrs/3.
    #print "vert count:", vertexCount
    #print "vert count % 3:", vertexAttrs%3
    #print "12% 3:", 12%3
    if not vertexAttrs%3. == 0:
        raise Exception
    #print int(vertexCount)
    autoCalcNode = object.xpath('./ATTR[' + str(nodeLocationVertexCount) + ']')[0]
    autoCalcNode.text = str(int(vertexCount))
    
    # Also delete the "autocalculate" for view factor to ground
    autoCalcNode = object.xpath('./ATTR[' + str(nodeLocationViewFacGround) + ']')[0]
    autoCalcNode.text = ""
    #print etree.tostring(object)
 
    
# STEP - Same as above, for Shading ##################################
# Find all objects
objects = thisIDF.xpathGetObjectByClassName("Shading:Building:Detailed")
# A surface has this many fixed ATTR, and 3*n vertex ATTR
fixedAttrs = 3 
nodeLocationVertexCount = 3

# Change the name to have no spaces or punctuation
for object in objects:
    #print etree.tostring(object)
    # Get all ATTR, count them
    attrCount = len(object.xpath('./ATTR'))
    #for thisAttr in object.xpath('./ATTR'):
    #    print thisAttr.text,
    vertexAttrs = attrCount - fixedAttrs
    #print vertexAttrs
    vertexCount = vertexAttrs/3.
    #print "vert count:", vertexCount
    #print "vert count % 3:", vertexAttrs%3
    #print "12% 3:", 12%3
    if not vertexAttrs%3. == 0:
        raise Exception
    #print int(vertexCount)
    autoCalcNode = object.xpath('./ATTR[' + str(nodeLocationVertexCount) + ']')[0]
    autoCalcNode.text = str(int(vertexCount))

# STEP - Change Boundary condition for floors ##################################
## Find all objects
#objects = thisIDF.xpathGetObjectByClassName("BuildingSurface:Detailed")
## A surface has this many fixed ATTR, and 3*n vertex ATTR
#fixedAttrs = 10 
#nodeLocationVertexCount = 10
#nodeLocationViewFacGround = 9  
#
## Change the name to have no spaces or punctuation
#for object in objects:
#    #print etree.tostring(object)
#    # Get all ATTR, count them
#    attrCount = len(object.xpath('./ATTR'))
#    #for thisAttr in object.xpath('./ATTR'):
#    #    print thisAttr.text,
#    vertexAttrs = attrCount - fixedAttrs
#    #print vertexAttrs
#    vertexCount = vertexAttrs/3.
#    #print "vert count:", vertexCount
#    #print "vert count % 3:", vertexAttrs%3
#    #print "12% 3:", 12%3
#    if not vertexAttrs%3. == 0:
#        raise Exception
#    #print int(vertexCount)
#    autoCalcNode = object.xpath('./ATTR[' + str(nodeLocationVertexCount) + ']')[0]
#    autoCalcNode.text = str(int(vertexCount))
#    
#    # Also delete the "autocalculate" for view factor to ground
#    autoCalcNode = object.xpath('./ATTR[' + str(nodeLocationViewFacGround) + ']')[0]
#    autoCalcNode.text = ""
#    #print etree.tostring(object)

# STEP - Change Boundary conditions for surfaces ##################################
# Select all BuildingSurface:Detailed objects with the word 'Surface' at the 5 ATTR position
xpathSearch =  "//CLASS[.=\"BuildingSurface:Detailed\"]/../ATTR[5][.=\"Surface\"]/.."
surfsWithSurfaceMatch = thisIDF.XML.xpath(xpathSearch)
for object in surfsWithSurfaceMatch:
    # Get the name of the target surface
    targetSurfaceName = object.xpath("./ATTR[6]")[0].text
    # Select all Surface objects that match this surface name, and sub select their Zone attribute (4)
    xpathSearch =  "//CLASS[.=\"BuildingSurface:Detailed\"]/../ATTR[1]" \
        "[.=\"" + targetSurfaceName + "\"]/../ATTR[4]"
    targetSurfObjectsZoneAttr = thisIDF.XML.xpath(xpathSearch)[0]
    # Change the targeting surfaces target object to this zone
    object.xpath("./ATTR[6]")[0].text = targetSurfObjectsZoneAttr.text
    # We have found a surface boundary, need to update it to a zone boundary condition
    object.xpath("./ATTR[5]")[0].text = "Zone"

###input()
##
### First, get all surface objects
##surfaceObjects = thisIDF.xpathGetObjectByClassName("BuildingSurface:Detailed")
### Loop over the surfaces
##for surface in surfaceObjects:
##    # Now sub-select all the attributes at the 5th position
##    xpathSearch =  "./ATTR[position()=5]"
##    #print xpathSearch
##    outsideBoundaryCondition = surface.xpath(xpathSearch)[0]
##    if outsideBoundaryCondition.text == "Surface":
##        # We have found a surface boundary, need to update it to a zone bounday
##        #print outsideBoundaryCondition.text
##        outsideBoundaryCondition.text = "Zone"
##        #print outsideBoundaryCondition.text
##        # Now select the surrounding surface again, then go back inside to the 6th position
##        outsideBoundaryTarget = outsideBoundaryCondition.xpath("./../ATTR[position()=6]")[0]
##        #print outsideBoundaryTarget.text
##        # Search root for this target surface name
##        
##
##    #print outsideBoundaryCondition.text
##    #author[last-name [position()=1]= "Bob"] 
##    # text() = \"Surface\"]"'


thisIDF.convertXMLtoIDF()
thisIDF.writeIdf(thisIDF.pathIdfOutput)
