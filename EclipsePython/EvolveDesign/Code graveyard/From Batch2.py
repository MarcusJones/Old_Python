    def nonDominatedSort(self,R_t):
        # R_t is the combined population
        
        # These are the Fronts
        fronts = list()
        
        # This is the first fronts
        fronts.append(list())
        
        # For each individual 'p' in main population 'P' do the following
        P = R_t
        
        for p in P:
            
            p.rank = -1
            
            # Slight modification here from orginal algorithm
            # Set Q is created to hold the OTHER individuals, no need to 
            # compare 'p' to 'p'
            Q = P[:]
            
            # Don't compare 'p' to 'p'
            Q.remove(p)
            
            # S_p This set would contain all individuals that are dominated by p
            S = list()
            
            # Domination counter
            # n_p This is the number of individuals that dominate p
            n = 0
            
            # For each individual q in P
            for q in Q:
                print "Comparing {0} and {1}".format(p.runID, q.runID)
                # If p dominated q
                if p.dominates(q):
                    print "{0} dominates {1} in at least 1 objective ".format(p.runID, q.runID)
                    # p dominates these
                    # Add 'q' to the set S_p, the set that contains dominated individuals
                    S.append(q)
                # Otherwise, if 
                elif q.dominates(p):
                    print "{0} dominates {1}".format(q.runID, p.runID)
                    # Domination counter
                    n += 1
                     
            if n == 0:
                print "Run {0} has rank 1".format(p.runID, q.runID)
                p.rank = 1
                fronts[0].append(p)
                print "fronts:", fronts
                print "fronts [0] (First front):", fronts[0]
            
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
                print "Individual {0} in Front {1}".format(p.runID,frontCounterI)
                print "This indiv has n: {0}, rank: {1}, and S: {2}".format(p.n, p.rank, p.S)
                for q in p.S:
                    print "   In this indiv S_p the next indiv in S_p has has n: {0}, rank: {1}, and S: {2}".format(q.n, q.rank, q.S)
                    q.n -= 1
                    if q.n == 0:
                        q.rank = frontCounterI + 1
                        BigQ.append(q)
            frontCounterI += 1
            fronts[frontCounterI] = BigQ

        frontCount = 0
        print "FRONT SUMMARY"
        for front in fronts:
            frontCount += 1
            print "In front {0}:".format(frontCount)
            for run in front:
                print "   Run {0}".format(run.runID)
                
#        for p in P:
#            print "Run {0} has front {1}".format(p.runID, p.rank)
#        

        print "RE FORCE THE FRONT RANKS!!!!!"
        frontCount = 0
        for front in fronts:
            frontCount += 1
            for run in front:
                thisRunID = run.runID
                for run in self.finishedQueue:
                    if run.runID == thisRunID:
                        run.rank = frontCount

        
        # Checking to see if finished Queue is ALSO updated
#        print " Checking to see if finished Queue is ALSO updated"
        for p in self.finishedQueue:
            print "Run {0} has rank {1}".format(p.runID, p.rank)

        #raw_input("Press Enter to continue...")

            
        #self.population = P
        
        #self.fronts = fronts
        
        return fronts


    def returnNextRunsOBSELETE(self):
        self.evaluateFirstFitness()
        self.createChildren()        
        pass 
    
    
    
    def evaluateFirstFitness(self):
        
        # These are the Fronts
        fronts = list()
        
        # This is the first fronts
        fronts.append(list())
        
        # For each individual 'p' in main population 'P' do the following
        P = self.finishedQueue
        
        for p in P:
            
            p.rank = "UNDEFINED"
            
            # Slight modification here from orginal algorithm
            # Set Q is created to hold the OTHER individuals, no need to 
            # compare 'p' to 'p'
            Q = P[:]
            
            # Don't compare 'p' to 'p'
            Q.remove(p)
            
            # S_p This set would contain all individuals that are dominated by p
            S = list()
            
            # Domination counter
            # n_p This is the number of individuals that dominate p
            n = 0
            
            # For each individual q in P
            for q in Q:
                print "Comparing {0} and {1}".format(p.runID, q.runID)
                # If p dominated q
                if p.dominates(q):
                    print "{0} dominates {1} in at least 1 objective ".format(p.runID, q.runID)
                    # p dominates these
                    # Add 'q' to the set S_p, the set that contains dominated individuals
                    S.append(q)
                # Otherwise, if 
                elif q.dominates(p):
                    print "{0} dominates {1}".format(q.runID, p.runID)
                    # Domination counter
                    n += 1
                     
