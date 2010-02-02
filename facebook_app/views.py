from annoying.decorators import render_to
import facebook.djangofb as facebook

@render_to('facebook_app/canvas.fbml')
@facebook.require_login()
def canvas(request):
    uid = request.facebook.uid
    return locals()
