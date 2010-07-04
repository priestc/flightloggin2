import datetime
from optparse import make_option

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from route.models import Route
from site_stats.models import Stat

class Command(BaseCommand):
    help = 'Calculate all stats and save to the database'
    
    
    
    def handle(self, *args, **options):
        
        # remove all empty routes first for accurate distance values
        Route.objects.filter(flight__pk__isnull=True).delete()
        
        start = datetime.datetime.now()
        ss = Stat()
        ss.save_to_db()
        stop = datetime.datetime.now()
        
        print "%s -- %s" % (datetime.datetime.now(), stop - start)
