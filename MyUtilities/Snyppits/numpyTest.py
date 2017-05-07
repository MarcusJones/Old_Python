import numpy as np

data = np.array([
         [11,12,13],
         [21,22,23],
         [31,32,33],
         [41,42,43],         
         ])

print data

rows = np.array([False, False, True, True], dtype=bool)
cols = np.array([True, True, False], dtype=bool)

newArray = data[rows][:,cols]


mask = rows[:,None]*cols[None,:]

mask = np.outer(rows,cols)

data[mask] = 0

print data


#
#data[mask] = 0
#
#
#print newArray
##print data[rows][:,cols] = 
## [[31 32]
##  [41 42]]
#
#
#data = np.array([
#     [11,12,13],
#     [21,22,23],
#     [31,32,33],
#     [41,42,43],         
#     ])
#
#print data
#data = np.array([
#     [11,12,13],
#     [21,22,23],
#     [0,0,33],
#     [0,0,43],         
#     ])
#
##matrixMask = np.outer(rows,cols)
#
##print matrixMask
#
##subArray = data[matrixMask].asarray()
#
##print data[rows][:,cols]

