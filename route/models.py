import re

from django.db import models
from django.db.models import Q

from annoying.functions import get_object_or_None

from airport.models import Airport
from navaid.models import Navaid

class Route(models.Model):

    fallback_string = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        ret = []
        for routebase in self.routebase_set.all():
            if routebase.airport:
                ret.append(routebase.airport.identifier)
                
            elif routebase.navaid:
                ret.append("@" + routebase.navaid.identifier)
                
            else:
                ret.append(routebase.unknown)

        return "-".join(ret)

    def fancy_display(self):
        ret = []
        for routebase in self.routebase_set.all():
            if routebase.airport:
                ret.append("<span class='found_airport' title='%s'>%s</span>" % (routebase.airport.title_display(), routebase.airport.line_display(), ) )
                
            elif routebase.navaid:
                ret.append("<span class='found_navaid' title='%s'>%s</span>" % (routebase.navaid.title_display(), routebase.navaid.line_display(), ) )
                
            elif routebase.unknown:
                ret.append("<span class='not_found'>%s</span>" % (routebase.unknown, ) )
                
            else:
                ret.append("??")

        return "-".join(ret)
        
    def is_p2p(self):
    
        route = unicode(self)
        
        wo_navaids = re.compile(r'@.+-').sub("", route)
        
        points = wo_navaids.replace("-"," ").split()     # an array with all non-navaid identifiers
        
        #return points
        
        return len(set(points)) > 1     # return whether or not there are unique non-navaid identifiers
    
        

######################################################################################################

class RouteBase(models.Model):
    route =    models.ForeignKey(Route)
    
    airport =  models.ForeignKey(Airport, null=True, blank=True)
    navaid  =  models.ForeignKey(Navaid, null=True, blank=True)
    custom =   models.ForeignKey(Custom, null=True, blank=True)
    
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
    
######################################################################################################  

def create_route_from_string(ostring):
    string = ostring
    
    string = normalize(string)
    points = string.split()
    unknown = False
    routebases = []
    
    print points
    
    for i, ident in enumerate(points):
        
        airport = None
        navaid = None
    
        if ident[0] == "@":
        
            first_rb = len(routebases) == 0
            
            if not first_rb and not routebases[i-1].unknown:
                last_point = routebases[i-1].airport or routebases[i-1].navaid
                navaid = Navaid.objects.filter(identifier=ident[1:]).distance(last_point.location).order_by('distance')[:1]
                
                try:
                    navaid = navaid[0]
                except IndexError:
                    navaid = None
                    
            else:
                navaid = get_object_or_None(Navaid, identifier=ident[1:])
            
            
            
            #assert False
            if navaid:
                routebases.append(RouteBase(navaid=navaid, sequence=i))
            
        else:
            airport = get_object_or_None(Airport, pk=ident)
        
            if not airport and len(ident) == 3:
                airport = get_object_or_None(Airport, pk="K" + ident)
        
            if airport:
                routebases.append(RouteBase(airport=airport, sequence=i))
       
        if not (airport or navaid):
            routebases.append(RouteBase(unknown=ident, sequence=i))
   
            
    route = Route(fallback_string=ostring)
    route.save()
    
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

