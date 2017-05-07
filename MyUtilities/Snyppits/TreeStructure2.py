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
import unittest


nodeTypes = ("Constant","AND","XOR")



class Node(object):
    def __init__(self,nodeType,leftChild,rightChild,constantData,nodeFunc):
        self.nodeType     = nodeType     
        self.leftChild    = leftChild    
        self.rightChild   = rightChild   
        self.constantData = constantData 
        self.nodeFunc     = nodeFunc
    def __and__(self,other):
        return Node("AND",self,other,None,)
    def __or__(self,other):
        return Node("XOR",self,other,None)
    
    def union(self):
        pass
    def intersect(self):
        pass
        
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

def printNode(node,X=None):
    if not X:
        X = ""
    if node.nodeType == "Constant":
        return( str(node.constantData) )
    elif node.nodeType == "AND":
        return  printNode(node.leftChild,X) + " AND " + printNode(node.rightChild,X)
    elif node.nodeType == "XOR":
        return  printNode(node.leftChild,X) + " XOR " + printNode(node.rightChild,X)
    else:
        raise      

def getLeaf(value):
    return Node("Constant",None,None,value)

class testTree(unittest.TestCase):
    def setUp(self):
        logging.debug("Setup".format())
        
        
        
    def test01_index(self):
        n2 = getLeaf(2)
        n3 = getLeaf(3)
        n4 = getLeaf(10)    
             
        #n1 = Node("AND",n2,n3,None)
        n1 = n2 & n3 & n4
        print "{} = {}".format(printNode(n1), evaluateNode(n1))
        assert(evaluateNode(n1) == 15)
        
        n1 = (n2 & n3) | n4
        print "{} = {}".format(printNode(n1), evaluateNode(n1))
        assert(evaluateNode(n1) == 0.5)

    
        n0 = n3 | n4  & n2 
        print "{} = {}".format(printNode(n1), evaluateNode(n1))
        
#        nA = n0 & ( n1 | n0 ) 
#        print "{} = {}".format(printNode(nA), evaluateNode(nA)) 
#        
              
if __name__ == "__main__":
    logging.config.fileConfig('..\\..\\MyUtilities\\LoggingConfig\\loggingNofile.conf')
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")
        
    logging.debug("Started _main".format())

    unittest.main()

    logging.debug("Finished _main".format())
        
    

    


        
class Idx(object):
    """This class does something for someone.
    
    Basic data structure is a list of pairs, where each pair is
    [header definition, the search value regex]
    
    This concept is applied twice, one list of pairs is for Union operations
    The other list of pais is for Intersect operations
    
     
    
    An Idx can only be instantiated created with ONE pair 
    
    Composite Idx can be created with operators;
    
    Idx1 & Idx2 | Idx3
    Idx1 & Idx2 | Idx3
    Idx1 & (Idx2 | Idx3)
    
    self ^ other     __xor__(self, other)
    self | other     __or__(self, other)

    """
    
    def __init__(self, headerDef=None, headerVal=None): 
        self.search_pair = (headerDef, headerVal)     
#        if not search_pairs:
#            self.search_pairs = ((headerDefs, "union", headerValues))
#        elif search_pairs:
#            for pair in search_pairs:
#                raise
#                self.search_pairs = search_pairs
#        else:
#            raise Exception("ERROR")
#        #print "New IDX",self.searchPairs
        self.index = 0
        
#    @classmethod
#    def fromTuple(cls, pairs):
#        #cls.searchPairs = pairs
#        return cls(None,None,pairs)
        
    def __str__(self):
        return str(self.search_pairs)
#    
#    def __add__(self, other):
#        raise
#        totalPairs = self.search_pairs + other.search_pairs
#        return self.__class__.fromTuple(totalPairs)

    def __and__(self, other):
        pass
#
#    
#    def __xor__(self, other):
#        pass
#    
#    def __or__(self, other):
#        pass
#    
    
    """    
    
    
    def __iter__(self):
        return self
        
    def next(self):
        try:
            result = self.search_pairs[self.index]
        except IndexError:
            # Reset for next time!
            self.index = 0
            raise StopIteration
        self.index+=1
        return result
 
#class DataFrameList(object):
#    """
#    AnalysisData consists of a matrix of size n-timeStepRows and m-DataColumns
#    Also has a n-length timeVector, and m-length headers and units
#    """
#    def __init__(self, 
#                 name,
#                 dataArray, 
#                 timeSeriesArray, 
#                 headersArray, 
#                 headersDef,
#                 ):
#        self.name = name
#        self.dataArray       = dataArray      
#        self.timeSeriesArray = timeSeriesArray
#        self.headersArray    = headersArray
#        self.headersDef = headersDef
#        
#        logging.info("{} Data: {} Time: {} Headers: {}".format(self.name, self.dataStr(),
#                                       self.timeStr(),
#                                       self.headStr(),
#                                       ))
#    def dataStr(self):
#        return np.shape(self.dataArray)
#    
#    def timeStr(self):
#        return np.shape(self.timeSeriesArray)
#    
#    def headStr(self):
#        return np.shape(self.headersArray)





class testIdx(unittest.TestCase):
    def setUp(self):
        print "**** {} ****".format(whoami())
        
    def test01_index(self):
        print "**** TEST {} ****".format(whoami())
        

        t1 = Tree("Attrib1","alp")
        t2 = Tree("Attrib2","quick")
        
        print t1, t2
        
        print t1 & t2
        
        #Tree(left, operator, right)
        
        #searchIdx = Idx("Attrib1","alp") & Idx("dd","asdf")
        #searchIdx = Idx.fromTuple("Attrib1","alp")
        #print searchIdx
        
        #searchIdx = Idx("Attrib1","alp") & Idx("dd","asdf")
        #print searchIdx
    