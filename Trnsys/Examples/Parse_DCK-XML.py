'''
Created on Feb 27, 2011

@author: UserXP
'''
# This script opens a TRNSYS DCK file and returns an XML file

from lxml import etree
import re

print "Starting"

fIn = open('..\\Test DCK files\\test.dck', 'r')
fOut = open('..\\XML Output\\test.xml', 'w')

xmlVer = "0.1"

# Calls the readlines method of object which returns a list
lines = fIn.readlines()

### Utility functions
if 1:
    def found_keyword(keywordDictionary, word):
        ''' Search the dictionary for the current word, return the matched word, or 0 '''
        for k, v in keywordDictionary.items():
            if re.match(k,word):
                # Found a TRNSYS .DCK keyword
                # Return the keyword
                return k
        # If nothing found, return 0
        return 0
        

# Keyword functions
def VERSION      (lines, lineIndex, currentXML):
    parentTag = "ControlCards"
    words = re.split('[=\s]', lines[lineIndex])
    thisUnitXML = etree.Element("VERSION")
    
    thisUnitXML.set("Version",words[1])

    return lineIndex, currentXML
  
def SIMULATION      (lines, lineIndex, currentXML):
    parentTag = "ControlCards"
    attributeNames = ["StartTime","StopTime","TimeStep"]
    
    # Split the line again, retrieve attribute values
    words = re.split('\s+', lines[lineIndex])
    tagName = words[0]
    attributeValues = words[1:len(attributeNames)+1]

    # Create this sub object
    thisUnitXML = etree.Element(tagName)
    for i in range(len(attributeNames)):
        thisUnitXML.set(attributeNames[i],attributeValues[i])
    
    # Add this sub object      
    currentXML.find(parentTag).append(thisUnitXML)

    return lineIndex, currentXML

def TOLERANCES     (lines, lineIndex, currentXML):
    parentTag = "ControlCards" 
    attributeNames = ["Integration","Convergence"]
      
    # Split the line again, retrieve attribute values
    words = re.split('\s+', lines[lineIndex])
    tagName = words[0]
    attributeValues = words[1:len(attributeNames)+1]

    # Create this sub object
    thisUnitXML = etree.Element(tagName)
    for i in range(len(attributeNames)):
        thisUnitXML.set(attributeNames[i],attributeValues[i])

    # Add this sub object      
    currentXML.find(parentTag).append(thisUnitXML)

    return lineIndex, currentXML
    
def LIMITS         (lines, lineIndex, currentXML):
    parentTag = "ControlCards" 
    attributeNames = ["MaxIterations",    "MaxWarnings",    "TraceLimit"]
       
    # Split the line again, retrieve attribute values
    words = re.split('\s+', lines[lineIndex])
    tagName = words[0]
    attributeValues = words[1:len(attributeNames)+1]

    # Create this sub object
    thisUnitXML = etree.Element(tagName)
    for i in range(len(attributeNames)):
        thisUnitXML.set(attributeNames[i],attributeValues[i])

    # Add this sub object      
    currentXML.find(parentTag).append(thisUnitXML)

    return lineIndex, currentXML
    
def DFQ             (lines, lineIndex, currentXML):
    parentTag = "ControlCards" 
    attributeNames = ["SolverMethod"]
      
    # Split the line again, retrieve attribute values
    words = re.split('\s+', lines[lineIndex])
    tagName = words[0]
    attributeValues = words[1:len(attributeNames)+1]

    # Create this sub object
    thisUnitXML = etree.Element(tagName)
    for i in range(len(attributeNames)):
        thisUnitXML.set(attributeNames[i],attributeValues[i])

    # Add this sub object      
    currentXML.find(parentTag).append(thisUnitXML)

    return lineIndex, currentXML
    
    
def WIDTH        (lines, lineIndex, currentXML): 
    parentTag = "ControlCards"
    attributeNames = ["NumberOfCharacters"]
      
    # Split the line again, retrieve attribute values
    words = re.split('\s+', lines[lineIndex])
    tagName = words[0]
    attributeValues = words[1:len(attributeNames)+1]

    # Create this sub object
    thisUnitXML = etree.Element(tagName)
    for i in range(len(attributeNames)):
        thisUnitXML.set(attributeNames[i],attributeValues[i])

    # Add this sub object      
    currentXML.find(parentTag).append(thisUnitXML)


    return lineIndex, currentXML

