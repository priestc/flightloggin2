from settings import SECRET_KEY
from django.http import Http404

class no_share(object):
    """Decorator to determine if the view should be executed based on
       whether the user elects it to be shared. Takes one argument; the
       name of the profile field that determines it's share status
    """

    def determine(self, view, field, request, *args, **kwargs):
        if kwargs.get('shared', True):
            
            if not field == 'NEVER':
                user = kwargs['display_user']
                from profile.models import Profile
                profile = Profile.get_for_user(user)
                go_ahead = getattr(profile, "%s_share" % field)
            
            if field == 'NEVER' or not go_ahead:
                from django.http import Http404
                raise Http404('not availiable for sharing')
            
        return view(request, *args, **kwargs)
    
    def __init__(self, field):
        self.field = field
    
    def __call__(self, view):
        def wrapper(request, *args, **kwargs):
            return self.determine(view, self.field, request, *args, **kwargs)
        return wrapper

class secret_key(object):
    def __init__(self, view):
        self.view = view
    
    def __call__(self, request, *args, **kwargs):
        """Don't let them in unless they have the secret key"""
        
        secret_key = request.GET.get('sk', '')
      
        if not secret_key:
            raise Http404('Need secret key')
        
        elif not secret_key == SECRET_KEY:
            raise Http404('Secret key incorrect')

        return self.view(request, *args, **kwargs)
