from annoying.functions import get_object_or_None
from django.contrib.auth.models import User
from django.http import Http404

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

###############################################################

def get_display_user():
    return getattr(_thread_locals, "display_user", None)

def get_shared():
    return getattr(_thread_locals, "shared", None)

def get_user():
    return getattr(_thread_locals, "user", None)

###############################################################

def is_shared(request, username):
    if request.user.is_authenticated():
        if username == request.user.username:
            return False, request.user             #viewing own logbook (passed username is the authenticated user)
        else:
            shared = True                          #viewing a shared logbook (user is logged into his own account)
    else:
        shared = True                              #viewing a shared logbook (user is not logged in at all)
        
    if shared:
        user=get_object_or_None(User, username=username)
    else:
        user=request.user
    
    try:
        ok_to_share = user.get_profile().share
    except:
        ok_to_share = True
      
    if not user or ( not ok_to_share and shared ):
        raise Http404
        
    return shared, user

##############################################################

class ShareMiddleware(object):
    """Middleware that determines if the user
    is vewing his own logbook, or viewing another."""
    
    def process_view(self, request, view, args, kwargs):

        if 'username' in kwargs:
            shared, display_user = is_shared(request, kwargs.pop('username'))
            
            _thread_locals.display_user = display_user
            _thread_locals.shared = shared
            _thread_locals.user = getattr(request, "user", None)
            
            return view(request, shared, display_user, *args, **kwargs)









