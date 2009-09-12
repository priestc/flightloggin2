from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('django.contrib.auth',
    url(r'^logout/$','views.logout', {"next_page": "/"}, name="logout"),
)

urlpatterns += patterns('',
    (r'^site-media/(?P<path>.*)$','django.views.static.serve', {'document_root': '/home/chris/Websites/flightloggin/media', 'show_indexes': True}),

    
    url(r'^$',                                                     "main.views.news",         name="root"),
    url(r'^news.html$',                                            "main.views.news",         name="news"),
    url(r'^faq.html$',                                             "main.views.faq",          name="faq"),
    url(r'^help.html$',                                            "main.views.help",         name="help"),
    url(r'^preferences.html$',                                     "profile.views.profile",   name="profile"),
    url(r'^manage.html$',                                          "manage.views.manage",     name="manage"),
    url(r'^import.html$',                                          "manage.views.import_s",   name="import"),
    
    ############################ graphs
    
    #(r'^(?P<username>\w+)/histogram-(?P<column>\w+).png$',         "graphs.views.histogram"),

    (r'^(?P<username>\w+)/line/(?P<type>\w+)/(?P<columns>[\w\-]+)/((?P<s>\d{4}.\d{1,2}.\d{1,2})-(?P<e>\d{4}.\d{1,2}.\d{1,2}))?(all)?.(?P<ext>(png|svg))$',
    # username/line/type/columns/(start_date-end_date) or (all).extension
    
                                                                   "graphs.views.line_generator"),
    
    ############################ maps
    
    
    url(r'^(?P<username>\w+)/routes-(?P<type>\w+).kmz$',              "maps.views.routes_kml",       name="kml-route"),
    
    url(r'^(?P<username>\w+)/airports-(?P<type>\w+).kmz$',            "maps.views.airports_kml",     name="kml-airport"),
    
    
    url(r'^(?P<username>\w+)/records.html$',                       "records.views.records",   name="records"),
    url(r'^(?P<username>\w+)/graphs.html$',                        "graphs.views.graphs",     name="graphs"),
    url(r'^(?P<username>\w+)/planes.html$',                        "plane.views.planes",      name="planes"),
    url(r'^(?P<username>\w+)/maps.html$',                          "maps.views.maps",         name="maps"),
    url(r'^(?P<username>\w+)/currency.html$',                      "currency.views.currency", name="currency"),
    
    url(r'^(?P<username>\w+)/backup/$',                            "logbook.views.backup",     name="backup"),
    url(r'^massentry.html$',                                       "logbook.views.mass_entry", name="mass-entry"),
    url(r'^massedit-page-(?P<page>\d+).html$',                     "logbook.views.mass_edit",  name="mass-edit"),
    
    (r'^admin/doc/',                                               include('django.contrib.admindocs.urls')),
    (r'^admin/',                                                   include(admin.site.urls)),
    (r'^openid/',                                                  include('django_openid_auth.urls')),    
    

    url(r'^(?P<username>\w+)/logbook.html$',                       "logbook.views.logbook",    name="logbook"),
    url(r'^(?P<username>\w+)/logbook-page-(?P<page>\d+).html',     "logbook.views.logbook",    name="logbook-page"),
    
    (r'^(?P<username>\w+)/$',                                      "django.views.generic.simple.redirect_to", {'url': 'logbook.html'}   ),
)


