import datetime

from django.db import models
from django.contrib.auth.models import User

class Duty(models.Model):
    user = models.ForeignKey(User)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        get_latest_by = 'start'
        verbose_name_plural = "Duties"
    
    def on_duty(self):
        """ 
        there is a start but there isnt a stop,
        the duty is still active
        """
        
        return self.start and not self.end
    
    def time_expire_duty(self):
        return self.start + datetime.timedelta(hours=14)
    
    @classmethod
    def latest_open(cls, user):
        try:
            return cls.objects.filter(user=user, end=None).latest()
            
        except Duty.DoesNotExist:
            return Duty()
    

class DutyFlight(models.Model):
    block_start = models.DateTimeField()
    block_end = models.DateTimeField()
    
    airborne_start = models.DateTimeField()
    airborne_end = models.DateTimeField()
    
    duty = models.ForeignKey(Duty)
    
    def landed(self):
        return bool(self.airborne_end)
