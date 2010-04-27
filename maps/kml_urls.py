from django.conf.urls.defaults import *
from plane.models import Plane

urlpatterns = patterns('maps.kml_views',
    url(
        r'tailnumber-(?P<tn>%s+)\.kmz$' % Plane.plane_regex,
        "routes_tailnumber_kml",
                                              name="routes_for_tailnumber-kml",
    ),
    
    url(
        r'type-(?P<ty>%s+)\.kmz$' % Plane.plane_regex,
        "routes_type_kml",
                                                    name="routes_for_type-kml",
    ),
    
    url(
        r'model-(?P<model>.+)\.kmz$',
        "routes_model_kml",
                                                   name="routes_for_model-kml",
    ),
    
    url(
        r'route-(?P<pk>\d+)(?P<f>[fr]?)\.kmz$',
        "single_route_kml",
                                                       name="single_route-kml",
    ),
    
    url(
        r'single_location-(?P<ident>[A-Z0-9]+)\.kmz$',
        "single_location_kml",
                                                    name="single_location-kml",
    ),
    
    url(
        r'(?P<type>(navaid|location|airport))-(?P<ident>[A-Z0-9]+)\.kmz$',
        "routes_location_kml",
                                                name="routes_for_location-kml",
    ),
    
    url(
        r'(?P<username>\w+)\.kmz$',
        "single_user",
                                                               name="user-kml",
    ),
)
