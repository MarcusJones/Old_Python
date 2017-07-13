
def applyZoneTemplate(IDFobj, templateObj):
    #print templateObj.templateDef
    # First, get the class to be multiplied;
    multClassObj = treeGetClass(templateObj.XML, templateObj.templateDef["multiply"])
    assert len(multClassObj) == 1, "Found {} objects, when only 1 is expected".format(templateObj.templateDef["multiply"])
    multClassObj = multClassObj[0]
    
    # Remove this class from the template, for further processing
    templateObj.XML.remove(multClassObj)

    # To get the fixed objects (all remaining)
    fixedObjects = templateObj.XML.xpath("//OBJECT")
    
    # Which are appended
    for object in fixedObjects:
        IDFobj.XML.append(object)
    
    # Get zone names
    targetZoneNames = idfGetZoneNameList(IDFobj, )
    
    zoneNameList=idfGetZoneNameList(IDFobj)
    for zoneName in zoneNameList:
        # Create an actual real copy, not just a reference
        thisMultiplyObject = copy.deepcopy(multClassObj)
        
        # Change the target zone name
        targetAttributeForZoneName = xpathRE(thisMultiplyObject, templateObj.templateDef["zoneName"])
        assert len(targetAttributeForZoneName) == 1, "Found {} objects, when only 1 is expected".format(templateObj.templateDef["multiply"])
        targetAttributeForZoneName = targetAttributeForZoneName[0]
        targetAttributeForZoneName.text = zoneName
        
        # Update the name of the object to be unique
        targetAttributeForUnqName = xpathRE(thisMultiplyObject, templateObj.templateDef["uniqueNameLoc"])
        assert len(targetAttributeForUnqName) == 1, "Found {} objects, when only 1 is expected".format(templateObj.templateDef["multiply"])
        targetAttributeForUnqName = targetAttributeForUnqName[0]
        
        newUniqueName = re.sub("ZoneName", zoneName, targetAttributeForUnqName.text)
        
        targetAttributeForUnqName.text = newUniqueName

        #printXML(thisMultiplyObject)
        IDFobj.XML.append(thisMultiplyObject)

    logging.debug(idStr("Appended {} {} objects from {} template".format(len(zoneNameList), templateObj.templateDef["multiply"],templateObj.ID ),
        IDFobj.ID))
    
    return IDFobj


   
def applyChange(IDFobj,change):
    """
    The method selects an ATTR node within a given named CLASS node with a given NAME (first attribute)
    and changes the value
    """
    className = change["class"]
    objectInstanceName = change["objName"]
    attributeComment= change["attr"]
    updateValue= str(change["newVal"])
    
    
    
    
    #print change
    xpathSearch = "".join([
        "//OBJECT/CLASS[re:match(text(), '" + className + "')]/..", # Select all class names
        "/ATTR[re:match(text(), '" + objectInstanceName + "')]/..", # Match the name
        "/ATTR/@Comment[re:match(.,'" + attributeComment+ "')]/..", # Same as above
        ])
    
    #targetClass = treeGetClass(IDFobj.XML, className)
    #print targetClass

    #print xpathRE(IDFobj.XML,"//OBJECT/CLASS[re:match(text(), '" + className + "')]")
    xmlClass = xpathRE(IDFobj.XML,"OBJECT/CLASS[re:match(text(), '" + className + "')]")
    #print xmlClass
    assert len(xmlClass) == 1
    #print printXML(xmlClass[0])
    #print printXML(xpathRE(xmlClass[0],"..")[0])
    #print 
    xmlAttr = xpathRE(xmlClass[0],"../ATTR[re:match(text(), '" + objectInstanceName + "')]/..")
    assert len(xmlAttr) == 1
    #xmlAttr = xpathRE(xmlClass[0],"/ATTR/@Comment[re:match(.,'" + attributeComment+ "')]/.."
    
    raise
    print xpathRE(IDFobj.XML,xpathSearch) 
    print xpathSearch
    queryElements = xpathRE(IDFobj.XML,xpathSearch) 
    #IDFobj.XML.xpath(xpathSearch,
    #                                   namespaces={"re": "http://exslt.org/regular-expressions"})
    print queryElements
    
    if not queryElements:
        raise NameError('Change attribute failed - {1} with name {2} not found in {0}'.format(className, attributeComment,objectInstanceName))

    for item in queryElements:
        oldValue = item.text
        
        item.text = updateValue

        
    logging.debug(idStr(
                'Updated "{0}" to "{1}" in "{2}" classes named "{5}" with comment "{3}" {4} times'.format(
                oldValue,updateValue,className,attributeComment,len(queryElements),objectInstanceName),
                IDFobj.ID)) 
    #return 
       




def tokenizeTemplateObj(IDDobj, className):
    raise
    classDef = treeGetClass(IDDobj.XML, className)
    assert len(classDef) == 1
    classDef = classDef[0]
    
    attribs = classDef.xpath("./ATTR")
    for attr in attribs:
        pass
    



                # Check for 'Name' attribute
                #print IDDboolHasField(classDef, "field",)
                #print IDDboolMatchField(classDef, "field", "Name")
                #print 
                #flgName = classDef.xpath("/ATTR[@field='Name']")
                #print classDef.xpath("./ATTR[@field='Name']")
                #print flgName
                #position = classDef.xpath("count(./ATTR[@field='Name']/preceding-sibling::*)+1")                
                #print tokenizeTemplateObj(IDDobj, objectClassName)
                
                #printXML(object.xpath('//CLASS')[0])





#--- Manipulate Objects / PENDING
def makeUniqueNames(IDFobj):
    allObjects = IDFobj.XML.xpath("OBJECT")
    print "Number of objects:", len(allObjects)
    xpathSearch = "//OBJECT/ATTR[1]/@Comment[re:match(.,'[/-]*[/s]*Name$')]/.."
    objects = IDFobj.XML.xpath(xpathSearch,
                namespaces={"re": "http://exslt.org/regular-expressions"})
    print "Number of objects:", len(objects)

    for ob in objects:
        print etree.tostring(ob)

    
    if 1:
        print "Number of names:", len(objects)
        for ob in objects:
            print etree.tostring(ob)

            
        print objects
        
        namedTupleList = [(object.xpath('preceding-sibling::*')[0].text, object.text) for object in objects]
        
        print namedTupleList
        
        nameList = tuple([x[1] for x in namedTupleList])
        
        print nameList
        
        countedDupList = IDFobj.countDuplicatesInList(nameList)
        
        print countedDupList
        
        print countedDupList
        
        for item in countedDupList:
            if item[1] > 1:
                print "Found {0} {1} names".format(item[0], item[1])
                object = IDFobj.XML.xpath("OBJECT/ATTR[1]/@Comment[re:match(.,'^[/s]*Office1')]/..".format(item[0]))
                print  len(object)
            else: 
                pass


def selectCommentedAttrAndChange(IDFobj,change):
    """
    The method selects an ATTR node within a given named CLASS node
    and changes the value
    """
    className = change[0]
    attributeComment= change[1]
    updateValue= change[2]
    
    xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]/../ATTR/@Comment[re:match(.,'" + attributeComment+ "')]/.."
    
    queryElements = IDFobj.XML.xpath(xpathSearch,
                                       namespaces={"re": "http://exslt.org/regular-expressions"})
    #print queryElements
    if not queryElements:
        raise NameError('Change attribute failed - {1} not found in {0}'.format(className, attributeComment))

    for item in queryElements:
        oldValue = item.text
        item.text = updateValue
        
    logging.debug(idStr(
                'Updated "{0}" to "{1}" in "{2}" class with comment "{3}" {4} times'.format(
                oldValue,updateValue,className,attributeComment,len(queryElements)),
                IDFobj.ID)) 









class Template(object):
    def __init__(self,ID, absolutePath, templateStyle, multiplyClass,zoneNamePointer):
        self.ID              = ID             
        self.absolutePath    = absolutePath  
        self.templateStyle = templateStyle
        self.multiplyClass   = multiplyClass  
        self.zoneNamePointer = zoneNamePointer
        
    def __str__(self):
        return self.ID

class SingularTemplate(Template):
    def __init__(self,ID, absolutePath, templateStyle, multiplyClass,zoneNamePointer):
        super(SingularTemplate, self).__init__(ID, absolutePath, templateStyle, multiplyClass,zoneNamePointer)
        logging.info("Created a SingularTemplate {0}".format(self))
    
class N2N_Template(Template):
    def __init__(self,ID, absolutePath, templateStyle, multiplyClass,zoneNamePointer):
        super(N2N_Template, self).__init__(ID, absolutePath, templateStyle, multiplyClass,zoneNamePointer)
        logging.info("Created a N2N_Template {0}".format(self))
        
class NamedN2N_Template(Template):
    def __init__(self,ID, absolutePath, templateStyle, multiplyClass,zoneNamePointer,namingList):
        super(NamedN2N_Template, self).__init__(ID, absolutePath, templateStyle, multiplyClass,zoneNamePointer)
        self.uniqueNamePointer = namingList[0]
        self.uniqueNameTemplate = namingList[1]
        self.namingList = namingList
        logging.info("Created a NamedN2N_Template {0}".format(self))
            
class NamedN2NwithPointers_Template(Template):
    def __init__(self,ID, absolutePath, templateStyle, multiplyClass,zoneNamePointer,namingList,pointerList):
        super(NamedN2N_Template, self).__init__(ID, absolutePath, templateStyle, multiplyClass,zoneNamePointer)
        self.namingList = namingList
        self.pointerList = pointerList
        logging.info("Created a NamedN2N_Template {0}".format(self))    
            
