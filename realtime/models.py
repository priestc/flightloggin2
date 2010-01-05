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
        return not bool(self.end)
    
    @classmethod
    def latest(cls, user):
        try:
            latest_duty = cls.objects.filter(user=user).latest()
            
        except Duty.DoesNotExist:
            latest_duty = Duty()
        
        return latest_duty
    

class DutyFlight(models.Model):
    block_start = models.DateTimeField()
    block_end = models.DateTimeField()
    
    airborne_start = models.DateTimeField()
    airborne_end = models.DateTimeField()
    
    duty = models.ForeignKey(Duty)
    
    def landed(self):
        return bool(self.airborne_end)
            
