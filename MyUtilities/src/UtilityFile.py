'''
Created on 2012-03-24

@author: Anonymous
'''
import logging.config
import os
import re
import shutil
import errno
import unittest
from utility_inspect import whoami, whosdaddy, listObject
import zipfile,os.path


#class SearchReplace(object):
#    def __init__(self, regex, value):
#        self.searchRegex = regex
#        self.value = value
#        
#    def __str__(self):
#        return "{} -> {}".format(self.searchRegex, self.value)
#
#    def __repr__(self):
#        return "{} -> {}".format(self.searchRegex, self.value)

#class SRInFileSuffix(object):
#    def __init__(self, regex, value, fileSuffix):
#        """
#        Same as SearchReplace, but with a file target
#        """
#        self.fileSuffix = fileSuffix
#        self.searchRegex = regex
#        self.value = value
#        
#    def __str__(self):
#        return "{} -> {} in {}".format(self.searchRegex, self.value, self.fileSuffix)
#
#    def __repr__(self):
#        return "{} -> {} in {}".format(self.searchRegex, self.value, self.fileSuffix)

#class Target(object):
#    def __init__(self,file, regex, value):
#        self.targetFile = file
#        self.searchRegex = regex
#        self.replaceValue = value
#        
#    def __str__(self):
#        return "{} -> {} in {}".format(self.searchRegex, self.replaceValue,self.targetFile)
#
#    def __repr__(self):
#        return "{} -> {} in {}".format(self.searchRegex, self.replaceValue,self.targetFile)

#    def makeReplacement(self,inThisFile):
#        # Open file
#        fIn = open(inThisFile,'r')
#        # Read it
#        fileData = fIn.read()
#        fIn.close()
#
#        # Search it
#        #matches = re.findall(self.searchRegex, fileData)
#        
#        # Count occurances
#        #print self.searchRegex
#        matches = re.findall(self.searchRegex, fileData)
#        
#        if not matches:
#            raise Exception("No matches in file")
#        elif len(matches) > 1:
#            pass
#            #raise Exception("More than one match ({}) for {}".format(len(matches),matches))
#        
#        #re.findall(pattern, string, flags)
#
#        #matches = re.findall(self.searchRegex, fileData)
#
#        # Search and sub it
#        fileData = re.sub(self.searchRegex, str(self.replaceValue), fileData)
#
#        # Write it back
#        outF = open(inThisFile,'w')
#        outF.write(fileData)
#        outF.close()
#
#        logString = "{} replacement for {} in {}".format(len(matches), self, inThisFile)
#        #logging.debug(logString)        
#    
#class FileWithDir(object):
#    def __init__(self,fileName, directory):
#        self.fileName = fileName
#        self.directory = directory
#        self.fullFilePath = os.path.join(self.directory,self.fileName)
#    
#    def copyTo(self,destinationPath):
#        shutil.copy(self.fullFilePath,destinationPath)
#    
#    def __str__(self):
#        return "{} in {}".format(self.fileName, self.directory )
#
#    def __repr__(self):
#        return "File {} in {}".format(self.fileName, self.directory )


def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''): continue
                path = os.path.join(path, word)
            zf.extract(member, path)


class FileObject(object):
    def __init__(self,filePath):
        """
        File wrapper
        Needs a path
        """
        self.filePath =os.path.normpath(filePath) 
        #self.fileData = None
        self.lines = None
        logString = "Created {0}".format(self)
        logging.debug(logString)
        
        
#    def loadData(self):
#        #prin 'reading:', self.inputFileTemplatePath
#        fIn = open(self.inputFilePath,'r')
#        # Don't read unicode... inputFileTemplate=unicode(fIn.read(),'utf-8')
#        self.fileData=fIn.read()
#        fIn.close()
#        logString = "File data loaded for {0}".format(self)
#        logging.debug(logString)

