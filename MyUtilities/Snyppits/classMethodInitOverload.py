class MyData:
    def __init__(self, data):
        "Initialize MyData from a sequence"
        #self.data = data
    
    @classmethod
    def fromAlpha(cls, a):
        "Initialize MyData from a file"
        data = open(filename).readlines()
        return cls(data)
    
    @classmethod
    def fromBeta(cls, datadict):
        "Initialize MyData from a dict's items"
        return cls(datadict.items())
    
MyData.from
