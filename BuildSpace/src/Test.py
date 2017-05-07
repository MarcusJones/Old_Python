'''
Created on Dec 5, 2011

@author: UserXP
'''

#RAN: python setup.py install
#
# from deap import dtm FAILS!
# then need to install mpi4py
# easy_install mpi4py
# error: Setup script exited with error: Unable to find vcvarsall.bat

# Now, downloaded source from google code
# Extracted mpi4py-1.2.2 directory to python site-
#
# Now needed MINGW C++ compiler:
# http://www.mingw.org/wiki/Getting_Started
# DL: http://sourceforge.net/projects/mingw/files/Installer/mingw-get-inst/mingw-get-inst-20111118/mingw-get-inst-20111118.exe/download
# Installed C and C++ compiler

from deap import dtm

print "Hello"

dtm.setOptions(communicationManager="deap.dtm.commManagerTCP")

def op(x):
    return x + 1./x     # Or any operation

def main():
    nbrs = range(1, 1000)
    results = dtm.map(op, nbrs)

dtm.start(main)