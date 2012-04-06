import os
from optparse import make_option

from dateutil.parser import parse

from boto.s3.connection import S3Connection

from django.core.management.base import NoArgsCommand
from django.conf import settings

import logging
log = logging.getLogger(__name__)

from easydump.mixins import DumpMixin

restore_cmd = 'pg_restore -d {manifest[database][NAME]} --role={manifest[database][USER]} --jobs={manifest[jobs]} {manifest[save_path]}'

class Command(NoArgsCommand, DumpMixin):
    
    option_list = NoArgsCommand.option_list + (
        make_option(
            '--dump',
            '-d',
            dest='dump',
            help="Dump to perform",
        ),
    )
    
    def handle(self, *args, **options):
        
        # get manifest
        dump = options['dump']
        manifest = self.get_manifest(dump)

        # connect to S3
        c = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
        bucket = c.get_bucket(manifest['s3-bucket'])
        
        # get the key for the correct dump (the latest one)
        key = self.get_latest(bucket)
        
        manifest['save_path'] = manifest['save_path'].format(key=key.name)
        
        if not os.path.exists(manifest['save_path']):
            log.info("Downloading from S3...")      
            key.get_contents_to_filename(manifest['save_path'])
            log.info("Done")
        else:
            log.info('not downloading because it already has been downloaded')
        
        # put into postgres
        cmd = restore_cmd.format(manifest=manifest)
        os.system(cmd)

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
        return bucket.get_key(key)