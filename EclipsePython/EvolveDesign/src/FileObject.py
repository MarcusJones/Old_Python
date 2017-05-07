'''
Created on 09.06.2011

@author: mjones
'''
import os
import logging.config

class FileObject(object):
    def __init__(self,filePath, name= "UNDEFINED", outputFilePath = "UNDEFINED"):
        self.inputFilePath = filePath
        self.fileData = str()
        self.name = name
        self.outputFilePath = outputFilePath
        logString = "Created file {0}".format(self)
        logging.info(logString)
        
    def loadData(self):
        #prin 'reading:', self.inputFileTemplatePath
        fIn = open(self.inputFilePath,'r')
        # Don't read unicode... inputFileTemplate=unicode(fIn.read(),'utf-8')
        self.fileData=fIn.read()
        fIn.close()
        logString = "File data loaded for {0}".format(self)
        logging.info(logString)

    def writeData(self):
        outF = open(self.outputFilePath,'w')
        outF.write(self.fileData)
        outF.close()
        # Free up that memory
        self.fileData = "UNDEFINED"        
        logString = "File data written for {0}".format(self)
        logging.info(logString)

    def __str__(self):
        return "File Object name:{0} input path: {1}, output path: {2}, data length: {3}".format(self.name, self.inputFilePath, self.outputFilePath, len(self.fileData))