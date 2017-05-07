from __future__ import division
'''
Created on 2012-08-25

@author: ANON
'''
#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""This is a Top Down parser for BUI files
Etc.
"""

#===============================================================================
# Set up
#===============================================================================
import logging.config
import UtilityInspect
from UtilityInspect import whoami, whosdaddy
import unittest
import re
from lxml import etree
from textwrap import dedent
from cStringIO import StringIO

#===============================================================================
# Code
#===============================================================================
def foundToken(tokenDictionary, inputString):
    """ Search the dictionary for the current word, return the corresponding value, or 0
    In this case, we are looping the dictionary to use the regex, instead of direct dict access
    using dict["key"]"""
    for k, v in tokenDictionary.items():
        if re.match(k,inputString):
            return v
        else:
            continue
    # Didn't find it
    return False


def TOKENPLACEHOLDER(blockLines, currentXML):
   #print "Token function: {} lines ".format(len(blockLines))
   #print blockLines
   #lineIndex = lineIndex + 1
   print blockLines

   return currentXML

def COMMENT(blockLines, currentXML):
    pass

primaryTokens = {
                r'^WALL\s\S+$': TOKENPLACEHOLDER,
                r'^ZONE\s\S+$': TOKENPLACEHOLDER,
                r'^PROPERTIES' : TOKENPLACEHOLDER   ,
                r'^TYPES' : TOKENPLACEHOLDER   ,
                r'^LAYER' : TOKENPLACEHOLDER   ,
                r'^INPUTS' : TOKENPLACEHOLDER   ,
                r'^SCHEDULE' : TOKENPLACEHOLDER   ,
                r'^WINDOW\s\S+$' : TOKENPLACEHOLDER   ,
                r'^GAIN' : TOKENPLACEHOLDER   ,
                r'^INFILTRATION' : TOKENPLACEHOLDER   ,
                r'^VENTILATION' : TOKENPLACEHOLDER   ,
                r'^COOLING' : TOKENPLACEHOLDER   ,
                r'^HEATING' : TOKENPLACEHOLDER   ,
                r'^ZONES' : TOKENPLACEHOLDER   ,
                r'^HEMISPHERE' : TOKENPLACEHOLDER   ,
                r'^ORIENTATIONS' : TOKENPLACEHOLDER   ,
                r'^INTERNAL_CALCULATION' : TOKENPLACEHOLDER   ,
                r'^BUILDING' : TOKENPLACEHOLDER   ,
                }


commentTokens = {
              r'^[*]+': COMMENT,
              }



class parserCursor(object):
    """The parser cursor object
    Iterates over a list of strings and checks item for token
    An item can be a i.e. line or a word
    Tokens are stored in a dictionary, the key is the regex to match token
    The value is the function to process the token
    A block is something that can span several items
    A token identifies the start of a block, until the next tokened item is seen
    The block is returned as a list
    Implements Iterator interface
    Takes a separate dictionary looking for comments
    This is a state machine with 3 states -

        1 wait for first block
        2 found block start
        3 transition to next block by closing last, and moving to 2
    """

    def __init__(self, linesList, tokenDict, commentDict):
        self.linesList = linesList
        self.idxLines = 0
        self.tokens = tokenDict
        logging.debug("Parser over {} lines with {} tokens".format(len(linesList), len(tokenDict)))

    def nextLineIdx(self):
        #nextLine = self.linesList[self.idxLines]
        self.idxLines += 1
        #return nextLine

    def currentString(self):
        #print "Current string:", self.linesList[self.idxLines]
        return self.linesList[self.idxLines]

    def __iter__(self):
        return self

    def endOfLines(self):
        return self.idxLines == len(self.linesList)

    def next(self):
        if self.endOfLines():
            raise StopIteration
        blockLines = list()

        # The START state, until we find a token
        # Also executed to store the block function
        while 1:
            tokenFunc = foundToken(self.tokens, self.currentString())
            if tokenFunc:
                break # Transition 1 or 4
            else:
                self.nextLineIdx()

        # The in block state
        while 1:
            # Start the block with the last line retrieved
            if not foundToken(commentTokens, self.currentString()):
                blockLines.append(self.currentString())
            # Check the next line
            self.nextLineIdx()
            # Break if found the next token, or EOF
            if self.endOfLines():
                break
            elif foundToken(self.tokens, self.currentString()):
                break
            else:
                continue

        return tokenFunc, blockLines


class allTests(unittest.TestCase):
    def skiptest010_commentStart(self):
        print "**** TEST {} ****".format(whoami())
        testString = dedent("""\
            *--------
            *  L a y e r s
            *--------
            LAYER DUMMY_TRNSYS3D
             RESISTANCE=      0.1
            LAYER PLASTERBOA
             CONDUCTIVITY=  0.576 : CAPACITY=   0.84 : DENSITY=    950
            LAYER FBRGLS_ASHRAE
             CONDUCTIVITY=  0.144 : CAPACITY=   0.84 : DENSITY=     12""")
        linesList = testString.split("\n")

        mainLoop = parserCursor(linesList,primaryTokens, commentTokens)
        for block in mainLoop:
            print block[0](block[1],None)

    def test020_fullFile(self):
        print "**** TEST {} ****".format(whoami())
        inputBuiFilePath = r"..\testBuiFiles\Building17.b17"

        # The input file
        fIn = open(inputBuiFilePath, 'r')
        linesList = fIn.readlines()
        fIn.close()

        mainLoop = parserCursor(linesList,primaryTokens, commentTokens)
        for block in mainLoop:
            block[0](block[1],None)
            #print "Iteration:", line


if __name__ == "__main__":
    logging.config.fileConfig('..\\..\\MyUtilities\\LoggingConfig\\loggingNofile.conf')
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())

    unittest.main()
    test010_cursorObject()

    logging.debug("Finished _main".format())



