from logbook.models import Flight
from route.models import RouteBase, Route
from share.decorator import no_share

from utils import *
from airport.models import Location

def single_route_kml(request, pk):
    """
    Return a KMZ file representing a single route. The route PK is passed in as
    opposed to a string representation of the route 
    """

    r = Route.objects.filter(flight__pk=pk)\
                     .values('kml_rendered', 'simple_rendered')\
                     
    f = RouteFolder(name="Route", qs=r, style="#red_line")

    return folders_to_kmz_response([f])

def single_location_kml(request, ident):
    """
    Return a KMZ file representing a single location. Passed in is the ident.
    """

    l = Location.objects.filter(identifier=ident).filter(loc_class=1)\
                     
    f = AirportFolder(name=ident, qs=l)

    return folders_to_kmz_response([f], add_icon=True)

#------------------------------------------------------------------------------

def routes_location_kml(request, ident):
    "Returns a KMZ of all routes flown to the passed location identifier"
    
    from django.db.models import Max
    
    qs = Route.objects\
              .filter(routebase__location__identifier=ident.upper())\
              .values('kml_rendered', 'simple_rendered')\
              .distinct()\
              .annotate(id=Max('id')) # clever way to get around
                                      # id without screwing up distinct()
              
    l = Location.objects.filter(identifier=ident).filter(loc_class=1)\
    
    folders=[0,1]
    folders[0] = AirportFolder(name="Airport", qs=l)
    folders[1] = RouteFolder(name="Routes", qs=qs)
    
    return folders_to_kmz_response(folders, ident, add_icon=True, compression=True)

def routes_type_kml(request, ty):
    "Returns a KMZ of all routes flown by the passed aircraft type"
    qs = Route.objects.filter(flight__plane__type=ty)
    return qs_to_time_kmz(qs)

def routes_tailnumber_kml(request, tn):
    "Returns a KMZ of all routes flown by the passed tailnumber"
    qs = Route.objects.filter(flight__plane__tailnumber=tn)
    return qs_to_time_kmz(qs)

#------------------------------------------------------------------------------

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
