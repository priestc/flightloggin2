from django.db import models
from signals import *

class NewsItem(models.Model):

    date = models.DateField()
    title = models.CharField(max_length=64)
    text = models.TextField()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["-date"]
        
    @models.permalink
    def get_absolute_url(self):
        return  ('news', [])
    
class HelpItem(models.Model):
    
    title = models.TextField()
    body = models.TextField()
    category = models.CharField(max_length=32, blank=True)
    order = models.SmallIntegerField(default=0)
    
    def __unicode__(self):
        return self.title
