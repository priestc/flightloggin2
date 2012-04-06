from datetime import datetime, timedelta

from dateutil import parser

from boto.s3.connection import S3Connection
from boto.s3.key import Key
    
from django.core.management.base import NoArgsCommand
from django.conf import settings

class Command(NoArgsCommand):
    
    def handle(self, *args, **options):
        two_weeks_ago = datetime.now() - timedelta(days=14)
        three_months_ago = datetime.now() - timedelta(days=90)
        
        # connect to S3 and get bucket
        conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
        bucket = conn.get_bucket('fl_dumps')
        
        keys = bucket.get_all_keys()
        
        for key in keys:
            dt = parser.parse(key.key)
            
            is_2_weeks_old = dt < two_weeks_ago
            is_3_months_old = dt < three_months_ago
            is_monday_9PM = dt.strftime("%w %H") == '1 18'
            
            if is_2_weeks_old:
                if is_monday_9PM:
                    print "keep:", dt
                else:
                    print "delete:", dt
                    key.delete()
            else:
                print "keep:", dt
