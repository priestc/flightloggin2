import re

from django.db import models
from django.db.models import Q

from annoying.functions import get_object_or_None

from airport.models import Airport, Custom, Navaid

class Route(models.Model):

    fancy_rendered =  models.TextField(blank=True, null=True)
    fallback_string = models.TextField(blank=True, null=True)
    simple_rendered = models.TextField(blank=True, null=True)
    
    p2p =             models.BooleanField()
    
    def __unicode__(self):
        return self.simple_rendered
        
    def as_list(self):
        """Returns a list of custom point objects that have
        consistent lat/lng properties no matter if it's a
        airport, navaid or an unknown point"""
        
        l = []
        
        class point(object):
            lat = 0
            lng = 0
        
        for rb in self.routebase_set.all():
            p = point()
            try:
                p.lat = rb.destination().location.x
                p.lng = rb.destination().location.y
                l.append(p)
            except AttributeError:
                pass                # .location will fail if the point is unknown. Just skit this point if this happens
            
        return l

#####################################################################################################

class RouteBase(models.Model):
    route =    models.ForeignKey(Route)
    
    airport =  models.ForeignKey(Airport, null=True, blank=True)
    navaid  =  models.ForeignKey(Navaid, null=True, blank=True)
    custom =   models.ForeignKey(Custom, null=True, blank=True, related_name="custom")
    
    unknown =  models.CharField(max_length=30, blank=True, null=True)
    
    sequence = models.PositiveIntegerField()
    
    def __unicode__(self):
        if self.airport:
            return "airport: " + self.airport.identifier
        
        elif self.navaid:
            return "navaid: " + self.navaid.identifier
            
        elif self.unknown:
            return "other: " + self.unknown
            
        else:
            return "????"
            
    def destination(self):
        return self.airport or self.navaid or self.custom or self.unknown
    
######################################################################################################  

def create_route_from_string(ostring):
    string = ostring
    
    if not string:
        return None
    
    string = normalize(string)
    points = string.split()
    unknown = False
    fancy_rendered = []
    simple_rendered = []
    routebases = []
    p2p = []
    
    for i, ident in enumerate(points):
        
        airport = None
        navaid = None
    
        if ident[0] == "@":  #must be a navaid
        
            first_rb = len(routebases) == 0  # is this the first routebase? if so don't try to guess which navaid is closest to the previous point
            
            if not first_rb and not routebases[i-1].unknown:
                navaid = Navaid.objects.filter(identifier=ident[1:])
                
                if navaid.count() > 1:
                    last_point = routebases[i-1].airport or routebases[i-1].navaid
                    navaid = navaid.distance(last_point.location).order_by('distance')[0]
                    
                elif navaid.count() == 0:
                    navaid = None
                    
                else:
                    navaid = navaid[0]
                    
            else:
                navaid = get_object_or_None(Navaid, identifier=ident[1:])

            if navaid:
                routebase = RouteBase(navaid=navaid, sequence=i)
                routebases.append(routebase)
                fancy_rendered.append("<span class='found_navaid' title='%s'>%s</span>" % (routebase.navaid.title_display(), routebase.navaid.line_display(), ) )
                simple_rendered.append("@" + routebase.navaid.identifier)
            
            
        else:
            airport = get_object_or_None(Airport, pk=ident)
        
            if not airport and len(ident) == 3:
                airport = get_object_or_None(Airport, pk="K" + ident)
        
            if airport:
                routebase = RouteBase(airport=airport, sequence=i)
                routebases.append(routebase)
                p2p.append(airport.pk)          # a landing airport, eligable for p2p testing
                fancy_rendered.append("<span class='found_airport' title='%s'>%s</span>" % (routebase.airport.title_display(), routebase.airport.line_display(), ) )
                simple_rendered.append(routebase.airport.identifier)
            
       
        if not (airport or navaid):
            routebase = RouteBase(unknown=ident, sequence=i)
            routebases.append(routebase)
            
            if not ident[0] == "@":                                         # not a unidentified navaid, assume a landing
                p2p.append(unknown)
                
            fancy_rendered.append("<span class='not_found'>%s</span>" % (routebase.unknown, ) )
            simple_rendered.append(routebase.unknown)
    
    fancy_rendered = "-".join(fancy_rendered)
    simple_rendered = "-".join(simple_rendered)
           
    is_p2p = len(set(p2p)) > 1
    route = Route(fancy_rendered=fancy_rendered, simple_rendered=simple_rendered, fallback_string=ostring, p2p=is_p2p)
    route.save()
    print "made new route"
    
    for routebase in routebases:
        routebase.route = route
        routebase.save()    
    
    return route
    
        
def normalize(string):
    import re
    string = string.upper()
    string = string.replace("LOCAL", " ")
    string = string.replace(" TO ", " ")
    return re.sub(r'[^a-zA-Z0-9_@]+', ' ', string).strip()

