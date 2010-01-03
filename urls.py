from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to
from django.contrib import admin

admin.autodiscover()

###############################################################################

from feeds.classes import LatestFlights
feeds = {
    'flights': LatestFlights,
}

###############################################################################

from route.sitemaps import RouteSitemap
from plane.sitemaps import TailnumberSitemap, TypeSitemap
from airport.sitemaps import LocationSitemap

sitemaps = {
    'tailnumber': TailnumberSitemap,
    'type': TypeSitemap,
    'route': RouteSitemap,
    'location': LocationSitemap,
}

##############################################################################

#handler404 = 'main.views.not_found'

## all views get `shared` and `display_user`
## variables from `username` via ShareMiddleware

urlpatterns = patterns('',

    (
        r'^icons/favicon.ico$',
        redirect_to,
        {'url': '/fl-media/icons/favicon.ico'},
    ),

    (
        r'forums/?$',
        "redirect.views.redirect_to_forums",
    ),

    (
        r'^sitemap.xml$',
        'django.contrib.sitemaps.views.index',
        {'sitemaps': sitemaps}
    ),
    
    (
        r'^sitemap-(?P<section>.+)\.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}
    ),


    
    url(
        r'^$',
        "django.views.generic.simple.redirect_to",
        {'url': 'news.html'},
                                                                    name="root"
    ),
    
    ############################ graphs

    (
        r'^(?P<username>\w+)/linegraph/' +
        r'(?P<columns>[\w\-]+)/' +
        r'((?P<dates>\d{4}.\d{1,2}.\d{1,2}-\d{4}.\d{1,2}.\d{1,2})/)?' +
        r'(?P<rate>(rate|norate)?)' +
        r'(?P<spikes>(-spikes|-nospikes)?)' +
        r'.(?P<ext>(png|svg))$',
        # username/linegraph/(columns)/(dates) or (all).extension
        "graphs.views.linegraph_image",
    ),
    
    (
        r'^(?P<username>\w+)/bargraph/' + 
        r'(?P<column>[\w]+)/' +
        r'(?P<func>[\w]+)/' +
        r'by-(?P<agg>[\w]+)' +
        r'.png$',
        # username/bargraph/(column)/(func)/by-(agg).png
        'graphs.views.bargraph_image',
    ),
    
    ################################## sigs
                                                              
    (       # old sig url format (for legacy)
        r'^(?P<username>\w+)/sigs/(?P<columns>[\w\-]+).png',
        "sigs.views.make_sig",
        {"font": "VeraMono", "logo": "nologo"},
    ),
    
    (       # new sig format
        r'^(?P<username>\w+)/(?P<logo>(logo|nologo))-sigs/' + 
        r'(?P<font>\w+)-(?P<size>\d{1,2})/(?P<columns>[\w\-]+).png',
        "sigs.views.make_sig",
    ),
    

    ################################ admin functions
    
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
    
    (
        r'^recalc-images.py$',
        "maps.states_views.render_all",
    ),
    
    (
        r'^histogram.py$',
        "graphs.views.histogram",
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
        r'^openid/',
        include('django_openid_auth.urls'),
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
    
    
        ############################ main site
    
    url(
        r'^logout/$','django.contrib.auth.views.logout',
        {"next_page": "/"},
                                                                  name="logout"
    ),   
        
    url(
        r'^update-airports.py$',
        "airport.views.update_airports",
                                                           name="del-airports",
    ),
    
    url(
        r'^change_email.html$',
        "backup.views.change_email",
                                                           name="change_email",
    ),
    
    url(
        r'^(?P<userid>\d+)_remove_email.html$',
        "backup.views.submit_change",
                                                    name="submit_change_email",
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
    
    url(
        r'^(?P<username>\w+)/realtime.html$',
        "realtime.views.realtime",
                                                               name="realtime",
    ),
    
    url(
        r'^(?P<username>\w+)/email-backup.html$',
        "backup.views.emailbackup",
                                                           name="email-backup",
    ),
    
    #--------------------------------------------------------------------------
     
    url(
        r'^tailnumber-(?P<tn>[\w\-\)\(]+).kmz$',
        "maps.kml_views.single_tailnumber_kml",
                                                       name="s-tailnumber-kml",
    ),
    
    url(
        r'^type-(?P<ty>[\w-]+).kmz$',
        "maps.kml_views.single_type_kml",
                                                             name="s-type-kml",
    ),
    
    url(
        r'^route-(?P<pk>[\w-]+).kmz$',
        "maps.kml_views.single_route_kml",
                                                            name="s-route-kml",
    ),
    
    url(
        r'^location-(?P<pk>[A-Z0-9]+).kmz$',
        "maps.kml_views.single_location_kml",
                                                         name="s-location-kml",
    ),
    
    #--------------------------------------------------------------------------
    
    url(
        r'^route-(?P<pk>[\w-]+)$',
        "maps.kml_views.single_route_kml",
        {'earth': False},                                  name="s-route-maps",
    ),
    
    url(
        r'^type-(?P<pk>[\w-]+)$',
        "maps.kml_views.single_route_kml",
        {'earth': False},                                   name="s-type-maps",
    ),
    
    #--------------------------------------------------------------------------
    
    url(
        r'^route-(?P<pk>[\w-]+).html$',
        "route.views.route_profile",
                                                          name="profile-route",
    ),
    
    url(
        r'^tailnumber-(?P<pk>[\w\-\)\(]+).html$',
        "plane.views.tailnumber_profile",
                                                     name="profile-tailnumber",
    ),
    
    url(
        r'^type-(?P<pk>[\w-]+).html$',
        "plane.views.type_profile",
                                                           name="profile-type",
    ),
    
    url(
        r'^navaid-(?P<pk>[A-Z0-9]+).html$',
        "airport.views.airport_profile",
        {"navaid": True},                                name="profile-navaid",
    ),
    
    url(
        r'^airport-(?P<pk>[A-Z0-9-]+).html$',
        "airport.views.airport_profile",
        {"navaid": False},                              name="profile-airport",
    ),
    
    url(
        r'^location-(?P<pk>[A-Z0-9-]+).html$',
        "airport.views.location_redirect",
                                                       name="profile-location",
    ),
    
    #--------------------------------------------------------------------------
    
    url(
        r'^(?P<username>\w+)/airports-(?P<type_>\w+).kmz$',
        "maps.kml_views.airports_kml",
                                                            name="kml-airport",
    ),
    
    url(
        r'^(?P<username>\w+)/routes-(?P<type_>\w+).kmz$',
        "maps.kml_views.routes_kml",
                                                              name="kml-route",
    ),
    
    #--------------------------------------------------------------------------
    
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
        r'^(?P<username>\w+)/linegraphs.html$',
        "graphs.views.linegraphs",
                                                             name="linegraphs",
    ),
    
    url(
        r'^(?P<username>\w+)/bargraphs.html$',
        "graphs.views.bargraphs",
                                                              name="bargraphs",
    ),
    
    url(
        r'^(?P<username>\w+)/planes.html$',
        "plane.views.planes",
                                                                 name="planes",
    ),
    
    url(
        r'^(?P<username>\w+)/mass_planes.html$',
        "plane.views.mass_planes",
                                                            name="mass-planes",
    ),
    
    url(
        r'^(?P<username>\w+)/maps.html$',
        "maps.views.maps",
                                                                   name="maps",
    ),
    
    url(
        r'^(?P<username>\w+)/states-(?P<type_>[\w\-]+).png$',
        "maps.states_views.image_redirect",
                                                              name="state-map",
    ),
    
    url(
        r'^(?P<username>\w+)/recalc-mine.py$',
        "maps.states_views.render_me",
                                                              name="render-me",
    ),
    
    url(
        r'^(?P<username>\w+)/milestones.html$',
        "milestones.views.milestones",
                                                             name="milestones",
    ),
    
    url(
        r'^smallbar/(?P<val>\d+(\.\d+)?)--(?P<max_val>\d+(\.\d+)?).png$',
        "milestones.views.smallbar",
                                                               name='smallbar',
    ),
    
    url(
        r'^(?P<username>\w+)/currency.html$',
        "currency.views.currency",
                                                               name="currency",
    ),
    
    url(
        r'^(?P<username>\w+)/locations.html$',
        "records.views.locations",
                                                              name="locations",
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
    
    (
        r'^lcl_dev_media/(?P<path>.*)$','django.views.static.serve',
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

