from django.db import models
from django.contrib.auth.models import User
from constants import *
from flightloggin.main.mixins import GoonMixin
from flightloggin.main.queryset_manager import QuerySetManager
from flightloggin.share.middleware import share

class Records(models.Model, GoonMixin):
    
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
        return "<a target='_blank' href='http://flightlogg.in%s'>Link</a>"\
                    % self.get_absolute_url()
    adminlink.allow_tags = True
    
    def has_something(self):
        return bool(self.text) is True
    has_something.boolean = True
        
    def save(self, *args, **kwargs):
        
        if not self.user:
            self.user = share.get_display_user()
        super(Records,self).save(*args, **kwargs)


     
class NonFlight(models.Model, GoonMixin):

    date =      models.DateField()
    user =      models.ForeignKey(User, blank=True)
    remarks =   models.TextField(blank=True)
    non_flying = models.IntegerField(choices=NON_FLYING_CHOICES, default=0, blank=False)

    ## add custom filters to custom manager
    from queryset_manager import NonFlightQuerySet as QuerySet
    
    objects =  QuerySetManager()        ## add custom filterset manager

    class Meta:
        get_latest_by = 'date'
    
    def __unicode__(self):
        return u"%s -- %s" % (self.date, self.get_non_flying_display() )
    
    def save(self, *args, **kwargs):
        from share.middleware import share
        try:
            self.user.pk
        except:
            self.user = share.get_display_user()
            
        super(NonFlight,self).save(*args, **kwargs)
