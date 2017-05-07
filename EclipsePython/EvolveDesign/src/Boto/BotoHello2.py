'''
Created on Jan 7, 2012

@author: MJones
'''

import logging.config
from ec2_launch_instance import launch_instance
from ec2_find_all_running_instances import *
# Note that we had to 
logging.config.fileConfig('..\\..\\LoggingConfig\\logging.conf')

logging.info("Started Boto test script")

# find_all_running_instances()

#===============================================================================
# Create a connection to EC2 service.
#===============================================================================
ec2 = boto.connect_ec2()
allReservations = ec2.get_all_instances()
for reservation in allReservations:
    reservation.stop_all()

print instances
for reserv in instances:
    for inst in reserv.instances:
        if inst.state == u'running':
            print "Terminating instance %s" % inst
            inst.stop()





print allReservations

for reservation in allReservations:
    reservation.stop_all()
    
print allReservations
"""
print (allReservations[0])
print type(allReservations[0])
print dir(allReservations[0])

print ""

print allReservations[0].instances[0]
print type(allReservations[0].instances[0])
print dir(allReservations[0].instances[0])
"""

#===============================================================================
# BETTER: 
#===============================================================================
"""
instances = [i for r in reservations for i in r.instances]
for i in instances:
    pprint(i.__dict__)
    break # remove this to list all instances
"""


#print dir(allReservations)
#print dir(allReservations[0])



#launch_instance(key_name="PrivateKey",key_extension='.pem',key_dir="C:\EC2",group_name="default")

logging.info("Finished Boto test script")
