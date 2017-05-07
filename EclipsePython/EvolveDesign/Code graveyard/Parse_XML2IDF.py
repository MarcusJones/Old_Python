'''
Created on Apr 14, 2011

@author: UserXP
'''
import re
from lxml import etree
import StringIO

fIn = open('..\\XML Output\\Test IDF.xml', 'r')
fTransform = open('..\\XSLT\\XML2IDF v3.xsl', 'r')

xmlFile = etree.parse(fIn)
xmlTransform = etree.parse(fTransform)

transform = etree.XSLT(xmlTransform)

# EnergyPlus_XML/OBJECT # Select all OBJECT nodes from the root
# /OBJECT/ATTR[last()] # Selects the last ATTR in an OBJECT 

#print etree.tostring(xmlFile, pretty_print=True)

#print etree.tostring(xmlTransform, pretty_print=True)

result_tree = transform(xmlFile)

print etree.tostring(result_tree, pretty_print=True)

