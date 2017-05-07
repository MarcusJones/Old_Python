'''
Created on Apr 1, 2011

@author: UserXP
'''
import re

print "Starting"

fIn = open('..\\Test OSM files\\OSM in.osm', 'r')
fOut = open('..\\OSM Output\\OSMout.txt', 'w')

# Calls the readlines method of object which returns a list
lines = fIn.readlines()

lineIndex = 0
zoneNameIndex = 0

while (lineIndex < len(lines)) :
    #print lineIndex
    #words = re.match('^\w+,', lines[lineIndex])
    
    #re.sub('Zone {\S+}', lines[lineIndex],"Generic name")
    #print lines[lineIndex].rstrip()
    
#    if re.search('Zone {\S+}', lines[lineIndex]):
#        pass
#        #print "Zone name FOUND"
#        #fOut.write(lines[lineIndex])
    
    # This Regular Expression matches the opening of any object
    objectOpenPattern = """
        ^      # beginning of string
        \w+    # 1 or more alphanumeric chars
        [\w:]*  # Any number of colons and alphanumerics
        ,        # Comma
        $        # End of the line 
        """
        
    # This RegEx matches the closing (just a semicolon) 
    objectClosePattern = """
        ;
        """

    # Found a Zone object 
    if re.search('Zone,', lines[lineIndex]):
        zoneNameIndex += 1
        # Split off the name attibute
        zoneName = re.split("[\{\}]", lines[lineIndex+1])[1]
        print "Zone name: ", zoneName
        newLineArray = []
        # Now replace all instances with new name, using a temp array
        for line in lines: 
            newLineArray += [re.sub(zoneName,str(zoneNameIndex), line)]
        # Reassign the array
        lines = newLineArray
        
    fOut.write(lines[lineIndex])
    
#    if words:
#        print "match"
#        print lines[lineIndex].rstrip()
#        while (lineIndex < len(lines)) :
#            words = re.search(';', lines[lineIndex])
#            print lines[lineIndex].rstrip()
#            if words:
#                #print "found End"
#                break
#
#            lineIndex += 1
    lineIndex += 1

fIn.close()

print "Finished"

print "Finished"