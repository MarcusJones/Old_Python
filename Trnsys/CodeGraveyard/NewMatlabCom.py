#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""This module does stuff
Etc.
"""

#===============================================================================
# Set up
#===============================================================================
from __future__ import division        
import logging.config
from UtilityInspect import whoami, whosdaddy


import numpy as np

try:
    import win32com.client
except:
    print 'win32com in missing, please install it'
    raise

#===============================================================================
# Code
#===============================================================================


class MatlabError(Exception):
    """Raised when a Matlab evaluation results in an error inside Matlab."""
    pass

class MatlabConnectionError(Exception):
    """Raised for errors related to the Matlab connection."""
    pass


class MatlabCom(object):
    """ Manages a matlab COM client.
 
    The process can be opened and close with the open/close methods.
    To send a command to the matlab shell use 'eval'.
    To load numpy data to the matlab shell use 'put'.
    To retrieve numpy data from the matlab shell use 'get'.
    """
    def __init__(self):
        self.client = None

    def open(self, visible=False):
        """ Dispatches the matlab COM client.
     
        Note: If this method fails, try running matlab with the -regserver flag.
        """
        if self.client:
            raise MatlabConnectionError('Matlab(TM) COM client is still active. Use close to '
                                            'close it')
        self.client = win32com.client.Dispatch('matlab.application')
        self.client.visible = visible
        
    def close(self):
        """ Closes the matlab COM client.
        """
        self._check_open()
        try:
            self.eval('quit();')
        except:
            pass
        del self.client

    def eval(self, expression, identify_erros=True):
        """ Evaluates a matlab expression synchronously.

        If identify_erros is true, and the last output line after evaluating the
        expressions begins with '???' an excpetion is thrown with the matlab error
        following the '???'.
        The return value of the function is the matlab output following the call.
        """
        #print expression
        self._check_open()
        ret = self.client.Execute(expression)
        #print ret
        if identify_erros and ret.rfind('???') != -1:
            begin = ret.rfind('???') + 4
            end = ret.find('\n', begin)
            raise MatlabError(ret[begin:end])        
        return ret

    def get(self, names_to_get, convert_to_numpy=True):
        """ Loads the requested variables from the matlab com client.
     
        names_to_get can be either a variable name or a list of variable names.
        If it is a variable name, the values is returned.
        If it is a list, a dictionary of variable_name -> value is returned.
     
        If convert_to_numpy is true, the method will all array values to numpy
        arrays. Scalars are left as regular python objects.
     
        """
        self._check_open()
        single_itme = isinstance(names_to_get, (unicode, str))
        if single_itme:        
            names_to_get = [names_to_get]
        ret = {}
        for name in names_to_get:
            ret[name] = self.client.GetWorkspaceData(name, 'base')
            # TODO(daniv): Do we really want to reduce dimensions like that? what if this a row vector?
            while isinstance(ret[name], (tuple, list)) and len(ret[name]) == 1:
                ret[name] = ret[name][0]
            if convert_to_numpy and isinstance(ret[name], (tuple, list)):
                ret[name] = np.array(ret[name])
        if single_itme:
            return ret.values()[0]
        return ret

    def put(self, name_to_val):
        """ Loads a dictionary of variable names into the matlab com client.        
        """
        self._check_open()
        for name, val in name_to_val.iteritems():
            # First try to put data as a matrix:
            try:
                self.client.PutFullMatrix(name, 'base', val, None)
            except:
                self.client.PutWorkspaceData(name, 'base', val)

    def _check_open(self):
        if not self.client:
            raise MatlabConnectionError('Matlab(TM) process is not active.')


#===============================================================================
# Unit testing
#===============================================================================

def _testing():
    logging.debug("RUNNING TESTS {}")
    matlab = MatlabCom()
    matlab.open()
    print matlab
    for i in xrange(100):
        ret = matlab.eval('disp \'hiush world%s\';' % ('b'*i))
        print ret
    
    matlab.put({'A' : [1, 2, 3]})
    ret = matlab.eval('A')
    print ret
    
    ret = matlab.eval("surf(peaks)")
    
    ret = matlab.eval("pause(4000)")
    
    ret = matlab.eval(
    """
    while true
    a = 1
    end
    """
    )
    
    logging.debug("FINISHED TESTS {}")
        
#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
        logging.config.fileConfig('..\\..\\MyUtilities\\LoggingConfig\\loggingNofile.conf')
        myLogger = logging.getLogger()
        myLogger.setLevel("DEBUG")

        logging.debug("Started _main".format())

        _testing()
        
        logging.debug("Started _main".format())
        