class Variant(object):
    def __init__(self, ID, sourceFileAbsPath, 
                 targetDirAbsPath, templateDescriptions, changesList):
        self.ID = ID
        #self.sourceFileRelPath = sourceFileRelPath
        self.sourceFileAbsPath = sourceFileAbsPath
        #self.targetDirRelPath = targetDirRelPath
        self.targetDirAbsPath = targetDirAbsPath
        # List of lists of templates 
        self.templateDescriptions = templateDescriptions
        # List of lists of changes        
        self.changesList = changesList
        
        logging.info("Created a Variant: {0}".format(self))
        
    def __str__(self):
        return "Variant ID: {0}, sourceFile: {1}, targetDir: {2}, with {3} templates, {4} changes".format(self.ID, self.sourceFileAbsPath, self.targetDirAbsPath, len(self.templateDescriptions), len(self.changesList))
    
    def checkTemplates(self):
        pass
    
    def createAbsolutePaths(self,):
        pass




def formatBlock(block):
        '''Format the given block of text, trimming leading/trailing
        empty lines and any leading whitespace that is common to all lines.
        The purpose is to let us list a code block as a multiline,
        triple-quoted Python string, taking care of indentation concerns.'''
        # separate block into lines
        lines = str(block).split('\n')
        # remove leading/trailing empty lines
        while lines and not lines[0]:  del lines[0]
        while lines and not lines[-1]: del lines[-1]
        # look at first line to see how much indentation to trim
        ws = re.match(r'\s*',lines[0]).group(0)
        if ws:
                lines = map( lambda x: x.replace(ws,'',1), lines )
        # remove leading/trailing blank lines (after leading ws removal)
        # we do this again in case there were pure-whitespace lines
        while lines and not lines[0]:  del lines[0]
        while lines and not lines[-1]: del lines[-1]
        return '\n'.join(lines)+'\n'





def nothtin():



        
        #print templateDefs
        
        
        #print len(templates)
        #sectionLimits[0] = sectionLimits[0]
        #print sectionLimits
        

    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(variants)
        
#    for start in variantBlockLimits:
#        print start, variantBlockLimits
#    print variantBlock
    
    
    
    
    raise
    #sheet = book.Sheets('(Variants)')

    
    
    
    
    
    
    
    
    
    
    xl.Visible = False
    
    variantsList = list()    
    # Scan down
    for row in range(1,1000):
        # Found a variant section row
        if sheet.Cells(row,1).Value != None and not re.search(r"skip",sheet.Cells(row,1).Value):
            # Load the general data
            ID = str(sheet.Cells(row,3).Value)
            #sourceFileRelPath = str(sheet.Cells(row,4).Value)
            #sourceFileRelPath = os.path.normpath(sourceFileRelPath)
            sourceFileAbsPath = str(sheet.Cells(row,4).Value)
            sourceFileAbsPath = os.path.normpath(sourceFileAbsPath)            
            targetDirRelPath = str(sheet.Cells(row,5).Value)
            targetDirRelPath = os.path.normpath(targetDirRelPath)
            # Load the templates
            templateDescriptions = list() 
            # First place cursor at first template 
            row = row + 3
            col = 3
            while sheet.Cells(row,col).Value != None:
                thisTemplate = list()
                for col in range(3,5):
                    thisTemplate.append(sheet.Cells(row,col).Value)
                templateDescriptions.append(thisTemplate)
                # Now carriage return
                row += 1
                col = 3
                
            # Load the changes
            changesList = list() 
            # First place cursor at first template 
            row = row + 1
            row = row + 1
            col = 3
            while sheet.Cells(row,col).Value != None:
                thisChange = list()
                for col in range(3,7):
                    aValue = str(sheet.Cells(row,col).Value)
                    thisChange.append(aValue)
                    #print aValue, "at", col
                changesList.append(thisChange)
                # Now carriage return
                row += 1
                col = 3       
            
            #sourceFileAbsPath = os.path.join(inputAbsDirStem,sourceFileRelPath)
            #sourceFileAbsPath = os.path.normpath(sourceFileAbsPath)
            targetDirAbsPath = os.path.join(targetAbsDirStem,targetDirRelPath,ID + ".idf")
            targetDirAbsPath = os.path.normpath(targetDirAbsPath)
            
            variantDef = {
                          "sourcePath":sourceFileAbsPath,
                          "targetDirAbsPath":targetDirAbsPath,
                          "templateDescriptions":templateDescriptions,
                          "changesList":changesList,
                          }
#            variantsList.append(Variant(
#                                        ID=ID,
#                                        #sourceFileRelPath = sourceFileRelPath,
#                                        sourceFileAbsPath = sourceFileAbsPath,
#                                        #targetDirRelPath=targetDirRelPath,
#                                        targetDirAbsPath = targetDirAbsPath,
#                                        templateDescriptions=templateDescriptions,
#                                        changesList=changesList,
#                                        )
#                                        )

    book.Close(SaveChanges=0) #to avoid prompt

    return variantsList 
    
#    while variantNumber != "None":
#        variantID = str(sheet.Cells(currentLine,colID).Value)
#        variantPath = str(sheet.Cells(currentLine,4).Value)
#        variantZoneMultiplyClass = str(sheet.Cells(currentLine,5).Value)
#        variantZoneNameReplaceTarget = str(sheet.Cells(currentLine,6).Value) 
#        print templateName
#        if (templateName == "None"):
#            break
#        templateList.append(Template(templateID, templatePath, templateZoneMultiplyClass, templateZoneNameReplaceTarget))
#        currentLine += 1
    
    book.Close(False)
    xl.Application.Quit()

#    for template in templateList:
#        print template.ID, template.inputPath

    
def listZones(IDFobj, zoneName=None):
    # Select all class objects which have ^Zone$ in the name (only zones) and return it's Parent (Object)
    xpathSearch = "//CLASS[re:match(text(), '^Zone$')]/.."
    
    zones = IDFobj.XML.xpath(xpathSearch,
                namespaces={"re": "http://exslt.org/regular-expressions"})
    
    zoneCntr = 1
    
    names = [] 
    for zone in zones:
        nameXml = zone.xpath('ATTR')
        #print nameXml[0]
        name = nameXml[0].text
        names.append(name)
        #print'{0:0} {1:20} | {2:10}'.format(zoneCntr, type[0].text, name[0].text)
        zoneCntr += 1

    logging.debug(idStr(
        "Returned list of {0} zones".format(len(names)),
        IDFobj.ID))
    
    return names

def queryClass(self, stringRegexQuery):
    xpathSearch = "//CLASS[re:match(text(), '" + stringRegexQuery + "')]"
    queryElements = self.XML.xpath(xpathSearch,
                namespaces={"re": "http://exslt.org/regular-expressions"})
    
    #print "Query", stringRegexQuery, "returns", len(queryElements), "elements"

    return queryElements
#--- XML Utilities
def listZonesWithName(IDFobj, zoneName='.'):
    
    # By default, the zoneName regex is '.' which matches ALL
    
    # Select all class objects which have ^Zone$ in the name (only zones) and return it's Parent (Object)
    #xpathSearch = "//CLASS[re:match(text(), '^Zone$')]/.."
    #xpathSearch = "//CLASS[re:match(text(), '{0}')]/../ATTR".format('^Zone$')
    xpathSearch = "//CLASS[re:match(text(), '{0}')]/../ATTR[1][re:match(text(), '{1}')]/..".format('^Zone$',zoneName)

    zones = IDFobj.XML.xpath(xpathSearch,
                namespaces={"re": "http://exslt.org/regular-expressions"})
    
    zoneCntr = 1
    
    names = [] 
    for zone in zones:
        nameXml = zone.xpath('ATTR')
        #print nameXml[0]
        name = nameXml[0].text
        names.append(name)
        zoneCntr += 1

    logging.debug(idStr(
        "Returned list of {0} zones matching {1}".format(len(names), zoneName),
        IDFobj.ID))
    
    return names


#TODO: Delete this
#def query(self, stringQuery):
#    
#    queryElements = self.XML.xpath(stringQuery)
#    
#    print "Query", stringQuery, "returns", len(queryElements), "elements"

def queryRe(self, XML, xpathSearch):
    
    queryElements = XML.xpath(xpathSearch,
                                   namespaces={"re": "http://exslt.org/regular-expressions"})
            
    return queryElements




#--- Manipulate Objects / CONFIRMED

def countDuplicatesInList(IDFobj,dupedList):
    uniqueSet = set(item for item in dupedList)
    return [(item, dupedList.count(item)) for item in uniqueSet]





#--- Introspection / PENDING

def thisObjectStatus(IDFobj):
    #print 'Status of ', IDFobj.ID
    if len(IDFobj.XML):
        countObjects = IDFobj.XML.xpath('OBJECT')
        #print IDFobj.ID, ': XML objects:', len(countObjects)
    if IDFobj.IDDstring:
        pass
        #print IDFobj.ID, ': IDF lines:,', len(IDFobj.IDDstring)
    if IDFobj.pathIdfOutput:
        pass
        #print IDFobj.ID, ': IDF output path',IDFobj.pathIdfOutput
    if IDFobj.pathXmlOutput:
        pass
        #print self.ID, ': IDF output path',self.pathXmlOutput


def linkedSurfaces(IDFobj,nameOfSpace):
    
    className = "OS:Surface"
    xpathSearch = "".join([
    "//OBJECT/CLASS[re:match(text(), '" + className + "')]",
    "/..",
    "/ATTR[4] [re:match(.,'" + nameOfSpace + "')]",
    "/..",
    ])
    # [re:match(.,'" + nameOfSpace + "')]
    queryElements = IDFobj.XML.xpath(xpathSearch,
                                   namespaces={"re": "http://exslt.org/regular-expressions"})
            
    #print 
    
    logging.debug(idStr('Returned {} linked surfaces of space {}'.format(len(queryElements),nameOfSpace),IDFobj.ID))
    
    return queryElements

def linkedZone(IDFobj,thisSpacesZoneName):
    
    className = "OS:ThermalZone"
    xpathSearch = "".join([
    "//OBJECT/CLASS[re:match(text(), '" + className + "')]",
    "/..",
    "/ATTR[1] [re:match(.,'" + thisSpacesZoneName + "')]",
    "/..",
    ])
    
    queryElements = IDFobj.queryRe(IDFobj.XML, xpathSearch)
    
    #print queryElements
    
    logging.debug(idStr('Returned {} linked zones to {}'.format(len(queryElements),thisSpacesZoneName),IDFobj.ID))
    
    return queryElements


