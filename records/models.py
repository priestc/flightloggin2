from django.db import models
from django.contrib.auth.models import User
from constants import *

class Records(models.Model):
    user = models.ForeignKey(User, unique=True, primary_key=True, editable=False)
    text = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = "Records"
        
    def save(self, *args, **kwargs):
        from share.middleware import share
        if not self.user:
            self.user = share.get_display_user()
        super(Records,self).save(*args, **kwargs)
        
class NonFlight(models.Model):

    date =      models.DateField()
    user =      models.ForeignKey(User, blank=True)
    remarks =   models.TextField(blank=True)
    non_flying = models.IntegerField(choices=NON_FLYING_CHOICES, default=0, blank=False)

    def __unicode__(self):
        return u"%s -- %s" % (self.date, self.get_non_flying_display() )
    
    def save(self, *args, **kwargs):
        from share.middleware import share
        try:
            self.user.pk
        except:
            self.user = share.get_display_user()
            
        super(NonFlight,self).save()
