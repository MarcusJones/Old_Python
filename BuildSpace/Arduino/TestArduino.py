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

import logging.config
import unittest

from utility_inspect import whoami, whosdaddy, listObject
#import serial as ser
from serial import Serial 
import time
#===============================================================================
# Code
#===============================================================================
class MyClass(object):
    """This class does something for someone. 
    """
    def __init__(self, aVariable): 
        pass
    
class MySubClass(MyClass):
    """This class does
     
    """
    def __init__(self, aVariable): 
        super(MySubClass,self).__init__(aVariable)
    def a_method(self):
        """Return the something to the something."""
        pass


#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):
    
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
    @unittest.skip("")
    def test010_Test(self):
        ## import the serial library
        print "**** TEST {} ****".format(whoami())    
        ## Boolean variable that will represent 
        ## whether or not the arduino is connected
        connected = False
        
        ## open the serial port that your ardiono 
        ## is connected to.
        ser = Serial("COM5", 9600)
        logging.debug("Created {}".format(ser))
        
        ## loop until the arduino tells us it is ready
        while not connected:
            serin = ser.read()
            connected = True

        
        ## Tell the arduino to blink!
        ser.write("1")
        logging.debug("Wrote 1 {}".format(ser))
        
        ## Wait until the arduino tells us it 
        ## is finished blinking
        while ser.read() == '1':
            ser.read()
        
        ## close the port and end the program
        ser.close()
        logging.debug("Closed {}".format(ser))
                
    #@unitttest.skip("")
    def test020_Test(self):
        ser = Serial("COM5", 9600)
        logging.debug("Created {}".format(ser))
        
        #5 volts over 10 bits
        resolution = 5 / (2**10) # V / bit
        resolution = resolution * 1000
        logging.debug("5 volts over 10 bits = {} millivolts per bit".format(resolution))
        
        #logging.debug("5 volts over 10 bits = {} Volts per decimal input".format(resolution))
                
        for i in range(10):
            logging.debug("Read line {}".format(ser))
            decimalIn = ser.readline()
            decimalIn = float(decimalIn)
            
            #print "Raw V:", raw_volts_V
            raw_mV = decimalIn * resolution
            print "Raw mV", raw_mV
            # 10 mV per degC
            temp_C = raw_mV / 100

            print "Temp C: {:.3f}".format(temp_C)
            
            #time.sleep(0.05)
            
        ser.close()
        logging.debug("Closed {}".format(ser))                

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
    