class UserMixin(object):
    def user(self, u):
        from django.contrib.auth.models import User
        if isinstance(u, User):
            if u.id == 1:
                # if user == 1, don't filter by user at all
                return self
            return self.filter(user=u,)
        return self.filter(user=User.objects.get(username=u))
