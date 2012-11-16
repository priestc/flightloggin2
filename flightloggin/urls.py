from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to
from django.contrib import admin

from django.conf import settings
username_regex = settings.REGEX_USERNAME

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

    (r'', include('landingpage.urls')),
    (r'landingpage', redirect_to, {'url': '/'}),
    (r'^planes/', include('plane.urls')),
    (r'^histogram/', include('histogram.urls')),
    (r'^kml/', include('maps.kml_urls')),

    (r'^search/locations\.html$', 'airport.views.search_airport'),
        
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
        r'^(?P<username>%s)/linegraph/' % username_regex +
        r'(?P<columns>[\w\-]+)/' +
        r'((?P<dates>\d{4}.\d{1,2}.\d{1,2}-\d{4}.\d{1,2}.\d{1,2})/)?' +
        r'(?P<rate>(rate|norate)?)' +
        r'(?P<spikes>(-spikes|-nospikes)?)' +
        r'.(?P<ext>(png|svg))$',
        # username/linegraph/(columns)/(dates) or (all).extension
        "graphs.views.linegraph_image",
    ),
    
    (
        r'^(?P<username>%s)/bargraph/' % username_regex + 
        r'(?P<column>[\w]+)/' +
        r'(?P<func>[\w]+)/' +
        r'by-(?P<agg>[\w]+)' +
        r'.png$',
        # username/bargraph/(column)/(func)/by-(agg).png
        'graphs.views.bargraph_image',
    ),
    
    ################################## sigs
    
    (       # new sig format
        r'^(?P<username>%s)/(?P<logo>(logo|nologo))-sigs/' % username_regex + 
        r'(?P<font>\w+)-(?P<size>\d{1,2})/(?P<columns>[\w\-]+)\.png',
        "sigs.views.make_totals_sig",
    ),
    
    (       # new sig format
        r'^(?P<username>%s)/ds-sigs/' % username_regex + 
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
        r'^(?P<username>%s)/email-backup.html$' % username_regex,
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
        r'^navaid/(?P<ident>[A-Z0-9]+)$',
        "airport.views.airport_profile",
        {"navaid": True},                                name="profile-navaid",
    ),
    
    url(
        r'^airport/(?P<ident>[A-Z0-9-_]+)$',
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
        r'^location-(?P<ident>[A-Z0-9-]+)(\.html)?$',
        "main.views.temp_redirect",
    ),
    url(
        r'^airport-(?P<ident>[A-Z0-9-]+)(\.html)?$',
        "main.views.temp_redirect",
    ),
    url(
        r'^navaid-(?P<ident>[A-Z0-9-]+)(\.html)?$',
        "main.views.temp_redirect",
    ),
    url(
        r'^model(-|/)(?P<ident>[A-Z0-9-]+)(\.html)?$',
        "main.views.temp_redirect",
    ),
    url(
        r'^type(-|/)(?P<ident>[A-Z0-9-]+)(\.html)?$',
        "main.views.temp_redirect",
    ),
    url(
        r'^tailnumber(-|/)(?P<ident>[A-Z0-9-]+)(\.html)?$',
        "main.views.temp_redirect",
    ),

    url(
        r'^route-(?P<ident>[A-Z0-9-]+)(\.html)?$',
        "main.views.temp_redirect",
    ),
    
    #--------------------------------------------------------------------------
    
    url(
        r'^badges/(?P<username>%s)$' % username_regex,
        "badges.views.badges",
                                                                 name="badges",
    ),
    
    url(
        r'^8710/(?P<username>%s)$' % username_regex,
        "auto8710.views.auto8710",
                                                                    name="est",
    ),
    
    url(
        r'^preferences/(?P<username>%s)$' % username_regex,
        "profile.views.profile",
                                                                name="profile",
    ),
    
    url(
        r'^import/(?P<username>%s)$' % username_regex,
        "manage.views.import_v",
                                                                 name="import",
    ),
    
    url(
        r'^export/(?P<username>%s)$' % username_regex,
        "manage.views.export",
                                                                 name="export",
    ),
    
    url(
        r'^records/(?P<username>%s)$' % username_regex,
        "records.views.records",
                                                                name="records",
    ),
    
    url(
        r'^events/(?P<username>%s)$' % username_regex,
        "records.views.events",
                                                                 name="events",
    ),
    
    url(
        r'^linegraphs/(?P<username>%s)$' % username_regex,
        "graphs.views.linegraphs",
                                                             name="linegraphs",
    ),
    
    url(
        r'^bargraphs/(?P<username>%s)$' % username_regex,
        "graphs.views.bargraphs",
                                                              name="bargraphs",
    ),

    url(
        r'^maps/(?P<username>%s)$' % username_regex,
        "maps.views.maps",
                                                                   name="maps",
    ),

    url(
        r'^sigs/(?P<username>%s)$' % username_regex,
        "sigs.views.sigs",
                                                                   name="sigs",
    ),
    
    url(
        r'^/print/(?P<username>%s).pdf$' % username_regex,
        "pdf.views.pdf",
                                                                    name="pdf",
    ),
    
    url(
        r'^states/(?P<username>%s)$' % username_regex,
        direct_to_template,
        {"template": "states.html"},
                                                                 name="states",
    ),

    url(
        r'^countries/(?P<username>%s)$' % username_regex,
        direct_to_template,
        {"template": "countries.html"},
                                                              name="countries",
    ),
    
    url(
        r'^states_data/(?P<username>%s)/(?P<type_>(unique|landings)+)\.json$' % username_regex,
        "maps.states_views.states_data",
                                                              name="state-data",
    ),
    
    url(
        r'^countries_data/(?P<username>\w+)/(?P<type_>(unique|landings)+)\.json$',
        "maps.states_views.countries_data",
                                                            name="country-data",
    ),

    url(
        r'^milestones/(?P<username>%s)$' % username_regex,
        "milestones.views.milestones",
                                                             name="milestones",
    ),
    
    url(
        r'^smallbar/(?P<val>\d+(\.\d+)?)--(?P<max_val>\d+(\.\d+)?)\.png$',
        "milestones.views.smallbar",
                                                               name='smallbar',
    ),
    
    url(
        r'^currency/(?P<username>%s)$' % username_regex,
        "currency.views.currency",
                                                               name="currency",
    ),
    
    url(
        r'^locations/(?P<username>%s)$' % username_regex,
        "records.views.locations",
                                                              name="locations",
    ),
    
    url(
        r'^backup/(?P<username>%s)$ % username_regex',
        "backup.views.backup",
                                                                 name="backup",
    ),
    
    url(
        r'^massentry/(?P<username>%s)$ % username_regex',
        "logbook.views.mass_entry",
                                                             name="mass-entry",
    ),
    
    url(
        r'^massedit-page-(?P<page>\d+)/(?P<username>%s)$' % username_regex,
        "logbook.views.mass_edit",
                                                              name="mass-edit",
    ),
    
    ###########################################################################
    
    url(
        r'logbook$',
        'logbook.views.root_logbook'
    ),

    url(
        r'^logbook/(?P<username>%s)$' % username_regex,
        "logbook.views.root_logbook",
                                                                name="logbook",
    ),

    url(
        r'^mobile/(?P<username>%s)$' % username_regex,
        "logbook.views.mobile_new_flight",
                                                      name="mobile-new-flight",
    ),
    
    url(
        r'^logbook-page-(?P<page>\d+)/(?P<username>%s)' % username_regex,
        "logbook.views.logbook",
                                                           name="logbook-page",
    ),
    
    url(
        r'^edit_flight-(?P<page>\d+)/(?P<username>%s)$' % username_regex,
        "logbook.views.edit_flight",
                                                            name="edit_flight",
    ),
    
    url(
        r'^new_flight-(?P<page>\d+)/(?P<username>%s)$' % username_regex,
        "logbook.views.new_flight",
                                                             name="new_flight",
    ),
    
    url(
        r'^delete_flight-(?P<page>\d+)/(?P<username>%s)$' % username_regex,
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
        r'.html$',
        "main.views.remove_html_redirection",
    )
)

