from django.db import models
from django.contrib.auth.models import User

class UsersToday(models.Model):
    date = models.DateField()
    logged_today = models.ManyToManyField(User, null=True)
    
    class Meta:
        get_latest_by = 'date'
        
    def __unicode__(self):
        return "%s (%s)" % (self.date, self.logged_today.count())
    
    def users_count(self):
        return self.logged_today.count()
    
    def usernames(self):
        users = self.logged_today.order_by('username')
        ret = []
        for u in users:
            ret.append(u.username)
        
        return ", ".join(ret)
    
    def email_usernames(self):
        users = self.logged_today.filter(profile__backup_freq=4).order_by('username')
        ret = []
        for u in users:
            ret.append(u.username)
        
        return ", ".join(ret)
        

#########################################################

   
import django.dispatch
edit_logbook = django.dispatch.Signal()

def add_to_email_queue(sender, **kwargs):
    """
    Add the user to the list of users who have edited their logbook
    today. This function gets called whenever a logbook is edited
    """
    
    import datetime
    today = datetime.date.today()
    ut,c = UsersToday.objects.get_or_create(date=today)
    ut.logged_today.add(sender)
    ut.save()

edit_logbook.connect(add_to_email_queue)
