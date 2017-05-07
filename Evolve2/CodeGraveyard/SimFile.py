"""
Created on Jan 22, 2012

Using Delegation (just accessing the File object), instead of Inheritance 
(inheriting the full class). This should make it clear and controlled. 
"""

import os

class SimFile(object):
    
    def __init__(self, baseDirectory, relPath="", mode="r"):
        self.baseDirectory = baseDirectory
        self.relPath = relPath
        self.fullPath = os.path.join(baseDirectory,relPath)
        self.fullPath = os.path.normpath(self.fullPath)
        self.mode = mode
    
    def open(self):
        self.fileObject = open(self.fullPath, self.mode)

    def close(self):
        self.fileObject.close()
        
    def delete(self):
        pass
    
    def copyAndRelink(self, newPath):
        # Copy
        return simFile(newPath)
    
    def __repr__(self):
        try:
            open(self.fullPath)
            flagExist =  "Exists"
        except IOError:
            flagExist =  "Does not Exist"
        
        return "simFile {0} at {1}".format(flagExist,self.fullPath)
    
def _test():
    myTestPath = r"c:\\test"
    myTestFile = "input.txt"
    myTestSimFile = simFile(myTestPath,myTestFile)
    
    print myTestSimFile
    
    myTestSimFile.open()
    

if __name__ == "__main__":
    _test()