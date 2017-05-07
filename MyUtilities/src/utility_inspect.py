'''
Created on 2012-04-13

@author: Anonymous
'''
from __future__ import print_function

import inspect

def whoami():
    return inspect.stack()[1][3]
def whosdaddy():
    return inspect.stack()[2][3]


def list_attrs(obj):
    attrs = vars(obj)
    # {'kids': 0, 'name': 'Dog', 'color': 'Spotted', 'age': 10, 'legs': 2, 'smell': 'Alot'}
    # now dump this in some way or another
    attr_list  = ["{} : {}".format(*item) for item in attrs.items()]
    print(attr_list)
    
def listObject(theObject,cols = 5):
    #return "\n".join(listObject.__dict__)
    print("********")
    print(type(theObject))
    items = dir(theObject)
    while(items):
        for i in range(cols):
            if items:
                print("{:<30}".format(items.pop(0)),end='')
        print()
        #print item
        
    #print dir(listObject)
    #return 1