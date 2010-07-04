import datetime
from optparse import make_option

from django.core.management.base import NoArgsCommand

from django.contrib.auth.models import User

from backup.classes import Backup, EmailBackup
from backup.models import UsersToday

class Command(NoArgsCommand):
    help = 'Sends email backups to each user depending on their preferences'
    
    option_list = NoArgsCommand.option_list + (
            make_option('--weekly',
                        '-w',
                        dest='weekly',
                        action='store_true',
                        help="Do the weekly schedule",
            ),
            
            make_option('--monthly',
                        '-m',
                        dest='monthly',
                        action='store_true',
                        help="Do the monthly schedule",
            ),
            
            make_option('--daily',
                        '-d',
                        dest='daily',
                        action='store_true',
                        help="Do the daily schedule",
            ),
            
            make_option('--biweekly',
                        '-b',
                        dest='biweekly',
                        action='store_true',
                        help="Do the biweekly schedule",
            ),
    )
    
    def handle(self, *args, **options):
        
        today = datetime.date.today()
        
        if options['weekly']:
            schedule = "weekly"
            week_ago = today - datetime.timedelta(days=7)
            records = UsersToday.objects.filter(date__gte=week_ago)
            users = User.objects.filter(profile__backup_freq=1,
                                        userstoday__in=records).distinct()
        
        elif options['biweekly']:
            schedule = "biweekly"
            two_weeks_ago = today - datetime.timedelta(days=14)
            records = UsersToday.objects.filter(date__gte=two_weeks_ago)
            users = User.objects.filter(profile__backup_freq=2,
                                        userstoday__in=records).distinct()
        
        elif options['monthly']:
            schedule = "monthly"
            month_ago = today - datetime.timedelta(days=30)
            records = UsersToday.objects.filter(date__gte=month_ago)
            users = User.objects.filter(profile__backup_freq=3,
                                        userstoday__in=records).distinct()
            
        elif options['daily']:
            schedule = "daily"
            today = datetime.date.today()
            records = UsersToday.objects.filter(date__gte=today)
            users = User.objects.filter(profile__backup_freq=4,
                                        userstoday__date=today)
        
        print "** %s ** - %s" % (schedule.upper(), datetime.datetime.now())
        print "%s emails to send" % users.count()
        print "%s total users in this interval\n" % \
                User.objects.filter(userstoday__in=records).distinct().count()
        
        start = datetime.datetime.now()
        for user in users:
            try:
                em = EmailBackup(user, auto=True)
            except Exception, e:
                ## do not raise exception of a single user's email can't be made,
                ## instead print the error message to the log
                print "ERROR: %s - %s" % (self.user, e)
            
            else:
                result = em.send()
                print "%s [%s]" % (user.username, result)
        
        print "total processing time: %s" % (datetime.datetime.now() - start)
