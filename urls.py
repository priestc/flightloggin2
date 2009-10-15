from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('django.contrib.auth',
    url(r'^logout/$','views.logout', {"next_page": "/"}, name="logout"),
)

from feeds.classes import LatestFlights
feeds = {
    'flights': LatestFlights,
}


## all views get `shared` and `display_user` variables from `username` via ShareMiddleware

urlpatterns += patterns('',
    
    url(r'^$',                                                     "django.views.generic.simple.redirect_to", {'url': 'news.html'}, name="root"),
   
    
    (r'^admin/doc/',                                               include('django.contrib.admindocs.urls')),
    (r'^admin/',                                                   include(admin.site.urls)),
    
    (r'^admin-manage.html$',                                       direct_to_template, {'template': 'manage.html'}),
    (r'^import_instructions.html$',                                direct_to_template, {'template': 'import_instructions.html'}),
    
    ############################ graphs

    (r'^(?P<username>\w+)/line/(?P<type_>\w+)/(?P<columns>[\w\-]+)/((?P<s>\d{4}.\d{1,2}.\d{1,2})-(?P<e>\d{4}.\d{1,2}.\d{1,2}))?(all)?.(?P<ext>(png|svg))$',
    # username/line/type/columns/(start_date-end_date) or (all).extension
    
                        "graphs.views.line_generator"),
                                                                   
    url(r'^(?P<username>\w+)/states-(?P<type_>[\-\w]+)?.(?P<ext>(png|svg))$',
    
                        "maps.states.view", name="state-map"),
                                                                   
    (r'^(?P<username>\w+)/sigs/(?P<columns>[\w\-]+).png',          "sigs.views.make_sig", ),
    
    ############################ main site
    
    (r'^feeds/(?P<url>.*)/$',                                      "django.contrib.syndication.views.feed", {'feed_dict': feeds}),
    
    (r'^easy-recalc-routes.py$',                                   "route.views.easy_recalc_routes"),
    (r'^hard-recalc-routes.py$',                                   "route.views.hard_recalc_routes"),
    (r'^del-routes.py$',                                           "route.views.del_routes"),
    
    url(r'^news.html$',                                            "main.views.news",         name="news"),
    url(r'^faq.html$',                                             "main.views.faq",          name="faq"),
    url(r'^help.html$',                                            "main.views.help",         name="help"),
    
    (r'^openid/',                                                  include('django_openid_auth.urls')),
    
    url(r'^(?P<username>\w+)/email-backup.html$',                  "backup.views.emailbackup", name="import"),
    url(r'^(?P<username>\w+)/routes-(?P<type_>\w+).kmz$',          "maps.views.routes_kml",    name="kml-route"),
    url(r'^(?P<username>\w+)/airports-(?P<type_>\w+).kmz$',        "maps.views.airports_kml",  name="kml-airport"),
    url(r'^(?P<username>\w+)/preferences.html$',                   "profile.views.profile",    name="profile"),
    url(r'^(?P<username>\w+)/import.html$',                        "manage.views.import_s",    name="import"),
    url(r'^(?P<username>\w+)/records.html$',                       "records.views.records",    name="records"),
    url(r'^(?P<username>\w+)/events.html$',                        "records.views.events",     name="events"),
    url(r'^(?P<username>\w+)/graphs.html$',                        "graphs.views.graphs",      name="graphs"),
    url(r'^(?P<username>\w+)/planes.html$',                        "plane.views.planes",       name="planes"),
    url(r'^(?P<username>\w+)/maps.html$',                          "maps.views.maps",          name="maps"),
    url(r'^(?P<username>\w+)/currency.html$',                      "currency.views.currency",  name="currency"),
    url(r'^(?P<username>\w+)/places.html$',                        "records.views.places",     name="places"),
    url(r'^(?P<username>\w+)/backup/$',                            "backup.views.backup",      name="backup"),
    url(r'^(?P<username>\w+)/massentry.html$',                     "logbook.views.mass_entry", name="mass-entry"),
    url(r'^(?P<username>\w+)/massedit-page-(?P<page>\d+).html$',   "logbook.views.mass_edit",  name="mass-edit"),
    url(r'^(?P<username>\w+)/logbook.html$',                       "logbook.views.logbook",    name="logbook"),
    url(r'^(?P<username>\w+)/logbook-page-(?P<page>\d+).html',     "logbook.views.logbook",    name="logbook-page"),
    url(r'^(?P<username>\w+)/sigs.html$',                          "sigs.views.sigs",          name="sigs"),
    url(r'^(?P<username>\w+)/print.pdf$',                          "pdf.views.pdf",            name="pdf"),
    
    (r'^site-media/(?P<path>.*)$','django.views.static.serve',     {'document_root': '/home/chris/Websites/flightloggin/media', 'show_indexes': True}),

    (r'^\w+/$',                                                    "django.views.generic.simple.redirect_to", {'url': 'logbook.html'}   ),
    
    (r'\.php',                                                     "redirect.views.redirect", ),
)

