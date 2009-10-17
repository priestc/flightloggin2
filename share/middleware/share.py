from annoying.functions import get_object_or_None
from django.contrib.auth.models import User
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

###############################################################

def get_display_user():
    user = getattr(_thread_locals, "display_user", None)
    if not user:
         user,c = User.objects.get_or_create(pk=999999, username="SHARE ERROR - UNKNOWN")
    return user

def get_shared():
    return getattr(_thread_locals, "shared", None)

def get_user():
    return getattr(_thread_locals, "user", None)

###############################################################

class Share(object):
    
    def __init__(self, request, username):
        self.username = username
        self.display_user = get_object_or_None(User, username=username)
        
        if not self.display_user:
            # not a valid username, raise 404
            raise Http404("Username doesn't exist")
        
        self.request = request
        self.useragent = request.META['HTTP_USER_AGENT']
        
    #########################
    
    @property
    def full_access(self):
        return False, self.display_user
    
    @property
    def shared_access(self):
        return True, self.display_user
    
    #########################
    
    @property
    def is_Google_KML(self):
        """is the requester google maps?"""
        return self.useragent == "Kml-Google; (+http://code.google.com/apis/kml)"
    
    @property
    def is_staff(self):
        """is the viewing person a site admin?"""
        return self.request.user.is_staff
    
    @property
    def own_account(self):
        """is the user looking at his/her own account?"""
        return self.display_user == self.request.user
    
    @property
    def can_share(self):
        """Is the display user allowing others to see his/her account?"""
        from profile.models import Profile
        try: 
            return self.display_user.get_profile().share
        except Profile.DoesNotExist:
            # if no profile, then just allow it
            return True  

    #########################

    @property
    def determine(self):
        
        if self.is_Google_KML:
            # Google gets let in no matter what
            return self.full_access
        
        if self.is_staff:
            # requester is a staffer, let them in
            return self.full_access
        
        if self.own_account:
            # requester is owner, let them in
            print "oa"
            return self.full_access
        
        if self.can_share:
            # the owner allows sharing, so grant restricted access
            print "share"
            return self.shared_access
        
        # user does not want others to see his/her logbook, raise 404
        raise PermissionDenied(
            "%s elects to not allow others to see his/her account" % self.username
        )

##############################################################

def cant_share_view(message):
    return HttpResponseForbidden(message)

##############################################################

class ShareMiddleware(object):
    """Middleware that determines if the user
    is vewing his own logbook, or viewing another."""
    
    def process_view(self, request, view, args, kwargs):

        if 'username' in kwargs:
            try:
                share = Share(request, kwargs.pop('username'))
                shared, display_user = share.determine
            except PermissionDenied, message:
                return cant_share_view(message)
            
            _thread_locals.display_user = display_user
            _thread_locals.shared = shared
            _thread_locals.user = getattr(request, "user", None)
            
            return view(request=request,
                        shared=shared,
                        display_user=display_user,
                        *args, **kwargs)









