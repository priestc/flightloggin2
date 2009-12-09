from django.db import models

class Duty(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    

class DutyFlight(models.Model):
    block_start = models.DateTimeField()
    block_end = models.DateTimeField()
    
    block_start = models.DateTimeField()
    block_end = models.DateTimeField()
    
    duty = models.ForeignKey(Duty)
