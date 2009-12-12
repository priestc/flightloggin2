from django.contrib.auth.models import User

class UserMixin(object):

    # the field where the user is linked to, this may be overwritten
    # by the classes that use this mixin
    user_field = "user" 
    
    def user(self, u):
        
        #------------- filter by everyone ------------------#
        
        if (u == 'ALL' or
            u == 1 or
            getattr(u, "id", 0) == 1):
               
            ## in the case of Location and Region, some filtering needs
            ## to be done...
            if "routebase" in self.user_field:
                return self.filter(routebase__isnull=False)
            
            # don't filter anything for the 'ALL' user
            return self
        
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
