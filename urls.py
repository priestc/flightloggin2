from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^site-media/(?P<path>.*)$','django.views.static.serve', {'document_root': '/home/chris/Websites/flightloggin/media', 'show_indexes': True}),


    url(r'^$',                                "main.views.news",        name="root"),
    url(r'^news/$',                           "main.views.news",        name="news"),
    url(r'^faq/$',                            "main.views.faq",         name="faq"),
    url(r'^help/$',                           "main.views.help",        name="help"),
    url(r'^preferences/$',                    "profile.views.profile",  name="profile"),
    url(r'^records/$',                        "records.views.records",  name="records"),
    url(r'^stats/$',                          "stats.views.stats",      name="stats"),
    url(r'^planes/$',                         "plane.views.planes",     name="planes"),
    url(r'^import/$',                         "import.views.import_s",  name="import"),
    url(r'^backup/$',                         "logbook.views.backup",   name="backup"),
    
    url(r'^mass_entry/$',                     "logbook.views.mass_entry",name="mass_entry"),
    url(r'^logbook/$',                        "logbook.views.logbook",  name="logbook"),
    url(r'^logbook-page-(?P<page>\d+)',       "logbook.views.logbook",  name="logbook-page"),
    

    (r'^admin/doc/',                          include('django.contrib.admindocs.urls')),
    (r'^admin/',                              include(admin.site.urls)),
    (r'^openid/',                             include('django_openid_auth.urls')),

)

urlpatterns += patterns('django.contrib.auth',
    url(r'^logout/$','views.logout', {"template_name": "home.html"}, name="logout"),
)
