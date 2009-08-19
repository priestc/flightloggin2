from django.contrib.gis.db import models
from constants import AIRPORT_TYPE, NAVAID_TYPE
from django.contrib.auth.models import User

class Navaid(models.Model):
    identifier      =       models.CharField(max_length=8)
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
        return "not yet implemented"
        
    def title_display(self):
        return self.name + " " + self.get_type_display()
        
    def line_display(self):
        return self.identifier

class Airport(models.Model):
    identifier      =       models.CharField(max_length=8, primary_key=True)

    name            =       models.CharField(max_length=96, blank=True)
    municipality    =       models.CharField(max_length=60, blank=True)
    country         =       models.ForeignKey("Country", null=True, blank=True)
    region          =       models.ForeignKey("Region", null=True, blank=True)
    type            =       models.IntegerField(choices=AIRPORT_TYPE)

    elevation       =       models.IntegerField(null=True)
    location        =       models.PointField()
    
    objects         =       models.GeoManager()

    class Meta:
        ordering = ["identifier", "country"]
        verbose_name_plural = "Airports"

    def __unicode__(self):
        return u"%s - %s" % (self.identifier, self.location_summary())

    def display_name(self):
        return " - ".join([self.identifier, self.name])

    def location_summary(self):
        ret = []

        for item in (self.municipality, self.region.name, self.country.name, ):
            if item and item != "United States" and item != "(unassigned)":
                ret.append(item)

        return ", ".join(ret)
        
    def line_display(self):
        return self.identifier
        
    def title_display(self):
        return self.location_summary()
        
class Custom(Airport):
    user = models.ForeignKey(User, blank=True, null=True)
    
class Region(models.Model):
    code = models.CharField(max_length=48)
    country = models.CharField(max_length=2)
    name = models.CharField(max_length=60)
    
    def __unicode__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=48)
    code = models.CharField(max_length=2, primary_key=True)
    continent = models.CharField(max_length=2)
    
    def __unicode__(self):
        return self.name
