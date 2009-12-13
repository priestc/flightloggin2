from django.db.models import Q
#from django.db.models.query import QuerySet
from django.contrib.gis.db.models.query import GeoQuerySet as QuerySet
from django.db.models import Sum
from main.mixins import UserMixin

class LocationQuerySet(QuerySet, UserMixin):
    user_field = 'routebase__route__flight__user'
    
    def user_own(self, user):
        return self.filter(loc_class=3, user=user)
    
class CountryRegionQuerySet(QuerySet, UserMixin):    
    user_field = 'location__routebase__route__flight__user'
