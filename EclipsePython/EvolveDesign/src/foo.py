'''
Created on 29.03.2011

@author: mjones
'''

import logging
import bar

LOG_FILENAME = '..\\Log files\\spam.log'

#log = logging.getLogger()
#hdlr = logging.FileHandler(LOG_FILENAME)
##formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#hdlr.setFormatter(formatter)
#log.addHandler(hdlr) 

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=LOG_FILENAME,
                    filemode='w')

logging.debug('This message should go to the log file')

#log.debug('This message should go to the log file')

bar.some_function()

a = bar.ClassA()