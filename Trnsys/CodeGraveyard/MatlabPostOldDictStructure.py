def showStructure(d):
    for system, value in d.iteritems():
        print system
        #print d[system]
        for pointGroup, value in d[system].iteritems():
            print '\t' + pointGroup
            #print d[system][pointGroup]
            cnt = 0
            for point in d[system][pointGroup]:
                cnt = cnt + 1
                print '\t\t', cnt
                #print "Here", point
                for key, value in point.iteritems():
                    #pass
                    print '\t\t  ' + key, " - ", show1line(value)
                    #print value
                    #raise
                    #print d[system][pointGroup]
                #print point
        #if isinstance(value, dict):
        #    showStructure(value, indent+1)
        #elif isinstance(value, list):
        #    for item in value:
        #        print '\t' * (indent+1) + str(value)
            
#        else:
#            print '\t' * (indent+1) + str(value)

def arrangeData(thisDataList):
    trnData = dict()
    objCount = 0
    for dataObj in thisDataList:
        objCount += 1
        # Assemble the point
        
        thisPoint = {"data":dataObj.dataColumns,
                     "headers":dataObj.headers,
                     "units":dataObj.units,
                     "source":dataObj.sourceFilePath,
                     "number":dataObj.number,
                     "description":dataObj.description,
                     "type":dataObj.pointType,
                     "system":dataObj.system,
                     }

        # Now place the point in the hierarchy
        
        # First, find the system 
        if dataObj.system not in set(trnData.keys()):
            #print "This is a new system;", dataObj.system
            
            # and therefore also a new point group

            # Create the point group first, and insert the point
            thisPointGroup  = {dataObj.pointType:[thisPoint]}

            #print "new", dataObj.system
            #print set(trnData.keys())
            
            # Now add the point group into the structure
            trnData[dataObj.system] = thisPointGroup
            
            #print "SEE"
            #showStructure(trnData)
            
        else:
            #print "This system already exists;", dataObj.system
            #print dataObj.pointType, "-", set(trnData[dataObj.system])
            #print dataObj.pointType not in set(trnData[dataObj.system])
            
            # Now check if the point type also exists
            if dataObj.pointType not in set(trnData[dataObj.system]):
                #thisPointGroup  = {dataObj.pointType:thisPoint}
                #print  thisPointGroup
                #print "This is a new point group, will add it to the ", dataObj.system 
                # + thisPointGroup

                #print "BEFORE", trnData

                
                trnData[dataObj.system][dataObj.pointType] = [thisPoint]


                #print "AFTER",trnData
                
                #print trnData[dataObj.system]
                #trnData[dataObj.system][dataObj.pointType] = {dataObj.pointType:thisPointGroup}
                #trnData[dataObj.system][dataObj.pointType].append(thisPoint)
                
                #print trnData[dataObj.system][dataObj.pointType]
                #print "Going to"
                #print "Point group ", type(thisPointGroup)#, thisPointGroup
                
                #trnData[dataObj.system][dataObj.pointType].append(thisPoint)
                
                
                #print "Full struct:", trnData
                #raise
            
            else:
                #print "this is an old point group:"
                #thisPointGroup  = {dataObj.pointType:thisPoint}
                trnData[dataObj.system][dataObj.pointType].append(thisPoint)
                
                
            #print "SEE"
            #showStructure(trnData)                
            #print "old", dataObj.system
        
        #print "PASS", objCount
        #showStructure(trnData)
   
    if 0: 
        testDict = {
                    "trnData":{
                               "systemA":{
                                          "MoA":[
                                                 {"data":1,
                                                 "units":1,
                                                 "headers":1
                                                 },
                                                 {"data":1,
                                                 "units":1,
                                                 "headers":1
                                                 },   
                                                 {"data":1,
                                                 "units":1,
                                                 "headers":1
                                                 },      
                                                 ],
                                          "Pow":[
                                                 {"data":1,
                                                 "units":1,
                                                 "headers":1},
                                                 ],
                                          },
                               "systemB":{
                                          "MoA":[
                                                 {"data":1,
                                                 "units":1,
                                                 "headers":1},
                                                 ]
                                          }                           
                               }
                    }
            
#    trndata
#        . systemA
#            . stateMoA
#                [a list!]
#            . statePow
#            . stateC
#        . systemB
#        . systemC

    logging.info("Arranged {} AnalysisData objects".format(len(thisDataList)))    
    return trnData


def showSimplerStructure(d):
    #print d
    cntSystems = 0
    for system, value in d.iteritems():
        cntSystems += 1
        
        cntGroups = 0
        thisSummaryString = ""
        for group, value in d[system].iteritems():
            cntGroups += 1
            
            cntPoints = 0
            
            #print group, type(group)
            #print "DFddddd", d[system][group]
            for point in d[system][group]:
                cntPoints += 1
            thisSummaryString += "[{} group with {} points]".format(group,cntPoints)
                
        print "{}-The {} system: {}".format(cntSystems,system,thisSummaryString)
    #print "{} systems".format(cntSystems)
        
