import datetime
import os
import time

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from django.core.management.base import NoArgsCommand
from django.conf import settings

class Command(NoArgsCommand):

    def handle(self, *args, **options):
          
        # do the dump only if it already hasn't been done yet
        if not os.path.exists('this_dump'):
            print("Dumping postgres...")
            os.system("pg_dump --clean --format=c -U postgres logbook > this_dump")
        else:
            print("Skipping postgres dump because it already exists")

        conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
        bucket = conn.get_bucket('fl_dumps')

        k = Key(bucket)
        k.key = datetime.datetime.now().isoformat()

        #upload file
        print("uploading to S3...")
        k.set_contents_from_filename('this_dump', reduced_redundancy=True)

        #clean up
        os.remove('this_dump')
