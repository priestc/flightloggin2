from django.contrib.auth.decorators import login_required
from share.decorator import secret_key
from django.http import Http404, HttpResponse
from annoying.decorators import render_to

from models import Location

################################


def clear_locations():

    #select all locations that are owned by the common user (pk=1)
    airports = Location.objects.filter(user__id=1)
    c = airports.count()
    
    airports.delete()
    
    return "%s locations deleted" % c
                        
@secret_key
def update_airports(request):
    import os
    from django.core.urlresolvers import reverse
    from django.conf import settings
    home = settings.PROJECT_PATH
    secret_key = settings.SECRET_KEY
    host = settings.SITE_URL
    url = reverse('clear-locations')
    
    print clear_locations()
    
    if request.GET.get('get') == 'true':
        urls = {}
        urls['navaids'] = "http://www.ourairports.com/data/navaids.csv"
        urls['airports'] = "http://www.ourairports.com/data/airports.csv"
        urls['countries'] = "http://www.ourairports.com/data/countries.csv"
        urls['regions'] = "http://www.ourairports.com/data/regions.csv"
        
        system_call = ""
        for name,url in urls.items():
            system_call += "wget -O - %s > %s/airport/fixtures/%s.csv;" % (url, home, name)
    
        os.system(system_call)
        
    from imports import airports, regions, countries, navaids
    
    regions()
    countries()
    airports()
    navaids()
    
    return HttpResponse("done!")


@render_to('location_profile.html')
def airport_profile(request, pk):
    
    from plane.models import Plane
    from logbook.models import Flight
    from django.contrib.auth.models import User
    
    loc = Location.objects.filter(identifier=pk)[0]
    
    users = User.objects\
                .filter(flight__route__routebase__location__identifier=pk)\
                .distinct()
    
    tailnumbers = Plane.objects\
                       .values_list('tailnumber', flat=True)\
                       .filter(flight__route__routebase__location__identifier=pk)\
                       .order_by('tailnumber')\
                       .distinct()
                       
    t_flights = Flight.objects\
                      .filter(route__routebase__location__identifier=pk)\
                      .count()
    return locals()
    
    
