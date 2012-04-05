from iso8601 import parse_date
import os

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from django.core.management.base import NoArgsCommand
from django.conf import settings

class Command(NoArgsCommand):

    def handle(self, *args, **options):
        
        conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
        bucket = conn.get_bucket('fl_dumps')

        key = self.get_latest(bucket)
        print key



    def get_latest(bucket):
        """
        Given a S3 bucket, return the key in that bucket named with the latest
        timestamp.
        """
        keys = [parse_date(k.name) for k in bucket.list()]
        latest = sorted(keys)