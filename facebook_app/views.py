from annoying.decorators import render_to
import facebook.djangofb as facebook

from django.db.models import Sum

from profile.models import Profile
from django.contrib.auth.models import User
from logbook.models import Flight

@facebook.require_login()
@render_to('facebook_app/canvas.fbml')
def canvas(request):
    uid = request.facebook.uid

    username = request.POST.get('username', None)
    secret_key = request.POST.get('secret_key', None)

    if username and secret_key:

	p = Profile.goon(user__username=username, secret_key=secret_key)

        if p:
            p.facebook_uid = uid
            p.save()
            message = "You are authenticated!"
        else:
            message = "There was an error :("

    return locals()

@facebook.require_login()
@render_to('facebook_app/profile_tab.fbml')
def profile_tab(request):
    uid = request.facebook.uid # 12314662 #
    
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
        
        airport_matches = 9
        
        fb_profiles = Profile.objects.filter(facebook_uid__gte=0)
        
    else:
        return canvas(request)
    
    return locals()

