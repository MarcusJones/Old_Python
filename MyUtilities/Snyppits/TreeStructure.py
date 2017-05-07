# A binary ordered tree example

class CNode:
    left , right, data = None, None, 0
    
    def __init__(self, data):
        # initializes the data members
        self.left = None
        self.right = None
        self.data = data

class CBOrdTree:
    def __init__(self):
        # initializes the root member
        self.root = None
    
    def addNode(self, data):
        # creates a new node and returns it
        return CNode(data)

    def insert(self, root, data):
        # inserts a new data
        if root == None:
            # it there isn't any data
            # adds it and returns
            return self.addNode(data)
        else:
            # enters into the tree
            if data <= root.data:
                # if the data is less than the stored one
                # goes into the left-sub-tree
                root.left = self.insert(root.left, data)
            else:
                # processes the right-sub-tree
                root.right = self.insert(root.right, data)
            return root
        
    def lookup(self, root, target):
        # looks for a value into the tree
        if root == None:
            return 0
        else:
            # if it has found it...
            if target == root.data:
                return 1
            else:
                if target < root.data:
                    # left side
                    return self.lookup(root.left, target)
                else:
                    # right side
                    return self.lookup(root.right, target)
        
    def minValue(self, root):
        # goes down into the left
        # arm and returns the last value
        while(root.left != None):
            root = root.left
        return root.data

    def maxDepth(self, root):
        if root == None:
            return 0
        else:
            # computes the two depths
            ldepth = self.maxDepth(root.left)
            rdepth = self.maxDepth(root.right)
            # returns the appropriate depth
            return max(ldepth, rdepth) + 1
            
    def size(self, root):
        if root == None:
            return 0
        else:
            return self.size(root.left) + 1 + self.size(root.right)

    def printTree(self, root):
        # prints the tree path
        if root == None:
            pass
        else:
            self.printTree(root.left)
            print root.data,
            self.printTree(root.right)

    def printRevTree(self, root):
        # prints the tree path in reverse
        # order
        if root == None:
            pass
        else:
            self.printRevTree(root.right)
            print root.data,
            self.printRevTree(root.left)

class myLeaf:
    def __init__(self,headerDef,searchVal):
        self.dat = (headerDef,searchVal)
        return idxTree(self.dat,None,None)
    
def Idx(headerDef,searchVal):
    data = (headerDef,searchVal)
    return idxTree(data,None,None)
    
class idxTree:
    def __init__(self,leftNode,rightNode,operator):
        self.leftNode = leftNode
        self.rightNode = rightNode
        self.operator = operator
        
        
        self.compositeMask = None
    
#    def getMask(self):
#        if not self.operator:
#            self.compositeMask = 1
#            return self.compositeMask
#    
    def getAND(self,leftNode,rightNode):
        leftVal = leftNode.runTree()
        rightVal = rightNode.runTree()
        print "{} and {}".format(leftVal,rightVal)
        andVal = leftVal + rightVal
        print " = {}".format(andVal)
        return andVal
        
    def getXOR(self,leftNode,rightNode):
        leftVal = leftNode.runTree()
        rightVal = rightNode.runTree()
        xorVal = leftVal + rightVal
        print "{} xor {} = {}".format(leftVal,rightVal,xorVal)
        xorVal = leftNode.runTree() - rightNode.runTree()
        return xorVal
        
    
    def runTree(self):
        if not self.operator:
            #self.compositeMask = 1
            #print "MASK {}, {}={}".format(self.compositeMask, self.leftNode[0] ,self.leftNode[1]),
            print "Leaf node, val is {}".format(self.leftNode[1])
            return self.leftNode[1]
        
        elif self.operator == "AND":
            #self.runTree = 
            print "try {} and {}".format(self.leftNode.printTree(),self.rightNode.printTree())
            
            self.getAND(self.leftNode,self.rightNode)
            
        elif self.operator == "XOR":
            #self.runTree = 
            self.getXOR(self.leftNode,self.rightNode)
            
                
    def printTree(self,lastString=None):
        if not lastString:
            lastString = ""
        # prints the tree path
        #print self.root
        #print "PRINTING"
        if not self.operator:
            #print "root empty"
            lastString = lastString + "{}={}".format(self.leftNode[0] ,self.leftNode[1])
        else:
            #print "root NOT empty",
            
            lastString = lastString + "("
            self.leftNode.printTree(lastString)
            #print root.data,
            
            lastString = lastString + self.operator
            
            self.rightNode.printTree(lastString)
            
            lastString = lastString + ")"
            
            #return lastString

    def __and__(self,other):
        return idxTree(self,other,"AND")
    
    def __or__(self,other):
        return idxTree(self,other,"XOR")
    
if __name__ == "__main__":
    tup1 = Idx("A",1)
    tup2 = Idx("B",2)
    
    print tup1.printTree()
     
    tup2.printTree()
    print 
    tup3 = tup1 & tup2
    #
    #print tup3.leftNode.leftNode
    
    tup3.printTree()
    #print tup3.operator
    
    tup4 = tup3 & tup2
    tup4.printTree()
    print 
    
    tup5 = tup4 | tup3
    tup5.printTree()
    print
    
    print "RUN TREE"
    
    tup5.runTree()
    
if __name__ == "__main2__":
    # create the binary tree
    BTree = CBOrdTree()
    # add the root node
    root = BTree.addNode(0)
    
    
    BTree.insert(root, data)
    
    
    # ask the user to insert values
    for i in range(0, 3):
        data = int(raw_input("insert the node value nr %d: " % i))
        # insert values
        BTree.insert(root, data)
    print
    
    BTree.printTree(root)
    print
    BTree.printRevTree(root)
    print
    data = int(raw_input("insert a value to find: "))
    if BTree.lookup(root, data):
        print "found"
    else:
        print "not found"
        
    print BTree.minValue(root)
    print BTree.maxDepth(root)
    print BTree.size(root)