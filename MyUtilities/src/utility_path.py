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

from config import *

import logging.config
import unittest

import os
import re
import time
from utility_inspect import whoami, whosdaddy
import sys
import shutil


def e(pathName):

    """
    pathName is a desired path on drive for a project
    Will return a numbered version of this path
    """
    logging.info("Filtering {}".format(rootPath,name_pat, ext_pat, recurse))

    #print pathName
    pathName = os.path.normpath(pathName)
    fullPathList = split_up_dir(pathName)

    lastDirName = fullPathList.pop()
    rootPath = "".join(fullPathList)


    revisionList = list()

    for path in os.listdir(rootPath):

        thisImmediateSubDir = split_up_dir(path).pop()

        if re.findall("{}".format(thisImmediateSubDir), path):
            thisImmediateSubDir
            revisionTextList = re.findall("[\d]+", base)
            if revisionTextList:
                revisionText = re.findall("r[\d]+", base)[0]
                #print revisionText
                revisionNumber = int(re.findall("[\d]+",revisionText)[0])

                fileRevisionList.append((revisionNumber, filename))

    if not fileRevisionList:
        return None


    # Sort, and pop the most recent (last) filename
    #latestRevisionFileName = (sorted(fileRevisionList)).pop()[1]
    #latestRevisionFileNumber = (sorted(fileRevisionList)).pop()[1]
    #latestRevisionFileNamePath = os.path.join(sourceFileDir, latestRevisionFileName)

    return sorted(fileRevisionList).pop()[0]


    #revNum = get_latest_rev_number(myDirString, myFileName, myFileExt)

    if revNum:
        revNum =  revNum + 1
        myFileName = myFileName + "_r" + "{0:02d}".format(revNum)
    else:
        myFileName = myFileName + "_r00"

    raise





def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            #print choice
            return valid[default]
        elif choice in valid:
            #print choice
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

def create_dir(f):
    logging.debug("Creating {}".format(f))

    if not os.path.exists(f):
        os.makedirs(f)

def count_files(f):
    items = [os.path.join(f,name) for name in os.listdir(f)]
    return len([item for item in items if os.path.isfile(item)])

def count_dirs(f):
    items = [os.path.join(f,name) for name in os.listdir(f)]
    return len([item for item in items if os.path.isdir(item)])



def erase_dir(f):

    if query_yes_no("ERASING directory: {}, sure?".format(f), None):
        shutil.rmtree(f)

def erase_dir_contents(folder, flgEverything = True):
#import os
#folder = '/path/to/folder'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path) and  not flgEverything:
                os.unlink(file_path)
            else:
                os.unlink(file_path)
        except Exception, e:
            print e



def path_exists(f):
    if os.path.exists(f):
        return True
    if not os.path.exists(f):
        return False

def split_up_dir(pathName):
    pathName = os.path.normpath(pathName)
    logging.debug("Splitting {}".format(pathName))
    drive,path_and_file=os.path.splitdrive(pathName)
    path,thisFile=os.path.split(path_and_file)
    #print path, thisFile
    pureFileName,extension = os.path.splitext( thisFile)
    if extension:
        raise Exception("This is meant for directories, not files")

    folders=[]
    #folders.append(extension)
    folders.append(pureFileName)
    while 1:
        path,folder=os.path.split(path)
        #print path,folder
        if folder!="":
            folders.append(folder)
        else:
            if path!="":
                folders.append(path)

            break

    folders.append(drive)
    folders.reverse()

    #print folders[-1]

    return folders

def split_up_path(pathName, flg_verbose = False):

    """
    """
    pathName = os.path.normpath(pathName)
    if flg_verbose:
        logging.debug("Splitting {}".format(pathName))
    drive,path_and_file=os.path.splitdrive(pathName)
    path,thisFile=os.path.split(path_and_file)
    pureFileName,extension = os.path.splitext( thisFile)
    folders=[]
    folders.append(extension)
    folders.append(pureFileName)
    while 1:
        path,folder=os.path.split(path)
        #print path,folder
        if folder!="":
            folders.append(folder)
        else:
            if path!="":
                folders.append(path)

            break

    folders.append(drive)
    folders.reverse()

    if flg_verbose:
        logging.debug("Result: {}".format(folders))

    return folders


