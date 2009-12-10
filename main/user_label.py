from django.conf import settings

def user_label(request):
    """ added a context variable called DEMO that is true if the demo is being
        displayed
    """
    
    # if requester is not logged in, display_user will not be there
    user = getattr(request, "display_user", "derp")
    
    if getattr(user, "id", 0) == settings.DEMO_USER_ID:
        return {"DEMO": True}
    return {}
