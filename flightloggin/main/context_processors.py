import random

from django.conf import settings
from flightloggin.style.constants import GOOGLE_ADS, WIKI_ADS
from flightloggin.profile.models import Profile
from django.contrib.sites.models import Site

def old_browser(request):
    ua = request.META.get('HTTP_USER_AGENT', "ff")
    
    if ("MSIE 7.0" in ua) or ("MSIE 6.0" in ua):
        old_browser = True
    else:
        old_browser = False
        
    return {'old_browser': old_browser}

def user_label(request):
    """
    Add a context variable called DEMO that is true if the demo user is being
    displayed
    """
    
    # if requester is not logged in, display_user will not be there
    user = getattr(request, "display_user", "derp")
    
    if getattr(user, "id", 0) == settings.DEMO_USER_ID:
        return {"DEMO": True}
    return {}

def figure_navbar(request):
    """
    Figure out which user the navbar is made for
    also add the shared variable so template cache tags don't freak out when
    the request.shared isn't set
    """
    
    from django.contrib.auth.models import User
    
    if getattr(request, "display_user", False):
        ## viewing an app page, print the navbar for the user whose app
        ## it belongs to
        ret = {"navbar_user": request.display_user}
    
    elif getattr(request, "user", User()).is_authenticated():
        ## the user is logged in, just viewing a common page
        ## print the navbar for their app
        ret = {"navbar_user": request.user}
    
    else:
        ## user is not logged in and viewing a common page
        ret = {"navbar_user": User(username="demo")}
        
    ret.update({"shared": getattr(request, "shared", False)})

    return ret

def site_url(request):
    gmk = settings.GOOGLE_MAPS_KEY
    url = Site.objects.get_current()
    return {"SITE_URL": url, "GOOGLE_MAPS_KEY": gmk}

def proper_ad(request):
    
    u = getattr(request, "display_user", None) or request.user
    style = Profile.get_for_user(u).style
    
    if True: #random.choice([True] * 20 + [False]):
        ad_text = GOOGLE_ADS[style]
    else:
        ad_text = WIKI_ADS[style]
    
    #######
    
    import os
    CSS_URL = os.path.join(settings.MEDIA_URL, "css", "style-%s" % style)
    
    return {"proper_ad": ad_text, 'CSS_URL': CSS_URL}
