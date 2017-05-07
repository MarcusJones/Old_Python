# Instantiates the file object into f
#f = open('C:\Scripting\L Python\\02 Snippits\\test.dck', 'r')
#f = open('D:\AllScripts\L Python\\02 Snippits\\test.dck', 'r')


#    def create_XML_child(currentXML, parentTagName, tagName, attributeNames, attributeValues):
#        '''Given XML object, Tag name, and a list of attributes and a list of values
#        currentXML, the XML object (in lxml)
#        tagName, name of the tag
#        attributeNames, tuple list
#        attributeValues, tuple list
#        Returns the XML object
#        '''
#        
#        # Pass in N attribute names, to coordinate with N words which have been parsed
#        xmlObjectName = "currentXML"
#        evalString = assemble_XML_SubElement_String(xmlObjectName, parentTagName, tagName, attributeNames, attributeValues)
#        
#        # Execute the assembled XML SubElement creator
#        # print evalString
#        exec(evalString)
#        return currentXML
        
#    def assemble_XML_SubElement_String(xmlObjectName, parentTagName, tagName, attributeNames, attributeValues):
#        # print "HERE",attributeNames, attributeValues
#        '''Create an eval statement 
#        xmlObjectName, the string
#        parentTagName, The parent tag
#        tagName, string for the current tag name to create
#        attributeNames, tuple list 
#        attributeValues, tuple list
#        '''
#        #currentXML.find(parentTag)
#        # Start the statement
#        evalString = "currentElement = etree.SubElement(" + xmlObjectName + ".find(\"" + parentTagName + "\"), tagName, "
#        #print attributeNames,attributeValues
#        # Append the statements for all attributes
#        #print range(len(attributeNames))
#        for i in range(len(attributeNames)):
#            print i
#            evalString += attributeNames[i]
#            evalString += "="
#            evalString += "\"" + attributeValues[i] + "\""
#            if i < len(attributeNames):
#                evalString += ","
#        evalString += ")"
#        return evalString

#str = 'VERSION 17'
#print str.split()

# from http://bytebaker.com/2008/11/03/switch-case-statement-in-python/
#options = {0 : zero,
#                1 : sqr,
#                4 : sqr,
#                9 : sqr,
#                2 : even,
#                3 : prime,
#                5 : prime,
#                7 : prime,
#}
#
#def zero():
#    print "You typed zero.\n"
#
#def sqr():
#    print "n is a perfect square\n"
#
#def even():
#    print "n is an even number\n"
#
#def prime():
#    print "n is a prime number\n"



# >>> import re
# >>> reObj = re.compile('.an.$')
# >>> bool(reObj.match("pants"))
# False
# >>> bool(reObj.match("pant"))
# True
# >>> 
# >>> words = ["show", "shoe", "band", "land", "sand", "pant", "pants"]
# >>> pattDict= {'sho.$':6, '.ilk$':8,'.an.$':78 }
# >>> for word in words:
# ...     for k, v in pattDict.items():
# ...         if re.match(k,word):
# ...             print word, v
# ...             
# show 6


from lxml.etree import XSLT,fromstring

xml = fromstring("<a key='value'>ez</a>")

xsl= fromstring("""<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method = "html"  version="1.0" encoding="UTF-8" omit-xml-declaration="yes" standalone="yes" indent="no"  />
    
    <xsl:template match="a">
    <xsl:value-of select="@key"/>
    </xsl:template>

</xsl:stylesheet>""")

style = XSLT(xsl)
result = style.apply( xml)
print style.tostring(result)