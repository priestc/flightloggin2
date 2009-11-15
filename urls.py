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


handler404 = 'main.views.not_found'

## all views get `shared` and `display_user`
## variables from `username` via ShareMiddleware

urlpatterns += patterns('',
    
    url(
        r'^$',
        "django.views.generic.simple.redirect_to",
        {'url': 'news.html'},
        name="root"
    ),
   
    (
        r'^admin/doc/',
        include('django.contrib.admindocs.urls')
    ),
    
    (
        r'^admin/',
        include(admin.site.urls),
    ),
    
    (
        r'^admin-manage.html$',
        direct_to_template,
        {'template': 'manage.html'},
    ),
    
    (   
        r'^clearlocations.py$',
        'airport.views.clear',
    ),
    
    ############################ graphs

    (
        r'^(?P<username>\w+)/linegraph/' +
        r'(?P<columns>[\w\-]+)/' +
        r'((?P<dates>\d{4}.\d{1,2}.\d{1,2}-\d{4}.\d{1,2}.\d{1,2})/)?' +
        r'(?P<rate>(rate|norate)?)' +
        r'.(?P<ext>(png|svg))$',
        # username/linegraph/(columns)/(dates) or (all).extension
        "graphs.views.graph_image",
    ),
                                
    url(
        r'^(?P<username>\w+)/states-(?P<type_>[\-\w]+)?.(?P<ext>(png|svg))$',
        "maps.states.view",
                                                            name="state-map",
    ),
                                                                   
    (
        r'^(?P<username>\w+)/sigs/(?P<columns>[\w\-]+).png',
        "sigs.views.make_sig",
    ),
    
    ############################ main site
    
    
    (
        r'^feeds/(?P<url>.*)/$',
        "django.contrib.syndication.views.feed",
        {'feed_dict': feeds},
    ),
    
    (
        r'^easy-recalc-routes.py$',
        "route.views.easy_recalc_routes"
    ),
    
    (
        r'^hard-recalc-routes.py$',
        "route.views.hard_recalc_routes",
    ),
    
    (
        r'^del-routes.py$',
        "route.views.del_routes",
    ),
    
    url(
        r'^news.html$',
        "main.views.news",
        name="news",
    ),
    
    url(
        r'^site_stats.html$',
        "site_stats.views.site_stats",
        name="site_stats",
    ),
    
    url(
        r'^faq.html$',
        "main.views.faq",
        name="faq",
    ),
    
    url(
        r'^help.html$',
        "main.views.help",
        name="help",
    ),
    
    (
        r'^openid/',
        include('django_openid_auth.urls'),
    ),
    
    url(
        r'^(?P<username>\w+)/email-backup.html$',
        "backup.views.emailbackup",
                                                          name="email-backup",
    ),
    
    url(
        r'^(?P<username>\w+)/routes-(?P<type_>\w+).kmz$',
        "maps.views.routes_kml",
                                                            name="kml-route",
    ),
    
    url(
        r'^(?P<username>\w+)/airports-(?P<type_>\w+).kmz$',
        "maps.views.airports_kml",
                                                            name="kml-airport",
    ),
    
    url(
        r'^(?P<username>\w+)/8710.html$',
        "auto8710.views.auto8710",
                                                                name="est",
    ),
    
    url(
        r'^(?P<username>\w+)/preferences.html$',
        "profile.views.profile",
                                                                name="profile",
    ),
    
    url(
        r'^(?P<username>\w+)/import.html$',
        "manage.views.import_v",
                                                                name="import",
    ),
    
    url(
        r'^(?P<username>\w+)/export.html$',
        "manage.views.export",
                                                                name="export",
    ),
    
    url(
        r'^(?P<username>\w+)/records.html$',
        "records.views.records",
                                                                name="records",
    ),
    
    url(
        r'^(?P<username>\w+)/events.html$',
        "records.views.events",
                                                                name="events",
    ),
    
    url(
        r'^(?P<username>\w+)/graphs.html$',
        "graphs.views.graphs",
                                                                name="graphs",
    ),
    
    url(
        r'^(?P<username>\w+)/planes.html$',
        "plane.views.planes",
                                                                name="planes",
    ),
    
    url(
        r'^(?P<username>\w+)/maps.html$',
        "maps.views.maps",
                                                                name="maps",
    ),
    
    url(
        r'^(?P<username>\w+)/currency.html$',
        "currency.views.currency",
                                                                name="currency",
    ),
    
    url(
        r'^(?P<username>\w+)/places.html$',
        "records.views.places",
                                                                name="places",
    ),
    
    url(
        r'^(?P<username>\w+)/backup/$',
        "backup.views.backup",
                                                                name="backup",
    ),
    
    url(
        r'^(?P<username>\w+)/massentry.html$',
        "logbook.views.mass_entry",
                                                            name="mass-entry",
    ),
    
    url(
        r'^(?P<username>\w+)/massedit-page-(?P<page>\d+).html$',
        "logbook.views.mass_edit",
                                                            name="mass-edit",
    ),
    
    url(
        r'^(?P<username>\w+)/logbook.html$',
        "logbook.views.logbook",
                                                                name="logbook",
    ),
    
    url(
        r'^(?P<username>\w+)/logbook-page-(?P<page>\d+).html',
        "logbook.views.logbook",
        name="logbook-page",
    ),
        
    url(
        r'^(?P<username>\w+)/sigs.html$',"sigs.views.sigs",
                                                                name="sigs",
    ),
    
    url(
        r'^(?P<username>\w+)/print.pdf$',
        "pdf.views.pdf",
                                                                name="pdf",
    ),
    
    url(
        r'^schedule-(?P<schedule>\w+).py$',
        "backup.views.schedule",
                                                            name="schedule",
    ),
    
    url(
        r'^stats_save.py$',
        "site_stats.views.save_to_db",
                                                            name="save_stats",
    ),
    
    (
        r'^site-media/(?P<path>.*)$','django.views.static.serve',
        {'document_root': '/srv/flightloggin/media',
            'show_indexes': True},
    ),

    (
        r'^\w+/$',
        "django.views.generic.simple.redirect_to",
        {'url': 'logbook.html'},
    ),
    
    (
        r'\.php',
        "redirect.views.redirect",
    ),
)

