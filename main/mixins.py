from django.contrib.auth.models import User

class UserMixin(object):
    
    user_field = "user"
    
    def user(self, u):
        
        if isinstance(u, User):
            # if user == 1, filter by all users
            if u.id == 1:
                
                ## in the case of Location and Region, some filtering needs
                ## to be done...
                if "routebase" in self.user_field:
                    return self.filter(routebase__isnull=False)
            
                ## the rest don't need to be filtered at all
                else:
                    return self
            
            
            ## filter by user instance
            kwarg = {self.user_field: u}
        else:
            ## filter by username
            kwarg = {self.user_field + "__username": u}

        return self.filter(**kwarg)
