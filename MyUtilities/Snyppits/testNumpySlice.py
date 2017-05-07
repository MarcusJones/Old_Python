

import numpy as np

A = np.array([range(4), range(4), range(4)])

print A
print

thisMask = [True, False,True,False]
print type(thisMask)
print A[:,thisMask]

print "Note difference!"
thisMask = np.array([True, False,True,False])
print type(thisMask)
print A[:,thisMask]

