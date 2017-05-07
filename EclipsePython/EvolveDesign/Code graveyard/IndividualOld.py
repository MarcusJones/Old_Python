'''
Created on Feb 27, 2011

@author: UserXP
'''
import random

class Individual:
    "An individual contains a list of variables"
    def __init__(self,name,variableList):
        self.name = name
        self.variables = variableList
    def list_variables(self):
        #for v in self.variables
        print '%-25s %10s %5s %10s' % ('Type', 'Name', 'Value', 'Attributes')
        for v in self.variables:
            print '%-25s %-10s %5f' % (v.type, v.name, v.value),
            print '   ', v.attribs

class Variable:
    "general variable class"
    def __init__(self,name,attribList = [0,1],targetFile=''):
        self.name = name
        self.targetFile = targetFile    # Search in this file for variable, 
                                        # or leave blank to use individual's file        

class RandomFloat(Variable):
    "this is a gene of type 'Random'"
    def __init__(self,name,attribList = [0,1],targetFile=''):
        Variable.__init__(self,name,targetFile)
        self.type = 'Random search float'
        self.attribTypes = [
                'lowerRange',             # Lower range of random variable
                'upperRange'            # Upper range of random variable
                ]
        self.attribs = dict(zip(self.attribTypes,attribList))
        self.value = random.uniform(self.attribs['lowerRange'], self.attribs['upperRange'])
    def next(self):
        self.value = random.uniform(self.attribs['lowerRange'], self.attribs['upperRange'])

myRSF1 = RandomFloat('X1')
myRSF2 = RandomFloat('X2')
myRSF3 = RandomFloat('X3')

myIndividual = Individual('Bill',[myRSF1,myRSF2,myRSF3])

myIndividual.list_variables()