def linkedSubSurfaces(IDFobj,surface):
    
    queryElements = []
    
    # Get surface name
    xpathSearch = "".join([
    "ATTR[1]", # Select the first attribute
    ])
    queryElements = surface.xpath(xpathSearch,
                                   namespaces={"re": "http://exslt.org/regular-expressions"})
    
    #print queryElements
    nameOfSurface = queryElements[0].text            

    className = "^OS:SubSurface$"
    xpathSearch = "".join([
    "//OBJECT/CLASS[re:match(text(), '" + className + "')]",
    "/..",
    "/ATTR[4] [re:match(.,'" + nameOfSurface + "')]",
    "/..",
    ])
    # [re:match(.,'" + nameOfSpace + "')]
    queryElements = IDFobj.XML.xpath(xpathSearch,
                                   namespaces={"re": "http://exslt.org/regular-expressions"})
    #print queryElements
    
    #logging.debug(idStr('Returned {0} linked sub-surfaces for surface {1}'.format(len(queryElements),nameOfSurface),IDFobj.ID))
    return queryElements



#----- OLD

def loadTemplatesOLD(templateDir):
    
    logging.debug("Loading templates from {0}".format(templateDir))
    
    #endCol = 1000
    #endRow = 1000           

    # Attach the excel COM object
    #xl = Dispatch('Excel.Application')

    # Open the input file
    #book = xl.Workbooks.Open(inputExcelPath)
    
    # Select the sheet
    #sheet = book.Sheets('Templates')

#    globalTemplatePath = sheet.Cells(1,2).Value
#    globalTemplatePath = os.path.normpath(globalTemplatePath)
    
    # Get the markers, place into a dictionary
    markerRow = 2
    markers = {}    
    for col in range(1,endCol):
        thisValue = sheet.Cells(markerRow,col).Value
        if thisValue != None:
            markers[str(thisValue)] = col -1
            #print thisValue
        #print markers
    
    # Could replace this whole section with xlrd module
    # But using COM is more fun!
    #templateArray = list()
    templatesList = list()

    # Loop through the templates
    for row in range(4,endRow):
        #thisTemplateID = sheet.Cells(row,1).Value
        # Found a template row
        if sheet.Cells(row,1).Value != None:
            # Start a list for this tempate
            #print thisTemplateID,
            # Now run over this row
            ID = sheet.Cells(row,1).Value
            relativePath = sheet.Cells(row,2).Value
            absolutePath = os.path.join(templatesFileDirStem,relativePath)
            absolutePath = os.path.normpath(absolutePath)
            templateStyle = sheet.Cells(row,3).Value
            multiplyClass = sheet.Cells(row,4).Value
            zoneNamePointer = sheet.Cells(row,5).Value
            
            namingList = list()
            for col in range(markers['Naming']+1,markers['Pointers']+1):
                thisValue = sheet.Cells(row,col).Value
                if thisValue != None:
                    namingList.append(str(thisValue))
                    
            pointerList = list()
            for col in range(markers['Pointers'],markers['End']+1):
                thisValue = sheet.Cells(row,col).Value
                if thisValue != None:
                    pointerList.append(str(thisValue))
                                   
            if templateStyle == "One":
                templatesList.append(SingularTemplate(ID, absolutePath, templateStyle, multiplyClass,zoneNamePointer))
            elif templateStyle == "N to N":
                templatesList.append(N2N_Template(ID, absolutePath, templateStyle, multiplyClass,zoneNamePointer))
            elif templateStyle == "Named N to N":
                templatesList.append(NamedN2N_Template(ID, absolutePath, templateStyle, multiplyClass,zoneNamePointer,namingList))


            #templateArray.append(templateList)
    
#    book.Close(SaveChanges=0) #to avoid prompt
#    xl.Application.Quit()

    book.Close(False)
    xl.Application.Quit()
    
    # Split up the list into seperate lists
#    for templateList in templateArray:
#        #generalList = templateList[0:markers['Naming']]
#        namingList = templateList[markers['Naming']:markers['Pointers']]
#        pointerList =  templateList[markers['Pointers']:-1]
#        #print generalList,namingList,pointerList
#        
#        templateStyle = generalList[2]
#        
#        if templateStyle == "One":
#            templatesList.append(SingularTemplate(generalList))
#        elif templateStyle == "N to N":
#            templatesList.append(N2N_Template(generalList))
#        elif templateStyle == "Named N to N":
#            templatesList.append(NamedN2N_Template(generalList,namingList,pointerList))

            
    return templatesList












