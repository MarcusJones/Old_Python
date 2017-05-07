'''
Created on 2012-04-10

@author: Anonymous
'''
import psutil
import logging.config


class ComputerResources():
    def __init__(self): pass
        # Stores the cpu averaging list
#        self.cpuPercents = deque([0,0,0,0,0])
#        self.currentAverageCPU = 0
#        self.currentCPU = 0
#    def update(self):
#        # Update the average CPU percent
#        self.cpuPercents.pop()
#        self.cpuPercents.appendleft(psutil.cpu_percent())
#        self.currentAverageCPU = sum(self.cpuPercents)/len(self.cpuPercents)
#        self.currentCPU = psutil.cpu_percent()
    def current_CPU(self):
        return psutil.cpu_percent()
    
def _test1():
    logging.debug("Started _test1".format())
    myCompRes = ComputerResources()
    print myCompRes.current_CPU()
    logging.debug("Finished _test1".format())

    #print c
    #wholeCommand
    
    
    #thisProc = subprocess.call("cmd")
    #
    #os.system('cmd')
    #subprocess.call("cmd")
    #thisProc = subprocess.call(wholeCommand, shell=True)
    #os.system("start " + wholeCommandString)


if __name__ == "__main__":
    logging.config.fileConfig('..\\LoggingConfig\\loggingNofile.conf')
    logging.debug("Started _main".format())


    _test1()
    
    logging.debug("Started _main".format())