#!/usr/bin/env python
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
from __future__ import division    

from config import *

import logging.config
import unittest
from pyper import (R, Str4R, runR,
                   has_numpy, has_pandas)

import numpy as np

from UtilityInspect import whoami, whosdaddy, listObject

#===============================================================================
# Code
#===============================================================================
class MyClass(object):
    """This class does something for someone. 
    """
    def __init__(self, aVariable): 
        pass
    
class MySubClass(MyClass):
    """This class does
     
    """
    def __init__(self, aVariable): 
        super(MySubClass,self).__init__(aVariable)
    def a_method(self):
        """Return the something to the something."""
        pass

def some_function():
    """Return the something to the something."""
    pass

#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):
    
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        # generate a R instance
        self.r = R(RCMD=r"C:\Apps\R\R-2.15.2\bin\x64\R.exe")
        
    def test010_StandardTests(self):
        print "**** TEST {} ****".format(whoami())
    
        r = self.r
        
        # disable numpy & pandas in R
        r.has_numpy = False
        r.has_pandas = False
    
        # run R codes
        print r.run('a <- 3')
        print r('a <- 3')
        print r(['a <- 3', 'b <- a*2', 'print(b)'])
        
        
        
    
        # test parameter conversion
        a = range(5)
        r('b <- %s' % Str4R(a))
    
        # set variables in R
        r.assign('b', a)
        r['b'] = a
        r.b = a
    
        # get value from R 
        b = r['b']
        b = r.b
        pi = r['pi']
        pi = r.pi
        # or from a more complex R expression
        val = r['(2*pi + 3:9)/5']
        # get value from R variables that may not exist
        bb = r.get('bb', 'No this variable!')
    
        # delete R variables
        del(r.a, r['b'])
    
        # test for more data structure
        print('\n\n-------Test without numpy & pandas----------\n')
        r.avec = 0, 1, 2, 3, 4
        r.alist = [1, (2, 3, 'any strings'), 4+5j]
        r('amat <- matrix(0:11, nrow=3, byrow=TRUE)')
        r('aary <- array(0:23, dim=c(3,4,2))')
        r('adfm <- data.frame(aa=1:3, bb=paste("s", 2:4, sep="-"))')
        print('R vector (avec): ' + repr(r.avec))
        print('R list (alist): ' + repr(r.alist))
        print('R matrix (amat): ' + repr(r.amat))
        print('R array (aary): ' + repr(r.aary))
        print('R data frame (adfm): ' + repr(r.adfm))
    
        if has_numpy:
            print('\n\n-------Test with numpy----------\n')
            r.has_numpy = True
            arange, array, reshape = np.arange, np.array, np.reshape
            # numpy arrays
            # one-dimenstion numpy array will be converted to R vector
            r.bvec = arange(5)
            # two-dimenstion numpy array will be converted to R matrix
            r.bmat = reshape(arange(12), (3, 4)) # a 3-row, 4-column matrix
            # numpy array of three or higher dimensions will be converted to R array
            r.bary = reshape(arange(24), (2, 3, 4)) # a 3-row, 4-column, 2-layer array 
            # one-dimenstion numpy record array will be converted to R data.framme
            r.bdfm = array([(1, 'Joe', 35820.0), (2, 'Jane', 41235.0), (3, 'Kate', 37932.0)], \
                    dtype=[('id', '<i4'), ('employee', '|S4'), ('salary', '<f4')])
            print('R vector (avec): ' + repr(r['avec']))
            print('R vector (bvec): ' + repr(r['bvec']))
            print('R matrix (amat): ' + repr(r['amat']))
            print('R matrix (bamat): ' + repr(r['bmat']))
            print('R array (aary): ' + repr(r['aary']))
            print('R array (bary): ' + repr(r['bary']))
            print('R data frame (adfm): ' + repr(r['adfm']))
            print('R data frame (bdfm): ' + repr(r['bdfm']))
    
        if has_pandas:
            print('\n\n-------Test with pandas----------\n')
            r.has_pandas = True
            print('R data frame (adfm): ' + repr(r.adfm))
            if has_numpy:
                print('R data frame (bdfm): ' + repr(r['bdfm']))
    
    
        # test huge data sets and the function runR
        print('\n\n-------Test for huge data sets----------\n')
        a = range(10000) #00)
        sa = 'a <- ' + Str4R(a)
        rlt = runR(sa, Robj=r) # If you want to launch a new R process. use "runR(sa)" or "runR(sa, Robj='path_to_R')" instead.
        print(rlt)
    
        print('\nTest passed!\n\n')
    
        del(r) # to eliminate the possible DOS windows
    
        # to use an R on remote server, you need to provide correct parameter to initialize the R instance:
        # rsrv = R(RCMD='/usr/local/bin/R', host='My_server_name_or_IP', user='username')
        
    def test020_SimpleCreation(self):
        print "**** TEST {} ****".format(whoami())
    
        # generate a R instance
        r = R(RCMD=r"C:\Apps\R\R-2.15.2\bin\x64\R.exe")
        
    def test010_SimpleCreation(self):
        r = R(RCMD=r"C:\Apps\R\R-2.15.2\bin\x64\R.exe")
        
        r('png("abc.png"); plot(1:5); dev.off()') # plotting in R
        
        In [1]: # LOAD PYTHON PACKAGES
        
        In [2]: import pandas as pd
        
        In [3]: import pyper as pr
        
        In [4]: # READ DATA
        
        In [5]: data = pd.read_table("/home/liuwensui/Documents/data/csdata.txt", header = 0)
        
        In [6]: # CREATE A R INSTANCE WITH PYPER
        
        In [7]: r = pr.R(use_pandas = True)
        
        In [8]: # PASS DATA FROM PYTHON TO R
        
        In [9]: r.assign("rdata", data)
        
        In [10]: # SHOW DATA SUMMARY
        
        In [11]: print r("summary(rdata)")
        try({summary(rdata)})
            LEV_LT3           TAX_NDEB           COLLAT1           SIZE1       
         Min.   :0.00000   Min.   :  0.0000   Min.   :0.0000   Min.   : 7.738  
         1st Qu.:0.00000   1st Qu.:  0.3494   1st Qu.:0.1241   1st Qu.:12.317  
         Median :0.00000   Median :  0.5666   Median :0.2876   Median :13.540  
         Mean   :0.09083   Mean   :  0.8245   Mean   :0.3174   Mean   :13.511  
         3rd Qu.:0.01169   3rd Qu.:  0.7891   3rd Qu.:0.4724   3rd Qu.:14.751  
         Max.   :0.99837   Max.   :102.1495   Max.   :0.9953   Max.   :18.587  
             PROF2              GROWTH2             AGE              LIQ         
         Min.   :0.0000158   Min.   :-81.248   Min.   :  6.00   Min.   :0.00000  
         1st Qu.:0.0721233   1st Qu.: -3.563   1st Qu.: 11.00   1st Qu.:0.03483  
         Median :0.1203435   Median :  6.164   Median : 17.00   Median :0.10854  
         Mean   :0.1445929   Mean   : 13.620   Mean   : 20.37   Mean   :0.20281  
         3rd Qu.:0.1875148   3rd Qu.: 21.952   3rd Qu.: 25.00   3rd Qu.:0.29137  
         Max.   :1.5902009   Max.   :681.354   Max.   :210.00   Max.   :1.00018  
             IND2A            IND3A            IND4A             IND5A        
         Min.   :0.0000   Min.   :0.0000   Min.   :0.00000   Min.   :0.00000  
         1st Qu.:0.0000   1st Qu.:0.0000   1st Qu.:0.00000   1st Qu.:0.00000  
         Median :1.0000   Median :0.0000   Median :0.00000   Median :0.00000  
         Mean   :0.6116   Mean   :0.1902   Mean   :0.02692   Mean   :0.09907  
         3rd Qu.:1.0000   3rd Qu.:0.0000   3rd Qu.:0.00000   3rd Qu.:0.00000  
         Max.   :1.0000   Max.   :1.0000   Max.   :1.00000   Max.   :1.00000  
        
        
        In [12]: # LOAD R PACKAGE
        
        In [13]: r("library(betareg)")
        Out[13]: 'try({library(betareg)})\nLoading required package: Formula\n'
        
        In [14]: # ESTIMATE A BETA REGRESSION
        
        In [15]: r("m <- betareg(LEV_LT3 ~ SIZE1 + PROF2 + GROWTH2 + AGE + IND3A, data = rdata, subset = LEV_LT3 > 0)")
        Out[15]: 'try({m <- betareg(LEV_LT3 ~ SIZE1 + PROF2 + GROWTH2 + AGE + IND3A, data = rdata, subset = LEV_LT3 > 0)})\n'
        
        In [16]: # OUTPUT MODEL SUMMARY
        
        In [17]: print r("summary(m)")
        try({summary(m)})
        
        Call:
        betareg(formula = LEV_LT3 ~ SIZE1 + PROF2 + GROWTH2 + AGE + IND3A, data = rdata, 
            subset = LEV_LT3 > 0)
        
        Standardized weighted residuals 2:
            Min      1Q  Median      3Q     Max 
        -7.2802 -0.5194  0.0777  0.6037  5.8777 
        
        Coefficients (mean model with logit link):
                     Estimate Std. Error z value Pr(>|z|)    
        (Intercept)  1.229773   0.312990   3.929 8.53e-05 ***
        SIZE1       -0.105009   0.021211  -4.951 7.39e-07 ***
        PROF2       -2.414794   0.377271  -6.401 1.55e-10 ***
        GROWTH2      0.003306   0.001043   3.169  0.00153 ** 
        AGE         -0.004999   0.001795  -2.786  0.00534 ** 
        IND3A        0.688314   0.074069   9.293  < 2e-16 ***
        
        Phi coefficients (precision model with identity link):
              Estimate Std. Error z value Pr(>|z|)    
        (phi)   3.9362     0.1528   25.77   <2e-16 ***
        ---
        Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1 
        
        Type of estimator: ML (maximum likelihood)
        Log-likelihood: 266.7 on 7 Df
        Pseudo R-squared: 0.1468
        Number of iterations: 25 (BFGS) + 2 (Fisher scoring) 
        
        
        In [18]: # CALCULATE MODEL PREDICTION
        
        In [19]: r("beta_fit <- predict(m, link = 'response')")
        Out[19]: "try({beta_fit <- predict(m, link = 'response')})\n"
        
        In [20]: # SHOW PREDICTION SUMMARY IN R
        
        In [21]: print r("summary(beta_fit)")
        try({summary(beta_fit)})
           Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
         0.1634  0.3069  0.3465  0.3657  0.4007  0.6695 
        
        
        In [22]: # PASS DATA FROM R TO PYTHON
        
        In [23]: pydata = pd.DataFrame(r.get("beta_fit"), columns = ["y_hat"])
        
        In [24]: # SHOW PREDICTION SUMMARY IN PYTHON
        
        In [25]: pydata.y_hat.describe()
        Out[25]: 
        count    1116.000000
        mean        0.365675
        std         0.089804
        min         0.163388
        25%         0.306897
        50%         0.346483
        75%         0.400656
        max         0.669489

#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print ABSOLUTE_LOGGING_PATH
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())
    
    #print FREELANCE_DIR
    
    unittest.main()
        
    logging.debug("Finished _main".format())
    




