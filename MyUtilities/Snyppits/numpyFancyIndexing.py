import numpy as np

data = np.array([
         [11,12,13],
         [21,22,23],
         [31,32,33],
         [41,42,43],         
         ])

print data


# Masking
rows = np.array([False, False, True, True], dtype=bool)
cols = np.array([True, True, False], dtype=bool)

mask = rows[:,None]*cols[None,:]
# Better?
mask = np.outer(rows,cols)



print "Get a NEW array"
newArray = data[rows][:,cols]
print newArray

print "MODIFY array in place"
data[mask] = 0

print data

print "MODIFY array in place, advanced"
data = np.array([
         [11,12,13],
         [21,22,23],
         [31,32,33],
         [41,42,43],         
         ])

data[mask] = data[mask] * -1
print data

print "MODIFY array in place, advanced with function"
data = np.array([
         [11,12,13],
         [21,22,23],
         [31,32,33],
         [41,42,43],         
         ])

def multMinus1(array):
    return array * -1

data[mask] = multMinus1(data[mask])

print data

print "MODIFY array in place, advanced with ALL true"
data = np.array([
         [11,12,13],
         [21,22,23],
         [31,32,33],
         [41,42,43],         
         ])

rows = np.array([True, True, True, True], dtype=bool)
cols = np.array([True, True, True], dtype=bool)
mask = np.outer(rows,cols)
print mask.dtype
def multMinus1(array):
    return array * -1

data[mask] = multMinus1(data[mask])

print data


print "Regular reassignment"
data = np.array([1, 2, 4, 5])
data[3] = -1
print data[3]


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

