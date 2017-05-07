
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
from __future__ import print_function

from config import *

import logging.config
import unittest
import psutil

from utility_inspect import whoami, whosdaddy, listObject

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

def some_function():
    """Return the something to the something."""
    pass

#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):

    def setUp(self):
        print("**** TEST {} ****".format(whoami()))

    def test000_disk(self):


    def test010_disk(self):
        print("**** TEST {} ****".format(whoami()))
        print(psutil.disk_partitions())
        print(psutil.disk_usage('/'))

    def test020_memory(self):
        print(psutil.virtual_memory())

    def test030_netstat(self):
        print("**** TEST {} ****".format(whoami()))
        print("IO")
        io_list = [(k,v) for (k,v) in psutil.net_io_counters(pernic=True).iteritems()]
        print("{:50} - {}".format(*io_list[0]))
        print("{:50} - {}".format(*io_list[-1]))


    def test040_netstat(self):
        print("**** TEST {} ****".format(whoami()))
        print("NETSTAT")
        #print(psutil.net_)
        #print(type(psutil.net_connections()[0]))
        this_conn = psutil.net_connections()[0]
        print(this_conn)
        print("{:30} : {}".format("File descriptor", this_conn.fd))
        print("{:30} : {}".format("Family", this_conn.family))
        print("{:30} : {}".format("Type", this_conn.type))
        print("{:30} : {}".format("Local address", this_conn.laddr))
        print("{:30} : {}".format("Remote address", this_conn.raddr))
        print("{:30} : {}".format("Status", this_conn.status))
        print("{:30} : {}".format("Process ID", this_conn.pid))
        this_pid = this_conn.pid
        print("{:30} : {}".format("***", "********"))
        print("{:30} : {}".format("This PID exists",psutil.pid_exists(this_pid)))
        this_process = psutil.Process(this_pid)
        print("{:30} : {}".format("Process object",this_process))
        #print("{:30} : {}".format("Process EXE",this_process.exe()))
        #print("{:30} : {}".format("Process name",this_process.name()))

        #print("{:30} : {}".format("Process name",this_process.name)
        #print(psutil.net_connections()[-1])
        #for conn in psutil.net_connections():
        #    print(dir(conn))
        #    break
        #    print("{}".format(conn))

    def test050_psutil_test(self):
        print("**** TEST {} ****".format(whoami()))

        psutil.test()

    def test060_processes(self):
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name'])
            except psutil.NoSuchProcess:
                pass
            else:
                print(pinfo)

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
