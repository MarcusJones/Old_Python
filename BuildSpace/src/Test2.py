'''
Created on Dec 6, 2011

@author: UserXP
'''

from deap import dtm
from deap import base
from deap import creator
from deap import tools

import random
#from numpy import array

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
#creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMax)
creator.create("Individual", list, typecode='b', fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("attr_bool", random.randint, 0, 1)

# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 100)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):
    return sum(individual),

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoints)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("map", dtm.map)

def main():
    random.seed(64)

    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("Avg", tools.mean)
    stats.register("Std", tools.std)
    stats.register("Min", min)
    stats.register("Max", max)

    algorithms.eaSimple(toolbox, pop, cxpb=0.5, mutpb=0.2, ngen=40, stats=stats, halloffame=hof)
    logging.info("Best individual is %s, %s", hof[0], hof[0].fitness.values)

    return pop, stats, hof

dtm.setOptions(communicationManager="deap.dtm.commManagerTCP")

dtm.start(main)     # Launch the first task