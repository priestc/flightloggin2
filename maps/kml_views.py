from django.views.decorators.cache import cache_page

from logbook.models import Flight
from route.models import RouteBase, Route
from share.decorator import no_share

from utils import *
from airport.models import Location

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
    
    r = Route.objects.filter(**kwarg)\
                     .values('kml_rendered', 'simple_rendered')\
                  
    f = RouteFolder(name="Route", qs=r, style="#red_line")

    return folders_to_kmz_response([f])

@cache_page(60 * 60 * 900)
def single_location_kml(request, ident):
    """
    Return a KMZ file representing a single location. Passed in is the ident.
    (as opposed to the pk)
    """

    l = Location.objects.filter(identifier=ident).filter(loc_class=1)\
                     
    f = AirportFolder(name=ident, qs=l)

    return folders_to_kmz_response([f], add_icon=True)

#------------------------------------------------------------------------------

@cache_page(60 * 60)
def routes_location_kml(request, ident):
    """
    Returns a KMZ of all routes flown to the passed location identifier,
    also adds a point over the passed identifier
    """
    
    #from django.db.models import Max
    
    qs = Route.objects\
              .filter(routebase__location__identifier=ident.upper())\
              .values('kml_rendered', 'simple_rendered')\
              .distinct()\
              #.annotate(id=Max('id')) # clever way to get around
                                      # id without screwing up distinct()
              
    l = Location.objects.filter(identifier=ident).filter(loc_class=1)\
    
    return qs_to_time_kmz(qs, big_points=(l[0].identifier, l))

#------------------------------------------------------------------------------

@cache_page(60 * 60)
def routes_model_kml(request, model):
    "Returns a KMZ of all routes flown by the passed aircraft type"
    
    qs = Route.objects.filter(flight__plane__model=model)
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
    return qs_to_time_kmz(qs)

#------------------------------------------------------------------------------
## soon to be deprecated functions below

@cache_page(60 * 5)
def single_user(request, uname):
    """
    Returns a combined KML file with both the routes and airports a single user
    has flown to
    """
    
    qs = Route.objects.filter(flight__user__username=uname)
    
    points = Location.objects\
                     .filter(routebase__route__in=qs)\
                     .filter(loc_class=1)\
    
    return qs_to_time_kmz(qs, big_points=('Airports', points))

@no_share('other')
def airports_kml(request, type_):
    from django.conf import settings
    
    if type_=="all":
        title = "All Airports"
        points = Location.objects\
                         .user(request.display_user)\
                         .filter(loc_class=1)\
                         .distinct()
                         
        custom = Location.objects\
                         .user(request.display_user)\
                         .filter(loc_class=3)\
                         .distinct()
                    
        folders = []
        if points:
            folders.append(AirportFolder(name="All Airports", qs=points))
            
        if custom:
            folders.append(AirportFolder(name="All Custom Locations", qs=custom))
    
    return folders_to_kmz_response(folders, title, add_icon=True)

@no_share('other')   
def routes_kml(request, type_):
    
    qs = Route.objects.user(request.display_user)
    
    if type_== "all":
        title = "All Routes"
        all_r = qs.values('kml_rendered', 'simple_rendered')\
                  .order_by()\
                  .distinct()

        folders=[]
        if all_r:
            folders.append(RouteFolder(name="All Routes", qs=all_r))
        
        return folders_to_kmz_response(folders, title)
        
    elif type_== "cat_class":
        return qs_to_catclass_kmz(qs)
            
    elif type_ == "flight_time":
        return qs_to_time_kmz(qs)
