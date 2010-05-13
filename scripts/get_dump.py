#!/usr/bin/env python

# gets the latest dump from Amazon S3

import datetime
import os

from boto.s3.connection import S3Connection
from dateutil import parser

# secret S3 keys should be set in environment variables
bucket = S3Connection().get_bucket('fl_dumps')

latest_key = None
latest_dt = datetime.datetime(1,1,1)

for key in bucket.get_all_keys():
    # go through all keys and return the one with the higest timestamp
    
    dt = parser.parse(key.key)
    
    if dt > latest_dt:
        latest_key = key
        latest_dt = dt

if latest_key:
    print "latest dump: %s" % latest_dt
    os.chdir('/srv/flightloggin/dumps') # change to dump dir
    latest_key.get_contents_to_filename('latest_dump') # download dump
