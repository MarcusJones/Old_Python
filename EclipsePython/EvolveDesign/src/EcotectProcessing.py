'''
Created on 2011-07-04

@author: mjones
'''
## Loading NumPy
import numpy

## Loading SciPy
import scipy

## Importing all NumPy functions, modules and classes
from numpy import *

import csv

#import matplotlib as plt
#from matplotlib import pyplot as plt
from matplotlib.pyplot import *

from mpl_toolkits.mplot3d import axes3d

filePath = r"C:\Documents and Settings\UserXP\Desktop\test"

openFile = open(filePath)

reader = csv.reader(openFile, delimiter=',')

allData = list(reader)

headers = allData[:5]
for row in headers:
    print row
    
analysisData = allData[5:]


for idx, row in enumerate(analysisData):
    analysisData[idx] = analysisData[idx][0:-1]
    #print row

dataArray=numpy.array(analysisData).astype('float')

#print dataArray
#print dataArray.shape

X = numpy.arange(0,dataArray.shape[0])
Y = numpy.arange(0,dataArray.shape[1])
X, Y = np.meshgrid(X, Y)
Z = dataArray.transpose()

print "X is {0}".format(X.shape)
print "Y is {0}".format(Y.shape)
print "Z is {0}".format(Z.shape)

fig = figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_wireframe(X, Y, Z)

hold(True)


#imshow(Z)
imshow(Z, cmap=cm.jet, norm=None, aspect=None, interpolation=None,
       alpha=None, vmin=None, vmax=None, origin=None, extent=None)
#contour(Z)
colorbar()
#imshow(X)
show()

#X = np.arange(-5, 5, 0.25)
#Y = np.arange(-5, 5, 0.25)
#X, Y = np.meshgrid(X, Y)
#R = np.sqrt(X**2 + Y**2)
#Z = np.sin(R)
#surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet,
#        linewidth=0, antialiased=False)
#ax.set_zlim3d(-1.01, 1.01)
#
#fig.colorbar(surf, shrink=0.5, aspect=10)
#
##---- Second subplot
#ax = fig.add_subplot(1, 2, 2, projection='3d')
#X, Y, Z = get_test_data(0.05)
#ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)





#plot(result)
#show()