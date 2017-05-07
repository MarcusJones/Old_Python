'''
Created on Mar 24, 2011

@author: UserXP
'''

# Had to disable the regexTarget as a RE Pattern object, won't deepcopy!


import random
import Utilities
import logging
import math
import re
log = logging.getLogger(__name__)

class Variable(object):
    "general variable class"
    def __init__(self,name,regexTarget,type):
        self.name = name
        #self.regexTarget = re.compile(regexTarget, re.U|re.M) 
        self.regexTarget = regexTarget
        self.type = type 
        
        logging.info("Initialized a Variable object to {0}".format(self))


    
    def __str__(self):
            try:
                thisMagnitude = self.len(self) 
            except:
                thisMagnitude = 'UNDEFINED'
            
            try:
                thisValue = round(self.value,2)
            except AttributeError:
                thisValue = "UNITIALIZED"
            except TypeError:
                thisValue = self.value
            
                
            #return "{0}: '{1}'={2}, magnitude: '{3}' target: '{4}'".format(self.type,self.name,thisValue,thisMagnitude,self.regexTarget.pattern)
            return "{0}: '{1}'={2}, magnitude: '{3}' target: '{4}'".format(self.type,self.name,thisValue,thisMagnitude,self.regexTarget)

class Constant(Variable):
    def __init__(self,name,regexTarget,value):
        super(Constant,self).__init__(
                                       name,regexTarget,
                                       "Constant"
        )        
        self.value = value
        
    def __len__(self):
        return 1
        
    def new(self):
        pass
            
class FloatList(Variable):
    def __init__(self,name,regexTarget,lowerRange,step,upperRange):
        super(FloatList,self).__init__(
                                       name,regexTarget,
                                       "Float list"
        )
        self.lowerRange = lowerRange
        self.step = step
        self.upperRange = upperRange
        self.list = Utilities.frange(self.lowerRange,self.upperRange,self.step)
        self.iterIndex = 0
        
    def __len__(self):
        return len(self.list)
 
#class Float(Variable):
#    def __init__(self,name,regexTarget,lowerRange,step,upperRange):
#        super(Float,self).__init__(
#                                       name,regexTarget,
#                                       "Float"
#        )
#        self.lowerRange = lowerRange
#        self.step = step
#        self.upperRange = upperRange
#        self.list = Utilities.frange(self.lowerRange,self.upperRange,self.step)
#        self.iterIndex = 0
#        
#    def __len__(self):
#        return 0

class RandomFloat(Variable):
    '''
    http://www.ibm.com/developerworks/library/l-pycon/index.html
    '''
    
    def __init__(self,name,regexTarget,lowerRange,upperRange):
        super(RandomFloat,self).__init__(
                                       name,
                                       regexTarget,
                                       "RandomFloat",
        )
        self.lowerRange = lowerRange
        self.upperRange = upperRange
        self.iterIndex = 0
        
        
        #self.value = random.uniform(self.lowerRange, self.upperRange)
        #self.value = "UNDEFINED" 
        #random.uniform(self.lowerRange, self.upperRange)

    def new(self):
        self.value = random.uniform(self.lowerRange, self.upperRange)
        logging.info("New value for {0}".format(self.name))
    
    def __iter__(self):
        return self
    
    def next(self):
        self.value = random.uniform(self.lowerRange, self.upperRange)
        #prin self.value
        return self.value
            
    def __len__(self):
        return self.numberOfVars

class LockedRandomFloat(Variable):
    '''
    http://www.ibm.com/developerworks/library/l-pycon/index.html
    '''
    
    def __init__(self,name,regexTarget,lowerRange,upperRange,value):
        super(LockedRandomFloat,self).__init__(
                                       name,
                                       regexTarget,
                                       "LockedRandomFloat",
        )
        self.lowerRange = lowerRange
        self.upperRange = upperRange
        self.iterIndex = 0
        self.value = value

    def mutate(self,mutationRate):
        pass

class CountedRandomFloat(Variable):
    '''
    http://www.ibm.com/developerworks/library/l-pycon/index.html
    '''
    
    def __init__(self,name,regexTarget,lowerRange,upperRange,numberOfVars):
        super(CountedRandomFloat,self).__init__(
                                       name,
                                       regexTarget,
                                       "CountedRandomFloat",
        )
        self.lowerRange = lowerRange
        self.upperRange = upperRange
        self.iterIndex = 0
        self.numberOfVars = numberOfVars
        self.count = 1
        self.value = random.uniform(self.lowerRange, self.upperRange)

    def __iter__(self):
        return self
    
    def next(self):
        if self.count > self.numberOfVars:
            raise StopIteration
        else:
            self.count += 1
            self.value = random.uniform(self.lowerRange, self.upperRange)
            #prin self.value
            return self.value
            
    def __len__(self):
        return self.numberOfVars
    

class RandomStringList(Variable):
    def __init__(self,name,regexTarget,list):
        super(RandomStringList,self).__init__(
                                       name,regexTarget,
                                       "RandomStringList"
        )
        self.list = list
    
    def new(self):
        self.value = random.choice(self.list)


class LockedRandomStringList(Variable):
    def __init__(self,name,regexTarget,list,value):
        super(LockedRandomStringList,self).__init__(
                                       name,regexTarget,
                                       "LockedRandomStringList"
        )
        self.list = list
        self.value = value
        
    def mutate(self):
        self.value = random.choice(self.list)
                        
class SequentialStringList(Variable):
    def __init__(self,name,regexTarget,list):
        super(SequentialStringList,self).__init__(
                                       name,regexTarget,
                                       "SequentialStringList"
        )
        self.list = list

    def __len__(self):
        return len(self.list)
    
    def __iter__(self):
        self.iterIndex = 0
        return self
    
    # Custom iterator, the variable will return the target Regex with 
    # the current variable
    def next(self):
        if self.iterIndex < len(self.list):
            current = self.list[self.iterIndex]
        else: 
            raise StopIteration
        self.iterIndex += 1
        return (self.regexTarget,str(current))    
    
#class RandomFloat(Variable):
#    "this is a gene of type 'Random'"
#    def __init__(self,name,regexTarget,lowerRange = 0,upperRange = 1):
#        super(RandomFloat,self).__init__(
#                                       name,regexTarget,
#                                       "Random search float"
#        )
#        self.lowerRange = lowerRange
#        self.upperRange = upperRange
#        self.value = random.uniform(self.attribs['lowerRange'], self.attribs['upperRange'])

if __name__ == "__main__":
    v1 = CountedRandomFloat("A1",r"VarX1",0,60,3)
    
    print v1
    
    v2 = RandomFloat("A1",r"VarX1",0,60)
    
    v3 = RandomStringList("A3",r"DefaultMaterial",("Wood","Steel","Cheese"))
    
    print v3.value
    v3.new()
    print v3.value
    
    #print v1
    #print len(v1)
    
    print v2.value
    v2.new()
    print v2.value
    
    #print v1.value
    #print v1.value
    #print v1.value

#    for value in v1:
#        print 'Val', value
