from annoying.decorators import render_to
import facebook.djangofb as facebook

from django.db.models import Sum

from profile.models import Profile
from django.contrib.auth.models import User
from logbook.models import Flight

@facebook.require_login()
@render_to('register.fbml')
def register(request):

    uid = request.facebook.uid
   
    if not request.facebook.added:
        message = "please add this app to register"
        return locals()
    
    username = request.POST.get('username', None)
    secret_key = request.POST.get('secret_key', None)

    if username and secret_key:
        p = Profile.goon(user__username=username, secret_key=secret_key)

        if p:
            p.facebook_uid = uid
            p.save()
            return profile_tab(request, registered=True)
        
        else:
            message = "There was an error :("

    return locals()

@facebook.require_login()
@render_to('profile_tab.fbml')
def profile_tab(request, registered=False):
    """
    Render the profile tab page. This is the main page for this app.
    If the user is not authenticated, it will redirect to the register
    view where the sign-up form is rendered.
    """
    
    if request.POST.get('username', None) and not registered:
        return register(request)
    
    ## uid == the uid of the person's profile, not the person
    ## viewing the app page
    uid = request.facebook.uid
    
    try:
        user = User.objects.get(profile__facebook_uid=uid)
    except User.DoesNotExist:
        user = None

    if user:
        tt = Flight.objects\
                   .user(user)\
                   .sim(False)\
                   .aggregate(s=Sum('total'))['s']
        
        last_flights = list(Flight.objects.user(user).order_by('-date')[:5])
        last_flights.reverse()
        
    else:
        return register(request)
    
    return locals()

@facebook.require_login()
@render_to('canvas.fbml')
def canvas(request):
    
    if request.POST.get('username', None):
        return register(request)
    
    users = User.objects.count()
    fb_users = Profile.objects.exclude(facebook_uid="").count()
    
    return locals()
