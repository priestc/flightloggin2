from django.contrib.auth.decorators import login_required
from share.decorator import secret_key
from django.http import Http404, HttpResponse

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
    
