'''
Created on Jun 12, 2011

@author: UserXP
'''
import random
import Variables
import SimulationRuns

def nonDominatedSort(R_t):
    # R_t is the combined population
    
    # These are the Fronts
    fronts = list()
    
    # This is the first fronts
    fronts.append(list())
    
    # For each individual 'p' in main population 'P' do the following
    #P = R_t
    
    for p in R_t:
        
        p.rank = -1
        
        # Slight modification here from orginal algorithm
        # Set Q is created to hold the OTHER individuals, no need to 
        # compare 'p' to 'p'
        Q = R_t[:]
        
        # Don't compare 'p' to 'p'
        Q.remove(p)
        
        # S_p This set would contain all individuals that are dominated by p
        S = list()
        
        # Domination counter
        # n_p This is the number of individuals that dominate p
        n = 0
        
        # For each individual q in P
        for q in Q:
            #print "Comparing {0} and {1}".format(p.runID, q.runID)
            # If p dominated q
            if p.dominates(q):
                #print "{0} dominates {1} in at least 1 objective ".format(p.runID, q.runID)
                # p dominates these
                # Add 'q' to the set S_p, the set that contains dominated individuals
                S.append(q)
            # Otherwise, if 
            elif q.dominates(p):
                #print "{0} dominates {1}".format(q.runID, p.runID)
                # Domination counter
                n += 1
                 
        if n == 0:
            #print "Run {0} has rank 1".format(p.runID, q.runID)
            p.rank = 1
            fronts[0].append(p)
            #print "fronts:", fronts
            #print "fronts [0] (First front):", fronts[0]
        
        # This p is finished, now assign the values
        p.n = n
        p.S = S
    
    frontCounterI = 0
    # Start the Front counter
    while (len(fronts[frontCounterI]) != 0):
        # Add a new Front
        fronts.append(list())
        # Used to store the members of the next front
        BigQ = list()
        for p in fronts[frontCounterI]:
            #print "Individual {0} in Front {1}".format(p.runID,frontCounterI)
            #print "This indiv has n: {0}, rank: {1}, and S: {2}".format(p.n, p.rank, p.S)
            for q in p.S:
                #print "   In this indiv S_p the next indiv in S_p has has n: {0}, rank: {1}, and S: {2}".format(q.n, q.rank, q.S)
                q.n -= 1
                if q.n == 0:
                    q.rank = frontCounterI + 1
                    BigQ.append(q)
        frontCounterI += 1
        fronts[frontCounterI] = BigQ

    frontCount = 0
    #print "FRONT SUMMARY"
    for front in fronts:
        frontCount += 1
        #print "In front {0}:".format(frontCount)
        for run in front:
            pass
            #print "   Run {0}".format(run.runID)
            
#        for p in P:
#            print "Run {0} has front {1}".format(p.runID, p.rank)
#        

    #print "RE FORCE THE FRONT RANKS!!!!!"
    frontCount = 0
    for front in fronts:
        frontCount += 1
        for run in front:
            thisRunID = run.runID
            for run in R_t:
                if run.runID == thisRunID:
                    run.rank = frontCount

    
    # Checking to see if finished Queue is ALSO updated
#        print " Checking to see if finished Queue is ALSO updated"
    for p in R_t:
        pass
        #print "Run {0} has rank {1}".format(p.runID, p.rank)

    return R_t
    
   
