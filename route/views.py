from django.http import HttpResponse
from models import Route
from annoying.decorators import render_to

@render_to('route_profile.html')
def route_profile(request, r):
    from django.contrib.auth.models import User
    from airport.models import Location
    from logbook.models import Flight
    from models import RouteBase
    from plane.models import Plane
    from django.db.models import Sum
    
    try:
        route = Route.objects.filter(simple_rendered__iexact=r)[0]
        rbs = RouteBase.objects\
                       .filter(route=route)\
                       .order_by('sequence')
    except:
        route = None
        rbs = None
        
    if not route:
        from django.http import Http404
        raise Http404
    
    users = Route.get_profiles(r, 'simple_rendered')
                    
    t_flights = Flight.objects\
                      .filter(route__simple_rendered__iexact=r)\
                      .count()
    
    types = Plane.objects\
                 .exclude(type="")\
                 .filter(flight__route__simple_rendered__iexact=r)\
                 .values_list('type', flat=True)\
                 .order_by()\
                 .distinct()
                    
    tailnumbers = Plane.objects\
                       .exclude(tailnumber="")\
                       .filter(flight__route__simple_rendered__iexact=r)\
                       .values_list('tailnumber', flat=True)\
                       .order_by('tailnumber')\
                       .distinct()
    
    return locals()
