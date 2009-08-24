from django.db import models
from django.contrib.auth.models import User
from constants import *

class Records(models.Model):
    user = models.ForeignKey(User, unique=True, primary_key=True)
    text = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = "Records"
        
class NonFlight(models.Model):

    date =      models.DateField()
    user =      models.ForeignKey(User, blank=False)
    remarks =   models.TextField(blank=True)
    
    staging = models.BooleanField(default=False)

    non_flying = models.IntegerField(choices=NON_FLYING_CHOICES, default=0, blank=False)

    def __unicode__(self):
        return u"%s -- %s" % (self.date, self.get_non_flying_display() )
