# -*- coding: utf-8 -*-
"""
Created on Sat Oct 08 14:36:53 2011

@author: UserXP
"""

import win32clipboard

def myPaste():
    win32clipboard.OpenClipboard()
    spyderClipText = win32clipboard.GetClipboardData()
    #print repr(spyderClipText)
    repairedText = spyderClipText.replace("\x00", "")
    #print repr(repairedText)
    win32clipboard.SetClipboardText(repairedText)
    win32clipboard.CloseClipboard()
    #return spyderClipText
    %paste 

print "foo"