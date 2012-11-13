import json

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import GEOSGeometry

from share.decorator import secret_key
from annoying.decorators import render_to
from models import Location, HistoricalIdent

################################

@render_to('location_profile.html')
def airport_profile(request, navaid, ident):
    
    from plane.models import Plane
    from logbook.models import Flight
    from django.contrib.auth.models import User
    from django.http import Http404
    

    loc = Location.goof(loc_class__in=(1,2), identifier=ident)
    
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
    
    previous_identifiers = HistoricalIdent.objects\
                               .filter(current_location=loc)
    
    if navaid:
        ty = 'navaid'
    else:
        ty = 'airport'
    
    kwargs ={'ident': loc.identifier, 'type': ty}
    
    kml_url = reverse("routes_for_location-kml", kwargs=kwargs)
    print kml_url
    
    return locals()
    
def location_redirect(request, ident):
    url = reverse('profile-airport', kwargs={'ident': ident})
    return HttpResponseRedirect(url)



@render_to('search_locations.html')
def search_airport(request):

    if not request.GET:
        return locals()
    
    from django.db.models import Q
    
    s = request.GET.get('q')
    
    q = ( Q(identifier__icontains=s) | Q(name__icontains=s) | Q(municipality__icontains=s)
        )
    
    results = Location.objects\
                      .filter(loc_class__in=(1,2,))\
                      .filter(q)
    
    count = results.count()
    did_something = True
    
    return locals()

@render_to('wiki_airport.html', mimetype="text/plain") #application/xml")
def export_to_xml(request, index):
    """
    Export all airports to an XML file for inputting into wikiPLANEia
    """
    
    index = int(index)
    size = 5000
    start = (index * size)
    article_start = 178 + (index * size)
    rev_start = 182 + (index * size)
    
    qs = Location.objects\
                 .select_related()\
                 .filter(country__code='US', loc_class=1)\
                 .exclude(loc_type=1)\
                 .order_by('identifier')[start:start+size]\
                 .iterator()
    
    airports = []
    for num,a in enumerate(qs):
        a.article_id = num + article_start
        a.rev_id = num + rev_start
        airports.append(a)
               
    return locals()  

def nearby_airports(request):
    """
    Return a list of airports that are near the lat and lng included in the POST
    """
    lng = request.GET['lng']
    lat = request.GET['lat']
    type_ = request.GET['type']
    
    point = GEOSGeometry('POINT(%s %s)' % (lng, lat))

    airports = Location.objects\
                       .exclude(location=None)\
                       .distance(point)\
                       .order_by('distance')
    
    if type_ == 'land':
        airports = airports.filter(loc_class=1)

    out = []
    for airport in airports[:10]:
        if airport.distance.mi < 10:
            a = {
                'ident': airport.identifier,
                'name': airport.name,
                'distance': "%.2f" % airport.distance.mi,
            }
            out.append(a)

    return HttpResponse(json.dumps(out), mimetype="application/json")





