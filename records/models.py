from django.db import models
from django.contrib.auth.models import User
from constants import *
from main.mixins import GoonMixin
from main.queryset_manager import QuerySetManager
from share.middleware import share

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

     
class NonFlight(models.Model, GoonMixin):
    """
    Represents a logbook event that is not a flight: medical, signoff, etc
    """
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
        return u"%s -- %s" % (self.date, self.get_non_flying_display())