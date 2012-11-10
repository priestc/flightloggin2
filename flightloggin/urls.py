from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to
from django.contrib import admin

from plane.models import Plane

admin.autodiscover()

handler500 = "main.views.handler500"

###############################################################################

from route.sitemaps import RouteSitemap
from plane.sitemaps import TailnumberSitemap, TypeSitemap, ModelSitemap
from airport.sitemaps import LocationSitemap

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
                                                           name="openid_login",
    ),
    
    url(
        r'^openid/complete/$',
        'login_complete',
        name='openid-complete'
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
        r'', include('landingpage.urls')
    ),

    (
        r'landingpage', redirect_to, {'url': '/'}
    ),

    (r'^histogram/', include('histogram.urls')),
    (r'^kml/', include('maps.kml_urls')),

    (r'^search/locations\.html$', 'airport.views.search_airport'),
    (r'^search/tailnumbers\.html$', 'plane.views.search_tailnumbers'),
    
    ('export_airports-(?P<index>\d{1,5}).xml', "airport.views.export_to_xml"),
    
    url(
        r'^help$',
        "main.views.help",
                                                                   name="help",
    ),
    
    url(
        r'^privacy_policy$',
        direct_to_template,
        {"template": "privacy.html"},
                                                                name="privacy",
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

    (
        r'^robots\.txt$',
        'main.views.robots'
    ),
    
    url(
        r'^$',
        redirect_to,
        {'url': '/landingpage'},
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
    
    (       # new sig format
        r'^(?P<username>\w+)/(?P<logo>(logo|nologo))-sigs/' + 
        r'(?P<font>\w+)-(?P<size>\d{1,2})/(?P<columns>[\w\-]+)\.png',
        "sigs.views.make_totals_sig",
    ),
    
    (       # new sig format
        r'^(?P<username>\w+)/ds-sigs/' + 
        r'(?P<font>\w+)-(?P<size>\d{1,2})/(?P<mode>[\w]+)\.png',
        "sigs.views.make_days_since_sig",
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
    
    url(
        r'^logout/$','django.contrib.auth.views.logout',
        {"next_page": "/"},
                                                                 name="logout",
    ),
    
    url(
        r'^change_email\.html$',
        "backup.views.change_email",
                                                           name="change_email",
    ),
    
    url(
        r'^(?P<userid>\d+)_remove_email\.html$',
        "backup.views.submit_change",
                                                    name="submit_change_email",
    ),
    
    url(
        r'^news$',
        "main.views.news",
                                                                   name="news",
    ),
    
    #--------------------------------------------------------------------------
    
    url(
        r'^site_stats$',
        "site_stats.views.site_stats",
                                                             name="site_stats",
    ),
    
    url(
        r'^stats_graph/(?P<item>[\w_]+)\.(?P<ext>(png|svg))$',
        "site_stats.views.stats_graph",
                                                            name="stats_graph",
    ),
    
    #--------------------------------------------------------------------------
    
    url(
        r'^(?P<username>\w+)/email-backup.html$',
        "backup.views.emailbackup",
                                                           name="email-backup",
    ),

    #--------------------------------------------------------------------------
    
    url(
        r'^route/(?P<r>[\w-]+)$',
        "route.views.route_profile",
                                                          name="profile-route",
    ),
    
    url(
        r'^tailnumber/(?P<tn>%s+)$' % Plane.plane_regex,
        "plane.views.tailnumber_profile",
                                                     name="profile-tailnumber",
    ),
    
    url(
        r'^type/(?P<ty>%s+)$' % Plane.plane_regex,
        "plane.views.type_profile",
                                                           name="profile-type",
    ),
    
    url(
        r'^model/(?P<model>.+)$',
        "plane.views.model_profile",
                                                          name="profile-model",
    ),
    
    url(
        r'^navaid/(?P<ident>[A-Z0-9]+)$',
        "airport.views.airport_profile",
        {"navaid": True},                                name="profile-navaid",
    ),
    
    url(
        r'^airport/(?P<ident>[A-Z0-9-]+)$',
        "airport.views.airport_profile",
        {"navaid": False},                              name="profile-airport",
    ),

    url(
        r'^location/(?P<ident>[A-Z0-9-]+)$',
        "airport.views.location_redirect",
                                                       name="profile-location",
    ),

    #### temporary redirect, remove at some point
    url(
        r'^location-(?P<ident>[A-Z0-9-]+)$',
        "main.views.temp_redirect",
    ),
    url(
        r'^airport-(?P<ident>[A-Z0-9-]+)$',
        "main.views.temp_redirect",
    ),
    url(
        r'^navaid-(?P<ident>[A-Z0-9-]+)$',
        "main.views.temp_redirect",
    ),
    url(
        r'^model-(?P<ident>[A-Z0-9-]+)$',
        "main.views.temp_redirect",
    ),
    url(
        r'^type-(?P<ident>[A-Z0-9-]+)$',
        "main.views.temp_redirect",
    ),
    url(
        r'^tailnumber-(?P<ident>[A-Z0-9-]+)$',
        "main.views.temp_redirect",
    ),
    url(
        r'^route-(?P<ident>[A-Z0-9-]+)$',
        "main.views.temp_redirect",
    ),
    
    #--------------------------------------------------------------------------
    
    url(
        r'^badges/(?P<username>\w+)$',
        "badges.views.badges",
                                                                 name="badges",
    ),
    
    url(
        r'^8710/(?P<username>\w+)$',
        "auto8710.views.auto8710",
                                                                    name="est",
    ),
    
    url(
        r'^preferences/(?P<username>\w+)$',
        "profile.views.profile",
                                                                name="profile",
    ),
    
    url(
        r'^import/(?P<username>\w+)$',
        "manage.views.import_v",
                                                                 name="import",
    ),
    
    url(
        r'^export/(?P<username>\w+)$',
        "manage.views.export",
                                                                 name="export",
    ),
    
    url(
        r'^records/(?P<username>\w+)$',
        "records.views.records",
                                                                name="records",
    ),
    
    url(
        r'^events/(?P<username>\w+)$',
        "records.views.events",
                                                                 name="events",
    ),
    
    url(
        r'^linegraphs/(?P<username>\w+)$',
        "graphs.views.linegraphs",
                                                             name="linegraphs",
    ),
    
    url(
        r'^bargraphs/(?P<username>\w+)$',
        "graphs.views.bargraphs",
                                                              name="bargraphs",
    ),
    
    url(
        r'^planes/(?P<username>\w+)$',
        "plane.views.planes",
                                                                 name="planes",
    ),
    
    url(
        r'^mass_planes/(?P<username>\w+)$',
        "plane.views.mass_planes",
                                                            name="mass-planes",
    ),
    
    url(
        r'^maps/(?P<username>\w+)$',
        "maps.views.maps",
                                                                   name="maps",
    ),

    url(
        r'^sigs/(?P<username>\w+)$',
        "sigs.views.sigs",
                                                                   name="sigs",
    ),
    
    url(
        r'^/print/(?P<username>\w+).pdf$',
        "pdf.views.pdf",
                                                                    name="pdf",
    ),
    
    url(
        r'^states/(?P<username>\w+)$',
        direct_to_template,
        {"template": "states.html"},
                                                                 name="states",
    ),

    url(
        r'^countries/(?P<username>\w+)$',
        direct_to_template,
        {"template": "countries.html"},
                                                              name="countries",
    ),
    
    url(
        r'^states_data/(?P<username>\w+)/(?P<type_>(unique|landings)+)\.json$',
        "maps.states_views.states_data",
                                                              name="state-data",
    ),
    
    url(
        r'^countries_data/(?P<username>\w+)/(?P<type_>(unique|landings)+)\.json$',
        "maps.states_views.countries_data",
                                                            name="country-data",
    ),

    url(
        r'^milestones/(?P<username>\w+)$',
        "milestones.views.milestones",
                                                             name="milestones",
    ),
    
    url(
        r'^smallbar/(?P<val>\d+(\.\d+)?)--(?P<max_val>\d+(\.\d+)?)\.png$',
        "milestones.views.smallbar",
                                                               name='smallbar',
    ),
    
    url(
        r'^currency/(?P<username>\w+)$',
        "currency.views.currency",
                                                               name="currency",
    ),
    
    url(
        r'^locations/(?P<username>\w+)$',
        "records.views.locations",
                                                              name="locations",
    ),
    
    url(
        r'^backup/(?P<username>\w+)$',
        "backup.views.backup",
                                                                 name="backup",
    ),
    
    url(
        r'^massentry/(?P<username>\w+)$',
        "logbook.views.mass_entry",
                                                             name="mass-entry",
    ),
    
    url(
        r'^massedit-page-(?P<page>\d+)/(?P<username>\w+)$',
        "logbook.views.mass_edit",
                                                              name="mass-edit",
    ),
    
    ###########################################################################
    
    url(
        r'logbook$',
        'logbook.views.root_logbook'
    ),

    url(
        r'^logbook/(?P<username>\w+)$',
        "logbook.views.root_logbook",
                                                                name="logbook",
    ),

    url(
        r'^mobile/(?P<username>\w+)$',
        "logbook.views.mobile_new_flight",
                                                      name="mobile-new-flight",
    ),
    
    url(
        r'^logbook-page-(?P<page>\d+)/(?P<username>\w+)',
        "logbook.views.logbook",
                                                           name="logbook-page",
    ),
    
    url(
        r'^edit_flight-(?P<page>\d+)/(?P<username>\w+)$',
        "logbook.views.edit_flight",
                                                            name="edit_flight",
    ),
    
    url(
        r'^new_flight-(?P<page>\d+)/(?P<username>\w+)$',
        "logbook.views.new_flight",
                                                             name="new_flight",
    ),
    
    url(
        r'^delete_flight-(?P<page>\d+)/(?P<username>\w+)$',
        "logbook.views.delete_flight",
                                                          name="delete_flight",
    ),

    url(
        r'^nearby_airports.json$',
        "airport.views.nearby_airports",
                                                             name="new_flight",
    ),

    ###########################################################################

    (
        r'^\w+/$',
        redirect_to,
        {'url': '/landingpage'},
    ),

    (
        r'.html$',
        "main.views.remove_html_redirection",
    )
)

