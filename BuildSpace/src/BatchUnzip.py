'''
Created on Dec 17, 2011

@author: UserXP
'''
import os
import scipy.io as sio
import re
import csv
import subprocess



projectDir = os.path.normpath(r"D:\\K\\00\\Library")

unzipExe = r'"C:\Apps\7-Zip\7z.exe" '

dirList=os.listdir(projectDir)

print os.getcwd()
print os.chdir(projectDir)

##for fname in dirList[0:2]:
for fname in dirList:
    thisUnzipCmd = unzipExe + ' X -y "' + os.path.join(projectDir,fname) + '"'
    print thisUnzipCmd
    #print os.system(thisUnzipCmd)
    subprocess.call(thisUnzipCmd)
    #os.system(thisUnzipCmd)




#
#out
#
#for item in os.listdir(projectDir):
#    os.path.basename(item)
#
#for item in os.walk(projectDir):
#    print item
#
#loadsFiles = list()
#[loadsFiles.append(os.path.join(projectDir, name, "OUT", "loads.out")) 
#    for name in os.listdir(projectDir) 
#    if os.path.isdir(os.path.join(projectDir, name)) ]
