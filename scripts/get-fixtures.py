#!/usr/bin/env python

# gets the latest dump from Amazon S3

from boto.s3.connection import S3Connection

conn = S3Connection()
bucket = conn.get_bucket('fl_dumps')

latest_key = None
latest_ts = 0
for key in bucket.get_all_keys():
    # go through all keys and return the one with the higest timestamp
    ts = key.get_metadata('timestamp')
    
    if ts > latest_ts:
        latest_key = key
        latest_ts = ts

latest_key.get_contents_to_filename('../dumps/latest_dump')