def listDirs(pathName):
    directories = list()
    for dirname in os.listdir(pathName):
        absPathName = os.path.join(pathName,dirname)
        #print pathName
        #print os.path.join(pathName, dirname)
        if os.path.isdir(absPathName):
            directories.append(absPathName)

    return directories

def get_most_recent_file(pathName):
    """From a directory, return the latest file by datetime
    """

    allFilePaths = list()
    for dirname, dirnames, filenames in os.walk(pathName):
        #for subdirname in dirnames:
        #    print os.path.join(dirname, subdirname)
        if filenames:
            for filename in filenames:
                thisFilePath = os.path.join(dirname, filename)
                allFilePaths.append(thisFilePath)

    greatestMtime = 0
    for filePath in allFilePaths:
            try:
                thisFileMtime = os.path.getmtime(filePath)
                if thisFileMtime > greatestMtime:
                    greatestMtime = thisFileMtime
            except:
                pass
    #print "last modified: {}".format(time.ctime(greatestMtime))
    return (pathName, greatestMtime)


def get_latest_revision(fullFilePath):
    """Take a full path as a signature, and search the dir for the latest revision file name

    """

    mySplitPath=  split_up_path(fullFilePath)
    myFileExt = mySplitPath.pop()
    myFileName = mySplitPath.pop()
    myFileDir = mySplitPath
    myDirString = "\\".join(myFileDir)
    #print myDir
    rev_num = get_latest_rev_number(myDirString, myFileName, myFileExt)

    if not rev_num:
        raise

    myFileName = myFileName + "_r" + "{0:02d}".format(rev_num)

    completePathList = myFileDir +  [myFileName + myFileExt]
    fullFilePathREV = os.path.join(*completePathList)


    logging.info("Latest file: {}".format(fullFilePathREV))

    return fullFilePathREV

def get_new_file_rev_path(fullFilePath):
    """Takes the entire full file path, returns
    a new file name with an _r## added to the file name
    i.e. the string
    'C:\TestSQL\DSpaceTest.sql'  becomes
    'C:\TestSQL\DSpaceTest_r00.sql' becomes
    'C:\TestSQL\DSpaceTest_r01.sql' becomes
    etc.
    """

    mySplitPath=  split_up_path(fullFilePath)

    #myDir = "".join(mySplitPath[0:-3])

    myFileExt = mySplitPath.pop()
    myFileName = mySplitPath.pop()
    myFileDir = mySplitPath
    myDirString = "\\".join(myFileDir)
    #print myDir
    revNum = get_latest_rev_number(myDirString, myFileName, myFileExt)

    if revNum != None:
        revNum =  revNum + 1
    #os.path.exists(fullDBpath)

    if revNum:
        #print "YES"
        #fullDBpath = fullDBpath + "1"
        myFileName = myFileName + "_r" + "{0:02d}".format(revNum)
    else:
        myFileName = myFileName + "_r00"

    #firstPart = mySplitPath[0:-2]
    #secondPart = [mySplitPath[-2] + mySplitPath[-1]]
    #mySplitPath = firstPart + secondPart
    completePathList = myFileDir +  [myFileName + myFileExt]
    fullFilePathREV = os.path.join(*completePathList)

    logging.info("New revision file: {}".format(fullFilePathREV))

    return fullFilePathREV

