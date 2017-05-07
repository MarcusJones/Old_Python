#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""This module holds the "controllers" for a search
A controller recieves settings (dict), and a DSpace object 
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:
from __future__ import division    
from __future__ import print_function

from config import *

import logging.config
import random

#--- Utility
def util_convert_numeric(item):
    if isinstance(item, str) or isinstance(item, unicode):
        item = len(item)
    else:
        pass
    return item

"""
An evaluation function follows the pattern;
input is the individual with a chromosome and an empty fitness vector
returns the individual with an evaluated object
"""
#--- Test evaluators

def minus_one_fitness(individual):
    new_fitness = list()
    for objective in individual.fitness:
        new_fitness.append((objective[0],-1))
    individual.fitness = new_fitness
    return individual

def sum_fitness(individual):
    """
    Simply the sum of the chromosome
    """
    for objective in individual.fitness:
        values  = [float( util_convert_numeric( allele[1]) ) for allele in individual.chromosome ]
        objective = sum(values)
        
    return individual.fitness # Must return an iterable!

def random_fitness(individual, ospace):
    """
    Returns the sums
    """
    new_fitness = list()
    for objective_name in ospace.objective_names:
        new_fitness.append((objective_name,random.random()))
    individual.fitness = new_fitness
    return individual

   