from django.views.decorators.cache import cache_page

from logbook.models import Flight
from flightloggin.route.models import RouteBase, Route
from flightloggin.share.decorator import no_share

from utils import *
from flightloggin.airport.models import Location

@cache_page(60 * 60 * 900)
def single_route_kml(request, pk, f=False):
    """
    Return a KMZ file representing a single route. The route PK is passed in as
    opposed to a string representation of the route.
    
    If f=true, the pk is the
    pk of the flight the route is connected to (for one case in the logbook
    template where the flight pk is only available)
    """
    
    if f == "f":
        kwarg = {"flight__pk": pk}
    else:
        kwarg = {"pk": pk}
    
    # the actual route object
    route = Route.goof(**kwarg)
    
    #get distinct routebases to make icons with
    rbs = route.routebase_set.all()
    
    # convert routebases into locations
    l = Location.objects.filter(routebase__in=rbs).distinct()
    
    # convert back to dict and just the relevent bits
    r = dict(kml_rendered=route.kml_rendered,
             simple_rendered=route.simple_rendered)
    
    # make the folders
    f = RouteFolder(name="Route", qs=[r], style="#red_line")
    a = AirportFolder(name='Points', qs=l)

    return folders_to_kmz_response([f,a], add_icon=True)

@cache_page(60 * 60 * 900)
def single_location_kml(request, ident):
    """
    Return a KMZ file representing a single location. Passed in is the ident.
    (as opposed to the pk). No routes!
    """

    l = Location.goof(identifier=ident, loc_class=1)
                     
    f = AirportFolder(name=ident, qs=[l])

    return folders_to_kmz_response([f], add_icon=True)

#------------------------------------------------------------------------------

@cache_page(60 * 60)
def routes_location_kml(request, ident, type):
    """
    Returns a KMZ of all routes flown to the passed location identifier,
    also adds a point over the passed identifier
    """
    
    if type == 'airport':
        lc=1
    elif type == 'navaid':
        lc=2
    else:
        lc=1
        
    #raises 404 if no location is found
    l = Location.goof(identifier=ident, loc_class=lc)
    
    qs = Route.objects\
              .filter(routebase__location__identifier=ident.upper())\
              .values('kml_rendered', 'simple_rendered')\
              .distinct()
    
    name = l.identifier
    
    return qs_to_time_kmz(qs, points=(name, [l]))

#------------------------------------------------------------------------------

@cache_page(60 * 60)
def routes_model_kml(request, model):
    "Returns a KMZ of all routes flown by the passed aircraft model"
    
    qs = Route.objects.filter(flight__plane__model=model.replace('_',' '))
    return qs_to_time_kmz(qs)

#------------------------------------------------------------------------------

@cache_page(60 * 60)
def routes_type_kml(request, ty):
    "Returns a KMZ of all routes flown by the passed aircraft type"
    
    qs = Route.objects.filter(flight__plane__type=ty)
    return qs_to_time_kmz(qs)

#------------------------------------------------------------------------------

@cache_page(60 * 60)
def routes_tailnumber_kml(request, tn):
    "Returns a KMZ of all routes flown by the passed tailnumber"
    
    qs = Route.objects.filter(flight__plane__tailnumber=tn)
    
    l = Location.objects\
                .filter(routebase__route__in=qs, loc_class=1)\
                .distinct()
                
    return qs_to_time_kmz(qs, points=("Airports", l))

@cache_page(60 * 5)
def single_user(request):
    """
    Returns a combined KML file with both the routes and airports a single user
    has flown to
    """
        
    qs = Route.objects.user(request.display_user)
    
    points = Location.objects\
                     .filter(routebase__route__in=qs)\
                     .filter(loc_class=1)\
                     .distinct()
    
    return qs_to_time_kmz(qs, points=('Airports', points))
