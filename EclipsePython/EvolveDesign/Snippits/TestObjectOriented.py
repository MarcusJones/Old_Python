'''
Created on 04.03.2011

@author: mjones
'''


class TestClass:
    def __init__(self, name):
        self.name = name

    def sayHi(self):
        print 'Hello, how are you?', self.name

instance = TestClass("T")
print instance

instance.sayHi()