#    def writeData(self):
#        outF = open(self.outputFilePath,'w')
#        outF.write(self.fileData)
#        outF.close()
#        # Free up that memory
#        self.fileData = "UNDEFINED"        
#        logString = "File data written for {0}".format(self)
#        logging.debug(logString)

    def __str__(self):
        return "File Object; exists={}, file={}, input path: {}".format(self.exists(), self.isFile(), self.filePath)
    
    def isFile(self):
        return os.path.isfile(self.filePath)
    
    def exists(self):
        #os.path.exists(self.filePath)
        return os.path.exists(self.filePath)
    
    def loadLines(self):
        if not self.exists():
            raise Exception("Problem on open; this file does not exist! ")
        elif not self.isFile():
            raise Exception("Problem on open; this is a directory! ")
        
        fIn = open(self.filePath,'r')
        self.lines = fIn.readlines()
        fIn.close()

        logging.debug("{} lines of text loaded for {}".format(len(self.lines),self))        
        
    def loadAllTextOLD(self):
        """
        Load the text into memory
        """
        
        
        if not self.exists():
            raise Exception("Problem on open; this file does not exist! ")
        elif not self.isFile():
            raise Exception("Problem on open; this is a directory! ")
        
        fIn = open(self.filePath,'r')
        
        # Don't read unicode... inputFileTemplate=unicode(fIn.read(),'utf-8')
        self.fileData=fIn.read().decode('ISO-8859-1')
        #self.fileData.decode()
        #self.fileData = self.fileData.encode('utf-8')
        fIn.close()
        logString = "{} lines of text loaded for {}".format(len(self.fileData),self)
        logging.debug(logString)        

    def copyToSameDir(self,newFileName):
        """
        Copy the file in the path to a new path, create and return this new path
        as a new FileObject
        """
        #print "Basename:", os.path.basename(self.filePath)
        #print "Dirname:", os.path.dirname(self.filePath)
        #print "Realpath:", os.path.realpath(self.filePath)
        #print "Split:", os.path.splitext(self.filePath)
        #print "Extension:", os.path.splitext(self.filePath)[1]

        thisDirPath = os.path.dirname(self.filePath)
        targetPath = os.path.join(thisDirPath,newFileName)
        
        # =os.path.normpath(self.filePath) 
        shutil.copyfile(self.filePath, targetPath)
        #copyfile(src, dst)
        
        return FileObject(targetPath)
        
    def copyToFullPath(self,newPathName):
        """
        Copy the file in the path to a new path, create and return this new path
        as a new FileObject
        """        
        #print "Basename:", os.path.basename(self.filePath)
        #print "Dirname:", os.path.dirname(self.filePath)
        #print "Realpath:", os.path.realpath(self.filePath)
        #print "Split:", os.path.splitext(self.filePath)
        #print "Extension:", os.path.splitext(self.filePath)[1]
        
        # Could ensure that it exists (??)
        #if not os.path.exists(newPathName):
        #    raise Exception("This directory does not exist!")
        
        targetPath = newPathName
        
        # =os.path.normpath(self.filePath) 
        #print targetPath
        shutil.copyfile(self.filePath, targetPath)
        #copyfile(src, dst)
        
        logString = "Copied {} to {}".format(self,newPathName)
        logging.debug(logString)
                
        return FileObject(targetPath)

    def printLines(self,lines=None):
        for line in self.lines:
            print line.strip()
    
    
    def writeFile(self, outpath):
        outF = open(outpath,'w')
        
        outF.write("".join(self.lines))
        outF.close()
        
        logString = "Wrote {}".format(outpath)
        logging.debug(logString)
    
    def getMatch(self,regexStr):
        matches = list()
        
        # First, make sure the file text is loaded 
        if not self.lines:
            self.loadLines()
        
        matched_line = None        
        for line in self.lines:
            thisMatch = re.search(regexStr,line,re.VERBOSE)
            if thisMatch:
                matched_line = thisMatch.group()
                break
        
        if not matched_line:
            raise Exception("Could not find {} in {}".format(regexStr,self))
            
        return matched_line

        
    def makeReplacements(self,replacements):
        """
        """
        # replacements should be a list
        assert replacements[0][0]
        
        if isinstance(replacements, basestring):
            replacements = list().append(replacements) 
        
        # First, make sure the file text is loaded 
        if not self.lines:
            self.loadLines()

        # Search and sub for each replacement
        newLines = []
        
        for repl in replacements:
            repl.append(0)
        
        for line in self.lines:
            newLine = line
            # Check this line for all replacements
            for repl in replacements:
                # First check ahead if it matches anywhere
                match = re.search(repl[0], line)
                if match:
                    repl[2] += 1
                    # Then do the sub
                    newLine = re.sub(repl[0], str(repl[1]), newLine)
            # Append it
            newLines.append(newLine)
        self.lines = newLines
        
        for repl in replacements:
            logging.debug("{} -> {} replaced in {} lines".format(repl[0], repl[1],  repl[2]))
        
#        for repl in replacements:
#            matchCount = 0
#            matchCount = 0
#            for line in self.lines:
#                match = re.search(repl[0], line)
#                if match:
#                    matchCount = matchCount + 1
#                newLines.append(re.sub(repl[0], str(repl[1]), line))
#        
        
    
    def makeReplacementsOLD(self,replacements):
        """
        Reads the file data
        Make the given n replacements
        Writes the file again!
        Optimization: Currently makes n passes, could be just one!
        
        replate 
        """
        # replacements should be a list
        if isinstance(replacements, basestring):
            replacements = list().append(replacements) 
        
        # First, make sure the file text is loaded 
        if not self.fileData:
            self.loadAllText()
        #print self.fileData 
        
        # Now count the matches for all replacements
        matchCount = 0
        for repl in replacements:
            #print repl
            matches = re.findall(repl[0], self.fileData)
            #print self.fileData
            #matches = re.search("FIND1", self.fileData)
            #print matches
            #print len(matches)
            #print re.sub(repl.searchRegex, str(repl.replaceValue))
            matchCount = matchCount + len(matches)
        
        # Make sure we have at least one match
        if not matchCount:
            raise Exception("Not a single match in file! \n {} \n {}".format(self,replacements))
        
        # We could also limit the maximum number of matches
        elif matchCount > 1:
            pass
            #raise Exception("More than one match ({}) for {}".format(len(matches),matches))

        # Search and sub for each replacement
        for repl in replacements:
            self.fileData = re.sub(repl[0], str(repl[1]), self.fileData)
        logString = "{} replacement for {}".format(matchCount, self)
        logging.debug(logString)
        
