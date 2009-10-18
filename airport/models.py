from django.contrib.gis.db import models

from constants import LOCATION_TYPE, LOCATION_CLASS
from django.contrib.auth.models import User


class Location(models.Model):
    """
    >>> from django.contrib.auth.models import User
    >>> u = User(pk=1)
    >>> c = Location(name="test", user=u, loc_type=3, location='POINT (-84.481517 34.322631)')
    >>> c.save()
    >>> c.region.name
    u'Georgia'    
    
    """
    
    loc_class = models.IntegerField(choices=LOCATION_CLASS,
                                         default=0, blank=True, null=True)
                                         
    user = models.ForeignKey(User, null=True)
    identifier = models.CharField(max_length=8)
    country = models.ForeignKey("Country", null=True, blank=True)
    region = models.ForeignKey("Region", null=True, blank=True)
    
    loc_type = models.IntegerField(choices=LOCATION_TYPE, default=0)

    name = models.CharField(max_length=96, blank=True)
    municipality = models.CharField(max_length=60, blank=True)
    elevation = models.IntegerField(null=True, blank=True)
    
    location = models.PointField(null=True, blank=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return u"%s" % self.identifier
    
    @classmethod
    def goon(cls, *args, **kwargs):
        from annoying.functions import get_object_or_None
        return get_object_or_None(cls,  *args, **kwargs)
        
    def region_name(self):
        if self.region:
            return self.region.name
        return "(unassigned)" # will be filtered away with other methods
        
    def country_name(self):
        if self.country:
            return self.country.name
        return "(unassigned)"

    def display_name(self):
        """Forward facing __unicode__, used in KML and similiar"""
        return "%s - %s" % (self.identifier, self.name)
        
    def line_display(self):
        "What gets put on the line on the route column"
        return self.identifier
        
    def title_display(self):
        "What gets put in the tooltip on the route column"
        return self.location_summary()
    
    def location_summary(self):
        """A friendly named location
           EX: 'Newark, Ohio', 'Lilongwe, Malawi'. 
        """
          
        ret = []
        for item in (self.municipality, self.region_name(), self.country_name(), ):
            if item and item != "United States" and item != "(unassigned)":
                ret.append(item)

        return ", ".join(ret)
    
    def save(self, *args, **kwargs):
        """ if it's a custom, automatically look up to see which country and
        or state the custom location falls into"""
        
        ## just save if it's not a custom point
        if self.loc_class == 1:
            return super(Location,self).save()
        
        if self.location:
            # automatically find which country the coordinates fall into
            loc = self.location.wkt
            
            country = getattr(
              WorldBorders.goon(mpoly__contains=loc), 'iso2',''
            )
                
            self.country = Country(code=country) # code = pk
            
            if country=='US':
                state = None
                # in the US, now find the state
                try:
                    state = getattr(
                        USStates.objects.get(mpoly__contains=loc), 'state',''
                    )
                except USStates.DoesNotExist:
                    print "NO STATE: %s" % self.identifier
                    
                if state:   
                    region = "US-%s" % state.upper() #FIXME
                    self.region = Region.objects.get(code=region)
        try:
            getattr(self, "user", None).username
        except:
            #user is not set, we now must get the current logged in user
            from share.middleware import share
            self.user = share.get_display_user()
        super(Location,self).save()
    
###############################################################################
    
class Region(models.Model):
    code = models.CharField(max_length=48)
    country = models.CharField(max_length=2)
    name = models.CharField(max_length=60)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('name', )
        
    @classmethod
    def goon(cls, *args, **kwargs):
        from annoying.functions import get_object_or_None
        return get_object_or_None(cls,  *args, **kwargs) 

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
    
    @classmethod
    def goon(cls, *args, **kwargs):
        from annoying.functions import get_object_or_None
        return get_object_or_None(cls,  *args, **kwargs)

##############################################################################

class USStates(models.Model):
    state = models.CharField(max_length=5)
    name = models.CharField(max_length=24)
    lon = models.FloatField()
    lat = models.FloatField()
    mpoly = models.MultiPolygonField(srid=4269)
    objects = models.GeoManager()
    
    class Meta:
        verbose_name_plural = "US State Borders"
        ordering = ('name', )
    
    def __unicode__(self):
        return self.name
































