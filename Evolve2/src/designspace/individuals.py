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
from design_space import Individual
#===============================================================================
# Code
#===============================================================================
class BasicIndividual(Individual):
    """
    """
    def __init__(self, labels, chromosome, indices, evaluator, fitness = None):
        super(BasicIndividual, self).__init__(labels, chromosome, indices, evaluator, fitness = None)

