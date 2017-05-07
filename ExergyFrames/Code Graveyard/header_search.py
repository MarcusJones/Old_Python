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
from __future__ import division    
import logging.config
from UtilityInspect import whoami, whosdaddy

from exergy_frame import getMask, maskUnion, maskIntersect
import unittest
#===============================================================================
# Code
#===============================================================================

def maskUnion():
    pass
def maskIntersect():
    pass
def getMask(headerDef,searchStr):
    pass

class Node(object):
    def __init__(self,leftChild,rightChild,search_pair,nodeFunc):
        #self.nodeType     = nodeType     
        self.leftChild    = leftChild    
        self.rightChild   = rightChild   
        self.search_pair = search_pair
        self.nodeFunc    = nodeFunc
        
    def __and__(self,other):
        """
        This is a bitwise intersection
        """
        return Node(self,other,None,intersect)
    
    def __or__(self,other):
        """
        This is a bitwise union
        """
        return Node(self,other,None,union)


def idx(headerDef,searchStr):
    searchPair = (headerDef,searchStr)
    return Node(None,None,searchPair,None)

def printSearch(node,X=None):
    if not X:
        X = ""
    if not node.nodeFunc:
        pairStr = "{}={}".format(node.search_pair[0],node.search_pair[1])
        return( pairStr )
    else:
        return  "{} *{}* {}".format(printSearch(node.leftChild,X), 
            str(node.nodeFunc.__name__),
            printSearch(node.rightChild,X))

def evaluateNode(node,X=None):
    if not X:
        X = 0
    if node.nodeType == "Constant":
        return(node.constantData)
    elif node.nodeType == "AND":
        return evaluateNode(node.leftChild,X) + evaluateNode(node.rightChild,X)
    elif node.nodeType == "XOR":
        return evaluateNode(node.leftChild,X) / evaluateNode(node.rightChild,X)
    else:
        raise        


#===============================================================================
# Unit testing
#===============================================================================

class testSearch(unittest.TestCase):
    def test010_SimpleCreation(self):
        print "**** TEST {} ****".format(whoami())
        n2 = idx("name","Temperature")
        n3 = idx("sensor","x45")
        n4 = idx("units","C")    
             
        #n1 = Node("AND",n2,n3,None)
        n1 = n2 & n3 | n4
        print printSearch(n1)
        #print "{} = {}".format(printSearch(n1), evaluateNode(n1))
        #assert(evaluateNode(n1) == 15)
        
#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    logging.config.fileConfig('..\\..\\LoggingConfig\\loggingNofile.conf')
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())

    unittest.main()
        
    logging.debug("Started _main".format())
    