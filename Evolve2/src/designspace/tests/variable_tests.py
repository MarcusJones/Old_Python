#===============================================================================
# Set up
#===============================================================================
# Standard:
from __future__ import division
from __future__ import print_function

from config import *

import logging.config
import unittest

from utility_inspect import whoami, whosdaddy, listObject

# Testing imports
from ..design_space import Variable

#===============================================================================
# Unit testing
#===============================================================================


class VariableTests(unittest.TestCase):
    def test010_SimpleTupleCreation(self):
        print("**** TEST {} ****".format(whoami()))
        v1 = Variable("C1",50)
        assert(len(v1)==1)
        assert(v1.ordered)
        v1 = Variable.ordered("C1",50)
        assert(len(v1)==1)
        assert(v1.ordered)

        v1 = Variable.unordered('c3',"string")
        assert(len(v1)==1)
        assert(not(v1.ordered))
        # From a list
        v1 = Variable.unordered('v3',[1,2,3,4])
        assert(len(v1)==4)
        assert(not(v1.ordered))
        # From a tuple
        v1 = Variable.ordered('v100',(1,2,3,4))
        assert(len(v1)==4)
        assert(v1.ordered)


    def test020_FromRange(self):
        print("**** TEST {} ****".format(whoami()))
        v1 = Variable.from_range('var232','1', '0.05', '5')
        assert(len(v1)==81)
        assert(v1.ordered)
        v1 = Variable.from_range('var2','-333.000000', '0.05', '5')
        assert(len(v1)==6761)
        assert(v1.ordered)

    def test030_Indivisible(self):
        print("**** TEST {} ****".format(whoami()))
        try:
            Variable.from_range('var22','0', '3.0', '100')
            self.fail( "Didn't raise AssertionError" )
        except AssertionError, e:
            print(e)
            self.assertEquals( 'Variable range is not evenly divisble by step size this is not supported.', e.message )

    def test040_FailUpperLowerRange(self):
        print("**** TEST {} ****".format(whoami()))
        try:
            Variable.from_range('var22','100', '3', '10')
            self.fail( "Didn't raise AssertionError" )
        except AssertionError, e:
            self.assertEquals( 'Upper range must be > lower', e.message )
            print(e)

    def test050_VarIteration(self):
        print("**** TEST {} ****".format(whoami()))
        v1 = Variable.from_range('VarNum','0', '.1', '.5')
        print("Test iteration of an ordered variable:")
        for var in v1:
            print(var.val_str())
        #print
        #print "Now the variable has a value;", v1
        assert(v1.value == 0.5)

        v1 = Variable.unordered('VarStr',["Blue","Red","Green"])
        print("Test iteration of an unordered variable:")
        for var in v1:
            #print newVar, var
            print(v1.val_str())
        assert(v1.value == "Green")

    def test060_RandomPoints(self):
        print("**** TEST {} ****".format(whoami()))
        newVar = Variable.from_range('VarNum','0', '.1', '10.0')
        newVar.get_random()
        print("Got a random value: ", newVar.val_str())
        newVar.get_random()
        print("Got a random value: ", newVar.val_str())
        newVar.get_random()
        print("Got a random value: ", newVar.val_str())

        newVar = Variable.unordered('VarStr',["Blue","Red","Green"])
        newVar.get_random()
        print("Got a random value: ", newVar.val_str())

    def test070_mutations(self):
        print("**** TEST {} ****".format(whoami()))
        var1 = Variable.from_range('X','0', '.1', '10')

        self.assertRaises(Exception, var1.step_random, )

        print(var1.get_random())

        print("Mutating var1 = {}".format(var1.val_str()))
        
        for idx in range(1,5):
            var1.step_random(1)
            print("Random step size {}: {}".format(1, var1.val_str()))
        for idx in range(1,5):
            var1.step_random(10)
            print("Random step size {}: {}".format(10, var1.val_str()))

        var2 = Variable.unordered('Y',["Blue","Red","Green","Purple","Yellow"])
        print(var2.get_random())
        
        # An un-ordered variable has no notion of a step direction
        self.assertRaises(AssertionError,var2.step_random,1)

        var3 = Variable.ordered('Y',["Blue","Red","Green","Purple","Yellow"])
        print(var3.get_random())

        for idx in range(1,100):
            var3.step_random(1)
        for idx in range(1,100):
            var3.step_random(10)
            #print var3.value