def LIST          (lines, lineIndex, currentXML): 
    parentTag = "ControlCards"
    attributeNames = ["NOLISTstatement"]
      
    # Split the line again, retrieve attribute values
    words = re.split('\s+', lines[lineIndex])
    tagName = words[0]
    attributeValues = words[1:len(attributeNames)+1]

    # Create this sub object
    thisUnitXML = etree.Element(tagName)
    for i in range(len(attributeNames)):
        thisUnitXML.set(attributeNames[i],attributeValues[i])

    # Add this sub object      
    currentXML.find(parentTag).append(thisUnitXML)


    return lineIndex, currentXML

def SOLVER       (lines, lineIndex, currentXML):
    parentTag = "ControlCards" 
    attributeNames = ["SolverStatement","MinimumRelaxationFactor","MaximumRelaxationFactor"]
      
    # Split the line again, retrieve attribute values
    words = re.split('\s+', lines[lineIndex])
    tagName = words[0]
    attributeValues = words[1:len(attributeNames)+1]

    # Create this sub object
    thisUnitXML = etree.Element(tagName)
    for i in range(len(attributeNames)):
        thisUnitXML.set(attributeNames[i],attributeValues[i])

    # Add this sub object      
    currentXML.find(parentTag).append(thisUnitXML)


    return lineIndex, currentXML

def NAN_CHECK    (lines, lineIndex, currentXML):
    parentTag = "ControlCards" 
    attributeNames = ["NanDEBUGStatement"]
      
    # Split the line again, retrieve attribute values
    words = re.split('\s+', lines[lineIndex])
    tagName = words[0]
    attributeValues = words[1:len(attributeNames)+1]

    # Create this sub object
    thisUnitXML = etree.Element(tagName)
    for i in range(len(attributeNames)):
        thisUnitXML.set(attributeNames[i],attributeValues[i])

    # Add this sub object      
    currentXML.find(parentTag).append(thisUnitXML)


    return lineIndex, currentXML

def OVERWRITE_CH (lines, lineIndex, currentXML): 
    parentTag = "ControlCards"
    attributeNames = ["OverwriteDEBUGStatement"]
      
    # Split the line again, retrieve attribute values
    words = re.split('\s+', lines[lineIndex])
    tagName = words[0]
    attributeValues = words[1:len(attributeNames)+1]

    # Create this sub object
    thisUnitXML = etree.Element(tagName)
    for i in range(len(attributeNames)):
        thisUnitXML.set(attributeNames[i],attributeValues[i])

    # Add this sub object      
    currentXML.find(parentTag).append(thisUnitXML)


    return lineIndex, currentXML
    
def TIME_REPORT  (lines, lineIndex, currentXML): 
    parentTag = "ControlCards"
    attributeNames = ["DisableTimeReport"]
      
    # Split the line again, retrieve attribute values
    words = re.split('\s+', lines[lineIndex])
    tagName = words[0]
    attributeValues = words[1:len(attributeNames)+1]

    # Create this sub object
    thisUnitXML = etree.Element(tagName)
    for i in range(len(attributeNames)):
        thisUnitXML.set(attributeNames[i],attributeValues[i])

    # Add this sub object      
    currentXML.find(parentTag).append(thisUnitXML)


    return lineIndex, currentXML
    
def EQSOLVER     (lines, lineIndex, currentXML): 
    parentTag = "ControlCards"
    attributeNames = ["EQUATIONSOLVERstatement"]
      
    # Split the line again, retrieve attribute values
    words = re.split('\s+', lines[lineIndex])
    tagName = words[0]
    attributeValues = words[1:len(attributeNames)+1]

    # Create this sub object
    thisUnitXML = etree.Element(tagName)
    for i in range(len(attributeNames)):
        thisUnitXML.set(attributeNames[i],attributeValues[i])

    # Add this sub object      
    currentXML.find(parentTag).append(thisUnitXML)

    return lineIndex, currentXML
    
def EQUATIONS     (lines, lineIndex, currentXML): 
    parentTag = "Equations"
    return lineIndex, currentXML

def CONSTANTS    (lines, lineIndex, currentXML): 
    ''' This is an example of a Sub-Loop in the parser, '''
    # Now do an internal loop
    while 1 :
        lineIndex += 1
        words = re.split('[=\s]', lines[lineIndex])
        # Check for a properly formatted equation
        if re.match(r"\w+\s*=\s*[0-9].*[0-9]*",lines[lineIndex]): pass
        elif (found_keyword(keywordDictionary, words[0])):
            # Found the next keyword, reduce the lineIndex so it can be parsed afterwards
            lineIndex -= 1
            break
    return lineIndex, currentXML
    
