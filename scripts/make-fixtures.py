#!/usr/bin/env python
# dump the database, then send it to Amazon S3

import datetime
import os
import time

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from local_settings import AWS_SECRET_KEY, AWS_ACCESS_KEY

# do the dump
os.system("pg_dump --clean --format=c -U postgres logbook > this_dump")

conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
bucket = conn.get_bucket('fl_dumps')

k = Key(bucket)

k.key = datetime.datetime.now().isoformat()

#set the timestamp for later retrieval
ts = time.mktime(datetime.datetime.now().timetuple())
k.set_metadata('timestamp', ts)

#upload file
k.set_contents_from_filename('this_dump')

#clean up
os.remove('this_dump')
