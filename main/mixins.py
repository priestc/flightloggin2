from django.contrib.auth.models import User
from django.conf import settings

class UserMixin(object):

    # the field where the user is linked to, this may be overwritten
    # by the classes that use this mixin
    user_field = "user"
    
    ## the join path to the routebase table. This table needs to be filtered
    ## even with the ALL user.
    routebase_join = None 
    
    def user(self, u):
        
        #------------- filter by everyone ------------------#
        
        if (u == 'ALL' or
            u == 1 or
            getattr(u, "id", 0) == 1 or
            u is None):
               
            ## in the case of Location and Region, some filtering needs
            ## to be done...
            if self.routebase_join:
                kwarg = {"%s__isnull" % self.routebase_join: False}
                return self.filter(**kwarg) ## distinct also should be added...
            
            # don't filter anything for the 'ALL' user,
            # except for the demo user
            return self.exclude(user__id=settings.DEMO_USER_ID)
        
        #------------- filter by user ----------------------#
        
        if isinstance(u, User):
            ## filter by user instance
            kwarg = {self.user_field: u}
            
        elif isinstance(u, int):
            ## filter by user id
            kwarg = {self.user_field + "__pk": u}  
            
        elif isinstance(u, str):
            ## filter by username
            kwarg = {self.user_field + "__username": u}

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
