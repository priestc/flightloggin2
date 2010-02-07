from django.views.decorators.cache import cache_page
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from share.decorator import secret_key
from annoying.decorators import render_to
from models import Location

################################
                        
@secret_key
def update_airports(request):
    import os
    from django.conf import settings
    home = settings.PROJECT_PATH
    secret_key = settings.SECRET_KEY
    host = settings.SITE_URL
    
    if request.GET.get('get') == 'true':
        urls = {}
        urls['navaids'] = "http://www.ourairports.com/data/navaids.csv"
        urls['airports'] = "http://www.ourairports.com/data/airports.csv"
        urls['countries'] = "http://www.ourairports.com/data/countries.csv"
        urls['regions'] = "http://www.ourairports.com/data/regions.csv"
        
        system_call = ""
        for name,url in urls.items():
            system_call += "wget -O - %s > %s/airport/fixtures/%s.csv;"\
                             % (url, home, name)
    
        os.system(system_call)
        
    from imports import airports, regions, countries, navaids
    
    regions()
    countries()
    airports()
    navaids()
    
    return HttpResponse("done!")


#@cache_page(60 * 15)
@render_to('location_profile.html')
def airport_profile(request, navaid, ident):
    
    from plane.models import Plane
    from logbook.models import Flight
    from django.contrib.auth.models import User
    from django.http import Http404
    
    try:
        loc = Location.objects.filter(loc_class__in=(1,2), identifier=ident)[0]
    except IndexError:
        #t_flights = 0
        #return locals()
        raise Http404('no such airport')
    
    if loc.loc_class == 1 and navaid:
        raise Http404
    
    if loc.loc_class == 2 and not navaid:
        raise Http404
        
    
    users = Location.get_profiles(ident, 'identifier')
    
    tailnumbers = Plane.objects\
                       .exclude(tailnumber="")\
                       .values_list('tailnumber', flat=True)\
                       .filter(flight__route__routebase__location__identifier=ident)\
                       .order_by('tailnumber')\
                       .distinct()
                       
    t_flights = Flight.objects\
                      .filter(route__routebase__location__identifier=ident)\
                      .count()
                      
    lc = loc.get_loc_class_display().lower()
    
    return locals()
    
def location_redirect(request, ident):
    url = reverse('profile-airport', kwargs={'ident': ident})
    return HttpResponseRedirect(url)
