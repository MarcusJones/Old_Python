'''
Created on 08.06.2011

@author: mjones
'''

import re
from copy import deepcopy

class VariableWithRE(object):
    "general variable class"
    def __init__(self,name,regexTarget,type):
        self.name = name
        self.regexTarget = re.compile(regexTarget, re.U|re.M) 
        self.type = type 
        
    def __deepcopy__(self,memo):
        return VariableWithRE(self.name, self.regexTarget, self.type)

class VariableWithoutRE(object):
    "general variable class"
    def __init__(self,name,regexTarget,type):
        self.name = name
        self.regexTarget = regexTarget
        self.type = type 

    def __deepcopy__(self,memo):
        return VariableWithoutRE(self.name, self.regexTarget, self.type)
       
if __name__ == "__main__":

    myVariable = VariableWithoutRE("myName","myRegexSearch","myType")
    print myVariable.regexTarget
    myVariableCopy = deepcopy(myVariable)
    
    #re.compile(regexTarget, re.U|re.M) 
    
    myVariable = VariableWithRE("myName","myRegexSearch","myType")
    print myVariable.regexTarget
    myVariableCopy = deepcopy(myVariable)
    
        
    
    

