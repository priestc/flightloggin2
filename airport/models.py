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
        
##############################################################################

class Navaid(Location):
    type = models.IntegerField(choices=NAVAID_TYPE, null=True, blank=True)
    
    def location_summary(self):
        return u"%s - %s" % (self.name, self.get_type_display() )
    
##############################################################################
        
class Custom(Location):
    user = models.ForeignKey(User)
    type = models.IntegerField(choices=AIRPORT_TYPE, null=True, blank=True)
    description = models.TextField(blank=True)
    
    def location_summary(self):
        if self.name:
            return self.name
        return "Custom"
    
    def save(self, *args, **kwargs):
        
        if self.location:
            # automatically find which country the coordinates fall into
            loc = self.location.wkt
            country = WorldBorders.objects.get(mpoly__contains=loc).iso2
            self.country = Country(code=country)
            
            if country=='US' or country=='UM':
                # in the US, now find the state
                state = USStates.objects.get(mpoly__contains=loc).state
                region = "US-%s" % state.upper()
                self.region = Region.objects.get(code=region)
        
        try:
            getattr(self, "user", None)
        except:
            from share.middleware import share
            self.user = share.get_display_user()
        super(Custom,self).save()
        
    class Meta:
        ordering = ('name', )

##############################################################################
        
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
    
    class Meta:
        ordering = ('name', )
    
###############################################################################
    
class Region(models.Model):
    code = models.CharField(max_length=48)
    country = models.CharField(max_length=2)
    name = models.CharField(max_length=60)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('name', )

##############################################################################

class Country(models.Model):
    name = models.CharField(max_length=48)
    code = models.CharField(max_length=2, primary_key=True)
    continent = models.CharField(max_length=2)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Countries"
        ordering = ('name', )
    
##############################################################################    
    
    
class WorldBorders(models.Model):
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    mpoly = models.MultiPolygonField()
    objects = models.GeoManager()

    class Meta:
        verbose_name_plural = "World Borders"
        ordering = ('name', )

    def __unicode__(self):
        return self.name

##############################################################################

class USStates(models.Model):
    state = models.CharField(max_length=2)
    name = models.CharField(max_length=24)
    lon = models.FloatField()
    lat = models.FloatField()
    mpoly = models.MultiPolygonField(srid=4269)
    objects = models.GeoManager()
    
    class Meta:
        verbose_name_plural = "US States"
        ordering = ('name', )
    
    def __unicode__(self):
        return self.name