#===============================================================================
# 
# def xslTransform(self, xslFilePath):
#    transformFileHandle = open(xslFilePath, 'r')
#    xmlTransform = etree.parse(transformFileHandle)
#    transform = etree.XSLT(xmlTransform)
#    self.XML = transform(xmlFile)
# 
# 
# 
# def _testAddZonesToSpaces():
#    spaceAndSurfAndSubs = formatBlock("""
#             OS:Space,
#             OS:Space 1,               ! Name
#             ,                         ! Space Type Name
#             ,                         ! Default Construction Set Name
#             ,                         ! Default Schedule Set Name
#             -0,                       ! Direction of Relative North {deg}
#             0,                        ! X Origin {m}
#             0,                        ! Y Origin {m}
#             0,                        ! Z Origin {m}
#             ,                         ! Building Story Name
#             OS:ThermalZone 2,         ! Thermal Zone Name
#             ;                         ! Part of Total Floor Area
#             
#             OS:Surface,
#             OS:Surface 1,             ! Name
#             Floor,                    ! Surface Type
#             ,                         ! Construction Name
#             OS:Space 1,               ! Space Name
#             Ground,                   ! Outside Boundary Condition
#             ,                         ! Outside Boundary Condition Object
#             NoSun,                    ! Sun Exposure
#             NoWind,                   ! Wind Exposure
#             ,                         ! View Factor to Ground
#             ,                         ! Number of Vertices
#             6,4,0,                    ! X,Y,Z Vertex 1 {m}
#             6,0,0,                    ! X,Y,Z Vertex 2 {m}
#             0,0,0,                    ! X,Y,Z Vertex 3 {m}
#             0,4,0;                    ! X,Y,Z Vertex 4 {m}
#    
#             OS:Surface,
#             OS:Surface 2,             ! Name
#             Wall,                     ! Surface Type
#             ,                         ! Construction Name
#             OS:Space 1,               ! Space Name
#             Outdoors,                 ! Outside Boundary Condition
#             ,                         ! Outside Boundary Condition Object
#             SunExposed,               ! Sun Exposure
#             WindExposed,              ! Wind Exposure
#             ,                         ! View Factor to Ground
#             ,                         ! Number of Vertices
#             0,0,2.7000000000000002,   ! X,Y,Z Vertex 1 {m}
#             0,0,0,                    ! X,Y,Z Vertex 2 {m}
#             6,0,0,                    ! X,Y,Z Vertex 3 {m}
#             6,0,2.7000000000000002;   ! X,Y,Z Vertex 4 {m}
#    
#             OS:Surface,
#             OS:Surface 5,             ! Name
#             Wall,                     ! Surface Type
#             ,                         ! Construction Name
#             OS:Space 2,               ! Space Name
#             Outdoors,                 ! Outside Boundary Condition
#             ,                         ! Outside Boundary Condition Object
#             SunExposed,               ! Sun Exposure
#             WindExposed,              ! Wind Exposure
#             ,                         ! View Factor to Ground
#             ,                         ! Number of Vertices
#             0,0,2.7000000000000002,   ! X,Y,Z Vertex 1 {m}
#             0,0,0,                    ! X,Y,Z Vertex 2 {m}
#             6,0,0,                    ! X,Y,Z Vertex 3 {m}
#             6,0,2.7000000000000002;   ! X,Y,Z Vertex 4 {m}            
#             
#             OS:SubSurface,
#             OS:SubSurface 1,          ! Name
#             FixedWindow,              ! Sub Surface Type
#             ,                         ! Construction Name
#             OS:Surface 2,             ! Surface Name
#             ,                         ! Outside Boundary Condition Object
#             ,                         ! View Factor to Ground
#             ,                         ! Shading Control Name
#             ,                         ! Frame and Divider Name
#             ,                         ! Multiplier
#             ,                         ! Number of Vertices
#             0.93427029703359998,0,2.1604596089317107,  ! X,Y,Z Vertex 1 {m}
#             0.93427029703359998,0,0.83675960893171086,  ! X,Y,Z Vertex 2 {m}
#             3.9024702970336,0,0.83675960893171086,  ! X,Y,Z Vertex 3 {m}
#             3.9024702970336,0,2.1604596089317107;  ! X,Y,Z Vertex 4 {m}
#             
#             OS:SubSurface,
#             OS:SubSurface 2,          ! Name
#             Door,                     ! Sub Surface Type
#             ,                         ! Construction Name
#             OS:Surface 2,             ! Surface Name
#             ,                         ! Outside Boundary Condition Object
#             ,                         ! View Factor to Ground
#             ,                         ! Shading Control Name
#             ,                         ! Frame and Divider Name
#             ,                         ! Multiplier
#             ,                         ! Number of Vertices
#             4.5089088920158424,0,2.0103999999999997,  ! X,Y,Z Vertex 1 {m}
#             4.5089088920158424,0,0,   ! X,Y,Z Vertex 2 {m}
#             5.4381088920158422,0,0,   ! X,Y,Z Vertex 3 {m}
#             5.4381088920158422,0,2.0103999999999997;  ! X,Y,Z Vertex 4 {m}
#             """)
#    
# 
#    thisIDF = IDF()
#    thisIDF.IDDstring = spaceAndSurfAndSubs
# 
#    thisIDF.parseIDFtoXML()
# 
#    thisIDF.cleanOutObject(keptClassesDict['openStudioGeomNoZones'])
#    
#    logging.info("The original XML:")
#    #thisIDF.printToScreenXml()
#    
#    thisIDF.addZonesToSpaces()
# 
#    logging.info("The new XML:")
#    #thisIDF.printToScreenXml()
# 
# def _testRenaming():
#    spaceAndSurfAndSubs = formatBlock("""
#             OS:Space,
#             OS:Space 1,               ! Name
#             ,                         ! Space Type Name
#             ,                         ! Default Construction Set Name
#             ,                         ! Default Schedule Set Name
#             -0,                       ! Direction of Relative North {deg}
#             0,                        ! X Origin {m}
#             0,                        ! Y Origin {m}
#             0,                        ! Z Origin {m}
#             ,                         ! Building Story Name
#             OS:ThermalZone 2,         ! Thermal Zone Name
#             ;                         ! Part of Total Floor Area
#             
#             OS:Surface,
#             OS:Surface 1,             ! Name
#             Floor,                    ! Surface Type
#             ,                         ! Construction Name
#             OS:Space 1,               ! Space Name
#             Ground,                   ! Outside Boundary Condition
#             ,                         ! Outside Boundary Condition Object
#             NoSun,                    ! Sun Exposure
#             NoWind,                   ! Wind Exposure
#             ,                         ! View Factor to Ground
#             ,                         ! Number of Vertices
#             6,4,0,                    ! X,Y,Z Vertex 1 {m}
#             6,0,0,                    ! X,Y,Z Vertex 2 {m}
#             0,0,0,                    ! X,Y,Z Vertex 3 {m}
#             0,4,0;                    ! X,Y,Z Vertex 4 {m}
#    
#             OS:Surface,
#             OS:Surface 2,             ! Name
#             Wall,                     ! Surface Type
#             ,                         ! Construction Name
#             OS:Space 1,               ! Space Name
#             Outdoors,                 ! Outside Boundary Condition
#             ,                         ! Outside Boundary Condition Object
#             SunExposed,               ! Sun Exposure
#             WindExposed,              ! Wind Exposure
#             ,                         ! View Factor to Ground
#             ,                         ! Number of Vertices
#             0,0,2.7000000000000002,   ! X,Y,Z Vertex 1 {m}
#             0,0,0,                    ! X,Y,Z Vertex 2 {m}
#             6,0,0,                    ! X,Y,Z Vertex 3 {m}
#             6,0,2.7000000000000002;   ! X,Y,Z Vertex 4 {m}
#    
#             OS:Surface,
#             OS:Surface 5,             ! Name
#             Wall,                     ! Surface Type
#             ,                         ! Construction Name
#             OS:Space 2,               ! Space Name
#             Outdoors,                 ! Outside Boundary Condition
#             ,                         ! Outside Boundary Condition Object
#             SunExposed,               ! Sun Exposure
#             WindExposed,              ! Wind Exposure
#             ,                         ! View Factor to Ground
#             ,                         ! Number of Vertices
#             0,0,2.7000000000000002,   ! X,Y,Z Vertex 1 {m}
#             0,0,0,                    ! X,Y,Z Vertex 2 {m}
#             6,0,0,                    ! X,Y,Z Vertex 3 {m}
#             6,0,2.7000000000000002;   ! X,Y,Z Vertex 4 {m}            
#             
#             OS:SubSurface,
#             OS:SubSurface 1,          ! Name
#             FixedWindow,              ! Sub Surface Type
#             ,                         ! Construction Name
#             OS:Surface 2,             ! Surface Name
#             ,                         ! Outside Boundary Condition Object
#             ,                         ! View Factor to Ground
#             ,                         ! Shading Control Name
#             ,                         ! Frame and Divider Name
#             ,                         ! Multiplier
#             ,                         ! Number of Vertices
#             0.93427029703359998,0,2.1604596089317107,  ! X,Y,Z Vertex 1 {m}
#             0.93427029703359998,0,0.83675960893171086,  ! X,Y,Z Vertex 2 {m}
#             3.9024702970336,0,0.83675960893171086,  ! X,Y,Z Vertex 3 {m}
#             3.9024702970336,0,2.1604596089317107;  ! X,Y,Z Vertex 4 {m}
#             
#             OS:SubSurface,
#             OS:SubSurface 2,          ! Name
#             Door,                     ! Sub Surface Type
#             ,                         ! Construction Name
#             OS:Surface 2,             ! Surface Name
#             ,                         ! Outside Boundary Condition Object
#             ,                         ! View Factor to Ground
#             ,                         ! Shading Control Name
#             ,                         ! Frame and Divider Name
#             ,                         ! Multiplier
#             ,                         ! Number of Vertices
#             4.5089088920158424,0,2.0103999999999997,  ! X,Y,Z Vertex 1 {m}
#             4.5089088920158424,0,0,   ! X,Y,Z Vertex 2 {m}
#             5.4381088920158422,0,0,   ! X,Y,Z Vertex 3 {m}
#             5.4381088920158422,0,2.0103999999999997;  ! X,Y,Z Vertex 4 {m}
#             """)    
#    thisIDF = IDF()
#    thisIDF.IDDstring = spaceAndSurfAndSubs
# 
#    thisIDF.parseIDFtoXML()
# 
#    thisIDF.cleanOutObject(keptClassesDict['openStudioGeomNoZones'])
#    
#    thisIDF.renameSpaces("FirstFloor")
# 
#    thisIDF.renameSurfaces("FirstFloor")
# 
# def _CleanOutSolarDecathlon2011():
# 
#    logging.debug("Cleaning out the decathlon file for further work!")
# 
#    logging.info("Started IDF test script")
# 
#    # The test    
#    inputIDF = r"D:\Dropbox\\00 Decathlon Development\EnergyPlus\Decath r11.idf"
#    outputIDF = r"D:\Freelancing\TemplateTestDirectory\Decath r11.idf"
# 
#    #testXMLout = r"C:\Freelance\Simulation\testOut.xml"
# 
#    testIDF = IDF(
#            pathIdfInput=inputIDF, 
#            XML=None, 
#            IDDstring = None, 
#            IDstring = None, 
#            description = None, 
#            pathIdfOutput = outputIDF
#            )
#    
# 
#    # Call the load        
#    testIDF.loadIDF()
#    # Call convert
#    testIDF.parseIDFtoXML()
#    
#    testIDF.convertXMLtoIDF()
#    
#    #testIDF.writeXml(testXMLout)
#    testIDF.cleanOutObject(keptClassesDict['onlyGeometry'])
# 
#    #testIDF.
#    
#    testIDF.convertXMLtoIDF()
# 
#    testIDF.writeIdf(outputIDF)
# 
#    logging.info("Finished Cleaning out the decathlon file for further work!")
#    
# 
# def _removeShadingSurfaces():
# 
#    logging.debug("Sta")
# 
#    logging.info("Started IDF test script")
# 
#    inputIDFpath = r"D:\Freelancing\046_Al_Ain_Tech_Th\IDF\Proposed_r00.idf"
#    outputIDFpath = r"D:\Freelancing\046_Al_Ain_Tech_Th\IDF\Baseline_r00.idf"
# 
#    inputIDF = IDF(
#            pathIdfInput=inputIDFpath, 
#            XML=None, 
#            IDDstring = None, 
#            IDstring = None, 
#            description = None, 
#            pathIdfOutput = outputIDFpath
#            )
#    
# 
#    # Call the load        
#    inputIDF.loadIDF()
#    # Call convert
#    inputIDF.parseIDFtoXML()
# 
#    inputIDF.deleteShadingSurfacesFromIDF()
#    
#    #testIDF.convertXMLtoIDF()
#    
#    #testIDF.writeXml(testXMLout)
#    #testIDF.cleanOutObject(keptClassesDict['onlyGeometry'])
# 
#    #testIDF.
#    
#    #inputIDF.convertXMLtoIDF()
# 
#    inputIDF.writeIdf(outputIDFpath)
# 
#    logging.info("Finished !")
#    
# 
# 
#    
# def OLDparseIDFtoXMLtextInput(self,IDFtext):
#    
#    #=======================================================================
#    # This is the updated version, with the capability to handle OSM files!
#    #=======================================================================
# 
#    lines = IDFtext.split("\n")
#    
#    #print lines
#    
#    # Start the XML tree
#    xmlVer = "0.1"
#    # Root tag
#    currentXML = etree.Element("EnergyPlus_XML", XML_version=xmlVer)
#    # A comment
#    commentXML = etree.Comment("XML Schema for EnergyPlus version 6 'IDF' files and OpenStudio version 0.3.0 'OSM' files")
#    currentXML.append(commentXML)
#    # Another comment
#    commentXML = etree.Comment("Schema created April. 2011 by Marcus Jones")
#    currentXML.append(commentXML)
#    
#    lineIndex = 0
#    #zoneNameIndex = 0
#    
#    #print len(lines)
#    
#    flagStart = False
#    flagEnd = False
#    
#    
#    # Loop over each line
#    while (lineIndex < len(lines)) :
#        
#        thisLine = lines[lineIndex]
#        
#        # Strip the comment
#        comment = "No comment"
#        if re.search(r"!", thisLine,re.VERBOSE):
#            values,comment = re.split(r"!", thisLine,re.VERBOSE)
#            comment = comment.rstrip()
#            comment = comment.lstrip()                
#            #print values
#            thisLine = values
#        # And strip any white space
#        thisLine = thisLine.rstrip()
#        thisLine = thisLine.lstrip()
# 
#        
#        #print thisLine
#        
#        # If it has no , or ;, completely skip the line
#        # Otherwise do this:
#        if re.search(r"[,;]", thisLine,re.VERBOSE):
#            
#            #print "2"
#            #print thisLine
#            
#            # This is a HACK
#            appendThis = ""
#            if re.search(r";", thisLine,re.VERBOSE):
#                appendThis = ";"
#            
#            items = re.split(r"[,;]", thisLine,re.VERBOSE)
#            
#            #print items
#            # re.split annoyingly returns an extra entry at the end 
#            # REMOVE IT
#            items = items[0:-1]
#            #print items
#            
#            # More HACK
#            items[-1] = items[-1] + appendThis
#            #print items
#            
#            for item in items:
#                item.rstrip()
#                item.lstrip()
#                
#                if not item and not flagStart:
#                    #print ""
#                    raise "Blank - Should NEVER see thsi!"
# 
#                # Found a ;, END
#                # Create an ATTR
#                elif re.search(r";", item,re.VERBOSE) and flagStart: 
#                    flagStart = False
#                    #print "END", item
#                    item = item.replace(r";","")
#                    thisAttrXML = etree.SubElement(thisObjectXML, "ATTR")
#                    thisAttrXML.text = item
#                    thisAttrXML.set("Comment", comment)
#                    
#                
#                # Found a START
#                # Create a CLASS
#                elif not flagStart:
#                    flagStart = True
#                    #print "START", item
# 
#                    # Start an Object
#                    thisObjectXML = etree.SubElement(currentXML, "OBJECT")
#                    # An object always has a Class
#                    thisClassXML = etree.SubElement(thisObjectXML, "CLASS")
#                    thisClassXML.text = item
#                
#                # Found a INSIDE
#                # Create an ATTR         
#                elif flagStart: 
#                    #print "INSIDE", item
#                    thisAttrXML = etree.SubElement(thisObjectXML, "ATTR")
#                    thisAttrXML.text = item
#                    thisAttrXML.set("Comment", comment)
#                    
# 
#             
#        lineIndex += 1
#        # END WHILE 
#    # END IF
#    XML = currentXML
#    
#    objects = self.XML.xpath('//OBJECT')
# 
#    logging.debug(idStr(
#        'Converted IDF to XML with {0} objects'.format(int(len(objects))),
#        self.ID))
#    
#    return XML
#    
#    
#    
# def _transformSpaceToZoneXPATH():
# 
#    spaceAndSurfaceText = formatBlock("""
#            OS:Space,
#            OS:Space 1,               ! Name
#            ,                         ! Space Type Name
#            ,                         ! Default Construction Set Name
#            ,                         ! Default Schedule Set Name
#            -0,                       ! Direction of Relative North {deg}
#            0,                        ! X Origin {m}
#            0,                        ! Y Origin {m}
#            0,                        ! Z Origin {m}
#            ,                         ! Building Story Name
#            OS:ThermalZone 2,         ! Thermal Zone Name
#            ;                         ! Part of Total Floor Area
#            
#            OS:Surface,
#            OS:Surface 1,             ! Name
#            Floor,                    ! Surface Type
#            ,                         ! Construction Name
#            OS:Space 1,               ! Space Name
#            Ground,                   ! Outside Boundary Condition
#            ,                         ! Outside Boundary Condition Object
#            NoSun,                    ! Sun Exposure
#            NoWind,                   ! Wind Exposure
#            ,                         ! View Factor to Ground
#            ,                         ! Number of Vertices
#            6,4,0,                    ! X,Y,Z Vertex 1 {m}
#            6,0,0,                    ! X,Y,Z Vertex 2 {m}
#            0,0,0,                    ! X,Y,Z Vertex 3 {m}
#            0,4,0;                    ! X,Y,Z Vertex 4 {m}
# 
#            OS:Surface,
#            OS:Surface 2,             ! Name
#            Wall,                     ! Surface Type
#            ,                         ! Construction Name
#            OS:Space 1,               ! Space Name
#            Outdoors,                 ! Outside Boundary Condition
#            ,                         ! Outside Boundary Condition Object
#            SunExposed,               ! Sun Exposure
#            WindExposed,              ! Wind Exposure
#            ,                         ! View Factor to Ground
#            ,                         ! Number of Vertices
#            0,0,2.7000000000000002,   ! X,Y,Z Vertex 1 {m}
#            0,0,0,                    ! X,Y,Z Vertex 2 {m}
#            6,0,0,                    ! X,Y,Z Vertex 3 {m}
#            6,0,2.7000000000000002;   ! X,Y,Z Vertex 4 {m}
# 
#            OS:Surface,
#            OS:Surface 5,             ! Name
#            Wall,                     ! Surface Type
#            ,                         ! Construction Name
#            OS:Space 2,               ! Space Name
#            Outdoors,                 ! Outside Boundary Condition
#            ,                         ! Outside Boundary Condition Object
#            SunExposed,               ! Sun Exposure
#            WindExposed,              ! Wind Exposure
#            ,                         ! View Factor to Ground
#            ,                         ! Number of Vertices
#            0,0,2.7000000000000002,   ! X,Y,Z Vertex 1 {m}
#            0,0,0,                    ! X,Y,Z Vertex 2 {m}
#            6,0,0,                    ! X,Y,Z Vertex 3 {m}
#            6,0,2.7000000000000002;   ! X,Y,Z Vertex 4 {m}            
#            """)
#    
#    spaceText = formatBlock("""
#            OS:Space,
#            OS:Space 1,               ! Name
#            ,                         ! Space Type Name
#            ,                         ! Default Construction Set Name
#            ,                         ! Default Schedule Set Name
#            -0,                       ! Direction of Relative North {deg}
#            0,                        ! X Origin {m}
#            0,                        ! Y Origin {m}
#            0,                        ! Z Origin {m}
#            ,                         ! Building Story Name
#            OS:ThermalZone 2,         ! Thermal Zone Name
#            ;                         ! Part of Total Floor Area
#            """)
# 
#    spaceAndSurfAndSubs = formatBlock("""
#            OS:Space,
#            OS:Space 1,               ! Name
#            ,                         ! Space Type Name
#            ,                         ! Default Construction Set Name
#            ,                         ! Default Schedule Set Name
#            -0,                       ! Direction of Relative North {deg}
#            0,                        ! X Origin {m}
#            0,                        ! Y Origin {m}
#            0,                        ! Z Origin {m}
#            ,                         ! Building Story Name
#            OS:ThermalZone 2,         ! Thermal Zone Name
#            ;                         ! Part of Total Floor Area
#            
#            OS:Surface,
#            OS:Surface 1,             ! Name
#            Floor,                    ! Surface Type
#            ,                         ! Construction Name
#            OS:Space 1,               ! Space Name
#            Ground,                   ! Outside Boundary Condition
#            ,                         ! Outside Boundary Condition Object
#            NoSun,                    ! Sun Exposure
#            NoWind,                   ! Wind Exposure
#            ,                         ! View Factor to Ground
#            ,                         ! Number of Vertices
#            6,4,0,                    ! X,Y,Z Vertex 1 {m}
#            6,0,0,                    ! X,Y,Z Vertex 2 {m}
#            0,0,0,                    ! X,Y,Z Vertex 3 {m}
#            0,4,0;                    ! X,Y,Z Vertex 4 {m}
# 
#            OS:Surface,
#            OS:Surface 2,             ! Name
#            Wall,                     ! Surface Type
#            ,                         ! Construction Name
#            OS:Space 1,               ! Space Name
#            Outdoors,                 ! Outside Boundary Condition
#            ,                         ! Outside Boundary Condition Object
#            SunExposed,               ! Sun Exposure
#            WindExposed,              ! Wind Exposure
#            ,                         ! View Factor to Ground
#            ,                         ! Number of Vertices
#            0,0,2.7000000000000002,   ! X,Y,Z Vertex 1 {m}
#            0,0,0,                    ! X,Y,Z Vertex 2 {m}
#            6,0,0,                    ! X,Y,Z Vertex 3 {m}
#            6,0,2.7000000000000002;   ! X,Y,Z Vertex 4 {m}
# 
#            OS:Surface,
#            OS:Surface 5,             ! Name
#            Wall,                     ! Surface Type
#            ,                         ! Construction Name
#            OS:Space 2,               ! Space Name
#            Outdoors,                 ! Outside Boundary Condition
#            ,                         ! Outside Boundary Condition Object
#            SunExposed,               ! Sun Exposure
#            WindExposed,              ! Wind Exposure
#            ,                         ! View Factor to Ground
#            ,                         ! Number of Vertices
#            0,0,2.7000000000000002,   ! X,Y,Z Vertex 1 {m}
#            0,0,0,                    ! X,Y,Z Vertex 2 {m}
#            6,0,0,                    ! X,Y,Z Vertex 3 {m}
#            6,0,2.7000000000000002;   ! X,Y,Z Vertex 4 {m}            
#            
#            OS:SubSurface,
#            OS:SubSurface 1,          ! Name
#            FixedWindow,              ! Sub Surface Type
#            ,                         ! Construction Name
#            OS:Surface 2,             ! Surface Name
#            ,                         ! Outside Boundary Condition Object
#            ,                         ! View Factor to Ground
#            ,                         ! Shading Control Name
#            ,                         ! Frame and Divider Name
#            ,                         ! Multiplier
#            ,                         ! Number of Vertices
#            0.93427029703359998,0,2.1604596089317107,  ! X,Y,Z Vertex 1 {m}
#            0.93427029703359998,0,0.83675960893171086,  ! X,Y,Z Vertex 2 {m}
#            3.9024702970336,0,0.83675960893171086,  ! X,Y,Z Vertex 3 {m}
#            3.9024702970336,0,2.1604596089317107;  ! X,Y,Z Vertex 4 {m}
#            
#            OS:SubSurface,
#            OS:SubSurface 2,          ! Name
#            Door,                     ! Sub Surface Type
#            ,                         ! Construction Name
#            OS:Surface 2,             ! Surface Name
#            ,                         ! Outside Boundary Condition Object
#            ,                         ! View Factor to Ground
#            ,                         ! Shading Control Name
#            ,                         ! Frame and Divider Name
#            ,                         ! Multiplier
#            ,                         ! Number of Vertices
#            4.5089088920158424,0,2.0103999999999997,  ! X,Y,Z Vertex 1 {m}
#            4.5089088920158424,0,0,   ! X,Y,Z Vertex 2 {m}
#            5.4381088920158422,0,0,   ! X,Y,Z Vertex 3 {m}
#            5.4381088920158422,0,2.0103999999999997;  ! X,Y,Z Vertex 4 {m}
#            """)
#    
#    #print spaceText
#    
#    thisIDF = IDF()
#    thisIDF.IDDstring = spaceAndSurfAndSubs
#    
#    thisIDF.parseIDFtoXML()
#    
#    logging.info("The original XML:")
#    #thisIDF.printToScreenXml()
#    
#    thisIDF.transformSpacesToZones()
#    
#    logging.info("The new XML:")
#    #thisIDF.printToScreenXml()
# 
# 
#    
# 
# 
# def listAllNames(IDFobj):
#    # Select all first listed attribute elements which are children of an object which has a comment of Name
#    objects = IDFobj.XML.xpath('OBJECT/ATTR[1][@Comment=\'Name\']')
#    #print objects
#    # List comprehension: returns sibling of object for each object in object list
#    namedTupleList = [(object.xpath('preceding-sibling::*')[0].text, object.text) for object in objects]
#    
#    print sorted(namedTupleList, key=lambda name: name[1])
# 
#    print '*** NAMES summary ***'
#    print'{0:20} | {1:10}'.format('CLASS', 'CLASSNAME')
#    print'{0:20} | {1:10}'.format('-----', '---------')        
#    for tuple in sorted(namedTupleList, key=lambda name: name[1]):
#        print'{0:20} | {1:10}'.format(tuple[0],tuple[1])            
#    )
#===============================================================================




  
    

