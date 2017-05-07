    
class TupleVar(Variable):
    def __init__(self,vTuple,name="NoName"):

        if isinstance(vTuple,tuple):
            pass
        elif isinstance(vTuple,int):
            vTuple = (vTuple,)
        elif isinstance(vTuple, list):
            vTuple = tuple(vTuple)
        elif isinstance(vTuple, str):
            vTuple = tuple([vTuple])            
        else:
            raise Exception("Need a list, int, float, or tuple")
        
        try:
            len(vTuple)
        except:
            print 'Initialize with a list or tuple'
            raise 
        
        #assert isinstance(vTuple, tuple), "{} not a tuple".format(vTuple)
        
        super(TupleVar,self).__init__(
                                       vTuple,
                                       name,                                       
                                       )

    def getType(self):
        return "ListVar"

    def next(self):
        return 

    def __iter__(self):
        return self

class FileVariable(object):
    """
    General variable class
    
    Can function as a math variable; just call
    """
    
    def __init__(self,target,targetFile = "Main Sim File",name="NoName",vType="NoType"):
        
        self.name = name
        # Target can be REGEX or XPATH
        self.target = target
        self.targetFile = targetFile 
        self.vType = vType
        
        logging.info("Created variable - {}".format(self))

    def __str__(self):
        try:
            thisVarLength = len(self) 
        except:
            thisVarLength = float('inf')

        return "{} = '{}', target: '{}', magnitude: '{}', targetFile: '{}'".format(
                                 self.vType,
                                 self.value,
                                 self.target,
                                 thisVarLength,
                                 self.targetFile,
                                 )

class FileConstant(Variable):
    
    
    def __init__(self,target,changeTo,targetFile,name="NoName"):
        
        vType = self.getType()

        self.value = changeTo
        
        super(Constant,self).__init__(
                                       target,
                                       targetFile,
                                       name,
                                       vType,
        )

    def getType(self):
        return "SequentialList"

    def __len__(self):
        return 1
        
    def new(self):
        pass

class FileBoundedSequentialNumber(Variable):
    """
    The range is inclusive; min >= value >= max
    """
    
    def __init__(self,target,targetFile,min,resolution,max,name="NoName",):
        
        # Make sure we have STRING inputs for the decimal case
        if (
            type(min) != type(str()) or 
            type(resolution)  != type(str()) or 
            type(max) != type(str())
            ):
        
            raise TypeError('Expected a string number! This is to ensure decimal precision!')
        
        vType = self.getType()
        
        self.min = Decimal(min)
        
        self.resolution = Decimal(resolution)
        
        self.max = Decimal(max)
        
        self.value = self.getInitialValue()
       
        super(BoundedSequentialNumber,self).__init__(
                                       target,
                                       targetFile,
                                       name,
                                       vType,
        )

    def getInitialValue(self):
        return self.min

    def getType(self):
        return "BoundedSequentialNumber"
    
    def __len__(self):
        return (self.max - self.min)/(self.resolution) + 1

    def next(self):
        if self.value >= self.max:         # threshhold terminator
            raise StopIteration     # end of iteration
        else:                       # look for usable candidate
            self.value += self.resolution
        self.value = self.value

    def __iter__(self):
        return self

class FileSequentialList(Variable):
    
    def __init__(self,target,dataList,targetFile,name="NoName"):
        
        vType = self.getType()

        self.dataList = dataList
        
        self.value = self.getInitialValue()

        
        super(SequentialList,self).__init__(
                                       target,
                                       targetFile,
                                       name,
                                       vType,
        )
    
    def getInitialValue(self):
                
        self.currentIndex = self.getInitialIndex()
        
        return self.dataList[self.currentIndex]
    
    def getType(self):
        return "SequentialList"
    
    def getInitialIndex(self):
        return 0
    
    def __len__(self):
        return len(self.dataList)
        
    def next(self):
        if self.currentIndex + 1  >= len(self):         # threshhold terminator
            raise StopIteration     # end of iteration
        else:                       # look for usable candidate
            self.currentIndex += 1
        self.value = self.dataList[self.currentIndex]

    def __iter__(self):
        return self
    
class FileRandomList(FileSequentialList):
    def __init__(self,target,dataList,targetFile,name="NoName"):
        
        super(FileRandomList,self).__init__(target,dataList,targetFile,name)

    def getType(self):
        return "RandomList"
        
    def getInitialIndex(self):
        allIndices = range(0,len(self.dataList))
        return random.choice(allIndices)
    
    def __len__(self):
        return float('inf')
    
    def next(self):
        allIndices = range(0,len(self.dataList))
        self.value = self.dataList[random.choice(allIndices)]
    
    def __iter__(self):
        return self
