import datetime
from optparse import make_option

from django.core.management.base import NoArgsCommand

from django.contrib.auth.models import User

class Command(NoArgsCommand):
    def handle(self, *a, **k):
        
        for user in User.objects.all():
            try:
                p = user.get_profile()
                print p.user.password, user.email
            except:
                pass
            
            