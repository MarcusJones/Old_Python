#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""This module does A and B.
Etc.
"""

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
import re

#===============================================================================
# Code
#===============================================================================
def found_token(token_dictionary, input_string):
    """ Search the dictionary for the current word, return the corresponding value, or 0
    In this case, we are looping the dictionary to use the regex, instead of direct dict access
    using dict["key"]"""
    #logging.debug("Looking for token from set of {} in {}".format(len(token_dictionary),input_string.strip()))

    for k, v in token_dictionary.items():
        if re.match(k,input_string):
            #print("Match")
            return v
        else:
            continue
    # Didn't find any matches
    return False



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
    Iterates over blocks, where a block is a list of lines
    Takes a separate dictionary looking for comments
    This is a state machine with 3 states -

        1 wait for first block
        2 found block start
        3 transition to next block by closing last, and moving to 2
    """

    def __init__(self, lines_list, token_dict, comment_dict):

        self.lines_list = lines_list
        self.idx_lines = 0
        self.tokens = token_dict
        self.comment_tokens = comment_dict
        logging.debug("Parser over {} lines with {} tokens".format(len(lines_list), len(token_dict)))

    def next_line_idx(self):
        #nextLine = self.lines_list[self.idx_lines]
        self.idx_lines += 1
        if self.idx_lines % 100000 == 0:
            print("{:00}% - {} of {}".format(self.idx_lines/len(self.lines_list)*100,self.idx_lines,len(self.lines_list)))
        #print(self.idx_lines,len())
        #return nextLine

    def current_string(self):
        #print "Current string:", self.lines_list[self.idx_lines]
        #print(self.idx_lines)
        return self.lines_list[self.idx_lines]

    def __iter__(self):
        return self

    def end_of_lines(self):
        return self.idx_lines == len(self.lines_list)

    def next(self):
        if self.end_of_lines():
            raise StopIteration
        blockLines = list()

        # The START state, until we find a token
        # Also executed to store the block function
        while 1:
            token_function = found_token(self.tokens, self.current_string())
            if token_function:
                break # Transition 1 or 4
            else:
                self.next_line_idx()
            if self.end_of_lines():
                raise Exception("No tokens found?")

        # The in block state
        while 1:
            # Start the block with the last line retrieved
            if not found_token(self.comment_tokens, self.current_string()):
                blockLines.append(self.current_string())
            # Check the next line
            self.next_line_idx()
            # Break if found the next token, or EOF
            if self.end_of_lines():
                break
            elif found_token(self.tokens, self.current_string()):
                break
            else:
                continue

        return {'function':token_function, 'lines': blockLines}

#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):

    def setUp(self):
        print("**** TEST {} ****".format(whoami()))

    def test010_SimpleCreation(self):
        print("**** TEST {} ****".format(whoami()))

#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print(ABSOLUTE_LOGGING_PATH)
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)


    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())

    #print FREELANCE_DIR

    unittest.main()

    logging.debug("Finished _main".format())
