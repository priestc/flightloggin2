from logbook.models import Flight
from route.models import RouteBase, Route
from is_shared import is_shared

from annoying.decorators import render_to
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context



def airports_kml(request, username):
    from settings import MEDIA_URL
    shared, display_user = is_shared(request, username)
    
    points = RouteBase.objects.filter(route__flight__user=display_user)
    
    ret = []
    for point in points:
        ret.append(point.destination())
        
    bases = set(ret)
    
    kml = get_template('base.kml').render(Context(locals() ))
    return HttpResponse(kml, mimetype="application/vnd.google-earth.kml+xml")
    
    
    
def routes_kml(request, username):
    
    shared, display_user = is_shared(request, username)
    
    routes = Route.objects.filter(flight__user=display_user)
    
    kml = get_template('base.kml').render(Context(locals() ))
    return HttpResponse(kml, mimetype="application/vnd.google-earth.kml+xml")
