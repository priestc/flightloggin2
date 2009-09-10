import re

from django.db import models
from django.db.models import Q

from annoying.functions import get_object_or_None
from mid.middleware import threadlocals

#from logbook.models import Flight
from airport.models import Airport, Custom, Navaid

class Route(models.Model):
    
    #flight = models.OneToOneField(Flight, related_name="route")

    fancy_rendered =  models.TextField(blank=True, null=True)
    fallback_string = models.TextField(blank=True, null=True)
    simple_rendered = models.TextField(blank=True, null=True)
    kml_rendered =    models.TextField(blank=True, null=True)
    
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
            
        elif self.custom:
            return "custom: " + self.custom.identifier
            
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
    kml_rendered = []
    routebases = []
    p2p = []
    
    for i, ident in enumerate(points):
    
        if ident[0] == "@":  #must be a navaid
        
            first_rb = len(routebases) == 0  # is this the first routebase? if so don't try to guess which navaid is closest to the previous point
            if not first_rb and not routebases[i-1].unknown:
                routebase, rendered = find_navaid(ident, i, last_rb=routebases[i-1])
            else:
                routebase, rendered = find_navaid(ident, i)
        
        elif ident[0] == "!":  #must be custom
        
            routebase, rendered = find_custom(ident, i)
            
        else:                  #must be an airport
            
            routebase, rendered = find_airport(ident, i, p2p=p2p)
            
        ########################################################################
       
        if not routebase:                                           ## no routebase? must unknown
            routebase = RouteBase(unknown=ident, sequence=i)
            
            if not ident[0] == "@":                                         # not a unidentified navaid, assume a landing
                p2p.append(unknown)
                
            rendered['fancy'] = "<span class='not_found'>%s</span>" % ident
            rendered['simple'] = ident
            rendered['kml'] = ""            # unknown airports get ignored when mapping routes
            
        
        routebases.append(routebase)
        fancy_rendered.append(rendered["fancy"])
        simple_rendered.append(rendered["simple"])
        kml_rendered.append(rendered["kml"])
    
    fancy_rendered = "-".join(fancy_rendered)
    simple_rendered = "-".join(simple_rendered)
    kml_rendered = "\n".join(kml_rendered)
           
    is_p2p = len(set(p2p)) > 1
    route = Route(fancy_rendered=fancy_rendered, kml_rendered=kml_rendered, simple_rendered=simple_rendered, fallback_string=ostring, p2p=is_p2p)
    route.save()
    
    print("made new route")
    
    for routebase in routebases:
        routebase.route = route
        routebase.save()    
    
    return route

###########################################################
###########################################################    
        
def normalize(string):
    """removes all cruf away from the route string, returns only the
       alpha numeric characters with clean seperators"""
    
    import re
    string = string.upper()
    string = string.replace("LOCAL", " ")
    string = string.replace(" TO ", " ")
    return re.sub(r'[^A-Z0-9!@]+', ' ', string).strip()
    
def find_navaid(ident, i, last_rb=None):
    """Searches the database for the navaid object according to ident. if it finds a match,
       it renders the 'kml', 'fancy', and 'simple' strings, and then creates and returns the
       routebase object"""
           
    if last_rb:     #done just assume no
        navaid = Navaid.objects.filter(identifier=ident[1:])
        if navaid.count() > 1:                                                          #if more than 1 navaids come up,
            last_point = last_rb.airport or last_rb.navaid                              #run another query to find the nearest
            navaid = navaid.distance(last_point.location).order_by('distance')[0]  
        elif navaid.count() == 0:
            navaid = None
        else:
            navaid = navaid[0]
    else:
        navaid = get_object_or_None(Navaid, identifier=ident[1:])       # no previous routebases, 
                                                                        # dont other with the extra queries trying to find the nearest based on the last
        
    if navaid:
        routebase = RouteBase(navaid=navaid, sequence=i)
        fancy = "<span class='found_navaid' title='%s'>%s</span>" % (navaid.title_display(), navaid.line_display(), )
        simple = "@" + navaid.identifier
        kml = "%f,%f,0" % (navaid.location.x, navaid.location.y)
    else:
        routebase=None; fancy=None; simple=None; kml=None
        
    return routebase, {"fancy": fancy, "simple": simple, "kml": kml}
    
##############################################################################################

def find_custom(ident, i):
    """Tries to find the custom point, if it can't find one, it adds it to the user's
       custom list
    """
    user = threadlocals.get_current_user()
    custom,created = Custom.objects.get_or_create(user=user, identifier=ident[1:])

   
    routebase = RouteBase(custom=custom, sequence=i)
    fancy = "<span class='found_custom' title='%s'>%s</span>" % (custom.title_display(), custom.line_display(), )
    simple = "!" + custom.identifier
    
    if custom.location:
        kml = "%f,%f,0" % (custom.location.x, custom.location.y)
    else:
        kml = ""

        
    return routebase, {"fancy": fancy, "simple": simple, "kml": kml}

##############################################################################################

def find_airport(ident, i, p2p):
    airport = get_object_or_None(Airport, identifier=ident)
        
    if not airport and len(ident) == 3:                         # if the ident is 3 letters and no hit, try again with an added 'K'
        airport = get_object_or_None(Airport, identifier="K" + ident)

    if airport:
        routebase = RouteBase(airport=airport, sequence=i)
        p2p.append(airport.pk)          # a landing airport, eligable for p2p testing

        fancy = "<span class='found_airport' title='%s'>%s</span>" % (airport.title_display(), airport.line_display(), )
        simple = airport.identifier
        kml = "%f,%f,0" % (airport.location.x, airport.location.y)
    else:
        routebase=None; fancy=None; simple=None; kml=None
        
    return routebase, {"fancy": fancy, "simple": simple, "kml": kml}

