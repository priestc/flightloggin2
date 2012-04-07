from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to
from django.contrib import admin

from flightloggin.plane.models import Plane

admin.autodiscover()

handler500 = "main.views.handler500"

###############################################################################

#from feeds.classes import LatestFlights, LatestNews
#feeds = {
#    'flights': LatestFlights,
#    'news': LatestNews,
#}

###############################################################################

from flightloggin.route.sitemaps import RouteSitemap
from flightloggin.plane.sitemaps import TailnumberSitemap, TypeSitemap, ModelSitemap
from flightloggin.airport.sitemaps import LocationSitemap

sitemaps = {
    'tailnumber': TailnumberSitemap,
    'type': TypeSitemap,
    'route': RouteSitemap,
    'model': ModelSitemap,
    'location': LocationSitemap,
}

###############################################################################

## all views get `shared` and `display_user`
## variables from `username` via ShareMiddleware

urlpatterns = patterns('django_openid_auth.views',

    url(
        r'^openid/login/$',
        'login_begin',
                                                                  name="login",
    ),
    
    (
        r'^openid/complete/$',
        'login_complete',
    ),
    
    url(
        r'^logo.gif$',
        'logo',
                                                            name='openid-logo',
    ),
)

###############################################################################

urlpatterns += patterns('',
    (
        r'^robots\.txt$',
        'main.views.robots'
    ),

    (r'^histogram/', include('flightloggin.histogram.urls')),
    (r'^kml/', include('maps.kml_urls')),
    (r'^facebook', include('flightloggin.facebook_app.urls')),
    
    (r'^search/locations\.html$', 'flightloggin.airport.views.search_airport'),
    (r'^search/tailnumbers\.html$', 'flightloggin.plane.views.search_tailnumbers'),
    
    ('export_airports-(?P<index>\d{1,5}).xml', "flightloggin.airport.views.export_to_xml"),
    
    url(
        r'^help.html$',
        "main.views.help",
                                                                   name="help",
    ),
    
    url(
        r'^privacy_policy.html$',
        direct_to_template,
        {"template": "privacy.html"},
                                                                name="privacy",
    ),
    
    url(
        r'^(?P<username>\w+)/realtime\.html$',
        "flightloggin.realtime.views.realtime2",
                                                               name="realtime",
    ),
    
    (
        r'^(?P<username>\w+)/duty_status/$',
        "flightloggin.realtime.views.ajax_duty_status",
    ),
    
    url(
        r'^(?P<username>\w+)/go_on_duty/$',
        "flightloggin.realtime.views.ajax_go_on_duty",
                                                        name="ajax_go_on_duty",
    ),
    
    url(
        r'^(?P<username>\w+)/go_off_duty/$',
        "flightloggin.realtime.views.ajax_go_off_duty",
                                                       name="ajax_go_off_duty",
    ),
    
    url(
        r'^(?P<username>\w+)/get_master_duty/$',
        "flightloggin.realtime.views.ajax_get_master_duty",
                                                   name="ajax_get_master_duty",
    ),
    ##########################################################################

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
        redirect_to,
        {'url': 'manews.html'},
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
        "flightloggin.graphs.views.linegraph_image",
    ),
    
    (
        r'^(?P<username>\w+)/bargraph/' + 
        r'(?P<column>[\w]+)/' +
        r'(?P<func>[\w]+)/' +
        r'by-(?P<agg>[\w]+)' +
        r'.png$',
        # username/bargraph/(column)/(func)/by-(agg).png
        'flightloggin.graphs.views.bargraph_image',
    ),
    
    ################################## sigs
                                                              
    (       # old sig url format (for legacy)
        r'^(?P<username>\w+)/sigs/(?P<columns>[\w\-]+)\.png',
        "flightloggin.sigs.views.make_totals_sig",
        {"font": "VeraMono", "logo": "nologo"},
    ),
    
    (       # new sig format
        r'^(?P<username>\w+)/(?P<logo>(logo|nologo))-sigs/' + 
        r'(?P<font>\w+)-(?P<size>\d{1,2})/(?P<columns>[\w\-]+)\.png',
        "flightloggin.sigs.views.make_totals_sig",
    ),
    
    (       # new sig format
        r'^(?P<username>\w+)/ds-sigs/' + 
        r'(?P<font>\w+)-(?P<size>\d{1,2})/(?P<mode>[\w]+)\.png',
        "flightloggin.sigs.views.make_days_since_sig",
    ),
    

    ################################ admin functions
    
    #(
    #    r'^feeds/(?P<url>.*)/$',
    #    "django.contrib.syndication.views.feed",
    #    {'feed_dict': feeds},
    #),
    
    (
        r'^admin/doc/',
        include('django.contrib.admindocs.urls')
    ),
    
    (
        r'^admin/',
        include(admin.site.urls),
    ),
    
        ############################ main site 
    
    #url(
    #    r'^logout/$','django.contrib.auth.views.logout',
    #    {"next_page": "/"},
    #                                                             name="logout",
    #),
    
    url(
        r'^change_email\.html$',
        "flightloggin.backup.views.change_email",
                                                           name="change_email",
    ),
    
    url(
        r'^(?P<userid>\d+)_remove_email\.html$',
        "flightloggin.backup.views.submit_change",
                                                    name="submit_change_email",
    ),
    
    url(
        r'^news\.html$',
        "main.views.news",
                                                                   name="news",
    ),
    
    #--------------------------------------------------------------------------
    
    url(
        r'^site_stats\.html$',
        "flightloggin.site_stats.views.site_stats",
                                                             name="site_stats",
    ),
    
    url(
        r'^stats_graph/(?P<item>[\w_]+)\.(?P<ext>(png|svg))$',
        "flightloggin.site_stats.views.stats_graph",
                                                            name="stats_graph",
    ),
    
    #--------------------------------------------------------------------------
    
    url(
        r'^(?P<username>\w+)/email-backup.html$',
        "flightloggin.backup.views.emailbackup",
                                                           name="email-backup",
    ),

    #--------------------------------------------------------------------------
    
    url(
        r'^route-(?P<r>[\w-]+)\.html$',
        "flightloggin.route.views.route_profile",
                                                          name="profile-route",
    ),
    
    url(
        r'^tailnumber-(?P<tn>%s+)\.html$' % Plane.plane_regex,
        "flightloggin.plane.views.tailnumber_profile",
                                                     name="profile-tailnumber",
    ),
    
    url(
        r'^type-(?P<ty>%s+)\.html$' % Plane.plane_regex,
        "flightloggin.plane.views.type_profile",
                                                           name="profile-type",
    ),
    
    url(
        r'^model-(?P<model>.+)\.html$',
        "flightloggin.plane.views.model_profile",
                                                          name="profile-model",
    ),
    
    url(
        r'^navaid-(?P<ident>[A-Z0-9]+)\.html$',
        "flightloggin.airport.views.airport_profile",
        {"navaid": True},                                name="profile-navaid",
    ),
    
    url(
        r'^airport-(?P<ident>[A-Z0-9-]+)\.html$',
        "flightloggin.airport.views.airport_profile",
        {"navaid": False},                              name="profile-airport",
    ),

    url(
        r'^location-(?P<ident>[A-Z0-9-]+)\.html$',
        "flightloggin.airport.views.location_redirect",
                                                       name="profile-location",
    ),
    
    #--------------------------------------------------------------------------
    
    url(
        r'^(?P<username>\w+)/8710\.html$',
        "flightloggin.auto8710.views.auto8710",
                                                                    name="est",
    ),
    
    url(
        r'^(?P<username>\w+)/preferences\.html$',
        "flightloggin.profile.views.profile",
                                                                name="profile",
    ),
    
    url(
        r'^(?P<username>\w+)/import\.html$',
        "flightloggin.manage.views.import_v",
                                                                 name="import",
    ),
    
    url(
        r'^(?P<username>\w+)/export\.html$',
        "flightloggin.manage.views.export",
                                                                 name="export",
    ),
    
    url(
        r'^(?P<username>\w+)/records\.html$',
        "flightloggin.records.views.records",
                                                                name="records",
    ),
    
    url(
        r'^(?P<username>\w+)/events\.html$',
        "flightloggin.records.views.events",
                                                                 name="events",
    ),
    
    url(
        r'^(?P<username>\w+)/linegraphs\.html$',
        "flightloggin.graphs.views.linegraphs",
                                                             name="linegraphs",
    ),
    
    url(
        r'^(?P<username>\w+)/bargraphs\.html$',
        "flightloggin.graphs.views.bargraphs",
                                                              name="bargraphs",
    ),
    
    url(
        r'^(?P<username>\w+)/planes\.html$',
        "flightloggin.plane.views.planes",
                                                                 name="planes",
    ),
    
    url(
        r'^(?P<username>\w+)/mass_planes\.html$',
        "flightloggin.plane.views.mass_planes",
                                                            name="mass-planes",
    ),
    
    url(
        r'^(?P<username>\w+)/maps\.html$',
        "maps.views.maps",
                                                                   name="maps",
    ),
    
    #url(
    #    r'^(?P<username>\w+)/states\.html$',
    #    direct_to_template,
    #    {"template": "states.html"},
    #                                                             name="states",
    #),
    
    url(
        r'^(?P<username>\w+)/states-(?P<type_>[\w\-]+)\.(?P<ext>(png|svg))$',
        "maps.states_views.render_image",
                                                              name="state-map",
    ),
    
    url(
        r'^(?P<username>\w+)/milestones\.html$',
        "flightloggin.milestones.views.milestones",
                                                             name="milestones",
    ),
    
    url(
        r'^smallbar/(?P<val>\d+(\.\d+)?)--(?P<max_val>\d+(\.\d+)?)\.png$',
        "flightloggin.milestones.views.smallbar",
                                                               name='smallbar',
    ),
    
    url(
        r'^(?P<username>\w+)/currency\.html$',
        "flightloggin.currency.views.currency",
                                                               name="currency",
    ),
    
    url(
        r'^(?P<username>\w+)/locations\.html$',
        "flightloggin.records.views.locations",
                                                              name="locations",
    ),
    
    url(
        r'^(?P<username>\w+)/backup/$',
        "flightloggin.backup.views.backup",
                                                                 name="backup",
    ),
    
    url(
        r'^(?P<username>\w+)/massentry\.html$',
        "flightloggin.logbook.views.mass_entry",
                                                             name="mass-entry",
    ),
    
    url(
        r'^(?P<username>\w+)/massedit-page-(?P<page>\d+)\.html$',
        "flightloggin.logbook.views.mass_edit",
                                                              name="mass-edit",
    ),
    
    ###########################################################################
    
    url(
        r'^(?P<username>\w+)/logbook\.html$',
        "flightloggin.logbook.views.root_logbook",
                                                                name="logbook",
    ),
    
    url(
        r'^(?P<username>\w+)/logbook-page-(?P<page>\d+)\.html',
        "flightloggin.logbook.views.logbook",
                                                           name="logbook-page",
    ),
    
    url(
        r'^(?P<username>\w+)/edit_flight-(?P<page>\d+)/$',
        "flightloggin.logbook.views.edit_flight",
                                                            name="edit_flight",
    ),
    
    url(
        r'^(?P<username>\w+)/new_flight-(?P<page>\d+)/$',
        "flightloggin.logbook.views.new_flight",
                                                             name="new_flight",
    ),
    
    url(
        r'^(?P<username>\w+)/delete_flight-(?P<page>\d+)/$',
        "flightloggin.logbook.views.delete_flight",
                                                          name="delete_flight",
    ),

    ###########################################################################
        
    url(
        r'^(?P<username>\w+)/sigs\.html$',
        "flightloggin.sigs.views.sigs",
                                                                   name="sigs",
    ),
    
    url(
        r'^(?P<username>\w+)/print\.pdf$',
        "flightloggin.pdf.views.pdf",
                                                                    name="pdf",
    ),
    
    #(
    #    r'^lcl_dev_media/(?P<path>.*)$',
    #    'django.views.static.serve',
    #    {'document_root': '/srv/flightloggin/media', 'show_indexes': True},
    #),

    (
        r'^\w+/$',
        redirect_to,
        {'url': 'logbook.html'},
    ),
)

