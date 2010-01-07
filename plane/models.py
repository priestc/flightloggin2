import re

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

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
    
    ## add custom filters to custom manager
    from utils import PlaneQuerySet as QuerySet
    
    objects =  QuerySetManager()        ## add custom filterset manager

    tailnumber =     models.CharField(                          max_length=32, help_text="e.g. N12345")
    user =           models.ForeignKey(                         User, blank=True, null=True)

    type =           models.CharField(    "Type Designator",    max_length=32, blank=True, help_text="e.g. C-152, BE-76")
    model =          models.CharField(    "Model Name",         max_length=32, blank=True, help_text="e.g. Skyhawk, Duchess")
    manufacturer =   models.CharField(                          max_length=32, blank=True, help_text="e.g. Cessna, Boeing")
    cat_class =      models.IntegerField( "Category/Class",     choices=CATEGORY_CLASSES, null=False, default=0)
    description =    models.TextField(                          blank=True)

    tags =           TagField()
    
    #regex that matches all tailnumbers and types
    plane_regex = r'[A-Za-z0-9-\[\]\)\(}{]'
    
    def save(self, *args, **kwargs):
        """Automatically fill in make/models if they are not already supplied
           and then save the object to the database
        """
        if not (self.manufacturer and
                self.model and
                self.cat_class) and self.type:
                
            from auto_fill import autofill
            d = autofill(self.type)
            
            if d.get('manufacturer', False):
                ## autofill hit a match, use that data
                self.manufacturer = d['manufacturer'] or ""
                self.model = d['model'] or ""
                self.cat_class = d['cat_class'] or 1
                self.tags = d['tags'] or ""
            
            if "frasca" in self.type.lower():
                self.manufacturer="Frasca"
                self.cat_class = 16
                
        if not self.user:
            from share.middleware import share
            self.user = share.get_display_user()
        
        # remove special characters and white space because they mess up
        # the url resolvers
        #XXX replace with model validators when django 1.2 drops
        
        # slip in a carrot to negate the regex
        reg = '[^' + self.plane_regex[1:]
      
        self.type =       re.sub(reg, '', self.type or "")
        self.tailnumber = re.sub(reg, '', self.tailnumber or "")

        super(Plane, self).save(*args, **kwargs)
    
    @classmethod    
    def get_users_tailnumber(cls, tailnumber):
        """Returns the users who also have flown in this tailnumber"""
        
        from django.contrib.auth.models import User
        return User.objects\
                   .filter(profile__social=True)\
                   .filter(plane__tailnumber=tailnumber).distinct()
                   
    @classmethod
    def get_users_type(cls, ty):
        """Returns the users who also have flown in this type"""
        
        from django.contrib.auth.models import User
        return User.objects\
                   .filter(profile__social=True)\
                   .filter(plane__type=ty).distinct()

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
    
    @classmethod
    def goon(cls, *args, **kwargs):
        """get object or None"""
        from annoying.functions import get_object_or_None
        return get_object_or_None(cls,  *args, **kwargs)
    
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
        tags = Tag.objects.get_for_object(self)
        ret = []
        for tag in tags:
            ret.append(tag.name)
        
        return ret
        
    def get_tags_quote(self):
        tags = Tag.objects.get_for_object(self)
        ret = []
        
        for tag in tags:
            if tag.name.find(' ') > 0:
                tag = "\"" + tag.name + "\""
            ret.append(str(tag))
        return ret

    class Meta:
        ordering = ["manufacturer", 'type', 'tailnumber']

    def is_turbine(self):
        return Plane.goon(pk=self.pk, tags__icontains="turbine") == self

    def is_hp(self):
        return Plane.goon(Q(pk=self.pk) & (Q(tags__icontains="high performance") | Q(tags__icontains="hp"))) == self
 
    def is_type_rating(self):
        return Plane.goon(pk=self.pk, tags__icontains="type rating") == self
        
    def is_complex(self):
        return Plane.goon(pk=self.pk, tags__icontains="complex") == self
    
    def is_jet(self):
        return Plane.goon(pk=self.pk, tags__icontains="jet") == self
    
    def is_tail(self):
        return Plane.goon(pk=self.pk, tags__icontains="tailwheel") == self

    #############################

    def is_multi(self):
        return self.cat_class in [2,4]
    
    def is_single(self):
        return self.cat_class in [1,3]

    def is_sea(self):
        return self.cat_class in [3,4]

    def is_mes(self):
        return self.cat_class == 4
    
    def is_sim(self):
        return self.cat_class >= 15

#tagging.register(Plane)
