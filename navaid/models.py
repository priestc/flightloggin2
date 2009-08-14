from django.contrib.gis.db import models
from constants import NAVAID_TYPE

class Navaid(models.Model):
    identifier      =       models.CharField(max_length=8, primary_key=True)
    name            =       models.CharField(max_length=96)
    municipality    =       models.CharField(max_length=60, blank=True)
    type            =       models.IntegerField(choices=NAVAID_TYPE)
    location        =       models.PointField()
    
    objects         =       models.GeoManager()

    class Meta:
        ordering = ["identifier"]
        verbose_name_plural = "Navaids"

    def __unicode__(self):
        return u"%s - %s" % (self.identifier, self.name)

    def display_name(self):
        return " - ".join([self.identifier, self.name])

    def location_summary(self):
        return "not implemented"
        
    def title_display(self):
        return self.name + " " + self.get_type_display()
        
    def line_display(self):
        return self.identifier
