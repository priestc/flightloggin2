import datetime

from django.contrib.auth.models import User
from django.conf import settings

class UserMixin(object):
    """
    Adds a user() method to the queryset object. Takes either a user instance,
    or a username string.
    """
    
    def user(self, u, disable_future=False):
        
        class_name = self.__class__.__name__
        alt_name = getattr(self, "qs_name", None)
        
        user_field = "user"
        routebase_join = None
        
        if class_name == "PlaneQuerySet":
            flight_date_field = "flight__date"
        
        elif class_name == "RouteQuerySet":
            flight_date_field = "flight__date"
            routebase_join = "routebase"
            user_field = "flight__user"
            
        elif class_name == "FlightQuerySet":
            flight_date_field = "date"
            #routebase_join = "route__routebase"
            
        elif class_name == "LocationQuerySet":
            user_field = "routebase__route__flight__user"
            
        elif class_name == "CountryRegionQuerySet":
            user_field = "location__routebase__route__flight__user"
            routebase_join = "location__routebase"
            
        #------------- filter by everyone ------------------#
        
        if (u == 'ALL' or
            u == 1 or
            getattr(u, "id", 0) == 1 or
            u is None):
               
            ## in the case of Location and Region, some filtering needs
            ## to be done...
            if routebase_join:
                kwarg = {"%s__isnull" % routebase_join: False}
                return self.filter(**kwarg)
            
            # don't filter anything for the 'ALL' user,
            # except exclude the demo user
            kwarg = {user_field + "__id": settings.DEMO_USER_ID}
            ret = self.exclude(**kwarg)
            
            if disable_future:
                # exclude flights that are logged in the future
                # mainly used for the ALL logbook view page
                kwarg = {flight_date_field + "__gt": datetime.date.today()}
                ret = ret.exclude(**kwarg)            
            
            return ret
        
        #------------- filter by user ----------------------#
        
        if isinstance(u, User):
            ## filter by user instance
            kwarg = {user_field: u}
            
        elif isinstance(u, int):
            ## filter by user id
            kwarg = {user_field + "__pk": u}  
            
        elif isinstance(u, str):
            ## filter by username
            kwarg = {user_field + "__username": u}

        return self.filter(**kwarg)

###############################################################################

from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404

class GoonMixin(object):
    @classmethod
    def goon(cls, *args, **kwargs):
        return get_object_or_None(cls, *args, **kwargs)
    
    @classmethod
    def goof(cls, *args, **kwargs):
        return get_object_or_404(cls, *args, **kwargs)
    
###############################################################################
    
class NothingHereMixin(object):
    @property
    def NothingHereGraph(self):
        from matplotlib.figure import Figure
        fig = Figure()
        fig.text(.5,.5,"Nothing to Show",fontsize=18,ha='center')
        return fig
