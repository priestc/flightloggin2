from django.conf.urls.defaults import *

urlpatterns = patterns('facebook_app.views',
    (
        r'canvas/$',
        'canvas',
    ),

    (
        r'profile-tab/?',
        'profile_tab',
    ),
)