def applyZoneTemplate(IDFobj, template, zoneClass, zoneClassAttribute, zoneName = '.'):
    
    """
    zoneClass - This is the target class which will be multiplied
    template - this is the template IDF Object
    """
    
    # Check for existing HVAC objects
    
    if zoneClass:
        # Extract the desired OBJECT which matches the CLASS
        # /CLASS[re:match(text(), '%s')] # Select all CLASS that match %s
        # /..                           # Select the parent of it  (an OBJECT)
        # [0]                           # (Take only the first object in the list)
        
        xpathSearch = "//CLASS[re:match(text(), '{0}')]/..".format(zoneClass)
        #print xpathSearch
        #print template.XML.xpath(xpathSearch,
        #   namespaces={"re": "http://exslt.org/regular-expressions"})
        multiplyObject = template.XML.xpath(xpathSearch,
           namespaces={"re": "http://exslt.org/regular-expressions"})[0]
        
        #print etree.tostring(multiplyObject)
        
        if not len(multiplyObject):
            raise 'No XML found:'
        
        # Remove the multiplied object from the template
        template.XML.remove(multiplyObject)
        logging.debug(idStr("Found the {0} zoneclass".format(zoneClass),IDFobj.ID))
        
    # To get the fixed objects
    fixedObjects = template.XML.xpath("//OBJECT")
    
    # Which are appended
    for object in fixedObjects:
        try:
            IDFobj.XML.append(object)
        except:
            raise Exception("There is nothing to apply the template to! Load the file and XML first!")

    if zoneClass:        
            # Get the zone names
            zoneNameList = IDFobj.listZonesWithName(zoneName)
            
            
            # Now pass in the OBJECT and the target text path (attribute)         
            IDFobj.createOverList(zoneNameList, multiplyObject, zoneClassAttribute)
    
    if zoneClass:
        logging.debug(idStr(
            "Appended {0} {1} objects accross {2} zones, and added {3} fixed objects".format(
               len(zoneNameList), zoneClass, len(zoneNameList), len(fixedObjects)),
            IDFobj.ID))
    else: 
        logging.debug(idStr(
                "Appended {0} fixed objects".format(len(fixedObjects)),
                IDFobj.ID))

