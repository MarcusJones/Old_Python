
import datetime
import time

inputFilePath = '..\\Test DCK files\\Begin.dck'

print 'reading:', inputFilePath    
fIn = open(inputFilePath,'r')
# Don't read unicode... inputFileTemplate=unicode(fIn.read(),'utf-8')
inputFileTemplate=fIn.read()
fIn.close()
translatedFile = inputFileTemplate
print ' writing:',
outF = open(r"c:\test.txt",'w')
#Unicode ... outF.write(self.translatedFile.encode('utf-8'))
outF.write(translatedFile)
outF.close()


#f = open('..\\Test DCK files\\test.dck', 'r')
#print f

#t1 = datetime.datetime.now()
#time.sleep(4)
#t2 = datetime.datetime.now()
#
#print t1, t2
#
#print datetime.timedelta(t1,t2)
#


t0 = datetime.datetime.now()

time.sleep(4)

delta_t = datetime.datetime.now() - t0

print str(delta_t.seconds)
#
#d = datetime.datetime.timedelta(delta_t)
#
#
#
#
#print d.seconds
# 


