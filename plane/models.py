from django.db import models
from django.contrib.auth.models import User

from annoying.functions import get_object_or_None
from tagging.fields import TagField
import tagging
from tagging.models import Tag

from constants import *

class QuerySetManager(models.Manager):
    def get_query_set(self):
        return self.model.QuerySet(self.model)
    
    def __getattr__(self, name):
        return getattr(self.get_query_set(), name)

class Plane(models.Model):
    
    from utils import QuerySet          ## add custom filters to custom manager
    
    objects =  QuerySetManager()        ## add custom filterset manager

    tailnumber =     models.CharField(                          max_length=32, help_text="e.g. N12345")
    user =           models.ForeignKey(                         User, blank=True, null=True)

    type =           models.CharField(    "Type Designator",    max_length=32, blank=True, help_text="e.g. C-152, BE-76")
    model =          models.CharField(    "Model Name",         max_length=32, blank=True, help_text="e.g. Skyhawk, Duchess")
    manufacturer =   models.CharField(                          max_length=32, blank=True, help_text="e.g. Cessna, Boeing")
    cat_class =      models.IntegerField( "Category/Class",     choices=CATEGORY_CLASSES, null=False, default=0)
    description =    models.TextField(                          blank=True)

    tags =           TagField()

    def __unicode__(self):
        if self.type:
            disp = " (" + self.type + ")"
        elif self.model:
            disp = " (" + self.model + ")"
        elif self.manufacturer:
            disp = " (" + self.manufacturer + ")"
        else:
            disp = ""
            
        return u"%s%s" % (self.tailnumber, disp)
    
    def fancy_name(self):
        ret = []
        if self.manufacturer:
            ret.append(self.manufacturer)
            
        if self.model:
            ret.append(self.model)
            
        elif self.type:
            ret.append(self.type)
            
        return " ".join(ret)
    
    def get_tags(self):
        return Tag.objects.get_for_object(self)
        
    def get_tags_quote(self):
        tags =  Tag.objects.get_for_object(self)
        ret = []
        
        for tag in tags:
            if tag.name.find(' ') > 0:
                tag = "\"" + tag.name + "\""
            ret.append(str(tag))
        return ret

    class Meta:
        ordering = ["manufacturer"]

    def is_turbine(self):
        return get_object_or_None(Plane, pk=self.pk, tags__icontains="turbine") == self

    def is_hp(self):
        return get_object_or_None(Plane, pk=self.pk, tags__icontains="high performance") == self
 
    def is_type_rating(self):
        return get_object_or_None(Plane, pk=self.pk, tags__icontains="type rating") == self
        
    def is_complex(self):
        return get_object_or_None(Plane, pk=self.pk, tags__icontains="complex") == self
    
    def is_jet(self):
        return get_object_or_None(Plane, pk=self.pk, tags__icontains="jet") == self
    
    def is_tail(self):
        return get_object_or_None(Plane, pk=self.pk, tags__icontains="tailwheel") == self

    #############################

    def is_multi(self):
        return self.cat_class in [2,4]

    def is_sea(self):
        return self.cat_class in [3,4]

    def is_mes(self):
        return self.cat_class == 4
    
    def is_sim(self):
        return self.cat_class >= 15

#tagging.register(Plane)
