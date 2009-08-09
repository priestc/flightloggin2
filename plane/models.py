from django.db import models
from django.contrib.auth.models import User

from tagging.fields import TagField
import tagging

from constants import *

class Plane(models.Model):

    tailnumber =     models.CharField(                          max_length=32)
    user =           models.ForeignKey(                         User, blank=False)

    type =           models.CharField(    "Type Designator",    max_length=32, blank=True)
    model =          models.CharField(    "Model Name",         max_length=32, blank=True)
    manufacturer =   models.CharField(                          max_length=32, blank=True)
    cat_class =      models.IntegerField( "Category/Class",     choices=CATEGORY_CLASSES, null=False, default=0)

    tags =           TagField()

    def __unicode__(self):
        return u"%s (%s)" % (self.tailnumber, self.type)

    class Meta:
        ordering = ["manufacturer"]

#tagging.register(Plane)