#        # Write it back 
#        outF = open(self.filePath,'w')
#        outF.write(self.fileData)
#        outF.close()
#
        

class FileObjectBaseSuffix(FileObject):
    def __init__(self,baseFilePath,suffixFilePath):
        """
        File wrapper
        Needs a path
        """
        #print baseFilePath, suffixFilePath
        filePath =os.path.normpath(baseFilePath+suffixFilePath) 
        #print filePath
        self.baseFilePath = baseFilePath
        self.suffixFilePath = suffixFilePath
        
        super(FileObjectBaseSuffix, self).__init__(filePath)
    
    def changeBase(self,newBasePath):
        self.filePath = os.path.join(newBasePath,self.suffixFilePath) 
        
    def changeSuffix(self,newSuffixPath):
        self.filePath = os.path.join(self.baseFilePath,newSuffixPath) 

    def copyToNewBasePath(self,newBasePath):
        """
        Copy the file in the path to a new base, create and return this new path
        as a new FileObject
        """        
        #print "1", newBasePath
        #print "2", self.suffixFilePath
        newPathName = os.path.join(newBasePath,self.suffixFilePath) 
        targetPath = newPathName
        
        # =os.path.normpath(self.filePath) 
        #print targetPath
        
        newDirectoryPath = os.path.dirname(newPathName)
        #print os.path.basename(newPathName)
        
        # Make the directory tree if doesn't exist
        try:
            os.makedirs(newDirectoryPath)
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise

        shutil.copyfile(self.filePath, targetPath)
        #copyfile(src, dst)
        
        return FileObjectBaseSuffix(newBasePath,self.suffixFilePath)
    
#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):
    
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
            
    def test010_SimpleCreation(self):
        print "**** TEST {} ****".format(whoami())

        testPath = r"C:\Eclipse\MyUtilities\TestingFiles\TestText.txt"
        thisObj = FileObject(testPath)
        thisObj.loadLines()
        thisObj.printLines()

        replacements = [[r"^WALL EXT_WALL$", "WALL REPLACED_WALL"],
                        [r"FRONT", "PIZZA"]]
        
        [
         [r"^WALL EXT_WALL$", "WALL REPLACED_WALL"],
         ]
        
        # Aft
        thisObj.makeReplacements(replacements)
        thisObj.printLines()
        
def _test1():
    logging.debug("Started _test1".format())
    
    replace1 = SearchReplace("FIND1","Apples!!!!!!!!!!!!!!!!!!")
    replace2 = SearchReplace("FIND2","**********************BEACH(((((((((")
    
    replaceVector = [replace1, replace2]
    
    thisPath = r'D:\Freelancing\Project Expansion Test Dir2\0.3_0.3_0.5_0.1_0.1_1.0_1.0\0.3_0.3_0.5_0.1_0.1_1.0_1.0_1.eso'
    thisPath = r'D:\Freelancing\Project Expansion Test Dir2\0.3_0.3_0.5_0.1_0.1_1.0_1.0\\'
    thisPath = r"D:\Freelancing\TestFileObject\thisTestFile.txt"
    
    template = FileObject(thisPath)
    #newFileObj.loadAllText()
    #template.copyToFullPath("Test2.text")
    
    workingFile = template.copyToSameDir("Test2.text")
    workingFile.makeReplacements(replaceVector)
    
    logging.debug("Finished _test1".format())

def _test2():
    logging.debug("Started _test1".format())
    
    replace1 = ("FIND1","Apples!!!!!!!!!!!!!!!!!!")
    replace2 = ("FIND2","**********************BEACH(((((((((")
    
    replaceVector = [replace1, replace2]
    
    thisPath = r'D:\Freelancing\Project Expansion Test Dir2\0.3_0.3_0.5_0.1_0.1_1.0_1.0\0.3_0.3_0.5_0.1_0.1_1.0_1.0_1.eso'
    thisPath = r'D:\Freelancing\Project Expansion Test Dir2\0.3_0.3_0.5_0.1_0.1_1.0_1.0\\'
    thisPath = r"D:\Freelancing\TestFileObject\thisTestFile.txt"
    
    
    thisPathBase = r"D:\Freelancing\TestFileObject\\"
    thisPathSuffix = r"\0A Folder\Test55.text"
    
    template = FileObjectBaseSuffix(thisPathBase,thisPathSuffix)
    
    
    
    print template
    #newFileObj.loadAllText()
    newFile = template.copyToNewBasePath("d:\\")
    
    print newFile
    #workingFile = template.copyToSameDir("Test2.text")
    #workingFile.makeReplacements(replaceVector)
    
    logging.debug("Finished _test1".format())


if __name__ == "__main__":
    logging.config.fileConfig('..\\LoggingConfig\\loggingNofile.conf')
    logging.debug("Started _main".format())

    unittest.main()
        
    #_test2()
    
    logging.debug("Started _main".format())
    
    