def get_files_by_name_ext(rootPath, search_name, search_ext):
    #print search_name
    #raise
    allFilePathList = list()
    for root, dirs, files in os.walk(rootPath):
        for this_name in files:
            thisFilePath = os.path.join(root, this_name)
            allFilePathList.append(thisFilePath)
    #print search_name
    # Filter
    resultFilePaths = list()
    #print allFilePathList

    for filePath in allFilePathList:
        #print os.path.splitext(filePath),
        basename = split_up_path(filePath,False)[-2]
        #print split_up_path(filePath)[-2]
        extension = split_up_path(filePath,False)[-1]
        #print search_name
        #print search_ext
        #print "Basename", basename
        #print "{}  {} {}".format(search_name, basename, re.match(search_name, basename))
        #print "{}  {} {}".format(search_ext, extension, re.search(search_ext, extension))
        #raise
        if re.search(search_name, basename) and re.search(search_ext, extension):
            #print filePath

            resultFilePaths.append(filePath)
#    resultFilePaths = [filePath for filePath in allFilePathList if
#                    os.path.splitext(filePath)[1].lower() == search_ext.lower() and os.path.basename(filePath) == search_name
#                    ]
#
    logging.info("Found {} {} file matching '{}' in {}".format(len(resultFilePaths),search_ext,search_name, rootPath))

    return resultFilePaths


def get_files_by_ext_recurse(rootPath,ext, ):
    ext = "." + ext

    # Walk the project dir
    allFilePathList = list()
    for root, dirs, files in os.walk(rootPath):
        for name in files:
            thisFilePath = os.path.join(root, name)
            allFilePathList.append(thisFilePath)


    # Filter
    resultFilePaths = list()

    resultFilePaths = [filePath for filePath in allFilePathList if
                    os.path.splitext(filePath)[1].lower() == ext.lower()
                    ]

    logging.info("Found {} {} files in {}".format(len(resultFilePaths),ext,rootPath))

    return resultFilePaths



def get_file_by_ext_one(rootPath,ext):
    ext = "." + ext

    # Walk the project dir
    allFilePathList = list()
    for item in os.listdir(rootPath):
        thisFilePath = os.path.join(rootPath, item)
        allFilePathList.append(thisFilePath)


    # Filter

    resultFilePaths = allFilePathList

    resultFilePaths = [filePath for filePath in resultFilePaths if
                    os.path.splitext(filePath)[1].lower() == ext.lower()
                    ]

    logging.info("Found {} {} files in {}".format(len(resultFilePaths),ext,rootPath))

    return resultFilePaths


def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]


def filter_paths_by_filename(paths,filter):

    print paths
    # Walk the project dir
    allFilePathList = list()
    for root, dirs, files in os.walk(rootPath):
        for name in files:
            thisFilePath = os.path.join(root, name)
            allFilePathList.append(thisFilePath)

    #print


    #print [os.path.splitext(filePath) for filePath in paths]
    resultFilePaths = list()
    for filePath in paths:
        thisFileName = os.path.splitext(os.path.split(filePath)[1])[0]
        if thisFileName in filter:
            resultFilePaths.append(filePath)

#    raise
#    #fileNames = [os.path.split(filePath)[1] for filePath in paths]
#    print [os.path.splitext(os.path.split(filePath)[1]
#                                        )[0] for filePath in paths]
#    print filter
#    resultFilePaths = [filePath for filePath in paths if
#                       os.path.splitext(
#                                        os.path.split(filePath)[1]
#                                        )[0] in filter
#                    ]
#    print resultFilePaths
    logging.info("Filtered {} files out of {}".format(len(resultFilePaths),len(paths)))

    return resultFilePaths


def get_current_file_dir(this_file):
    return os.path.dirname(os.path.realpath(this_file))


def get_latest_rev_number(sourceFileDir, sourceFileName, extensionFilter):
    """Takes a directory, and a filter for extensions
    INCLUDING the period i.e.
    ".sql", ".idf"
    Returns an integer
    """
    fileRevisionList = list()
    for filename in os.listdir(sourceFileDir):
        #print filename, sourceFileName

        if re.findall("{}".format(sourceFileName), filename):
            base, extension = os.path.splitext(filename)
            if extension == extensionFilter:
                revisionTextList = re.findall("[\d]+", base)
                if revisionTextList:
                    revisionText = re.findall("r[\d]+", base)[0]
                    revisionNumber = int(re.findall("[\d]+",revisionText)[0])
                    fileRevisionList.append((revisionNumber, filename))

    if not fileRevisionList:
        return None
    latest = sorted(fileRevisionList).pop()[0]
    logging.info("Latest revision in {} - {}  - {}: {}".format(sourceFileDir, sourceFileName, extensionFilter, latest))

    return latest



