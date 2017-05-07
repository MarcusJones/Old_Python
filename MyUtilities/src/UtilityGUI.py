
from __future__ import division    
#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""This module does A and B. 
Etc.
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:


from config import *

import logging.config
import unittest

from utility_inspect import whoami, whosdaddy, listObject
import wx
from utility_path import filter_files_dir

#===============================================================================
# Code
#===============================================================================
class MyClass(object):
    """This class does something for someone. 
    """
    def __init__(self, aVariable): 
        pass

class runDirectory(wx.Frame):
    """
    Does *something* with a directory
    Pass in the something as a function
    """
    
    #----------------------------------------------------------------------
    def __init__(self, dirName = "c:", fileName=".", extensionSearch = "html$", runFunc = None):
        
        
        self.runFunction = runFunc
        self.dirName = dirName
        self.extensionSearch = extensionSearch
        self.fileName = fileName
        
        self.update()
        
        box = wx.BoxSizer(wx.VERTICAL)
        
        # Start GIU
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "File and Folder Dialogs Tutorial")
        self.panel = wx.Panel(self, -1)
        
        # Test
        self.t1 = wx.TextCtrl(self.panel, wx.ID_ANY, "Test it out and see")
        #wx.CallAfter(t1.SetInsertionPoint, 0)        
        box.Add(self.t1, 0, wx.EXPAND)
        self.Bind(wx.EVT_TEXT, self.EvtText, self.t1)
        self.t1.Bind(wx.EVT_CHAR, self.EvtChar)
        
        # Text
        title = wx.StaticText(self.panel, wx.ID_ANY, 'Current directory')
        box.Add(title, 0, wx.EXPAND)
        
        #print self.dirName
        # Text control box, shows current dir
        self.textBox1 = wx.TextCtrl(self.panel, wx.ID_ANY, "{}".format(self.dirName) )
        box.Add(self.textBox1, 0, wx.EXPAND)

        # Text
        title = wx.StaticText(self.panel, wx.ID_ANY, 'Extension')
        box.Add(title, 0, wx.EXPAND)

        # Text control box, shows current extension
        self.textBox2 = wx.TextCtrl(self.panel, wx.ID_ANY, self.extensionSearch)
        self.textBox2.Bind(wx.EVT_KEY_DOWN, self.change_ctrl_ext)
        
        self.Bind(wx.EVT_TEXT, self.EvtText, self.t1)
        self.t1.Bind(wx.EVT_CHAR, self.EvtChar)        
        box.Add(self.textBox2, 0, wx.EXPAND)
        
        # Change dir
        self.dirDlgBtn = wx.Button(self.panel, label="Change directory")
        self.dirDlgBtn.Bind(wx.EVT_BUTTON, self.onDir)
        box.Add(self.dirDlgBtn, flag=wx.LEFT, border=10)
        
        # Run        
        self.runButton = wx.Button(self.panel, -1, 'Run {}'.format("Placeholder function name"))
        self.runButton.Bind(wx.EVT_BUTTON, self.onRun)
        box.Add(self.runButton, 0, wx.EXPAND)
        
        # List
        self.listBox1 = wx.ListBox(self.panel, -1,choices=self.filesList)
        box.Add(self.listBox1, 0, wx.EXPAND)

        #self.listBox1 = wx.ListBox(self.panel,choices=[], id = wx.ID_ANY,name='listBox1', parent=self,style=0)
        #self.listBox1.SetBackgroundColour(wx.Colour(255, 255, 128))
        #self.listBox1.Bind(wx.EVT_LISTBOX, self.OnListBox1Listbox,
        #id=wxID_FRAME1LISTBOX1)        
        
        # Finalize form
        self.panel.SetSizer(box)
        self.Centre()
        

    def update(self):
        # Get files
        self.filesList =  filter_files_dir(self.dirName,self.fileName,self.extensionSearch)
        print "Update: dir {}, ext {} ".format(self.dirName, self.extensionSearch)
        #self.lbox.SetItems(self.choices)
        
    def EvtText(self, event):
        print "Hit {} - {}".format(whoami(), event.GetString())
        self.update()        
        #self.log.WriteText('EvtText: %s\n' % event.GetString())
        #print "Update: dir {}, ext {} ".format(self.dirName, self.extensionSearch)

    def EvtTextEnter(self, event):
        #self.log.WriteText('EvtTextEnter\n')
        print "Hit {}; {}".format(whoami(), event.GetString())
        self.update()        
        #print "Update: dir {}, ext {} ".format(self.dirName, self.extensionSearch)
        
        #event.Skip()

    def EvtChar(self, event):
        print "Hit {}".format(whoami())
        self.update()
        #self.log.WriteText('EvtChar: %d\n' % event.GetKeyCode())
        #print "Update: dir {}, ext {} ".format(self.dirName, self.extensionSearch)
        event.Skip()


        
    def change_ctrl_ext(self,event):
        print "Hit {}".format(whoami())
        self.update()
             
    def onRun(self, event):
        logging.debug("Run function {}".format(self.dirName))
        print "Hit {}".format(whoami())
        self.runFunction(self.dirName)
        self.update()
        
    def onDir(self, event):
        """
        Show the DirDialog and print the user's choice to stdout
        """
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
        
        if dlg.ShowModal() == wx.ID_OK:
            self.dirName = dlg.GetPath()
            logging.debug("Selected Dir: {}".format(self.dirName))
            self.textBox1.ChangeValue(self.dirName)
            
        dlg.Destroy()
        
        self.update()
        
        
