
# Find the simulation input file
simulationInputFile = "C:\Simulations\Baseline Short.idf"
# What string are we looking for?
searchString = "$$ReplaceThis$$"
# What do we want to replace it with?
angles = "0","90","180","270"

print angles

# For every replacement value in list of values:
for thisAngle in angles:
    # Open the input file
    inputFile = open(simulationInputFile)
    # Open the output file
    outputFileName = "c:\Simulations\output " + str(thisAngle) + " degree rotation.idf"
    outputFile = open(outputFileName,'w')
    print "Now writing file:", outputFileName    
    # For every line of the input file:
    for line in inputFile:
        # If searchString is found, replace it with thisAngle
        newLine = line.replace(searchString, thisAngle)
        # Write the line to the output file
        outputFile.write(newLine)
    outputFile.close()
    print "Finished writing this angle!"
inputFile.close()
print "Finished the whole script!"

#string.replace(str, old, new[, maxreplace])

#"the first number you want, followed by the first number you don't want."