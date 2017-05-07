'''
Created on 2012-04-14

@author: Anonymous
'''
import numpy as np

list2 = [[1,2], [3,4]]

list3 = [["asdf","asdf"], ["asdfa","dddd"]]


print list2


array2 = np.array(list3, dtype="object")

print array2
print np.shape(array2)