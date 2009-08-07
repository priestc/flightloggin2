from django.conf.urls.defaults import *

urlpatterns = patterns('airport',
        #url(r'^export$',                        "views.export", name="export-airports"),
        url(r'^(?P<pk>\S{1,7})/$',              "views.airport", name="view-airport"),
)
