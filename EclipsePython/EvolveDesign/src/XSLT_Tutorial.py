'''
Created on Apr 15, 2011

@author: UserXP
'''
'''
Created on Apr 14, 2011

@author: UserXP
'''
import re
from lxml import etree
import StringIO

fIn = open('..\\XML Output\\TutorialXML.xml', 'r')
fTransform = open('..\\XSLT\\TutorialXSL.xsl', 'r')

xmlFile = etree.parse(fIn)
xmlTransform = etree.parse(fTransform)

transform = etree.XSLT(xmlTransform)

result_tree = transform(xmlFile)


print etree.tostring(result_tree, pretty_print=True)

