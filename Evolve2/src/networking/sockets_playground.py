#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================
from __future__ import division
from __future__ import print_function
"""This module does A and B.
Etc.
"""


"""
http://www.co-pylit.org/courses/ITSE1359/Networking/index.html
http://www.binarytides.com/python-socket-programming-tutorial/
"""


#===============================================================================
# Set up
#===============================================================================
# Standard:



from config import *

import logging.config
import unittest

from utility_inspect import whoami, whosdaddy, listObject

import urllib2
import re

import socket   #for sockets
import sys  #for exit

#===============================================================================
# Code
#===============================================================================
def get_local_ip():
    """Alias for a socket function
    """
    return socket.gethostbyname(socket.gethostname())

def get_external_ip_BROKEN():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('google.com', 80))
    ip = sock.getsockname()[0]
    sock.close()
    return ip

def check_connection():
    """Check internet connection by opening google.com
    """
    try:
        urllib2.urlopen("http://www.google.com").close()
    except urllib2.URLError:
        return False
    else:
        return True

def get_external_ip():
    """Use an external service to check IP address
    Regex match the returned HTML document for IP
    """

    f = urllib2.urlopen("http://www.canyouseeme.org/")
    html_doc = f.read()
    f.close()
    m = re.search('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',html_doc)
    return m.group(0)


def this_sock():
    try:
        #create an AF_INET, STREAM socket (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
        sys.exit();

    print('Socket Created: {}'.format(s))

    host = 'www.google.com'

    try:
        remote_ip = socket.gethostbyname( host )

    except socket.gaierror:
        #could not resolve
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    return('Ip address of ' + host + ' is ' + remote_ip)

#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print(ABSOLUTE_LOGGING_PATH)
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)


    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())

    #print FREELANCE_DIR

    unittest.main()

    logging.debug("Finished _main".format())