def YesNoOLD(parent, question, caption = 'Yes or no?'):
    dlg = wx.MessageDialog(parent, question, caption, wx.YES_NO | wx.ICON_QUESTION)
    result = dlg.ShowModal() == wx.ID_YES
    dlg.Destroy()
    return result

def simpleYesNo(question="Question; Yes or No?"):
    print wx
    print dir(wx)
    
    app = wx.PySimpleApp()
    retCode = wx.MessageBox(question, "", wx.YES|wx.NO)
    if (retCode == 2):
        return True
    else:
        return False  
         




class MyForm(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self, startingDir = "c:"):
        
        self.dirName = startingDir
        
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "File and Folder Dialogs Tutorial")
        self.panel = wx.Panel(self, -1)
        
        
        
        box = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(self.panel, wx.ID_ANY, 'Current directory')
        box.Add(title, 0, wx.EXPAND)
        
        
        self.textBox1 = wx.TextCtrl(self.panel, wx.ID_ANY, self.dirName )
        box.Add(self.textBox1, 0, wx.EXPAND)
        

        box.Add(wx.Button(self.panel, -1, 'Button2'), 0, wx.EXPAND)
        
        box.Add(wx.Button(self.panel, -1, 'Button3'), 0, wx.ALIGN_CENTER)
        
        #self.onDir = "asdf"
        self.dirDlgBtn = wx.Button(self.panel, label="Show DirDialog")
        self.dirDlgBtn.Bind(wx.EVT_BUTTON, self.onDir)
        box.Add(self.dirDlgBtn, flag=wx.LEFT, border=10)

        self.panel.SetSizer(box)
        self.Centre()
        
    #- onDir ---------------------------------------------------------------------
    def onDir(self, event):
        """
        Show the DirDialog and print the user's choice to stdout
        """
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
        
        if dlg.ShowModal() == wx.ID_OK:
            self.dirName = dlg.GetPath()
            logging.debug("Selected Dir: {}".format(self.dirName))
            self.textBox1.ChangeValue(self.dirName)
            
        dlg.Destroy()

def runDirFilter(runFunction):

        
    app = wx.App(False)
    dirName = "C:\Dropbox\BREEAM ENE 5 Results1\\"
    
    
    frame = runDirectory(dirName = "c:", fileName=".", extensionSearch = "html$", runFunc =runFunction)
    
    frame.Show()
    app.MainLoop()

def YesNoOLD(parent, question, caption = 'Yes or no?'):
    dlg = wx.MessageDialog(parent, question, caption, wx.YES_NO | wx.ICON_QUESTION)
    result = dlg.ShowModal() == wx.ID_YES
    dlg.Destroy()
    return result

def simpleYesNo(question="Question; Yes or No?"):
    print wx
    print dir(wx)
    
    app = wx.PySimpleApp()
    retCode = wx.MessageBox(question, "", wx.YES|wx.NO)
    if (retCode == 2):
        return True
    else:
        return False  
         
#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):
    
    def setUp(self):
        print "**** TEST {} ****".format(whoami())

    @unittest.skip("")         
    def test020_SimpleCreation(self):
        print "**** TEST {} ****".format(whoami())
        print "BETTER?"
        ret = simpleYesNo("Test")
        print "Got  answer;", ret

    @unittest.skip("")         
    def test030_getDir(self):
        print "**** TEST {} ****".format(whoami())
        app = wx.App(False)
        frame = MyForm()
        frame.Show()
        app.MainLoop()

    def test040_getDirFOrm(self):

        print "**** TEST {} ****".format(whoami())
        

        def testFunction1(dirName):
            print "Test function RUN"
            print dirName
        
        runDirFilter(testFunction1)

        
         
#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print ABSOLUTE_LOGGING_PATH
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())
    
    #print dir(wx)
    print wx.__file__
    
    #print FREELANCE_DIR
    
    unittest.main()
        
    logging.debug("Finished _main".format())


