from __future__ import division    
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
from config import *

import logging.config
import unittest

from utility_inspect import whoami
from utility_inspect import whoami, whosdaddy

import random

from deap import base
# Contains Toolbox, Fitness, (Tree)

from deap import creator
# The factory for creating classes

from deap import tools

#===============================================================================
# Code
#===============================================================================

# Defines the Fitness object, now contained in the creator module
# A Fitness object stores values and weights, that's it really
creator.create("FitnessMax", base.Fitness, weights=(1.0,))

# An Individual is a pure python list of values, with one additional attribute, the fitness object
creator.create("Individual", list, fitness=creator.FitnessMax)

# The toolbox can clone() and map(), additional methods you can register()
toolbox = base.Toolbox()

# The toolbox now has a random generator function called attr_bool
# Attribute generator
toolbox.register("attr_bool", random.randint, 0, 1)

# Structure initializers
# There is now a function called "individual", which is an alias for tools.initRepear
# Therefore, this creates a list with 100 random 1's or 0's
toolbox.register("individual", tools.initRepeat, creator.Individual, 
    toolbox.attr_bool, 100)


# There is now a function called "population", which is a list of "individuals"
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):
    return sum(individual),

# Operator registering
# There is now a function called "evaluate", defined above
toolbox.register("evaluate", evalOneMax)
# There is now a function called "mate", which is 2 point crossover
# Each individual must have a __len__, __getitem__, __setitem__ 
# Each individual must be indexable
toolbox.register("mate", tools.cxTwoPoints)
# There is now a function called "mutate", each individual must have __not__, __getitem__, __setitem__ 
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
# There is now a function called "select", which receives a population of individuals
# Individuals need __gt__ 
toolbox.register("select", tools.selTournament, tournsize=3)



def firstExample():
    random.seed(64)
    
    
    # register("population", tools.initRepeat, list, toolbox.individual)
    pop = toolbox.population(n=300)
    CXPB, MUTPB, NGEN = 0.5, 0.2, 40
    
    print "Start of evolution"
    
    # Evaluate the entire population
    # Applies the evaluate to each indiv in pop
    fitnesses = map(toolbox.evaluate, pop)
    
    # Applies the fitnesses to each indiv
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    
    print "  Evaluated %i individuals" % len(pop)
    
    # Begin the evolution
    for g in range(NGEN):
        print "-- Generation %i --" % g
        
        # Tournament selection register("select", tools.selTournament, tournsize=3)
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        
        
        # Clone the selected individuals
        offspring = map(toolbox.clone, offspring)
    
        
        # Apply crossover and mutation on the offspring
        # Extended Slices [start:stop:step]
        # So this is every EVEN child mating with every ODD child
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
    
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        print "  Evaluated %i individuals" % len(invalid_ind)
        
        # The population is entirely replaced by the offspring
        pop[:] = offspring
        
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        
        print "  Min %s" % min(fits)
        print "  Max %s" % max(fits)
        print "  Avg %s" % mean
        print "  Std %s" % std
    
    print "-- End of (successful) evolution --"
    
    best_ind = tools.selBest(pop, 1)[0]
    print "Best individual is %s, %s" % (best_ind, best_ind.fitness.values)

#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print ABSOLUTE_LOGGING_PATH
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    firstExample()
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())
    
    #print FREELANCE_DIR
    
    #unittest.main()
        
    logging.debug("Finished _main".format())
    