 
#
#sys.path.append(localLibrariesPath) 
##print sys.path
#

#
## Execute
#print "Execute TRNSYS" 
#

#
#maxProcesses = 4
#
#numberOfExecutes = 10
#numberOfRuns = 0
#
#singleTrnsysProcesses = range(maxProcesses)
#print singleTrnsysProcesses
#numberOfRuns += 1

#print "Finished initializing"
#    
#while numberOfRuns <= numberOfExecutes:
#    print numberOfRuns
#    numberOfRuns += 1
#
#print singleTrnsysProcesses
#
#print psutil.get_pid_list()
#print psutil.cpu_times()
#for i in range(0,100):
#    time.sleep(1)
#    print psutil.cpu_percent()

#for i in range(1, 11):
#    #time.sleep(2)
#    print i, singleTrnsysProcess.poll()
#    print i, singleTrnsysProcess.pid


#Popen.poll()
#    Check if child process has terminated. Set and return returncode attribute.


# Insantiate the CSV file

#csvFile = open('..\\Log files\\runLog.csv', 'wb')
#csvFile.close()
#csvFile = open('..\\Log files\\runLog.csv', 'a')
#csvLog = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#
#csvLog.writerow(["Time",
#                    "Number Pending", 
#                    "Number Running",
#                    "Average CPU", 
#                    "Instant CPU",
#                    "Total Phys Mem",
#                    "Total Avail Mem",
#                    "Total Virtual Mem",
#                    "Total available virtual mem"
#                    ])
#
#csvFile.close()