def applyNamedNNZoneTemplate(IDFobj, template, zoneClass, zoneClassAttribute, zoneName, originalTemplate):
    
    """
    zoneClass - This is the target class which will be multiplied
    template - this is the template IDF Object
    """
    
    # Check for existing HVAC objects

    # Extract the desired OBJECT which matches the CLASS
    # /CLASS[re:match(text(), '%s')] # Select all CLASS that match %s
    # /..                           # Select the parent of it  (an OBJECT)
    # [0]                           # (Take only the first object in the list)
    
    xpathSearch = "//CLASS[re:match(text(), '{0}')]/..".format(zoneClass)
    #print xpathSearch
    #print template.XML.xpath(xpathSearch,
    #   namespaces={"re": "http://exslt.org/regular-expressions"})
    
    try:
        multiplyNamedNNObject = template.XML.xpath(xpathSearch,
           namespaces={"re": "http://exslt.org/regular-expressions"})[0]
    except:
        raise
    
    # Remove the multiplied object from the template
    template.XML.remove(multiplyNamedNNObject)
    logging.debug(idStr("Found the {0} NamedNN zoneclass".format(zoneClass),IDFobj.ID))
    
    # To get the fixed objects
    fixedObjects = template.XML.xpath("//OBJECT")
    
    # Which are appended
    for object in fixedObjects:
        IDFobj.XML.append(object)

    # Get the zone names
    zoneNameList = IDFobj.listZonesWithName(zoneName)
    # Now pass in the OBJECT and the target text path (attribute)   
    IDFobj.createNamedNNObjectOverList(zoneNameList, multiplyNamedNNObject, 
                                     zoneClassAttribute, originalTemplate.uniqueNamePointer, originalTemplate.uniqueNameTemplate)
    
    logging.debug(idStr(
        "Appended {0} {1} objects accross {2} zones, and added {3} fixed objects".format(
           len(zoneNameList), zoneClass, len(zoneNameList), len(fixedObjects)),
        IDFobj.ID))



#--- Template utilities



        
def applyTemplateNewStyle(IDFobj, templateDescriptions, templatesList):
    templateDescName = templateDescriptions[0]
    accrossDescZones = templateDescriptions[1]
    
    flagFound = False
    for template in templatesList:
        if templateDescName == template.ID:
            flagFound = True                
            #print templateDescName, "found"
            
            # Try to load the template into memory
            sysTemplateIdfObject = IDF.fromIdfFile(template.absolutePath)
#                try:        
#                    sysTemplateIdfObject = IDF.fromIdfFile(template.absolutePath)
#                except:
#                    raise NameError('Template {0} not found at path {1}'.format(template.ID, template.absolutePath))
#                
            # Handle each style of template                
            if template.templateStyle == "One":
                IDFobj.applyZoneTemplate(sysTemplateIdfObject, template.multiplyClass, template.zoneNamePointer, accrossDescZones)
            elif template.templateStyle == "N to N":
                IDFobj.applyZoneTemplate(sysTemplateIdfObject, template.multiplyClass, template.zoneNamePointer, accrossDescZones)
            elif template.templateStyle == "Named N to N":
                #print template.namingList
                IDFobj.applyNamedNNZoneTemplate(sysTemplateIdfObject, template.multiplyClass, template.zoneNamePointer, accrossDescZones, template)                    
            else:
                raise "Template style not correct"

    if not flagFound: 
        print templateDescName, template.ID
        raise NameError('Template \'{0}\' does not exist in currently loaded templates'.format(templateDescName))

def applyWallConstruction(IDFobj,wallType,boundaryCondition,defaultName):
    surfaceObjects = IDFobj.xpathGetObjectByClassName('BuildingSurface:Detailed')
    
    """        
    BuildingSurface:Detailed,
      OS:Surface 303,           ! Name
      Wall,                     ! Surface Type
      000_Interior Wall,        ! Construction Name
      ZONE 101_2 ATRI,          ! Zone Name
      Surface,                  ! Outside Boundary Condition
      OS:Surface 428,           ! Outside Boundary Condition Object
      NoSun,                    ! Sun Exposure
      NoWind,                   ! Wind Exposure
      ,                         ! View Factor to Ground
      ,                         ! Number of Vertices
      5.24250598139002,-13.7416292810289,4.5,  ! X,Y,Z Vertex 1 {m}
      5.24250598139002,-13.7416292810289,0,  ! X,Y,Z Vertex 2 {m}
      12.3861216936323,-18.1278932934966,0,  ! X,Y,Z Vertex 3 {m}
      12.3861216936323,-18.1278932934966,4.5;  ! X,Y,Z Vertex 4 {m}
            """
    
    validWallTypes = [
                 "Floor",
                 "Wall",
                 "Ceiling",
                 "Roof",
                 ] # [1]
    
    validBoundaryTypes = [
                     "Adiabatic",
                     "Surface",
                     "Zone",
                     "Outdoors",
                     "Ground",
                     
                     ] # ATTR[4]
    
    matchCounter = 0 
    #print "CHECKKKKKKKKKK", wallType, boundaryCondition

    for surface in surfaceObjects:
        if (re.search(wallType, surface.xpath("ATTR")[1].text) and 
                re.search(boundaryCondition, surface.xpath("ATTR")[4].text )):
            #print "FOUND", wallType, boundaryCondition
            
            surface.xpath("ATTR")[2].text = defaultName
            #print "Window"
            matchCounter += 1
            
            
    return matchCounter

def applyFenestrationConstruction(IDFobj,fenestrationType,boundaryCondition,defaultName):
    surfaceObjects = IDFobj.xpathGetObjectByClassName('FenestrationSurface:Detailed')
    
    """        
FenestrationSurface:Detailed,
OS:SubSurface 86,         ! Name
Window,                   ! Surface Type
ASHRAE_189.1-2009_ExtWindow_ClimateZone 4-5,  ! Construction Name
OS:Surface 287,           ! Building Surface Name
,                         ! Outside Boundary Condition Object
,                         ! View Factor to Ground
,                         ! Shading Control Name
,                         ! Frame and Divider Name
,                         ! Multiplier
,                         ! Number of Vertices
-0.0179605120660973,0.0179605124181794,2.56305386664356,  ! X,Y,Z Vertex 1 {m}
-0.0179605120660973,0.0179605124181794,0.76,  ! X,Y,Z Vertex 2 {m}
-21.1904120250467,21.1904124404449,0.76,  ! X,Y,Z Vertex 3 {m}
-21.1904120250467,21.1904124404449,2.56305386664356;  ! X,Y,Z Vertex 4 {m}
          """

    matchCounter = 0 
    for surface in surfaceObjects:
        if (re.search(surface.xpath("ATTR")[1].text, fenestrationType)):
            #### DISABLED BOUNDARY CONDITION CHECK - WILL APPLY TO ALL ###
            # and 
            #    re.search(surface.xpath("ATTR")[4].text, boundaryCondition)):
            name = surface.xpath("ATTR")[2].text
            #print "FOUND", fenestrationType, boundaryCondition, name, defaultName

            surface.xpath("ATTR")[2].text = defaultName
            matchCounter += 1
            


    return matchCounter