#-- Update ----

def copy_file(src,dst):
    shutil.copyfile(src, dst)

    logString = "Copied {} to {}".format(src,dst)
    logging.debug(logString)

def filter_files_dir(rootPath, name_pat = ".", ext_pat = ".*", recurse = False, flg_verbose = False):
    """
    Filter files in a directory by name and extension
    """
    matches = list()

    for root, dirs, files in os.walk(rootPath):
        # Ensure we don't go into sub directories if recursion is off
        if rootPath == root and not recurse:
            # Loop over the files in this dir
            for fileName in files:
                this_name, this_ext = os.path.splitext(fileName)
                if re.search(name_pat, this_name) and re.search(ext_pat, this_ext):
                    #print root, this_name, this_ext
                    full_path = os.path.join(root, this_name+ this_ext)
                    matches.append(full_path)

                #thisFilePath = os.path.join(root, fileName)

                #print thisFilePath
        elif rootPath != root and not recurse:
            #print "skip"
            pass
        elif recurse:
            print "Recursion not yet supported"
            raise
        else:
            raise
    logging.info("Filtering {}, {}, {} - Recurse {}, found {}".format(rootPath,name_pat, ext_pat, recurse,len(matches)))
    return matches

def get_latest_rev(rootPath, name_pat = ".", ext_pat = ".*", recurse = False, flg_verbose = False):
    """
    Get latest revision full path
    """
    matches = filter_files_dir(rootPath, name_pat, ext_pat, recurse)
    revisionList = list()
    for fullPath in matches:
        if flg_verbose:
            print fullPath

        fName = split_up_path(fullPath)[-2]
        #print fName
        if re.search("[\d]+$", fName):
            revisionText = re.findall("[\d]+$", fName)[0]
            revisionNum = int(revisionText)
            revisionList.append((revisionNum, fullPath))


    if revisionList:
        lastRevPath = revisionList.pop()[1]
        logging.info("Last revision; {}".format(lastRevPath))

        return lastRevPath
    else:
        raise Exception("Couldn't find revisions in {} filename {} . {}".format(rootPath,name_pat,ext_pat))
        pass
    #return os.path.join(sourceFileDir,sorted(fileRevisionList).pop()[1] )


#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):

    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        self.testDir = HTMLdataDir = os.getcwd() + r"\..\test_paths_dirs"
        self.testDir = os.path.abspath(self.testDir)

    def test010_filter1(self):

        get_files_by_name_ext(r'C:\newtestdir', "results", "csv")

    @unittest.skip("")
    def test010_Filter(self):
        print "**** TEST {} ****".format(whoami())
        #print get_latest_rev_number(self.testDir,"","")
        print "Matches"
        matches = filter_files_dir(self.testDir)
        for path in matches:
            print path

        assert len(matches) == 6

        print "Matches"
        matches = filter_files_dir(self.testDir, ext_pat = "txt")
        for path in matches:
            print path

        assert len(matches) == 3

        print "Matches"
        matches = filter_files_dir(self.testDir, "text", ext_pat = "txt")
        for path in matches:
            print path

        assert len(matches) == 2
    @unittest.skip("")
    def test020_FilterRev(self):
        print "**** TEST {} ****".format(whoami())
        #print get_latest_rev_number(self.testDir,"","")
        print get_latest_rev(self.testDir, "text", ext_pat = "txt")
#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print ABSOLUTE_LOGGING_PATH
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)


    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())

    #print FREELANCE_DIR

    unittest.main()

    logging.debug("Finished _main".format())

