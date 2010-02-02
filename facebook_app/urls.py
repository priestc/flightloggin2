from django.conf.urls.defaults import *

urlpatterns = patterns('facebook_app.views',
    (
        r'canvas/$',
        'canvas',
    ),
)