#            if n == 0:
#                print "Run {0} has rank 1".format(p.runID, q.runID)
#                print "fronts:", fronts
#                print "fronts [0] (First front):", fronts[0]
            
            # This p is finished, now assign the values
            p.n = n
            p.S = S
            
            if n == 0:
                fronts[0].append(p)
                p.rank = 1
                                        
        print "Current status of finishedQueue"
        for run in self.finishedQueue:
            print "   Run: {0}, n: {1}, rank: {2}, len(S): {3}".format(run.runID,run.n,run.rank,len(run.S))                                

        print "Current status of P"
        for run in P:
            print "   Run: {0}, n: {1}, rank: {2}, len(S): {3}".format(run.runID,run.n,run.rank,len(run.S))                                
    
        print "Current status of Q"
        for run in Q:
            print "   Run: {0}, n: {1}, rank: {2}, len(S): {3}".format(run.runID,run.n,run.rank,len(run.S))                                

    
        frontCounterI = 0
        # Start the Front counter
        while (len(fronts[frontCounterI]) != 0):
            # Add a new Front
            fronts.append(list())
            # Used to store the members of the next front
            BigQ = list()
            for p in fronts[frontCounterI]:
                print "Individual {0} in Front {1}".format(p.runID,frontCounterI)
                print "This indiv has n: {0}, rank: {1}, and S: {2}".format(p.n, p.rank, p.S)
                for q in p.S:
                    print "   In this individual's S, the next indiv in S is id: {0}, n: {1}, rank: {2}, and S: {3}".format(q.runID,q.n, q.rank, q.S)
                    q.n -= 1
                    if q.n == 0:
                        q.rank = frontCounterI + 1
                        BigQ.append(q)
                    print "   Now, it is; id: {0}, n: {1}, rank: {2}, and S: {3}".format(q.runID,q.n, q.rank, q.S)
                        
            frontCounterI += 1
            fronts[frontCounterI] = BigQ

        print "Current status of finishedQueue"
        for run in self.finishedQueue:
            print "   Run: {0}, n: {1}, rank: {2}, len(S): {3}".format(run.runID,run.n,run.rank,len(run.S))                                

        print "Current status of P"
        for run in P:
            print "   Run: {0}, n: {1}, rank: {2}, len(S): {3}".format(run.runID,run.n,run.rank,len(run.S))                                
    
        print "Current status of Q"
        for run in Q:
            print "   Run: {0}, n: {1}, rank: {2}, len(S): {3}".format(run.runID,run.n,run.rank,len(run.S))                                

        frontCount = 0
        print "FRONT SUMMARY"
        for front in fronts:
            frontCount += 1
            print "In front {0}:".format(frontCount)
            for run in front:
                print "   Run {0}".format(run.runID)

        print "RE FORCE THE FRONT RANKS!!!!!"
        frontCount = 0
        for front in fronts:
            frontCount += 1
            for run in front:
                thisRunID = run.runID
                for run in self.finishedQueue:
                    if run.runID == thisRunID:
                        run.rank = frontCount

        print "Current status of finishedQueue"
        for run in self.finishedQueue:
            print "   Run: {0}, n: {1}, rank: {2}, len(S): {3}".format(run.runID,run.n,run.rank,len(run.S))                                

        print "Current status of P"
        for run in P:
            print "   Run: {0}, n: {1}, rank: {2}, len(S): {3}".format(run.runID,run.n,run.rank,len(run.S))                                
    
        print "Current status of Q"
        for run in Q:
            print "   Run: {0}, n: {1}, rank: {2}, len(S): {3}".format(run.runID,run.n,run.rank,len(run.S))                                

        frontCount = 0
        print "FRONT SUMMARY"
        for front in fronts:
            frontCount += 1
            print "In front {0}:".format(frontCount)
            for run in front:
                print "   Run {0}".format(run.runID)
        
                
#        for p in P:
#            print "Run {0} has front {1}".format(p.runID, p.rank)
#        
        # Checking to see if finished Queue is ALSO updated
#        print " Checking to see if finished Queue is ALSO updated"
        for p in self.finishedQueue:
            print "Run {0} has rank {1}".format(p.runID, p.rank)
            
        #self.population = P
        
        #self.fronts = fronts
        
        return fronts
    
    
    
    
    
    
    #            
#            
#            #******************
#            
#            # Evaluate it            
#            self.generationList[-1].executeParallel()
#            
#            # Plot it
#            self.generationList[-1].plotPopulation()
#            
#            # Record it
#            self.generationList[-1].listFitnesses()
#            self.generationList[-1].printResult(self.outputResultsFile)
#            
#            # Sort it with the previous generation
#            Q = self.generationList[-1].finishedQueue
#            P = self.generationList[-2].finishedQueue
#            
#            R_t = list()
#            for individual in Q:
#                R_t.append(individual)
#            for individual in P:
#                R_t.append(individual)
#                
#            R_t_ranked = Genetics.nonDominatedSort(R_t)
#            
#            # Create the next generation
#            Q_t = Genetics.createQ_t(R_t_ranked)
#            
#            # Put Q_t into a generation
#            generationNumber = len(self.generationList) + 1
#            generationDirectory = self.systemDirectory + "\\Generation_{0:03d}".format(generationNumber)
#            nextGeneration = Generation(
#                                         str(generationNumber),
#                                         generationDirectory,
#                                         self.executablePath,
#                                         self.inputTemplateFileObjects,
#                                         self.maxProcesses,
#                                         self.maxCPUtime
#                                         )
#            nextGeneration.individualRunList = Q_t
#            self.generationList.append(nextGeneration)   
#            
#            # Evaluate it            
#            self.generationList[-1].executeParallel()
#            
#            # Plot it
#            self.generationList[-1].plotPopulation()
#            
#            # Record it
#            self.generationList[-1].listFitnesses()
#            self.generationList[-1].printResult(self.outputResultsFile)
#     






















