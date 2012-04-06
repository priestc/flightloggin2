import logging
import os
from optparse import make_option

from dateutil.parser import parse

from boto.s3.connection import S3Connection

from django.core.management.base import NoArgsCommand
from django.conf import settings

log = logging.getLogger(__name__)

PROJECT_PATH = getattr(settings, 'PROJECT_PATH', None)
TEMP_LOCATION = getattr(settings, 'TEMP_LOCATION', None)

class Command(NoArgsCommand):
    
    option_list = NoArgsCommand.option_list + (
        make_option(
            '--dump',
            '-d',
            dest='dump',
            help="Dump to perform",
        ),
    )
    
    def handle(self, *args, **options):
        DUMP_MANIFEST = getattr(settings, 'DUMP_MANIFEST')
        dump = options['dump']
        manifest = DUMP_MANIFEST[dump]                
        c = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
        bucket = c.get_bucket(manifest['s3-bucket'])
        latest_key = self.get_latest(bucket)
        key = bucket.get_key(latest_key)
        path = self.get_save_path()
        save_path = os.path.join(path, '{0}-{1}'.format(dump, key.name))
        
        if not os.path.exists(save_path):       
            key.get_contents_to_filename(save_path)
        else:
            log.info('not downloading because it already has been downloaded')
        
        # put into postgres
        cmd = 'pg_restore -d %s %s' % (manifest['database'], save_path)
        os.system(cmd)

    def get_save_path(self):
        """
        Based on the settings provided, figure out where to save incoming dumps
        """
        if TEMP_LOCATION:
            return TEMP_LOCATION
            
        if PROJECT_PATH:
            return PROJECT_PATH
        
        return '.' # if no setting can be found, use current dir

    def get_latest(self, bucket):
        """
        Given a S3 bucket, return the key in that bucket named with the latest
        timestamp.
        """
        keys = [{'dt': parse(k.name), 'string': k.name} for k in bucket.list()]
        latest = sorted(keys, key=lambda x: x['dt'])[-1]
        key = latest['string']
        dt = latest['dt']
        log.info("Using latest dump from: {0:%B %m, %y -- %X}".format(dt))
        return key