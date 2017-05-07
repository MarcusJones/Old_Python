import win32com.client
#import MatlabCom
from subprocess import call


def _testMlab():
    call([r"D:\apps\Matlab\bin\matlab.exe", r"/Automation"])
    
    #ml = win32com.client.Dispatch('matlab.application')
    
    #ml.Execute("surf(peaks)")
    #for i in xrange(100):
    #    ret = ml.eval('disp \'hiush world\'')
        #print ret
#    ml.Execute ("plot([0 18], [7 23])")
#    #ml.Visible = False;
#    ml.Execute("surf(peaks)")
#    ml.Execute("figure")
#    ml.Execute("surf(peaks)")
#
#    #ml.Execute("pause(4)")
#    #ml.Visible = True;
#    
#    ml.Execute ("1+1")
#    
#    ml.Execute("pause(99999999999999999)")