        
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
#        super(RandomFloat,self).__init__(
#                                       name,
#                                       regexTarget,
#                                       "RandomFloat",
#        )
#        self.lowerRange = lowerRange
#        self.upperRange = upperRange
#        self.iterIndex = 0
#        
#        
#        #self.value = random.uniform(self.lowerRange, self.upperRange)
#        #self.value = "UNDEFINED" 
#        #random.uniform(self.lowerRange, self.upperRange)
#
#    def new(self):
#        self.value = random.uniform(self.lowerRange, self.upperRange)
#        logging.info("New value for {0}".format(self.name))
#    
#    def __iter__(self):
#        return self
#    
#    def next(self):
#        self.value = random.uniform(self.lowerRange, self.upperRange)
#        #prin self.value
#        return self.value
#            
#    def __len__(self):
#        return self.numberOfVars
#
#class LockedRandomFloat(Variable):
#    '''
#    http://www.ibm.com/developerworks/library/l-pycon/index.html
#    '''
#    
#    def __init__(self,name,regexTarget,lowerRange,upperRange,value):
#        super(LockedRandomFloat,self).__init__(
#                                       name,
#                                       regexTarget,
#                                       "LockedRandomFloat",
#        )
#        self.lowerRange = lowerRange
#        self.upperRange = upperRange
#        self.iterIndex = 0
#        self.value = value
#
#    def mutate(self,mutationRate):
#        pass
#
#class CountedRandomFloat(Variable):
#    '''
#    http://www.ibm.com/developerworks/library/l-pycon/index.html
#    '''
#    
#    def __init__(self,name,regexTarget,lowerRange,upperRange,numberOfVars):
#        super(CountedRandomFloat,self).__init__(
#                                       name,
#                                       regexTarget,
#                                       "CountedRandomFloat",
#        )
#        self.lowerRange = lowerRange
#        self.upperRange = upperRange
#        self.iterIndex = 0
#        self.numberOfVars = numberOfVars
#        self.count = 1
#        self.value = random.uniform(self.lowerRange, self.upperRange)
#
#    def __iter__(self):
#        return self
#    
#    def next(self):
#        if self.count > self.numberOfVars:
#            raise StopIteration
#        else:
#            self.count += 1
#            self.value = random.uniform(self.lowerRange, self.upperRange)
#            #prin self.value
#            return self.value
#            
#    def __len__(self):
#        return self.numberOfVars
#    
#
#class RandomStringList(Variable):
#    def __init__(self,name,regexTarget,list):
#        super(RandomStringList,self).__init__(
#                                       name,regexTarget,
#                                       "RandomStringList"
#        )
#        self.list = list
#    
#    def new(self):
#        self.value = random.choice(self.list)
#
#
#class LockedRandomStringList(Variable):
#    def __init__(self,name,regexTarget,list,value):
#        super(LockedRandomStringList,self).__init__(
#                                       name,regexTarget,
#                                       "LockedRandomStringList"
#        )
#        self.list = list
#        self.value = value
#        
#    def mutate(self):
#        self.value = random.choice(self.list)
#                        
#class SequentialStringList(Variable):
#    def __init__(self,name,regexTarget,list):
#        super(SequentialStringList,self).__init__(
#                                       name,regexTarget,
#                                       "SequentialStringList"
#        )
#        self.list = list
#
#    def __len__(self):
#        return len(self.list)
#    
#    def __iter__(self):
#        self.iterIndex = 0
#        return self
#    
#    # Custom iterator, the variable will return the target Regex with 
#    # the current variable
#    def next(self):
#        if self.iterIndex < len(self.list):
#            current = self.list[self.iterIndex]
#        else: 
#            raise StopIteration
#        self.iterIndex += 1
#        return (self.regexTarget,str(current))    
#    
##class RandomFloat(Variable):
##    "this is a gene of type 'Random'"
##    def __init__(self,name,regexTarget,lowerRange = 0,upperRange = 1):
##        super(RandomFloat,self).__init__(
##                                       name,regexTarget,
##                                       "Random search float"
##        )
##        self.lowerRange = lowerRange
##        self.upperRange = upperRange
##        self.value = random.uniform(self.attribs['lowerRange'], self.attribs['upperRange'])

