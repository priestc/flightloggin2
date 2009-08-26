from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^site-media/(?P<path>.*)$','django.views.static.serve', {'document_root': '/home/chris/Websites/flightloggin/media', 'show_indexes': True}),


    url(r'^$',                                   "main.views.news",        name="root"),
    url(r'^news.html$',                          "main.views.news",        name="news"),
    url(r'^faq,html$',                           "main.views.faq",         name="faq"),
    url(r'^help.html$',                          "main.views.help",        name="help"),
    url(r'^preferences.html$',                   "profile.views.profile",  name="profile"),
    url(r'^records.html$',                       "records.views.records",  name="records"),
    url(r'^stats.html$',                         "stats.views.stats",      name="stats"),
    url(r'^planes.html$',                        "plane.views.planes",     name="planes"),
    url(r'^import.html$',                        "import.views.import_s",  name="import"),
    url(r'^backup.tsv$',                         "logbook.views.backup",   name="backup"),
    
    url(r'^(?P<username>\w+)/mass_entry.html$',                    "logbook.views.mass_entry", name="mass_entry"),
    url(r'^(?P<username>\w+)/logbook.html$',                       "logbook.views.logbook",    name="logbook"),
    url(r'^(?P<username>\w+)/logbook-page-(?P<page>\d+).html',     "logbook.views.logbook",    name="logbook-page"),
    

    (r'^admin/doc/',                          include('django.contrib.admindocs.urls')),
    (r'^admin/',                              include(admin.site.urls)),
    (r'^openid/',                             include('django_openid_auth.urls')),

)

urlpatterns += patterns('django.contrib.auth',
    url(r'^logout/$','views.logout', {"template_name": "/"}, name="logout"),
)
