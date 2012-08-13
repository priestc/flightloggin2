from django.conf.urls.defaults import *

urlpatterns = patterns('landingpage.views',
    url(r'^$', "landingpage", name="landingpage"),
    url(r'new_login$', 'new_login', name='new_login'),
    url(r'fb_registration_callback', 'fb_registration_callback', name='fb_registration_callback'),
)