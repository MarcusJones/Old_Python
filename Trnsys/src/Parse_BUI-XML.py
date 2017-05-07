from __future__ import division    

#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""This is a Top Down parser for BUI files
Etc.
"""

#===============================================================================
# Set up
#===============================================================================
import logging.config
import UtilityInspect
from UtilityInspect import whoami, whosdaddy
import unittest
import re
from lxml import etree
from textwrap import dedent
from cStringIO import StringIO


#===============================================================================
# Code
#===============================================================================
def foundToken(tokenDictionary, inputString):
    """ Search the dictionary for the current word, return the corresponding value, or 0 
    In this case, we are looping the dictionary to use the regex, instead of direct dict access 
    using dict["key"]"""
    for k, v in tokenDictionary.items():
        if re.match(k,inputString):
            return v
        else:
            continue
    # Didn't find it
    return False
    
def splitBuiLine(line):
    return re.split('\s*=\s*|\s+', line.rstrip())

def nullFunction(lines, lineIndex, currentXML):
    print lineIndex, whoami(),
    lineIndex += 1
    return lineIndex, currentXML

def COMMENT(lines, lineIndex, currentXML):
    print lineIndex, whoami(),
    print lines[lineIndex],
    lineIndex += 1
    return lineIndex, currentXML

def WALL(lines, lineIndex, currentXML):
    #print whoami(),
    print lineIndex, whoami(),
    
    #print lineIndex, 'WALL', splitBuiLine(lines[lineIndex])
    #re.split('\s+', lines[lineIndex].rstrip())
    #lines[lineIndex].split('= ')
    lineIndex = lineIndex + 1
    print  lineIndex, 'WALL', splitBuiLine(lines[lineIndex])
    lineIndex = lineIndex + 1
    print  lineIndex, 'WALL', splitBuiLine(lines[lineIndex])
    lineIndex = lineIndex + 1
    print  lineIndex, 'WALL', splitBuiLine(lines[lineIndex])
    lineIndex = lineIndex + 1
    print  lineIndex, 'WALL', splitBuiLine(lines[lineIndex])
    lineIndex = lineIndex + 1
    print  lineIndex, 'WALL', splitBuiLine(lines[lineIndex])
    lineIndex = lineIndex + 1
    
    return lineIndex, currentXML

def ZONE(lines, lineIndex, currentXML):
    print lineIndex, whoami(),
    items =  lines[lineIndex].split()
    
    thisZoneXML = etree.Element("ZONE")
    thisZoneXML.attrib['name']=items[1]
    lineIndex +=1    
    while foundToken(secondaryTokens_ZONE, lines[lineIndex]):
        k = foundToken(secondaryTokens_ZONE, lines[lineIndex])
        lineIndex, thisZoneXML = secondaryTokens_ZONE[k](lines, lineIndex, thisZoneXML)
        print 
        
    currentXML.append(thisZoneXML)
    
    return lineIndex, currentXML

def addTagWithValue(root,name,value):
    newElement = etree.Element(name)
    newElement.text = value
    root.append(newElement)
    return root

def zWALL(lines, lineIndex, thisZoneXML):
    print lineIndex, whoami(),
    thisWallXML = etree.Element("WALL")
    standardItems = re.split(r'\s*=\s*|\s*=\s*|\s*:\s*|\s+',lines[lineIndex].rstrip())
    
    addTagWithValue(thisWallXML,"MATERIAL",standardItems[1])
    addTagWithValue(thisWallXML,"SURF",standardItems[3])
    addTagWithValue(thisWallXML,"AREA",standardItems[5])
    thisBoundXML = etree.Element("BOUNDARY")
    
    # Now process the boundaries
    lineItems = re.split(r':',lines[lineIndex].rstrip())
    boundaryItems = lineItems[3:]
    boundaryLine = ":".join(boundaryItems)
    print boundaryLine
    
    k = foundToken(secondaryTokens_BOUNDARY,boundaryLine)
    if not k:
        raise Exception("Returned k; {}, On line; {}".format(k,boundaryLine))
    else:
        secondaryTokens_BOUNDARY[k](boundaryItems, thisBoundXML)
    
    thisWallXML.append(thisBoundXML)
    #thisWallXML.append(etree.Element("MATERIAL",1))
    
    
    #("root", interesting="totally")
    #print standardItems,

    lineIndex = lineIndex + 1
    thisZoneXML.append(thisWallXML)
    return lineIndex, thisZoneXML

def zWINDOW(lines, lineIndex, thisZoneXML):
    print lineIndex, whoami(),
    thisZoneXML.append(etree.Element("WINDOW"))

    lineIndex = lineIndex + 1
    return lineIndex, thisZoneXML

def zAIRNODE(lines, lineIndex, currentXML):
    print lineIndex, whoami(),
    lineIndex = lineIndex + 1
    return lineIndex, currentXML

def zRADIATIONMODE(lines, lineIndex, currentXML):
    print lineIndex, whoami(),
    print lines[lineIndex],
    lineIndex = lineIndex + 1
    # We actually want the NEXT line!
    print lineIndex, "Radiation data;", lines[lineIndex],
    lineIndex = lineIndex + 1
    return lineIndex, currentXML

def zREGIME(lines, lineIndex, currentXML):
   print lineIndex, whoami(),
   lineIndex = lineIndex + 1
   return lineIndex, currentXML
def zGAIN(lines, lineIndex, currentXML):
   print lineIndex, whoami(),
   lineIndex = lineIndex + 1
   return lineIndex, currentXML
def zVENTILATION(lines, lineIndex, currentXML):
   print lineIndex, whoami(),
   lineIndex = lineIndex + 1
   return lineIndex, currentXML
def zCOOLING(lines, lineIndex, currentXML):
   print lineIndex, whoami(),
   lineIndex = lineIndex + 1
   return lineIndex, currentXML
def zHEATING(lines, lineIndex, currentXML):
   print lineIndex, whoami(),
   lineIndex = lineIndex + 1
   return lineIndex, currentXML
def zCAPACITANCE(lines, lineIndex, currentXML):
   print lineIndex, whoami(),
   lineIndex = lineIndex + 1
   return lineIndex, currentXML

def zINFILTRATION(lines, lineIndex, currentXML):
   print lineIndex, whoami(),
   lineIndex = lineIndex + 1
   return lineIndex, currentXML

# The NEXT line is actually the interesting one...

def PROPERTIES(lines, lineIndex, currentXML):
   print lineIndex, whoami(),
   lineIndex = lineIndex + 6
   return lineIndex, currentXML

def TOKENPLACEHOLDER(blockLines, currentXML):
   #print "Token function: {} lines ".format(len(blockLines))
   #print blockLines
   #lineIndex = lineIndex + 1
   return currentXML

def boundADJACENT(boundList, currentXML):
   #print lineIndex, whoami(),
   print "BoundaryItems;", boundList
   addTagWithValue(currentXML,"boundADJACENT","temp")
   
   
   #lineIndex = lineIndex + 1
   return currentXML

def boundEXTERNAL(boundList, currentXML):
   #print lineIndex, whoami(),
   print "BoundaryItems;", boundList
   addTagWithValue(currentXML,"boundADJACENT","temp")
   return currentXML

def boundIDENTICAL(boundList, currentXML):
   #print lineIndex, whoami(),
   print "BoundaryItems;", boundList
   addTagWithValue(currentXML,"boundADJACENT","temp")
   return currentXML

def boundINPUT(boundList, currentXML):
   #print lineIndex, whoami(),
   print "BoundaryItems;", boundList
   addTagWithValue(currentXML,"boundADJACENT","temp")
   return currentXML


secondaryTokens_ZONE =     {
                    r'^WALL\s*=': zWALL,
                    r'^WINDOW\s*=': zWINDOW,
                    r'^AIRNODE\s*': zAIRNODE,
                    r'^RADIATIONMODE\s*': zRADIATIONMODE,
                 r'^\sREGIME'      : zREGIME        ,
                 r'^\sGAIN'        : zGAIN          ,
                 r'^\sINFILTRATION' : zINFILTRATION   ,
                 
                 r'^\sVENTILATION' : zVENTILATION   ,
                 r'^\sCOOLING'     : zCOOLING       ,
                 r'^\sHEATING'     : zHEATING       ,
                 r'^\sCAPACITANCE' : zCAPACITANCE   ,                   
                    }

secondaryTokens_BOUNDARY=     {
                    r'\sADJACENT': boundADJACENT,
                    r'\sEXTERNAL': boundEXTERNAL,
                    r'\sBOUNDARY=IDENTICAL': boundIDENTICAL,
                    r'\sBOUNDARY=INPUT': boundINPUT,
                    
                    }

primaryTokens = {
                r'^WALL\s\S+$': WALL,
                r'^ZONE\s\S+$': ZONE,
                r'^PROPERTIES' : PROPERTIES   ,
                r'^TYPES' : TOKENPLACEHOLDER   ,
                r'^LAYER' : TOKENPLACEHOLDER   ,
                r'^INPUTS' : TOKENPLACEHOLDER   ,
                r'^SCHEDULE' : TOKENPLACEHOLDER   ,
                r'^WINDOW' : TOKENPLACEHOLDER   ,
                r'^GAIN' : TOKENPLACEHOLDER   ,
                r'^INFILTRATION' : TOKENPLACEHOLDER   ,
                r'^VENTILATION' : TOKENPLACEHOLDER   ,
                r'^COOLING' : TOKENPLACEHOLDER   ,
                r'^HEATING' : TOKENPLACEHOLDER   ,
                r'^ZONES' : TOKENPLACEHOLDER   ,
                r'^HEMISPHERE' : TOKENPLACEHOLDER   ,
                r'^ORIENTATIONS' : TOKENPLACEHOLDER   ,
                r'^INTERNAL_CALCULATION' : TOKENPLACEHOLDER   ,
                r'^BUILDING' : TOKENPLACEHOLDER   ,
                }

commentTokens = {   
              r'^[*]+': COMMENT,
              }


#===============================================================================
# Unit testing
#===============================================================================

"""
An object to handle blocks
Recieves the XML
Returns the XML
Has some general properties, but also has a slot for the specific behavior
"""


class parserCursor(object):
    """The parser cursor object
    """
    def __init__(self, linesList, tokenDict):
        self.linesList = linesList
        self.idxLines = 0
        self.tokens = tokenDict
        self.firstTime = True
        #self.currentString = "" 
        self.tokenFunc = None
        #logging.debug("Parser over {} lines with {} tokens".format(len(linesList), len(tokenDict)))
    
    def nextLineIdx(self):
        #nextLine = self.linesList[self.idxLines]
        self.idxLines += 1
        #return nextLine
    
    def currentString(self):
        print "Current string:", self.linesList[self.idxLines]
        return self.linesList[self.idxLines]
    
    def __iter__(self):
        return self
    
    def next(self):
        blockLines = list()
        
        # This is essentially a state machine style parse
        # The START state, until we find a token
        while 1:
            self.tokenFunc = foundToken(self.tokens, self.currentString())
            if self.tokenFunc:
                break # Transition 1 or 4
            else:
                self.nextLineIdx()

        while 1:
            # Start the block with the last line retrieved
            blockLines.append(self.currentString())
            #print "Appended", self.currentString()
            # Check the next line
            self.nextLineIdx()
            if foundToken(self.tokens, self.currentString()):
                break
            else:
                blockLines.append(self.currentString())
        
        return blockLines


def test010_cursorObject(self):
    print "**** TEST {} ****".format(whoami())
    testString = dedent("""\
        *--------
        *  L a y e r s
        *--------
        LAYER DUMMY_TRNSYS3D
         RESISTANCE=      0.1
        LAYER PLASTERBOA
         CONDUCTIVITY=  0.576 : CAPACITY=   0.84 : DENSITY=    950
        LAYER FBRGLS_ASHRAE
         CONDUCTIVITY=  0.144 : CAPACITY=   0.84 : DENSITY=     12""")
    #testFileLike = StringIO(testString)
    linesList = testString.split("\n")

    mainLoop = parserCursor(linesList,primaryTokens)
    for line in mainLoop:
        print "Iteration:", line


class allTests(unittest.TestCase):
    def setUp(self):
        print "**** SETUP {} ****".format(whoami())
        inputBuiFilePath = r"..\testBuiFiles\Building17.b17"
        
        # The input file
        fIn = open(inputBuiFilePath, 'r')
        self.lines = fIn.readlines()
        fIn.close()
        logging.debug("Loaded {} into {} lines".format(inputBuiFilePath,len(self.lines)))
        
        # The Output file
        outputXMLFile = '..\\XML Output\\test.xml'
        self.fOut = open(outputXMLFile, 'w')
        
        # Initialize the XML
        xmlVer = "0.1"
        currentXML = etree.Element("TRNSYSBUI_XML", XML_version=xmlVer)
        currentXML = etree.Element("TRNSYS_XML", XML_version=xmlVer)
        commentXML = etree.Comment("XML Schema for TRNSYS version 17 BUI file")
        currentXML.append(commentXML)
        commentXML = etree.Comment("Schema created Aug. 2012 by Marcus Jones")
        currentXML.append(commentXML)
        self.xml = currentXML
        
    def test010_cursorObject(self):
        print "**** TEST {} ****".format(whoami())
        testString = dedent("""\
            *  L a y e r s
            LAYER DUMMY_TRNSYS3D
             RESISTANCE=      0.1
            LAYER PLASTERBOA
             CONDUCTIVITY=  0.576 : CAPACITY=   0.84 : DENSITY=    950
            LAYER FBRGLS_ASHRAE
             CONDUCTIVITY=  0.144 : CAPACITY=   0.84 : DENSITY=     12""")
        testFileLike = StringIO(testString)
        linesList = testString.split("\n")

        mainLoop = parserCursor(linesList,primaryTokens)
        for line in mainLoop:
            print "Iteration:", line
        
    def skip010_SimpleCreation(self):
        print "**** TEST {} ****".format(whoami())
        inputBuiFilePath = r"..\testBuiFiles\Building17.b17"

        fIn = open(inputBuiFilePath, 'r')
        fOut = open('..\\XML Output\\test.xml', 'w')
        
        xmlVer = "0.1"
        
         Calls the readlines method of object which returns a list
        lines = fIn.readlines()
        logging.debug("Opened {} with {} lines".format(inputBuiFilePath,len(lines)))
        
        k = foundToken(primaryTokens,'VERSIN')
        print k
        print primaryTokens[k]
        primaryTokens[k]()
            
    def skiptest010_(self):
        print "**** TEST {} ****".format(whoami())
        testString = dedent("""\
            *  L a y e r s
            LAYER DUMMY_TRNSYS3D
             RESISTANCE=      0.1
            LAYER PLASTERBOA
             CONDUCTIVITY=  0.576 : CAPACITY=   0.84 : DENSITY=    950
            LAYER FBRGLS_ASHRAE
             CONDUCTIVITY=  0.144 : CAPACITY=   0.84 : DENSITY=     12""")

        lines = testString.split("\n")
        idxLines = 0
        flagBlock = False
        blockFunction = None
        blockLines = list()
        while (idxLines < len(lines) ) :
            # This is essentially a state machine style parse
            # There are four states in the loop 
            tokenFunc = foundToken(primaryTokens, lines[idxLines])
            
            if tokenFunc and not flagBlock:
                # STATE: Start first block
                # This is the start of a new block
                # Start a new blockLines, and store the blockFunction
                # This can only occur ONCE
                print "{:20}: {}".format(tokenFunc.__name__, lines[idxLines] )                                
                blockLines.append(lines[idxLines])
                blockFunction = tokenFunc
                flagBlock = True
                
            elif not tokenFunc and flagBlock:
                # STATE: Continue block              
                # The block continues until we meet the next token
                # Don't do anything but keep appending lines
                print "{:20}: {}".format("In block", lines[idxLines] )
                # But don't append any comments
                if not foundToken(commentTokens, lines[idxLines]):     
                    blockLines.append(lines[idxLines])        
                      
            elif tokenFunc and flagBlock:
                # STATE: Next block transition                    
                # We found a token after a block, the block ends
                # flagBlock is True for the new block
                # Run the blockFunction on the blockLines, reset all after
                blockFunction(blockLines, self.xml)
                print "{:20}: {}".format(tokenFunc.__name__, lines[idxLines] )
                flagBlock = True
                blockLines = list()
                blockFunc = None
                blockLines.append(lines[idxLines])
                blockFunction = tokenFunc
                flagBlock = True
                
            elif not tokenFunc and not flagBlock:
                # STATE: Start with comments
                # This can only occur at the beginning of the lines since
                # after the first block, we must be inside a block, or starting a new one
                print "{:20}: {}".format("Comment", lines[idxLines] )                                                
                commentLine = foundToken(commentTokens, lines[idxLines])
                if commentLine:
                    # This is a comment
                    flagBlock = False
                else:
                    raise Exception("Unrecognized line, expected a comment:\n{}".format(lines[idxLines]))
                
            idxLines += 1
        
    def skiptest020_runMainLoop(self):
        print "**** TEST {} ****".format(whoami())
        lines = self.lines

        # Calls the readlines method of object which returns a list
        
        lineIndex = 0

        startLine =  0
        endLine = len(lines)
        endLine = 642
        lineIndex = startLine 
        while (lineIndex < endLine ) :
            #words = re.split('[=\s]', lines[lineIndex])
            # Check for KEYWORDS in the FIRST word
            k = foundToken(primaryTokens, lines[lineIndex])
            if k: 
                # Call the corresponding function from the dictionary
                # Note that lines is passed instead of words, since each line may be better split in different ways
                # lineIndex can also be updated by the function, to facilitate local loops
                lineIndex, self.xml = primaryTokens[k](lines, lineIndex, self.xml)
            else:
                print lineIndex, "NOTOKEN", lines[lineIndex],
                lineIndex += 1
            
        resultXML = (etree.tostring(self.xml, pretty_print=True))
        
        self.fOut.write(self.xml)
        logging.debug("Wrote to {}".format(outputXMLFile))
        
            #


#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    logging.config.fileConfig('..\\..\\MyUtilities\\LoggingConfig\\loggingNofile.conf') 
    myLogger = logging.getLogger() 
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())

    #unittest.main()
    test010_cursorObject()
        
    logging.debug("Finished _main".format())
    
