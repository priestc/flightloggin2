from annoying.functions import get_object_or_None
from django.contrib.auth.models import User
from django.http import Http404

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