#
#            
#            
#        else:
#            
#            R_t = self.generationList[-1].finishedQueue()
#            
#            Genetics.nonDominatedSort(R_t)
#            
#
#            prevGeneration = self.generationList[-1]
#    
#            '''
#            The first generation is random
#            '''
#            
#            logging.info("Evolutionary System '{0}' creating initial generation".format(self.name))
#            
#            generationNumber = len(self.generationList)
#            
#            generationDirectory = self.systemDirectory + "\\Generation_{0:03d}".format(generationNumber)
#            
#            # nextGeneration is a simple blank generation, goal:
#            # Populate the nextGeneration.individualRunList
#            nextGeneration = Generation(
#                                         str(generationNumber),
#                                         generationDirectory,
#                                         self.executablePath,
#                                         self.inputTemplateFileObjects,
#                                         self.maxProcesses,
#                                         self.maxCPUtime
#                                         )
#    
#            #firstGeneration.createInitialGeneration(self.popSize, self.designSpace, self.inputTemplateFilePath)
#            
#            #nextGeneration.loadDesignSpace(self.designSpace)
#            
#            #nextGeneration.createRandomRuns(self.popSize)
#            
#            print nextGeneration
#            
#            nextGenerationRuns = prevGeneration.createNextGenerationFirstTime(str(generationNumber))
#            
#            for run in nextGenerationRuns:
#                nextGeneration.individualRunList.append(run)
#    
#            # self.generationList.append(nextGeneration)
#    
#               
#                # Create the next generation from the current one
#                nextGeneration = self.createNextGeneration(prevGeneration)
#                
#                # Add it to the list!
#                self.generationList.append(nextGeneration)
#    
#                #raw_input("Press Enter to continue...")
#            
#        logging.info("List has {0} generation(s)".format(len(self.generationList)))
#        # Return the last generation
#            
#        return self.generationList[-1]
#         




def createChildren(nextDirectory):
    # THIS NEEDS TO BE UNIQUE, NO p against p
    # (ALWAYS A TIE)        
    thisPopulation = self.finishedQueue[:]
    
    childPopulation = list()
    
    for childNumber in range(len(thisPopulation)/2):
        #print "Child number:", childNumber
        
        parent1 = self.binaryTournament(
                        random.choice(thisPopulation),
                        random.choice(thisPopulation))

        parent2 = self.binaryTournament(
                        random.choice(thisPopulation),
                        random.choice(thisPopulation))
        
        twoChildrenVarVec = self.combine(parent1, parent2)
        
        #self.popSize = popSize
        #self.inputFilePath = inputFilePath
        #self.designSpace = designSpace
        #self.loadTemplate(inputFilePath)
        #self.createRandomIndividuals(self.popSize)

        runIDcounter = self.finishedQueue[-1].runID
        
        for variableVector in twoChildrenVarVec:
            runIDcounter += 1
            aChild = SimulationRuns.TrnsysRun(
                runIDcounter, 
                self.batchPath + "\\Individual_{0:03d}".format(runIDcounter),
                self.executablePath,
                self.inputTemplateFileObjects,
                variableVector
                )
            childPopulation.append(aChild)
            
            
#            for aChild in twoChildren: 
#                childPopulation.append(aChild)
#            
    return childPopulation
        #self.




def createNextGenerationFirstTime():
    
    popSize = len(self.finishedQueue)
    
    # First, sort the generation into fronts
    fronts = self.evaluateFirstFitness()
    
    #self.population
    # THIS NEEDS TO BE UNIQUE, NO p against p
    childPopulation = self.createChildren()
    
    print "Child population has length: {0}, children: {1}".format(len(childPopulation), childPopulation)
    
    parentPopulation = self.finishedQueue
    R_t = parentPopulation + childPopulation
    
    # All non-dominated fronts of R_t
    fronts = self.nonDominatedSort(R_t)
    # This will be the next population, P_t+1
    nextPopulation = list()
    iCounter = 0
    
    print len(fronts[iCounter])
    
    while (len(nextPopulation) + len(fronts[iCounter])) < popSize:
        # Crowding distance here!
        # Calculate crowding distance in fronts[iCounter]
        for individual in fronts[iCounter]:
            nextPopulation.append(individual)
            
        print "Added front {0}, with {1} individuals to the next population, now at {2}".format(iCounter,len(fronts[iCounter]), len(nextPopulation))
        if len(nextPopulation) == popSize:
            break
        iCounter += 1
        
    print "Next population is size {0}, therefore need {1} - {0} = {2} more".format(len(nextPopulation),popSize,popSize - len(nextPopulation))
    
    howManyMore = popSize - len(nextPopulation)
    for count in range(howManyMore):
        print "Topping up with 1 more..."
        nextPopulation.append(fronts[iCounter].pop())
         
    print "Created a new population: {0}".format(nextPopulation)
    return nextPopulation
           
   