def UNIT         (lines, lineIndex, currentXML): 
    parentTag = "Units" 
    attributeNames = ["Number","TypeNumber","SubType"]
    
    # Split the line again, retrieve attribute values
    words = re.split('\s+', lines[lineIndex])
    tagName = words[0]
    attributeValues = words[1], words[3], words[4]
   
    # Create this sub object
    thisUnitXML = etree.Element(tagName)
    
    for i in range(len(attributeNames)):
        thisUnitXML.set(attributeNames[i],attributeValues[i])
    
    # Add the subobjects
    thisUnitXML.append(etree.Element("Parameters"))
    thisUnitXML.append(etree.Element("Inputs"))
    thisUnitXML.append(etree.Element("ExternalFiles"))
    thisUnitXML.append(etree.Element("Labels"))
    thisUnitXML.append(etree.Element("UNIT_NAME"))
    thisUnitXML.append(etree.Element("MODEL"))
    thisUnitXML.append(etree.Element("POSITION"))
    thisUnitXML.append(etree.Element("LAYER"))
    
    # Now do an internal loop until the next keyword is found
    while 1 :
        
        lineIndex += 1
        # Split on white space
        words = re.split('[\s+]', lines[lineIndex])
        
        # The general unit information
        if re.match(r"^\*\$UNIT_NAME",lines[lineIndex]):
            thisText = re.split(r"^\*\$UNIT_NAME",lines[lineIndex])[1]
            thisUnitXML.find("UNIT_NAME").text = thisText
            #print thisText
        elif re.match(r"^\*\$MODEL",lines[lineIndex]):
            thisText = re.split(r"^\*\$MODEL",lines[lineIndex])[1]
            thisUnitXML.find("MODEL").text = thisText
            #print thisText
        elif re.match(r"^\*\$POSITION",lines[lineIndex]):
            thisText = re.split(r"^\*\$POSITION",lines[lineIndex])[1]
            thisUnitXML.find("POSITION").text = thisText
            #print thisText
        elif re.match(r"^\*\$LAYER",lines[lineIndex]):
            thisText = re.split(r"^\*\$LAYER",lines[lineIndex])[1]
            thisUnitXML.find("LAYER").text = thisText
            #print thisText
            
        # Check for parameters            
        elif re.match(r"^PARAMETERS",lines[lineIndex]):
            # Loop over the parameters
            numParams = re.split(r"\s",lines[lineIndex].rstrip())
            # The next numParams lines are the parameters
            for i in range(1,int(numParams[1])):
                lineIndex += 1
                
                # Create a parameter object
                parameterXML = etree.Element("PARAMETER")
                
                # Add the description and the value
                parameterXML.text = re.split(r"!",lines[lineIndex])[0].rstrip()
                descriptionText = re.split(r"!",lines[lineIndex])[1].rstrip()
                parameterXML.set("Desc",descriptionText)
                
                # Append to the proper subobject
                thisUnitXML.find("Parameters").append(parameterXML)
        # Check for inputs
        elif re.match(r"^INPUTS",lines[lineIndex]):
            numInputs = re.split(r"\s",lines[lineIndex].rstrip())
            numInputs = int(numInputs[1])
            # Get the initial values
            lineIndexInitials = lineIndex + numInputs + 2
            initialValues = re.split(r"\s",lines[lineIndexInitials].rstrip())
            
            # print "INITIAL VALS", initialValues
            
            for i in range(1,numInputs):
                lineIndex += 1
                # Create an Input object
                inputXML = etree.Element("INPUT")
                
                # Break off the incoming unit
                fromUnitString = re.split(r"!",lines[lineIndex].rstrip())[0]
                fromUnit = re.split(r",",fromUnitString.rstrip())[0]
                intoPort = re.split(r",",fromUnitString.rstrip())[1]
                
                # Break off the descriptors
                unitDescriptorString = re.split(r"!",lines[lineIndex].rstrip())[1]
                
                if re.search(r"\[unconnected\]",unitDescriptorString):
                    fromUnitDesc = "Unconnected"
                    intoInputDesc = re.split(r"\[unconnected\]",unitDescriptorString.strip())[1]
                else:
                    fromUnitDesc = re.split(r"->",unitDescriptorString.rstrip())[0]
                    intoInputDesc = re.split(r"->",unitDescriptorString.rstrip())[1]
                   
                # Assemble the INPUT
                # First, the initial value element
                initialValueXML = etree.Element("INITIAL_VALUE")
                initialValueXML.text = initialValues[i].strip()
                
                # The FROM UNIT element
                fromUnitXML = etree.Element("FROM_UNIT")
                fromUnitXML.text = fromUnit.strip()
                fromUnitXML.set("Desc",fromUnitDesc.strip())

                # The INTO PORT element
                intoPortXML = etree.Element("INTO_PORT")
                intoPortXML.text = intoPort.strip()
                intoPortXML.set("Desc",intoInputDesc.strip())
                
                # Append the three onto the INPUT element
                inputXML.append(initialValueXML)
                inputXML.append(fromUnitXML)
                inputXML.append(intoPortXML)
                
                # And apend the completed INPUT into the Inputs section
                thisUnitXML.find("Inputs").append(inputXML)
                
        # Check for inputs
        elif re.match(r"^ASSIGN",lines[lineIndex]):
            thisXML = etree.Element("ASSIGN")
            thisXML.text = re.split(r"ASSIGN",lines[lineIndex].strip())[1]
            thisUnitXML.find("ExternalFiles").append(thisXML)
            
        elif re.match(r"^LABELS",lines[lineIndex]):
            numLabels = re.split(r"\s+",lines[lineIndex].rstrip())
            numLabels = int(numLabels[1])
            for i in range(1,numLabels+1):
                lineIndex += 1
                # Create an Input object
                labelXML = etree.Element("LABEL")
                labelXML.text = lines[lineIndex]
                thisUnitXML.find("Labels").append(labelXML)

        elif (found_keyword(keywordDictionary, words[0])):
            # Found the next keyword, reduce the lineIndex so it can be parsed
            lineIndex -= 1
            break
        
    # Add this sub object      
    currentXML.find(parentTag).append(thisUnitXML)
    
    return lineIndex, currentXML

    
