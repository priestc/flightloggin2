from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^site-media/(?P<path>.*)$','django.views.static.serve', {'document_root': '/home/chris/Websites/flightloggin/media', 'show_indexes': True}),


    url(r'^$',                                "main.views.home",        name="root"),
    url(r'^home/$',                           "main.views.home",        name="home"),
    url(r'^faq/$',                            "main.views.faq",         name="faq"),
    url(r'^walkthrough/$',                    "main.views.walkthrough", name="walkthrough"),
    url(r'^preferences/$',                    "profile.views.profile",  name="profile"),
    url(r'^records/$',                        "records.views.records",  name="records"),
    url(r'^planes/$',                         "plane.views.planes",     name="planes"),
    url(r'^import/$',                         "import.views.import_s",  name="import"),
    
    url(r'^logbook/$',                        "logbook.views.logbook",  name="logbook"),
    url(r'^logbook-page-(?P<page>\d+)',       "logbook.views.logbook",  name="logbook_page"),
    

    (r'^admin/doc/',                          include('django.contrib.admindocs.urls')),
    (r'^admin/',                              include(admin.site.urls)),
    (r'^openid/',                             include('django_openid_auth.urls')),

)

urlpatterns += patterns('django.contrib.auth',
    url(r'^accounts/logout/$','views.logout', {"template_name": "home.html"}, name="logout"),
)
