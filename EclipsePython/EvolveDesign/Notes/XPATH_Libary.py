# To enable the regular expression search capability, include the namespace as follows:
self.XML.xpath(xpathSearch,namespaces={"re": "http://exslt.org/regular-expressions"})

# Each CLASS is actually surrounded by an OBJECT, the OBJECT contains the attributes and the class name
# To return the whole object, we can use:
xpathSearch = "//CLASS//.."

# All ATTR with the exact text value of searchVal
xpathSearch = "//ATTR[text() = \"" + searchVal + "\"]"

# The BuildingSurface:Detailed class's parents' first attribute if it has the target name, it's parent's 4th attribute
xpathSearch =  "//CLASS[.=\"BuildingSurface:Detailed\"]/../ATTR[1]" \
        "[.=\"" + targetSurfaceName + "\"]/../ATTR[4]"

# Select all BuildingSurface:Detailed objects, then back to OBJECT, then find the word 'Surface' at the 5 ATTR position
xpathSearch =  "//CLASS[.=\"BuildingSurface:Detailed\"]/../ATTR[5][.=\"Surface\"]/.."

# Get all BuildingSurface:Detailed objects with the value "Surface" in ATTR[5] (Outside Boundary Condition Object)
xpathSearch = "//ATTR[5][text() = \"Surface\"]"

# Return the 2nd ATTR of all CLASS elements in the document
xpathSearch = "//CLASS//..//ATTR[2]"

# Return the first attribute in the current context only
xpathSearch = "./ATTR[1]"

# Return the OBJECT (Parent /..) with a CLASS of classNameRegex 
xpathSearch = "//CLASS[re:match(text(), '" + classNameRegex + "')]/.."

# Return the nummAttr ATTR of all className CLASS 
xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]//..//ATTR[" + str(numAttr)+  "]"

# Find a CLASS object with the name matching className, and return it's PARENT ..
xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]/.."

# Select all class objects which have Zone in the name and return it's Parent (Object)
xpathSearch = "//CLASS[re:match(text(), '^Zone$')]/.."

# To print an XMLobject in text use
from lxml import etree
print(etree.tostring(XMLobject, pretty_print=True))

http://msdn.microsoft.com/en-us/library/ms256086.aspx