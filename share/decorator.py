from settings import SECRET_KEY
from django.http import Http404

class no_share(object):
    """Decorator to determine if the view should be executed based on
       whether the user elects it to be shared. Takes one argument; the
       name of the profile field that determines it's share status
    """

    def determine(self, view, field, request, *args, **kwargs):
        
        print "--- %s" % request.shared
        
        if not getattr(request, 'shared'):
            ## if it's not shared, then do nothing (user is viewing their
            ## own account)
            return view(request, *args, **kwargs)
        
        user = request.display_user
        
        from profile.models import Profile
        profile = Profile.get_for_user(user)
        
        if not field == 'NEVER':
            from django.conf import settings
            if getattr(user, "id", 0) == settings.DEMO_USER_ID:
                ## demo user, let them go hog wild
                return view(request, *args, **kwargs)
                
            go_ahead = getattr(profile, "%s_share" % field)

        
        ## can not view page because the user doesn't want it shared,
        ## either redirect to a page that can be shared, or redirect
        ## to the root page
        if field == 'NEVER' or not go_ahead:
            from django.http import HttpResponseRedirect
            from django.core.urlresolvers import reverse
            
            if getattr(profile, "logbook_share"):
                url = reverse('logbook', kwargs={"username": user.username})
            elif getattr(profile, "other_share"):
                url = reverse('linegraphs', kwargs={"username": user.username})
            else:
                url = "/"
                
            return HttpResponseRedirect(url)
        
        # passes validation, render the view    
        return view(request, *args, **kwargs) 
    
    def __init__(self, field):
        self.field = field
    
    def __call__(self, view):
        def decorator(request, *args, **kwargs):
            return self.determine(view, self.field, request, *args, **kwargs)
        return decorator

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