def applyDefaultConstructions(IDFobj):

    #    Interior Wall,           !- Name
    intWalls = IDFobj.applyWallConstruction("Wall", "Surface", "Interior Wall")
    #    Exterior Wall,           !- Name
    extWalls = IDFobj.applyWallConstruction("Wall", "Outdoors", "Exterior Wall")
    # Ada wall
    adaWalls = IDFobj.applyWallConstruction("Wall", "Adiabatic", "Exterior Wall")
    
    #    Exterior Door,           !- Name
    #IDFobj.applyWallConstruction("Wall", "Surface", "Exterior Door")
    
    #    Air Wall,                !- Name
    #
    #    Interior Partition,      !- Name
    #
    #    Interior Door,           !- Name
    #
    
    
    #    Interior Floor,          !- Name
    intFloors = IDFobj.applyWallConstruction("Floor", "Surface", "Interior Floor")
    
    #    Exterior Floor,          !- Name
    extFloors = IDFobj.applyWallConstruction("Floor", "Outside", "Exterior Floor")
    
    # Ada floor
    adaFloors  = IDFobj.applyWallConstruction("Floor", "Adiabatic", "Interior Floor")
    
    # Ground floor
    groundFloor  = IDFobj.applyWallConstruction("Floor", "Ground", "Exterior Floor")
    
    
    #    Interior Ceiling,        !- Name
    intRoofs = IDFobj.applyWallConstruction("Ceiling", ".", "Interior Ceiling")
    #print intRoofs
    #raise
    
    
    
    #    Exterior Roof,           !- Name
    extRoofs = IDFobj.applyWallConstruction("Roof", "Outdoors", "Exterior Roof")
    
    # Ada roof
    adaRoofs = IDFobj.applyWallConstruction("Roof", "Adiabatic", "Interior Ceiling")

    logging.debug(idStr(
        "{} intWalls,{} extWalls, {} adaWalls, {} intFloors, {} extFloors, {} adaFloors, {} groundFloor, {} intRoofs, {} extRoofs, {} adaRoofs".format(
           intWalls,extWalls,adaWalls,intFloors,extFloors,adaFloors,groundFloor,intRoofs,extRoofs,adaRoofs
           ),
        IDFobj.ID))   
    
    
    # Windows
    windows = IDFobj.applyFenestrationConstruction("Window", ".", "Exterior Window")
    
    doors = IDFobj.applyFenestrationConstruction("Door", ".", "Exterior Wall")
    
    logging.debug(idStr(
        "{} windows".format(
           windows
           ),
        IDFobj.ID))   


def applyDumbConstructions(IDFobj):
    
    # The surfaces first
    # Select all surfaces
    fenestrationObjects = IDFobj.xpathGetObjectByClassName('FenestrationSurface:Detailed')
    
    for surface in surfaceObjects:
        surface.xpath("ATTR")[2].text = "dumbwall"

    for window in fenestrationObjects:
        window.xpath("ATTR")[2].text = "dumbwindow"
        
        
    #className = 
    #className = "Zone"

    #xpathSearch = "//OBJECT/CLASS[re:match(text(), '^" + className + "$')]/.."
    
    #xpathSearch = "//OBJECT/CLASS[re:match(text(), '^" + className + "$')]/.."

    #queryElements = IDFobj.XML.xpath(xpathSearch,
    #            namespaces={"re": "http://exslt.org/regular-expressions"})
     
    #className = 'FenestrationSurface:Detailed'
                           

    logging.debug(idStr(
        "Updated {} BuildingSurface:DETAILED and {} 'FenestrationSurface:Detailed' to DUMB construction".format(
           len(surfaceObjects),len(fenestrationObjects)),
        IDFobj.ID))           



def merge(IDFobj, newIDF):
    
    mergeObjects = newIDF.XML.xpath('//OBJECT')
    
    for object in mergeObjects:
        IDFobj.XML.append(object)

    logging.debug(idStr(
        'Blind merge with {} objects'.format(int(len(mergeObjects))),
        IDFobj.ID))   



#--- CLASS
class IDD(object):
    def __init__(self, pathIDD):
        self.pathIDD = pathIDD
        self.loadIDD()
        self.parseIDDtoXML()

    @property
    def numObjects(self):
        if self.XML is not None:
            objects = self.XML.xpath('//OBJECT')
            return(int(len(objects)))
        else:
            return 0 
        
    def loadIDD(self):
        # Define input and output full file paths
        fIn = open(self.pathIDD, 'r')
       
        # Calls the readlines method of object which returns a list object of lines
        #self.IDFlines = fIn.readlines()
        
        self.IDDstring = fIn.read()
        
        countLines = 0
        for line in self.IDDstring.split('\n'):
            countLines += 1

        logging.debug('Loaded IDD {} with {} lines'.format(
                                                 self.pathIDD,
                                                 countLines,
                                                 ))
        
        fIn.close()
    #--- Convert data
        
        
    def parseIDDtoXML(self):
        
        #=======================================================================
        # This is the updated version, with the capability to handle OSM files!
        #=======================================================================
        
        # create a local copy
        lines = []
        
        for line in self.IDDstring.split('\n'):
            lines.append(line)

            
        # Start the XML tree
        xmlVer = "0.1"
        # Root tag
        currentXML = etree.Element("EnergyPlus_XML", XML_version=xmlVer)
        # A comment
        commentXML = etree.Comment("XML Schema for EnergyPlus version 7.2 'IDD' file")
        currentXML.append(commentXML)
        # Another comment
        commentXML = etree.Comment("Schema created March. 2013 by Marcus Jones")
        currentXML.append(commentXML)
        
        lineIndex = 0
        
        def group():
            pass        
        def comment():
            pass
        
        def empty():
            pass   
        tokenDict = {
                     r"^ \s* ! [\w \s]+ $" : comment,
                     r"^ \s* \\group \s [\w \s]+ $" : group,
                     r"^ \s* $" : empty
                     }    

        # Loop over each line
        while (lineIndex < len(lines)) :
            
            thisLine = lines[lineIndex]
            found = None
            for token in tokenDict:
                #print token
                if re.search(token, thisLine, re.VERBOSE):
                    found = tokenDict[token]

            if found:
                print tokenDict[token].__name__,
            else:
                print "NO MATCH",
            print thisLine
                                
            #-------------
                       
            lineIndex += 1



        logging.debug('Converted IDD to XML:{} {}, {} objects'.format( 
                                                       type(self.XML),
                                                       self.XML,
                                                       self.numObjects,
                                                       ))



def createOverList(IDFobj, textList, xmlObject, targetRegXpathReplace):
    """
    textList is a list of names to update in the xmlObject
    the xmlObject is the 
    """
    
    for textItem in textList:
        # Create an actual real copy, not just a reference
        thisMultiplyObject = copy.deepcopy(xmlObject)
        
        #print "Before", etree.tostring(thisMultiplyObject)
        
        # Select the attribute within the object (the target)
        targetPath = thisMultiplyObject.xpath(targetRegXpathReplace,
                                    namespaces={"re": "http://exslt.org/regular-expressions"})
        #print targetPath
        #print etree.tostring(targetPath[0])
        
        # Convert out of the list
        targetPath[0].text = textItem
        
        #print "AFter", etree.tostring(thisMultiplyObject)
        
        # Append the updated object
        IDFobj.XML.append(thisMultiplyObject)
        
    logging.debug(idStr(
        "Appended {0} objects".format(len(textList)),
        IDFobj.ID))   





def addZonesToSpaces(IDFobj):
    
    OSzoneTemplate = formatBlock("""
    OS:ThermalZone,
    Name,         ! Name
    ,                         ! Multiplier
    ,                         ! Ceiling Height {m}
    ,                         ! Volume {m3}
    ,                         ! Floor Area {m2}
    ,                         ! Zone Inside Convection Algorithm
    ,                         ! Zone Outside Convection Algorithm
    ,                         ! Zone Conditioning Equipment List Name
    ,                         ! Zone Air Inlet Node or NodeList Name
    ,          ! Zone Air Exhaust Node or NodeList Name
    ,          ! Zone Air Node Name
    ,                         ! Zone Return Air Node Name
    ,                         ! Primary Daylighting Control Name
    ,                         ! Fraction of Zone Controlled by Primary Daylighting Control
    ,                         ! Secondary Daylighting Control Name
    ,                         ! Fraction of Zone Controlled by Secondary Daylighting Control
    ,                         ! Illuminance Map Name
    OS:Rendering:Color 2,     ! Group Rendering Name
    ,                         ! Thermostat Name
    No;                       ! Use Ideal Air Loads    
    """)

    OSzoneTemplateXML = IDFobj.parseIDFtoXMLtextInput(OSzoneTemplate)
    OSzoneTemplateXML = OSzoneTemplateXML.xpath("OBJECT")[0]
    
    # Get all spaces
    className = "OS:Space$"
    xpathSearch = "//CLASS[re:match(text(), '" + className + "')]/.."
    spaceElements = IDFobj.queryRe(IDFobj.XML, xpathSearch)
    
    logging.debug(idStr('Found {0} spaces'.format(len(spaceElements)),IDFobj.ID))

    for space in spaceElements:
        
        # Get the name of the space
        queryElements = IDFobj.queryRe(space,"ATTR[1]")
        nameOfSpace = queryElements[0].text
        #print nameOfSpace
        
        logging.debug(idStr('Processing {0}'.format(nameOfSpace),IDFobj.ID))
        
        
        # Now add a zone to this space
        
        # Checkout a template
        newOSzoneTemplate = copy.deepcopy(OSzoneTemplateXML)
        
        # Change the name in the template
        queryElements = IDFobj.queryRe(newOSzoneTemplate, "ATTR[1]")
        zoneNameAttr = queryElements[0]
        thisZoneName = "{} Zone".format(nameOfSpace)
        zoneNameAttr.text = thisZoneName
        
        # Now link the space with the new zone
        queryElements = IDFobj.queryRe(space,"ATTR[10]")
        spaceZoneAttr = queryElements[0]
        spaceZoneAttr.text = thisZoneName
        
        #print OSzoneTemplateXML
        #IDFobj.printToScreenXml(OSzoneTemplateXML)
        
        IDFobj.XML.append(newOSzoneTemplate)
        
        #IDFobj.countAllClasses()

        
        
        logging.debug(idStr('Check - Zone name in Space: {0}, Zone name in Zone: {1}'.format(
                     zoneNameAttr.text,spaceZoneAttr.text
                     ),IDFobj.ID))


    logging.debug(idStr('Added and linked {0} zones'.format(len(spaceElements)),IDFobj.ID))

       

