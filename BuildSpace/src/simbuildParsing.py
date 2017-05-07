#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""This module does A and B. 
Etc.
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:
from __future__ import division    

from config import *

import xml
print xml

from lxml import etree

import logging.config
import unittest

from utility_inspect import whoami, whosdaddy, listObject

TEST_DCK = """
UNIT 3 TYPE 3     Type3b
*$UNIT_NAME Type3b
*$MODEL .\Hydronics\Pumps\Single Speed\Type3b.tmf
*$POSITION 56 192
*$LAYER Water Loop # 
PARAMETERS 5
50        ! 1 Maximum flow rate
4.19        ! 2 Fluid specific heat
60        ! 3 Maximum power
0.05        ! 4 Conversion coefficient
0.5        ! 5 Power coefficient
INPUTS 3
0,0        ! [unconnected] Inlet fluid temperature
0,0        ! [unconnected] Inlet mass flow rate
9,1         ! Type14h:Average value of function ->Control signal
*** INITIAL INPUT VALUES
20 40 1 
"""

TEST_RAD = """
void plastic red_plastic
0
0
5  .7  .05  .05  .05  .05
#  red  green  blue  specularity  roughness  #

red_plastic sphere ball
0
0
4  .7  1.125  .625  .125
"""


TEST_IDF = """
  Pump:ConstantSpeed,
    Chiller Plant ChW Circ Pump,  !- Name
    Chiller Plant ChW Supply Inlet Node,  !- Inlet Node Name
    Chiller Plant ChW Pump Outlet Node,  !- Outlet Node Name
    autosize,                !- Rated Flow Rate {m3/s}
    179352,                  !- Rated Pump Head {Pa}
    autosize,                !- Rated Power Consumption {W}
    0.9,                     !- Motor Efficiency
    0.0,                     !- Fraction of Motor Inefficiencies to Fluid Stream
    INTERMITTENT;            !- Pump Control Type
"""

some_xml_data = """
<ROOT>
<OBJECT>
  <CLASS>Pump:ConstantSpeed</CLASS>
  <ATTR desc="Name" units="">ChW Circ Pump</ATTR>
  <ATTR desc="Inlet" units="">ChW Supply Node</ATTR>
  <ATTR desc="Outlet" units="">ChW Pump Node</ATTR>
  <ATTR desc="Flow" units="m3/s">autosize</ATTR>
  <ATTR desc="Head" units="kPa">17.9</ATTR>
  <ATTR desc="Power" units="W"> autosize</ATTR>
  <ATTR desc="Efficiency" units="-">0.9</ATTR>
  <ATTR desc="Inefficiencies" units="-">0.0</ATTR>
  <ATTR desc="Control" units="">INTERMITTENT</ATTR>
</OBJECT>
<OBJECT>
  <CLASS>TEST22</CLASS>
  <ATTR desc="Inefficiencies" units="-">0.0</ATTR>
</OBJECT>
</ROOT>
"""

TEST_EPLUS_XML = """
<OBJECT>
  <CLASS>Pump:ConstantSpeed</CLASS>
  <ATTR desc="Name">ChW Circ Pump</ATTR>
  <ATTR desc="Inlet">ChW Supply Node</ATTR>
  
  <ATTR desc="Outlet">ChW Pump Node</ATTR>
  <ATTR desc="Flow", units="m3/s">autosize</ATTR>
  
  <ATTR desc="Head", units="kPa">17.9</ATTR>
  <ATTR desc="Power", units="W"> autosize</ATTR>
  <ATTR desc="Efficiency", units="-">0.9</ATTR>
  <ATTR desc="Inefficiencies", units="-">0.0</ATTR>
  <ATTR desc="Control Type">INTERMITTENT</ATTR>
</OBJECT>

<OBJECT>
  <CLASS>Pump:ConstantSpeed</CLASS>
  <ATTR desc="Name">ChW Circ Pump</ATTR>
  <ATTR desc="Inlet">ChW Supply Node</ATTR>
  
  <ATTR desc="Outlet">ChW Pump Node</ATTR>
  <ATTR desc="Flow", units="m3/s">autosize</ATTR>
  
  <ATTR desc="Head", units="kPa">17.9</ATTR>
  <ATTR desc="Power", units="W"> autosize</ATTR>
  <ATTR desc="Efficiency", units="-">0.9</ATTR>
  <ATTR desc="Inefficiencies", units="-">0.0</ATTR>
  <ATTR desc="Control Type">CONSTANT</ATTR>
</OBJECT>

<OBJECT>
  <CLASS>TEST22</CLASS>
  <ATTR desc="Name">ChW Circ Pump</ATTR>

</OBJECT>
"""


#===============================================================================
# Code
#===============================================================================
class MyClass(object):
    """This class does something for someone. 
    """
    def __init__(self, aVariable): 
        pass
    
#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):
    
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
            
    def test010_SimpleCreation(self):
        print "**** TEST {} ****".format(whoami())
        
        model = etree.fromstring(some_xml_data)
        # First, select all Pump:ConstantSpeed 
        search = "//CLASS[text()='Pump:ConstantSpeed']/.."
        constantPumps = model.xpath(search)
        for pump in constantPumps:
            search = ("//ATTR[@desc='Control' and "
             "text()='INTERMITTENT']")
            intermittentPump = pump.xpath(search)
            if intermittentPump:
                search = "//ATTR[@desc='Head']"
                pumpHead = intermittentPump[0].xpath(search)
                pumpHead[0].text = "9.5"
                
                
                
            #print intermittentPump
            #print etree.tostring(intermittentPump[0])
            #print pump.to_sting
    
            #print etree.tostring(pump)
        
        
        print etree.tostring(model)
#        results2 = model.xpath("//CLASS[.='Pump:ConstantSpeed']/../ATTR")
#        for result in results2:
#            print result.text
                
        
        
        #print model
        #model.xpath(

#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print ABSOLUTE_LOGGING_PATH
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())
    
    #print FREELANCE_DIR
    
    unittest.main()
        
    logging.debug("Finished _main".format())
    