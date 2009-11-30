from django.contrib.auth.models import User

class UserMixin(object):
    
    user_field = "user"
    
    def user(self, u):
        
        if isinstance(u, User):
            if u.id == 1:
                # if user == 1, don't filter by user at all
                return self
            ## filter by user instance
            kwarg = {self.user_field: u}
        else:
            ## filter by username
            kwarg = {self.user_field + "__username": u}

        return self.filter(**kwarg)
