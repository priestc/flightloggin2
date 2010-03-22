import re

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.safestring import mark_safe

from tagging.fields import TagField
import tagging
from tagging.models import Tag

from main.mixins import GoonMixin
from constants import *

from utils import PlaneQuerySet
from main.enhanced_model import QuerySetManager, EnhancedModel

class Plane(EnhancedModel):

    objects =        QuerySetManager(PlaneQuerySet)

    tailnumber =     models.CharField(                        max_length=32, help_text="e.g. N12345")
    user =           models.ForeignKey(                       User, blank=True, null=True)

    type =           models.CharField(    "Type Designator",  max_length=32, blank=True, help_text="e.g. C-152, BE-76")
    model =          models.CharField(    "Model Name",       max_length=32, blank=True, help_text="e.g. Skyhawk, Duchess")
    manufacturer =   models.CharField(                        max_length=32, blank=True, help_text="e.g. Cessna, Boeing")
    cat_class =      models.IntegerField( "Category/Class",   choices=CATEGORY_CLASSES, null=False, default=0)
    description =    models.TextField(                        blank=True)
    hidden =         models.BooleanField(default=False)
    retired =        models.BooleanField(default=False)
    tags =           TagField()
    
    #regex that matches all tailnumbers and types
    plane_regex = r'[A-Za-z0-9-\[\]\)\(}{\.]'
    
    @classmethod
    def reverse_plane_regex(cls):
        return '[^' + cls.plane_regex[1:]
    
    @classmethod
    def currency_types(cls, user):
        """
        Returns all types in the user's logbook that are tagged as being fair
        game for the type currency section
        """
        
        curr_q = (models.Q(tags__icontains='tr') |
                  models.Q(tags__icontains='type rating') |
                  models.Q(tags__icontains='currency'))
        
        return tuple(cls.objects.user(user)\
                                .filter(curr_q)\
                                .values_list('type', flat=True)\
                                .order_by()\
                                .distinct())
        
    
    def save(self, *args, **kwargs):
        """
        Automatically fill in make/models if they are not already supplied
        and then save the object to the database
        """
        if (not self.manufacturer and
            not self.model and
            not self.cat_class) and self.type:
                
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
                
        self.clean_type()
        self.clean_tailnumber()
                
        if not self.user:
            from share.middleware import share
            self.user = share.get_display_user()
        
        super(Plane, self).save(*args, **kwargs)
    
    @classmethod    
    def get_users_tailnumber(cls, tailnumber):
        """Returns the users who also have flown in this tailnumber"""
        
        from django.contrib.auth.models import User
        return User.objects\
                   .filter(profile__social=True)\
                   .filter(plane__tailnumber=tailnumber).distinct()
                   
    @classmethod
    def get_profiles(cls, **kwarg):
        """
        Returns the profiles of the users who have flown in this
        type/tail/whatever. Takes one kwarg; model='blah', type='blah'
        """
        
        field = kwarg.keys()[0]
        val = kwarg.values()[0]
        
        kwarg = {"user__flight__plane__%s__iexact" % field: val}
        
        from profile.models import Profile
        return Profile.objects\
                   .filter(**kwarg)\
                   .filter(social=True)\
                   .values('user__username', 'user__id', 'logbook_share')\
                   .order_by('user__username')\
                   .distinct()
    
    @classmethod
    def regex_tail_type(cls, s):        
        return re.sub(cls.reverse_plane_regex(), '', s or "")
    
    def hidden_tag(self):
        if self.hidden:
            return mark_safe("<span class='remarks_tag'>[Hidden]</span>")
        else:
            return ""

    def retired_tag(self):
        if self.retired:
            return mark_safe("<span class='remarks_tag'>[Retired]</span>")
        else:
            return ""
                   
    def clean_tailnumber(self):
        """
        remove special characters and white space because they mess up
        the url resolvers
        !!replace with model validators when django 1.2 drops!!
        """
        self.tailnumber = Plane.regex_tail_type(self.tailnumber)
        
    def clean_type(self):
        """
        remove special characters and white space because they mess up
        the url resolvers
        !!replace with model validators when django 1.2 drops!!
        """
        self.type = Plane.regex_tail_type(self.type)
        

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
        """ Is this plane a sim, ftd or pcatd? (cat_class greater than 15) """
        return self.cat_class >= 15

#tagging.register(Plane)
