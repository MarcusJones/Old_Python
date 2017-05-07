'''
Created on 02.03.2011

@author: mjones
'''
from lxml import etree
from lxml.etree import XSLT,fromstring
import re

fromstring
trnXML = fromstring("""
      <Parameters>
        <PARAMETER Desc=" 1 Maximum flow rate">50</PARAMETER>
        <PARAMETER Desc=" 2 Fluid specific heat">4.19</PARAMETER>
        <PARAMETER Desc=" 3 Maximum power">60</PARAMETER>
        <PARAMETER Desc=" 4 Conversion coefficient">0.05</PARAMETER>
      </Parameters>
      """)

xsl= fromstring("""
    <stylesheet version="1.0" 
    xmlns="http://www.w3.org/1999/XSL/Transform">
    <output method="text"/>
    
     <template match="PARAMETER">Found it!</template>
    
    </stylesheet>
    """)


style = XSLT(xsl)

result = style.apply(trnXML)

print style.tostring(result)
