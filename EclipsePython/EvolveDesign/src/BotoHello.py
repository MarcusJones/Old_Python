'''
Created on Jan 3, 2012

@author: UserXP
'''

import os
import time
import logging.config
from boto.s3.connection import S3Connection
#import boto.ec2
import boto

logging.config.fileConfig('..\\LoggingConfig\\logging.conf')

#logging = logging.getLogger("zipper")
#print logging.getLogger('boto')
#print logging.getLogger('root')


logging.info("Started Boto EC2 test script")

#myLogFile = os.path.normpath(r'c:\EC2\boto.log')
#boto.set_stream_logger('pynas-uploader')

#boto.set_file_logger('pynas-uploader', myLogFile, 2)


TARGET_REGION = 'eu-west-1'

#===============================================================================
# Establish connection
#===============================================================================
connection = S3Connection()
logging.info("Connection established: {0}".format(connection))


#===============================================================================
# Check S3
#===============================================================================
buckets = connection.get_all_buckets()  # returns a list of bucket objects
logging.info("S3 buckets: {0}".format(buckets))

#===============================================================================
# Check EC2
#===============================================================================
ec2 = boto.connect_ec2()
zones = ec2.get_all_zones()
logging.info("EC2 zones from default region: {0}".format(zones))
ec2 = boto.ec2.connect_to_region(TARGET_REGION)
zones = ec2.get_all_zones()
logging.info("EC2 zones from {0} region: {1}".format(TARGET_REGION,zones))

allRegions = boto.ec2.regions()
logging.info("All regions: {0}".format(allRegions))

logging.info("Finished")



"""
from boto.s3 import Connection

import boto

import boto
s3 = boto.connect_s3()


connection = Connection()

ec2_conn = boto.connect_ec2()

images = ec2_conn.get_all_images(image_ids=['ami-b111f4d8'])
"""

#print images