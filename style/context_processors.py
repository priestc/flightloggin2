from django.conf import settings

def css_path(request):
    """ Return the path to the CSS directory based on the display user's
        profile. if no display user, it falls back to request.user
    """
    u = getattr(request, "display_user", None) or request.user

    from profile.models import Profile
    style = Profile.get_for_user(u).style
    
    import os
    CSS_URL = os.path.join(settings.MEDIA_URL, "css", "style-%s" % style)
         
    return {"CSS_URL": CSS_URL}
