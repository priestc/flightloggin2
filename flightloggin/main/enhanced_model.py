from django.contrib.gis.db.models import GeoManager
from django.db.models import Model, Manager

from django.contrib.gis.db.models.query import GeoQuerySet
from django.db.models.query import QuerySet

from mixins import UserMixin, GoonMixin


class ManagerMixin(object):
    def __init__(self, qs_class=None, name=None):
        """
        Passed in should be a class descended from QuerySet. If that qs_class
        attribute is left blank, then a name must be passed in, which the
        default QuerySet class will be renamed to
        """
        
        super(ManagerMixin,self).__init__()
        
        if not qs_class:
            qs_class = self.qs
            
        self.queryset_class = qs_class
        
        if name:
            self.queryset_class.__name__ = name
        
    def get_query_set(self):
        return self.queryset_class(self.model)
    
    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)
                 
###################################################
        
class EnhancedQuerySet(QuerySet, UserMixin):
    pass

class EnhancedGeoQuerySet(GeoQuerySet, UserMixin):
    pass

###################################################

class QuerySetManager(ManagerMixin, Manager):
    qs = EnhancedQuerySet

class GeoQuerySetManager(ManagerMixin, GeoManager):
    qs = EnhancedGeoQuerySet

###################################################
   
class EnhancedModel(Model, GoonMixin):
    class Meta:
        abstract = True
