'''
Created on 20.04.2011

@author: mjones
'''

import re
from lxml import etree
import logging

def xpathRE(tree, strXpath):
    """
    This function is just an alias for the etree.xpath function,
    just to avoid having to always declare the namespace 're:'
    """
    return tree.xpath(strXpath, 
        namespaces={"re": "http://exslt.org/regular-expressions"})

testXml = '..\\XML\\Test IDF.xml'

testXmlFH = open(testXml, 'r')

tree = etree.parse(testXmlFH)

# Find a CLASS object with the name matching className, and return it's PARENT
xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]/.."

# Select all class objects which have Zone in the name and return it's Parent (Object)
xpathSearch = "//CLASS[re:match(text(), '^Zone$')]/.."
zones = self.XML.xpath(xpathSearch,
            namespaces={"re": "http://exslt.org/regular-expressions"})
       for zone in zones:
            #print zone.text
            type = zone.xpath('CLASS')
            name = zone.xpath('ATTR')


# The tree object
#print tree

# The tree text
#print(etree.tostring(tree))

# select all OBJECTS anywhere
#print tree.xpath('//OBJECT')

# Select all NAMES anywhere
#print tree.xpath('//NAME')

# Select all ZoneLoads objects
#zoneLoadsObjs = tree.xpath("//NAME[re:match(text(), 'ZoneLoads')]", 
#        namespaces={"re": "http://exslt.org/regular-expressions"})

# Select all class objects with text equal to ZoneLoads
zoneLoadsObjs = xpathRE(tree, "//CLASS[re:match(text(), 'ZoneLoads')]") 
#tree.xpath("//NAME[re:match(text(), 'ZoneLoads')]", 
#        namespaces={"re": "http://exslt.org/regular-expressions"})

for obj in zoneLoadsObjs:
    print obj.text
    obj.text = 'HAHA'

# The tree text
print(etree.tostring(tree))

#    Expression     Description
#    nodename     Selects all child nodes of the named node
#    /     Selects from the root node
#    //     Selects nodes in the document from the current node that match the selection no matter where they are
#    .     Selects the current node
#    ..     Selects the parent of the current node
#    @     Selects attributes
#    
#    In the table below we have listed some path expressions and the result of the expressions:
#    Path Expression     Result
#    bookstore     Selects all the child nodes of the bookstore element
#    /bookstore     Selects the root element bookstore
#    
#    Note: If the path starts with a slash ( / ) it always represents an absolute path to an element!
#    bookstore/book     Selects all book elements that are children of bookstore
#    //book     Selects all book elements no matter where they are in the document
#    bookstore//book     Selects all book elements that are descendant of the bookstore element, no matter where they are under the bookstore element
#    //@lang     Selects all attributes that are named lang

#/bookstore/book[1]     Selects the first book element that is the child of the bookstore element.
#/bookstore/book[last()]     Selects the last book element that is the child of the bookstore element
#/bookstore/book[last()-1]     Selects the last but one book element that is the child of the bookstore element
#/bookstore/book[position()<3]     Selects the first two book elements that are children of the bookstore element
#//title[@lang]     Selects all the title elements that have an attribute named lang
#//title[@lang='eng']     Selects all the title elements that have an attribute named lang with a value of 'eng'
#/bookstore/book[price>35.00]     Selects all the book elements of the bookstore element that have a price element with a value greater than 35.00
#/bookstore/book[price>35.00]/title     Selects all the title elements of the book elements of the bookstore element that have a price element with a value greater than 35.00