def checkStructure(d):
    #print d
    cntSystems = 0
    for system, value in d.iteritems():
        cntSystems += 1
        
        cntGroups = 0
        thisSummaryString = ""
        for group, value in d[system].iteritems():
            cntGroups += 1
            
            cntPoints = 0
            
            #print group, type(group)
            #print "DFddddd", d[system][group]
            thesePointNumbers = set()
            for point in d[system][group]:
                cntPoints += 1
                print "[{} system {} group ]".format(system, group)
                print point
                if point[group]["number"] in thesePointNumbers:
                    raise
                else:
                    thesePointNumbers.add(point[group]["number"])
                
            #thisSummaryString += "[{} group with {} points]".format(group,cntPoints)
                
        #print "{}-The {} system: {}".format(cntSystems,system,thisSummaryString)
    #print "{} systems".format(cntSystems)
        



       
def showSimplerStructure(d):
    #print d
    cntSystems = 0
    for system, value in d.iteritems():
        cntSystems += 1
        
        cntGroups = 0
        thisSummaryString = ""
        for group, value in d[system].iteritems():
            cntGroups += 1
            
            cntPoints = 0
            
            #print group, type(group)
            #print "DFddddd", d[system][group]
            for point in d[system][group]:
                cntPoints += 1
            thisSummaryString += "[{} group with {} points]".format(group,cntPoints)
                
        print "{}-The {} system: {}".format(cntSystems,system,thisSummaryString)
    #print "{} systems".format(cntSystems)
        
def checkStructure(d):
    #print d
    cntSystems = 0
    for system, value in d.iteritems():
        cntSystems += 1
        
        cntGroups = 0
        thisSummaryString = ""
        for group, value in d[system].iteritems():
            cntGroups += 1
            
            cntPoints = 0
            
            #print group, type(group)
            #print "DFddddd", d[system][group]
            thesePointNumbers = set()
            for point in d[system][group]:
                cntPoints += 1
                print "[{} system {} group ]".format(system, group)
                print point
                if point[group]["number"] in thesePointNumbers:
                    raise
                else:
                    thesePointNumbers.add(point[group]["number"])
                
            #thisSummaryString += "[{} group with {} points]".format(group,cntPoints)
                
        #print "{}-The {} system: {}".format(cntSystems,system,thisSummaryString)
    #print "{} systems".format(cntSystems)
        


def showStructure(d):
    for system, value in d.iteritems():
        print system
        #print d[system]
        for pointGroup, value in d[system].iteritems():
            print '\t' + pointGroup
            #print d[system][pointGroup]
            cnt = 0
            for point in d[system][pointGroup]:
                cnt = cnt + 1
                print '\t\t', cnt
                #print "Here", point
                for key, value in point.iteritems():
                    #pass
                    print '\t\t  ' + key, " - ", show1line(value)
                    #print value
                    #raise
                    #print d[system][pointGroup]
                #print point
        #if isinstance(value, dict):
        #    showStructure(value, indent+1)
        #elif isinstance(value, list):
        #    for item in value:
        #        print '\t' * (indent+1) + str(value)
            
#        else:
#            print '\t' * (indent+1) + str(value)






def _load_decathlon():
    #epwData = load_EPW_file(r'D:\Dropbox\00 Decathlon Development\Weather\EPW\CZ08RV2.epw')
    #print epwData
    #saveToMat([epwData],r"D:\Dropbox\00 Decathlon Development\02 Modeling update (shades)")
    #epwData.save_mat()
    
    #### LOAD THE FILES ####
    #projectDir = r"D:\Dropbox\00 Decathlon Development\02 Modeling update (shades)\Variants\00 TEST project only\OUT"
    projectDir = r"C:\DropBox\00 Decathlon Development\02 Modeling update (shades)\Variants\00 Open Open"
    outputMatDir = r"C:\Dropbox\00 Decathlon Development\02 Modeling update (shades)\output.mat"
    descriptionsFilePath = r"C:\DropBox\00 Decathlon Development\02 Modeling update (shades)\Input Data\Parameters r02.xlsx"
    resultFiles = load_BAL_files(projectDir) + load_OUT_files(projectDir)
    
    # Augment with descriptsion
    augmentDescriptions(resultFiles,descriptionsFilePath)
    
    convertKJHtoKW(resultFiles)
    
    #### ARRANGE THE FILES ####
    arrangedDictionary = arrangeData(resultFiles)
    showStructure(arrangedDictionary)
    showSimplerStructure(arrangedDictionary)
    
    #### GET THE TIME ####
    # Always customize the time when comparing different sources
    timeVector = getTime(resultFiles)
    timeColumns = [(2013,0,0,hour,0,0) for hour in timeVector]
    timeArray = numpy.array(timeColumns)
    timeDict = {"timeColumns":timeArray}
    #arrangedDictionary["time"] = timeDict
    
    exportDict = {}
    exportDict["trnData"] = arrangedDictionary
    exportDict["time"] = timeDict
    
    
    #### SAVE ####
    saveToMat(exportDict,outputMatDir)
    
    logging.info("Finished {}".format(whoami()))

def _testLoadOut():
    outFiles = load_OUT_files(r"D:\Dropbox\00 Decathlon Development\02 Modeling update (shades)\Variants\00 Open Open")

def _testLoadAll():
    projectDir = r"D:\Dropbox\00 Decathlon Development\02 Modeling update (shades)"
    outputMatDir = r"D:\Dropbox\00 Decathlon Development\02 Modeling update (shades)\output.mat"
    projectDir = r"C:\Dropbox\00 Decathlon Development\02 Modeling update (shades)"
    outputMatDir = r"C:\Dropbox\00 Decathlon Development\02 Modeling update (shades)\output.mat"    
    #balFiles = load_BAL_files(projectDir)
    outFiles = load_OUT_files(projectDir)
    saveToMat([outFiles])
