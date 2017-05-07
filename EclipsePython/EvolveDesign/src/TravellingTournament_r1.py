'''
Created on Nov 12, 2011

@author: UserXP
'''
import os
import re
import win32clipboard

def sc():
    """
    Function spyder_copy()
    """
    win32clipboard.OpenClipboard()
    clipText = win32clipboard.GetClipboardData()
    newClipText = re.sub(r'\x00', '', clipText)
    win32clipboard.SetClipboardText(newClipText)
    win32clipboard.CloseClipboard()

def tour_length(distancesMatrix,tour):
    """
    Returns
    """
    total=0
    num_cities=len(tour)
    for i in range(num_cities):
        j=(i+1)%num_cities
        city_i=tour[i]
        city_j=tour[j]
        total+=distancesMatrix[city_i,city_j]
    return total


print "foo"

# City names
cityName = "ATL NYM PHI MON FLA PIT CIN CHI STL MIL HOU COL SF SD LA ARI".split(" ")

#dataSets = for dir("")

dataSetRootPath ="..\\TravellingTournamentFiles\\"  

dataSetsPaths = [os.path.normpath(dataSetRootPath + fileName) for 
    fileName in os.listdir(dataSetRootPath) if re.search(".txt",fileName)]
dataSetsNames = [re.split("\\\\|.txt",fileName)[2] for 
    fileName in dataSetsPaths] # Much better to use os.path split here
dataSetDistances = [genfromtxt(dataSetPath) for dataSetPath in dataSetsPaths]
dataSetDict = dict(zip(dataSetsNames,dataSetDistances))


thisDataSet = dataSetDict["data4"]









data = genfromtxt()
dataSetPath = os.path.normpath(dataSetRootPath + fileName)

#
if re.split("\\\\|.txt","data10.txt"):
    print "t"

print re.split("\\\\|.txt","data10.txt")[0]

dataSetData