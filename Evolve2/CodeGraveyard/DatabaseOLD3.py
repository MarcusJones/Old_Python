

    
class OLDCODE(object):
#def varsToVals(vList):
#    return tuple([var.generatedValue for var in vList])

    def storeGeneration(DSpace, genNum, fileName):
        for indiv in DSpace.futureQueue:
            pass
    
    def pickleHistory(history, fullFilePath):
        fh = open(fullFilePath, 'w')
        cPickle.dump(history,fh)
        fh.close()
    
    def unpickleHistory(fullFilePath):
        fh = open(fullFilePath, 'r')
        history = cPickle.load(fh)
        fh.close()
        return history
    
    def saveHistoryToMat(history, matFullPath, convertNoneFit = False):
        
        if convertNoneFit:
            for key, val in history.iteritems():
                if not history[key]["fit"]:
                    history[key]["fit"] = 0
                    
        savemat(matFullPath, history, oned_as='row')
        
        logging.info("Saved objects into {} ".format( matFullPath))
    
    def updateHistory(historyDict,individuals,generation=0):
        """Update the dictionary holding the historical values
        """
        # historyDict is either blank, or has already been updated 
        for indiv in individuals:
            if indiv.key in historyDict:
                #print "Already here"
                historyDict[indiv.key]["gens"].append(generation)
                historyDict[indiv.key]["fit"] = indiv.fitness
            else:
                historyDict[indiv.key] = {"fit" : indiv.fitness, "gens": list()}
                historyDict[indiv.key]["gens"].append(generation)
        
        return historyDict
