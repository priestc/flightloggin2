from django.contrib.gis.db import models
from constants import AIRPORT_TYPE, NAVAID_TYPE
from django.contrib.auth.models import User

class Location(models.Model):
    identifier      =       models.CharField(max_length=8)

    name            =       models.CharField(max_length=96, blank=True)
    municipality    =       models.CharField(max_length=60, blank=True)
    country         =       models.ForeignKey("Country", null=True, blank=True)
    region          =       models.ForeignKey("Region", null=True, blank=True)

    elevation       =       models.IntegerField(null=True, blank=True)
    location        =       models.PointField(null=True, blank=True)
    
    objects         =       models.GeoManager()

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"%s" % self.identifier
        
    def region_name(self):
        if self.region:
            return self.region.name
        return "(unassigned)"
        
    def country_name(self):
        if self.country:
            return self.country.name
        return "(unassigned)"

   # def display_name(self):
   #     """Forward facing __unicode__, used in KML and similiar"""
   #     return "%s - %s" % (self.identifier, self.name)
        
    def line_display(self):
        "What gets put on the line on the route column"
        return self.identifier
        
    def title_display(self):
        "What gets put in the tooltip on the route column"
        return self.location_summary()
        

#####################################################################
#####################################################################


class Navaid(Location):
    type = models.IntegerField(choices=NAVAID_TYPE, null=True, blank=True)
    
    def location_summary(self):
        return u"%s - %s" % (self.name, self.get_type_display() )
        
class Custom(Location):
    user = models.ForeignKey(User)
    type = models.IntegerField(choices=AIRPORT_TYPE, null=True, blank=True)
    description = models.TextField(blank=True)
    
    def location_summary(self):
        if self.name:
            return self.name
        return "Custom"
    
    def save(self, *args, **kwargs):
        
        try:
            getattr(self, "user", None)
        except:
            from share.middleware import share
            self.user = share.get_display_user()
        super(Custom,self).save()
        
class Airport(Location):
    type = models.IntegerField(choices=AIRPORT_TYPE, null=True, blank=True)
    
    def location_summary(self):
        """A friendly named location
           EX: 'Newark, Ohio', 'Lilongwe, Malawi'. 
        """
          
        ret = []
        for item in (self.municipality, self.region_name(), self.country_name(), ):
            if item and item != "United States" and item != "(unassigned)":
                ret.append(item)

        return ", ".join(ret)
    
#####################################################################
    
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
