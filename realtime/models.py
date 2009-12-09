from django.db import models
from django.contrib.auth.models import User

class Duty(models.Model):
    user = models.ForeignKey(User)
    start = models.DateTimeField()
    end = models.DateTimeField()
    
    class Meta:
        get_latest_by = 'end'
        verbose_name_plural = "Duties"
    
    def on_duty(self):
        return bool(self.end)
    

class DutyFlight(models.Model):
    block_start = models.DateTimeField()
    block_end = models.DateTimeField()
    
    airborne_start = models.DateTimeField()
    airborne_end = models.DateTimeField()
    
    duty = models.ForeignKey(Duty)
    
    def landed(self):
        return bool(self.airborne_end)
            