def END     (lines, lineIndex, currentXML): 
    return lineIndex, currentXML

#        patObject = """
#            ^      # beginning of string
#            \w+    # 1 or more alphanumeric chars
#            [\w:]*  # Any number of colons and alphanumerics
#            ,        # Comma
#            """
#            # Used to include end of line:
#            #$        # End of the line
#        


#superPatternDictionary = {
#                          linearStyle
#                          }

keywordDictionary =     {
                    'VERSION': VERSION, 
                    'CONSTANTS':CONSTANTS,
                    'SIMULATION':SIMULATION,
                    'TOLERANCES':TOLERANCES,
                    'LIMITS':LIMITS,
                    'DFQ':DFQ,
                    'WIDTH':WIDTH,
                    'LIST':LIST,
                    'SOLVER':SOLVER,
                    'NAN_CHECK':NAN_CHECK,
                    'OVERWRITE_CH':OVERWRITE_CH,
                    'TIME_REPORT':TIME_REPORT,
                    'EQSOLVER':EQSOLVER,
                    'UNIT':UNIT,
                    'EQUATIONS':EQUATIONS,
                    'END':END,
                    }

lineIndex = 0

currentXML = etree.Element("TRNSYS_XML", XML_version=xmlVer)
commentXML = etree.Comment("XML Schema for TRNSYS version 17 DCK file")
currentXML.append(commentXML)
commentXML = etree.Comment("Schema created Feb. 2011 by Marcus Jones")
currentXML.append(commentXML)

etree.SubElement(currentXML, "ControlCards")
etree.SubElement(currentXML, "Units")

while (lineIndex < len(lines)) :
    words = re.split('[=\s]', lines[lineIndex])
    # print words
    # Check for KEYWORDS in the FIRST word
    k = found_keyword(keywordDictionary, words[0])
    if k: 
        # Call the corresponding function from the dictionary
        # Note that lines is passed instead of words, since each line may be better split in different ways
        # lineIndex can also be updated by the function, to facilitate local loops
        lineIndex, currentXML = keywordDictionary[k](lines, lineIndex, currentXML)
    lineIndex += 1

fIn.close()

resultXML = (etree.tostring(currentXML, pretty_print=True))

fOut.write(resultXML )
fOut.close

print "Finished"