from django.http import HttpResponse
from django.views.generic.simple import direct_to_template

import facebook.djangofb as facebook

@facebook.require_login()
def canvas(request):
    return direct_to_template(request,
                              'facebook_app/canvas.fbml',
                              extra_context={'uid': request.facebook.uid})

