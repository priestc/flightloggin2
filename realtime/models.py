import datetime

from django.db import models
from django.contrib.auth.models import User

class Duty(models.Model):
    user = models.ForeignKey(User)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    
    def __unicode__(self):
        return self.user.username
    
    @classmethod
    def latest_open(cls, user):
        try:
            return cls.objects.filter(user=user, end=None).latest()
            
        except Duty.DoesNotExist:
            return None
           
    class Meta:
        get_latest_by = 'start'
        verbose_name_plural = "Duties"
        
    def is_valid(self):
        t = []
        for block in self.closed_blocks():
            t.append(block.is_valid())
            
    ############
    
    def on_duty(self):
        """ 
        there is a start but there isnt a stop,
        the duty is still active
        """
        
        return self.start and not self.end
    
    def time_expire_duty(self):
        """
        Time until the duty expires
        """
        
        return self.start + datetime.timedelta(hours=14)
    
    def duty_length(self):
        """
        The length of the duty time
        """
        
        if self.start and self.end:
            return self.end - self.start
        else:
            return ""
    
    def closed_blocks(self):
        """
        Returns all closed block times in order of when the block was opened
        """
        
        blocks = []
        for block in self.dutyflight_set.order_by('block_start'):
            if block.block_finished():
                blocks.append(block)
        
        return blocks
    
    def closed_airbornes(self):
        """
        Returns all closed block times in order of when the block was opened
        """
        
        blocks = []
        for block in self.dutyflight_set\
                         .filter(airborne_end__isnull=False)\
                         .order_by('block_start'):
                         
            if block.airborne_finished():
                blocks.append(block)
        
        return blocks
    
    def latest_open_block(self):
        try:
            df = self.dutyflight_set.order_by('-block_start')[0]
        except IndexError:
            return None
        
        if df.block_finished():
            return None
        else:
            return df
    
    
    
    
       
    def total_block(self):
        """
        Total of all closed blocks, in decimal hours
        """
        cb = self.closed_blocks()
        
        total_time = 0
        for block in cb:
            total_time += block.total_block_hours()
        
        return total_time
    
    def total_airborne(self):
        """
        Total of all closed blocks, in decimal hours
        """
        cb = self.closed_airborns()
        
        total_time = 0
        for block in cb:
            total_time += block.total_airborne_hours()
        
        return total_time
            
    
#------------------------------------------------------------------------------

class DutyFlight(models.Model):
    block_start = models.DateTimeField()
    airborne_start = models.DateTimeField(null=True, blank=True)
    airborne_end = models.DateTimeField(null=True, blank=True)
    block_end = models.DateTimeField(null=True, blank=True)
    
    
    duty = models.ForeignKey(Duty)
    
    #####################################
    
    def is_valid(self):
        """
        Checks to see that all datetimes fall in the correct order
        """
        if self.airborne_start:
            a = self.block_start < self.airborne_start
            
        if self.airborne_end:
            a = self.block_start < self.airborne_start < self.airborne_end
        
        if self.block_end:
            a = self.block_start < self.airborne_start < self.airborne_end < self.block_end
            
        # block must start after the duty begins
        b = self.duty.start < self.block_start
        
        # the block has to end before the duty ends
        # (ignore is check if the duty has not yet ended)
        if not self.duty.on_duty():
            c = self.block_end < self.duty.end
        else:
            c = True
            
        return a and b and c
        
    is_valid.boolean = True
    
    def airborne_finished(self):
        """
        Has the plane landed yet?
        """
        
        return self.airborn_start and self.airborne_end
    
    def block_finished(self):
        """
        Has the block time closed yet?
        """
        
        return self.block_start and self.block_end
    
    def airborne_time(self):
        """
        The length of the airborn portion
        """

        if self.airborne_start and self.airborne_end:
            return self.airborne_end - self.airborne_start
        else:
            return ""
        
    def block_time(self):
        """
        The length of the block as a datetime.timedelta
        """

        if self.block_start and self.block_end:
            return self.block_end - self.block_start
        else:
            return ""
    
    def block_time_hours(self):
        """
        The length of the block in decimal hours
        """

        td = self.block_time()
        
        return (td.seconds / 60.0) / 60.0

    def airborne_time_hours(self):
        """
        The length of the airborne portion in decimal hours
        """

        td = self.airborne_time()
        
        return (td.seconds / 60.0) / 60.0

    def pointer(self):
        if not self.block_start:
            return "start_block"
        
        if not self.airborne_start:
            return "start_airborne"
            
        if not self.airborne_end:
            return "end_airborne"
            
        if not self.block_end:
            return "end_block"



        
