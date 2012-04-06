import datetime
import os
import time

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.db import models

class Command(NoArgsCommand):

    def handle(self, *args, **options):
          
        # do the dump only if it already hasn't been done yet
        if not os.path.exists('this_dump'):
            print("Dumping postgres...")
            os.system("pg_dump --clean --no-owner --format=c logbook > this_dump")
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
        
    
    def get_tables(self, manifest):
        """
        For a given manifest, return all the database tables that we are going
        to dump.
        """
        all_models = model.get_models()
        dump_models = []
        
        for model in all_models:
            if model.__name__ not in manifest['exclude-models']:
                dump_models.append(m._meta.db_table)
        
        return dump_models
        