def recombineAndMutate(parent1,parent2,
                       mutationProbabilityReal,
                       mutationProbabilityString,
                       crossoverDistributionIndex,
                       mutationDistributionIndex,
                       ):
    """
    Takes two parent SimulationRun objects
    Creates two children SimulationRun objects
    """
    nc = crossoverDistributionIndex
    nm = mutationDistributionIndex
    #print "Combine {0} and {1}".format(parent1.runID,parent2.runID)

    # This causes an error      c1VariableVector = list() WHY?  
    c1VariableVector = []
    c2VariableVector = []
    
    #print "Parent1 variable:"
    count = 0
    for variable in parent1.variableVector:
        
        if parent1.variableVector[count].type == "RandomFloat" or parent1.variableVector[count].type == "LockedRandomFloat":
            
            # Copy these attributes
            lowerRange = parent1.variableVector[count].lowerRange
            upperRange = parent1.variableVector[count].upperRange
            name = parent1.variableVector[count].name
            regexTarget = parent1.variableVector[count].regexTarget

            p1 = parent1.variableVector[count].value
            p2 = parent2.variableVector[count].value
            
            u = random.uniform(0, 1)
            term1 = (2*u)
            term2 = (1/float(1+nc))
            beta = term1**term2
            
            c1Value = 0.5*((1-beta)*p1 + (1+beta)*p2)

            c2Value = 0.5*((1+beta)*p1 + (1-beta)*p2)

            # Mutation
            
            mutationRoll = random.uniform(0,1)
            if mutationRoll < mutationProbabilityReal:
                r = random.uniform(0,1)
                if r < 0.5:
                    sigma = (2*r)**(1/float(nm+1)) - 1
                if r >= 0.5:
                    sigma = 1-(2*(1-r))**(1/float(nm+1))
                c1Value = c1Value + (upperRange - lowerRange)*sigma
                
            mutationRoll = random.uniform(0,1)
            if mutationRoll < mutationProbabilityReal:
                r = random.uniform(0,1)
                if r < 0.5:
                    sigma = (2*r)**(1/float(nm+1)) - 1
                if r >= 0.5:
                    sigma = 1-(2*(1-r))**(1/float(nm+1))
                c2Value = c2Value + (upperRange - lowerRange)*sigma

            if c1Value > upperRange:
                c1Value = upperRange
            elif c1Value < lowerRange:
                c1Value = lowerRange
            
            if c2Value > upperRange:
                c2Value = upperRange
            elif c2Value < lowerRange:
                c2Value = lowerRange
                                    
            c1Var = Variables.LockedRandomFloat(name,regexTarget,lowerRange,upperRange,c1Value)
            c2Var = Variables.LockedRandomFloat(name,regexTarget,lowerRange,upperRange,c2Value)
            
            c1VariableVector.append(c1Var)
            c2VariableVector.append(c2Var)
                            
        elif parent1.variableVector[count].type == "RandomStringList" or parent1.variableVector[count].type == "LockedRandomStringList" :
            name = parent1.variableVector[count].name
            regexTarget = parent1.variableVector[count].regexTarget
            list = parent1.variableVector[count].list
            
            beta = random.choice([0,1])
            
            if beta:
                c1Value = parent1.variableVector[count].value
                c2Value = parent2.variableVector[count].value
            if not beta:
                c1Value = parent2.variableVector[count].value
                c2Value = parent1.variableVector[count].value
                                
            c1Var = Variables.LockedRandomStringList(name,regexTarget,list,c1Value)
            c2Var = Variables.LockedRandomStringList(name,regexTarget,list,c2Value)
            
            
            mutationRoll = random.uniform(0,1)
            if mutationRoll < mutationProbabilityString:
                c1Var.mutate()

            mutationRoll = random.uniform(0,1)
            if mutationRoll < mutationProbabilityString:
                c2Var.mutate()
            
            c1VariableVector.append(c1Var)
            c2VariableVector.append(c2Var)
        elif parent1.variableVector[count].type == "Constant":
            c1VariableVector.append(parent1.variableVector[count])
            c2VariableVector.append(parent1.variableVector[count])
        else:
            raise
        
        count += 1
            
    
    #raw_input("Press Enter to continue...")
    #return child
    return [c1VariableVector,c2VariableVector]



def binaryTournament(individuals):
    
    #print "Let the tournament begin! Competitors: {0} and {1}".format(parent1.runID,individual2.runID)

    # Who has a better rank? (lower)
    if individuals[0].rank == individuals[1].rank:
        #print "Tie! Returning {0}".format(parent1.runID) 
        return individuals[0]
    # Front rank is better, lower
    if individuals[0].rank < individuals[1].rank:
        #print "{0} Wins!".format(parent1.runID) 
        return individuals[0]
    else:
        #print "{0} Wins!".format(individual2.runID)
        return individuals[1]


        
def createQ_t(R_t_ranked,popSize,
                       mutationProbabilityReal,
                       mutationProbabilityString,
                       crossoverDistributionIndex,
                       mutationDistributionIndex,
              ):
    """ 
    Receives R_t, a ranked list
    Produces Q_t, ready for evaluation
    """
    
    # Selection
    
    for individual in R_t_ranked:
        individual.parentCount = 0
    
    Q_t = list()
    
    # Since we create 2 children at a time, need to loop only 1/2 times
    for childNumber in range(popSize/2):
        
        
        # Choose both parents by tournament        
        
        parent1 = binaryTournament(random.sample(R_t_ranked, 2))
        parent1.parentCount += 1
        
        parent2 = binaryTournament(random.sample(R_t_ranked, 2))
        parent2.parentCount += 1
        
        twoChildrenVarVec = recombineAndMutate(parent1, parent2,
                       mutationProbabilityReal,
                       mutationProbabilityString,
                       crossoverDistributionIndex,
                       mutationDistributionIndex,
                       )

        for variableVector in twoChildrenVarVec:
            aChild = SimulationRuns.TrnsysRun(
                -1, 
                "UNDEFINED",
                "UNDEFINED",
                ["UNDEFINED"],
                variableVector
                )
            Q_t.append(aChild)
    
#    targetFilePath = "C:\\result.csv"
#
#    for individual in R_t_ranked:
#        print individual.runID,
#        print individual.rank,
#        print individual.v
#        for result in individual.fitness.results:
#            print result.value
#        #print individual.
#     
#
#        resultStringList = list()
#        for result in self.results:
#            resultStringList.append(str(result))
#            
#        resultString = ', '.join(resultStringList)
#        resultString = "(" + resultString + ")"
#        return resultString     
#     
#     
#        
#        varStringList = list()
#        #varStringList.append("(")
#        for variable in self.variableVector:
#            try:
#            #prin variable.value
#                varStringList.append(str(round(variable.value,1)))
#            except:
#                varStringList.append(variable.value,)
#
#        fitnessStringList = list()
#        for result in self.fitness.results:
#            value = result.value
##            print value
##            print repr(value)
##            print type(value)
#        
#            fitnessStringList.append(str(round(value,1)))
#        
#        resultList = varStringList + fitnessStringList
#        resultString = ','.join(resultList)
#        resultString += "\n"
#
#        resultFile = open(targetFilePath,'a')
#        resultFile.write(resultString)
#        resultFile.close()
        
    return Q_t

    
    
    