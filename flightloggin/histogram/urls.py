from django.conf.urls.defaults import *

urlpatterns = patterns('flightloggin.histogram.views',

    url(
        r'^model-(?P<model>.+)\.png$',
        "model",
                                                        name="histogram-model",
    ),
    
    url(
        r'^type-(?P<type_>.+)\.png$',
        "type_",
                                                         name="histogram-type",
    ),
    
    url(
        r'^user_totals.png$',
        "user_totals",
                                                  name="histogram-user_totals",
    ),
)
