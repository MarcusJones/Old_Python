'''
Created on 2011-07-04

@author: mjones
'''
## Loading NumPy
import numpy
import scipy
#import numpy as np

class SimplePlot(object):
    def __init__(self,dataX,dataY, title, textLabels,show, savePath = None):
        
        plt.figure()
        plt.clf        
        plt.plot(dataX, dataY,'ro')
        
        for text in range(len(dataX)):
            pass
            #print text
            #print textLabels[text]
            #plt.text(dataX[text], dataY[text], textLabels[text])

if __name__ == "__main__":
    pass
