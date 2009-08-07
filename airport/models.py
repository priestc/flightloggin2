from django.contrib.gis.db import models
from constants import AIRPORT_TYPE

class Airport(models.Model):
    identifier      =       models.CharField(max_length=8, primary_key=True)

    name            =       models.CharField(max_length=96)
    municipality    =       models.CharField(max_length=60)
    country         =       models.ForeignKey("Country")
    region          =       models.ForeignKey("Region")
    type            =       models.IntegerField(choices=AIRPORT_TYPE)

    elevation       =       models.IntegerField(null=True)
    location        =       models.PointField()

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

class Region(models.Model):
    code = models.CharField(max_length=48)
    country = models.CharField(max_length=2)
    name = models.CharField(max_length=60)

class Country(models.Model):
    name = models.CharField(max_length=48)
    code = models.CharField(max_length=2, primary_key=True)
    continent = models.CharField(max_length=2)
