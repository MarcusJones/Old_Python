'''
Created on Dec 3, 2011

@author: UserXP
'''
from BeautifulSoup import BeautifulSoup
import re
import os
import re
import cProfile
from win32com.client import Dispatch
import logging.config
from time import sleep

RANGE = range(3, 8)
 
def word():
    word = Dispatch('Word.Application')
    doc = word.Documents.Add()
    word.Visible = True
    sleep(1)
 
    rng = doc.Range(0,0)
    rng.InsertAfter('Hacking Word with Python\r\n\r\n')
    sleep(1)
    for i in RANGE:
        rng.InsertAfter('Line %d\r\n' % i)
        sleep(1)
    rng.InsertAfter("\r\nPython rules!\r\n")
 
    doc.Close(False)
    word.Application.Quit()

#def select

if __name__ == '__main__':
    word()