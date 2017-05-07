'''
Created on 29.03.2011

@author: mjones
'''
import logging

logger = logging.getLogger(__name__)

class ClassA:
    
    def __init__(self):
        print __name__
        logger.info('creating an instance of Auxiliary')
    def do_something(self):
        logger.info('doing something')
        a = 1 + 1
        logger.info('done doing something')

def some_function():
    logger.info('received a call to "some_function"')

xpathSearch = "".join([
    "//OBJECT/CLASS[re:match(text(), '" + "AA" + "')]/..",
    "/ATTR[re:match(text(), '" + "AA"  + "')]/..",
    "/ATTR/@Comment[re:match(.,'" + "AA" + "')]/..",
    ])

print xpathSearch