def extractClassesCopy(IDFobj, className):
    """
    Search for the regex in className, select matches, and return them as a new IDF object
    """
    
    # Find a CLASS object with the name matching className, and return it's PARENT
    xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]/.."
    
    queryElements = IDFobj.XML.xpath(xpathSearch,
                namespaces={"re": "http://exslt.org/regular-expressions"})
    
    currentXML = myRootNode()
    # Create the new IDF object with this root
    returnIDF = IDF.fromXmlObject(currentXML)
    
    for object in queryElements:
        returnIDF.XML.append(object)
        
        
    logging.debug(idStr(
        'Extracted {0} {1} objects'.format(len(queryElements), className),
        self.ID))
  
    return returnIDF




         


def DeleteOrphanedZones(IDFobj):

    ### GET SPACES ###
    xpathSearch = "//CLASS[re:match(text(), '^OS:Space$')]/.."
    #xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]/"
    spaces = IDFobj.querySelfRE(xpathSearch)
    logging.debug("Loaded {} spaces".format(len(spaces)))

    
    ### GET ZONES ###
    xpathSearch = "//CLASS[re:match(text(), '^OS:ThermalZone')]/.."
    #xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]/"
    zones = IDFobj.querySelfRE(xpathSearch)
    logging.debug("Loaded {} zones".format(len(zones)))
        
    
    ### LOOP Both REVERSE ###
    notFound = 0
    for zone in zones:    
        zoneName = zone.xpath("ATTR")[0].text
        found = False
        for space in spaces:    
        
            thisSpaceName = space.xpath("ATTR")[0].text
            thisSpacePointsToZoneName = space.xpath("ATTR")[9].text                    
            #zoneName = zone.xpath("ATTR")[0].text
            if re.search("^"+zoneName+"$",thisSpacePointsToZoneName):
                #print 
                #print "Match"
                #print "Space: {}, Space points to {}, Zone exists here: {}".format(thisSpaceName,thisSpacePointsToZoneName,zoneName)
                #newZoneName =  "ZONE " + thisSpaceName
                
                #print "New name:" + newZoneName
                found = True
                #space.xpath("ATTR")[9].text = newZoneName
                #zone.xpath("ATTR")[0].text =  newZoneName
        if not found:
                IDFobj.XML.remove(zone)
                notFound += 1
            
    logging.debug("Checked {} zones over {} spaces, deleted {} zones.".format(len(zones),len(spaces),notFound))


def createNamedNNObjectOverList(IDFobj, textList, xmlObject, targetRegXpathReplace,uniqueNamePointer,uniqueNameTemplate):
    """
    textList is a list of names to update in the xmlObject
    the xmlObject is the 
    """
    
    if not textList:
        raise ValueError("Probable error: No zones specified for the template, try i.e. '.' ")
    
    for textItem in textList:
        # Create an actual real copy, not just a reference
        thisMultiplyObject = copy.deepcopy(xmlObject)

        # Select the attribute within the object (the target)
        targetPath = thisMultiplyObject.xpath(targetRegXpathReplace,
                                    namespaces={"re": "http://exslt.org/regular-expressions"})

        targetPath[0].text = textItem

        targetPath = thisMultiplyObject.xpath(uniqueNamePointer,
                                    namespaces={"re": "http://exslt.org/regular-expressions"})
        
        
        
        newUniqueName = re.sub("ZoneName", textItem, uniqueNameTemplate)
        
        targetPath[0].text = newUniqueName
        
        #print "AFter", etree.tostring(thisMultiplyObject)
        
        # Append the updated object
        IDFobj.XML.append(thisMultiplyObject)
        
    logging.debug(idStr(
        "Appended {0} objects while updating names to i.e. {1}".format(len(textList),newUniqueName),
        IDFobj.ID))   


def deleteShadingSurfacesFromIDF(IDFobj):

    ### GET SHADING ###
    xpathSearch = "//CLASS[re:match(text(), '^Shading:Building:Detailed')]/.."
    #xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]/"
    shades = IDFobj.querySelfRE(xpathSearch)
    logging.debug("Found {} shading surfaces".format(len(shades)))
        
    ### LOOP ###
    for shade in shades:    
        IDFobj.XML.remove(shade)
            
    logging.debug("Removed {} ^Shading:Building:Detailed objects".format(len(shades)))


def renameSpaces(IDFobj,tag):
    tag =  " " + tag
    className = "^OS:Space$"
    xpathSearch = "//CLASS[re:match(text(), '" + className + "')]/.."
    queryElements = IDFobj.queryRe(IDFobj.XML, xpathSearch) 
    spaceElements = queryElements
    
    logging.debug(idStr('Found {0} spaces'.format(len(spaceElements)),IDFobj.ID))
    
    # First, rename all spaces with a space number
    for space in spaceElements:

        # Get the space name
        xpathSearch = "ATTR[1]"
        queryElements = IDFobj.queryRe(space, xpathSearch)
        spaceNameElement = queryElements[0]
        originalNameOfSpace = spaceNameElement.text
        newNameOfSpace = spaceNameElement.text + tag
        spaceNameElement.text = newNameOfSpace
        
        logging.debug(idStr('Renaming space {0} with tag: {1} '.format(originalNameOfSpace, tag),IDFobj.ID))
        
        # Get the pointer to the zone
        queryElements = IDFobj.queryRe(space, "ATTR[10]")
        thisSpacesZoneName =  queryElements[0].text
        # Rename the linked zone
        if thisSpacesZoneName: 
            # NOTE that a space points to the zone!
            #nameOfZone = queryElements[0].text
            # Update previously linked thermal zones
            # Get zone name 
            linkedZones = IDFobj.linkedZone(thisSpacesZoneName)
            if linkedZones:
                for element in linkedZones:
                    # First, update the zone name
                    queryElements = IDFobj.queryRe(element, "ATTR[1]")
                    nameAttr = queryElements[0]
                    nameAttr.text = nameAttr.text + tag
                    # Then update the space to point to this renamed zone
                    queryElements = IDFobj.queryRe(space,"ATTR[10]")
                    zoneAttr = queryElements[0]
                    zoneAttr.text = zoneAttr.text + tag
                logging.debug(idStr('Linked zone {0} to space {1}, with pointer {2}'.format(nameAttr.text, newNameOfSpace, zoneAttr.text),IDFobj.ID))
            else: 
                logging.debug(idStr('Thermal zone MISSING for {0} (original name)'.format(originalNameOfSpace),IDFobj.ID))
        else:
            logging.debug(idStr('No thermal zone specified for {0}'.format(nameOfSpace),IDFobj.ID))

        # Update previously linked surfaces
        linkedSurfs = IDFobj.linkedSurfaces(originalNameOfSpace)
        for linkedSurf in linkedSurfs:
            # Update the pointer in the surface\
            queryElements = IDFobj.queryRe(linkedSurf, "ATTR[4]")
            nameAttr = queryElements[0]
            nameAttr.text = newNameOfSpace
            logging.debug(idStr('Pointer of {0} updated to {1}'.format(IDFobj.queryRe(linkedSurf, "ATTR[1]")[0].text, IDFobj.queryRe(linkedSurf, "ATTR[4]")[0].text),IDFobj.ID))
       
    # Then, rename all surfaces 
#        for surface in allSurfaces: 
#            # Find associated sub surfaces
#            for linkedSurface in linkedSurfs:
#                linkedSubSurfs = self.linkedSubSurfaces(linkedSurface)
#
#            allSurfaces =self.queryClass("OS:Surface")
#            
        
def renameSurfaces(IDFobj,tag):
    tag =  " " + tag
    className = "OS:Surface"
    xpathSearch = "//CLASS[re:match(text(), '" + className + "')]/.."
    queryElements = IDFobj.queryRe(IDFobj.XML, xpathSearch) 
    surfaceElements = queryElements
    
    logging.debug(idStr('Found {0} surfaces'.format(len(surfaceElements)),IDFobj.ID))
    
    numSubSurfaces = 0
    
    for surface in surfaceElements:
        # Get linked sub surfaces
        linkedSubSurfs = IDFobj.linkedSubSurfaces(surface)
        
        # Rename the surface
        queryElements = IDFobj.queryRe(surface, "ATTR[1]")
        surfaceNameElement = queryElements[0]
        originalNameOfSurface = surfaceNameElement.text
        newNameOfSurface = surfaceNameElement.text + tag
        surfaceNameElement.text = newNameOfSurface
        
        # Rename the linked subs
        for subsurf in linkedSubSurfs:
            queryElements = IDFobj.queryRe(subsurf, "ATTR[4]")
            subSurfaceNamePointer = queryElements[0]
            subSurfaceNamePointer.text = newNameOfSurface
        
        numSubSurfaces += len(linkedSubSurfs)
        
        logging.debug(idStr('Updated  {0} subsurfaces for surface {1}'.format(len(linkedSubSurfs), newNameOfSurface),IDFobj.ID))

    logging.debug(idStr('Renamed  {0} surfaces and {1} SubSurfaces'.format(len(surfaceElements),numSubSurfaces),IDFobj.ID))

