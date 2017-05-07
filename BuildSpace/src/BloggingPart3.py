'''
Created on Jan 15, 2012

@author: UserXP
'''

import os
import csv

# Specify directory and file extension
searchDirectory = os.path.normpath(r"C:\\Project5\\Output")
searchEnding = "out"

# Collect the file names of interest from the directory
inputFilePaths = list()
for filename in os.listdir(searchDirectory): 
    if filename.endswith(searchEnding):
        # Found a file with proper extension
        fullFilePath = os.path.join(searchDirectory, filename)
        # Add it to our running list
        inputFilePaths.append(fullFilePath)

# Some feedback on what was found
print "Found {0} '{1}' files in {2}. ".format(len(inputFilePaths), searchEnding, searchDirectory)

# For each file found, process each in turn
for filePath in inputFilePaths:
    # Open it
    openedFile = open(filePath)
    # Read it as a comma separated style format
    openedCSV = csv.reader(openedFile, delimiter="\t")
    # ! Skip the header line !
    openedCSV.next()
    # Blank list for storing data
    coolingLoad = list()
    heatingLoad = list()
    # For each row of the file
    for row in openedCSV:
        # For each row, access the 2nd and 3rd column
        # Convert [kJ/hr] into [Watts]
        thisHoursCoolingLoad = float(row[1]) / 3.6
        thisHoursHeatingLoad = float(row[2]) / 3.6
        # Save the data to our list
        coolingLoad.append(thisHoursCoolingLoad)
        heatingLoad.append(thisHoursHeatingLoad)
        # Calculate the cooling and heating load in [Wh]
        totalCoolingLoad = sum(coolingLoad)
        totalHeatingLoad = sum(heatingLoad)
        # Calculate the average load in [W]
        meanCoolingLoad = sum(coolingLoad)/len(coolingLoad)
        meanHeatingLoad = sum(heatingLoad)/len(heatingLoad)
    # Close the file
    openedFile.close()
    # Write results for the processed file
    print "Summary for", filePath
    print "   Cooling: {0:7.0f} Wh, Heating: {1:7.0f} Wh, Avg. Cooling: {2:7.0f} W, Avg. Heating: {3:7.0f} W".format(
        totalCoolingLoad, 
        totalHeatingLoad,
        meanCoolingLoad,
        meanHeatingLoad,
        )


#Work with a Short, Self Contained, Correct (Compilable), Example http://sscce.org/
#Deal with text headers!


#Handle sub-directories: 
#os.walk()