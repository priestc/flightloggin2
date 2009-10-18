from django.db import models
from django.contrib.auth.models import User
from constants import *

class Records(models.Model):
    
    @classmethod
    def goon(cls, *args, **kwargs):
        """get object or None"""
        from annoying.functions import get_object_or_None
        return get_object_or_None(cls,  *args, **kwargs)
    
    user = models.ForeignKey(User, unique=True, primary_key=True, editable=False)
    text = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.user)
    
    @models.permalink
    def get_absolute_url(self):
        return ('records', [self.user.username])

    class Meta:
        verbose_name_plural = "Records"
        
    def adminlink(self):
        return "<a target='_blank' href='http://beta.flightlogg.in%s'>Link</a>"\
                    % self.get_absolute_url()
    adminlink.allow_tags = True
    
    def has_something(self):
        return bool(self.text) is True
    has_something.boolean = True
        
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
