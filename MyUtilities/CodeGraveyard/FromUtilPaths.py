
def printProjectDevelopment():
    pathName = r"Q:\2500\03 Projects\01 Project development"
    projectDirs =  listDirs(pathName)
    
    recentFileTuples = list()
    for pathName in projectDirs:
        #print "**** {}".format(pathName)
        fileTuple = getMostRecentFile(pathName)
        recentFileTuples.append(fileTuple)
#    

    recentFileTuples.sort(key=lambda tup: tup[1], reverse=True)
    for fileTuple in recentFileTuples:
        print "{} ^^^ {}".format(time.ctime(fileTuple[1]), fileTuple[0])

def printCurrentProjects():
    pathName = r"Q:\2500\03 Projects\02 Current projects"
    projectDirs =  listDirs(pathName)
    
    recentFileTuples = list()
    for pathName in projectDirs:
        #print "**** {}".format(pathName)
        fileTuple = getMostRecentFile(pathName)
        recentFileTuples.append(fileTuple)
#    

    recentFileTuples.sort(key=lambda tup: tup[1], reverse=True)
    for fileTuple in recentFileTuples:
        print "{} ^^^ {}".format(time.ctime(fileTuple[1]), fileTuple[0])

def _testing():
    logging.debug("RUNNING TESTS {}")
    printProjectDevelopment()
    printCurrentProjects()
    logging.debug("FINISHED TESTS {}")



def OBSELETElocateHTMLfiles(projectDir):
    #===========================================================================
    # Locate the HTML table files
    #===========================================================================
    
    logging.info("Looking in {0}".format(projectDir))
    
    tableFileNames = list()
    for name in os.listdir(projectDir):
        if re.search(".html$",name):
            #print name
            logging.info("Found {0}".format(name))
            tableFileNames.append(name)
            
    logging.info("Found {0} HTML".format(len(tableFileNames)))
    return tableFileNames 
