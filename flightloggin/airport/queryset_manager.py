from django.db.models import Q
#from django.db.models.query import QuerySet
from django.contrib.gis.db.models.query import GeoQuerySet as QuerySet
from django.db.models import Sum
from flightloggin.main.mixins import UserMixin

class LocationQuerySet(QuerySet, UserMixin):
    routebase_join = "routebase"
    
    def user_own(self, user):
        """ an additional user queryset methos, but for custom locations owned
        by the user, instead of just locations used by the user
        """
        return self.filter(loc_class=3, user=user)
    
class CountryRegionQuerySet(QuerySet, UserMixin):
    routebase_join = "location__routebase"
