from annoying.decorators import render_to
import facebook.djangofb as facebook
from profile.models import Profile

@render_to('facebook_app/canvas.fbml')
@facebook.require_login()
def canvas(request):
    uid = request.facebook.uid

    username = request.POST['username']
    secret_key = request.POST['secret_key']

    p = Profile.goon(user__username=username, secret_key=secret_key)

    if p:
        p.facebook_uid = uid
        p.save()
        message = "You are authenticated!"
    else:
        message = "There was an error :("

    return locals()

@render_to('facebook_app/canvas.fbml')
@facebook.require_login()
def profile_tab(request):
    uid = request.facebook.uid
    return locals()

