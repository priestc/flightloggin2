import re

from django.db import models
from django.db.models import Q

from annoying.functions import get_object_or_None
from share.middleware import share

from airport.models import Airport, Custom, Navaid

class Route(models.Model):
    """Represents a route the user went on for the flight
    
    >>> r=Route.from_string("!custom -> @hyp  //vta -= mer")
    >>> r
    <Route: CUSTOM-HYP-KVTA-MER>
    >>> r.fancy_rendered
    u'<span title="Custom" class="found_custom">CUSTOM</span>-<span title="El Nido - VOR-DME" class="found_navaid">HYP</span>-<span title="Newark, Ohio" class="found_airport">KVTA</span>-<span title="MER" class="not_found">MER</span>'
    >>> vta=Airport.objects.get(identifier="KVTA")
    >>> vta.municipality = "CHANGED NAME"
    >>> vta.save()
    >>> r.easy_render()
    >>> r.fancy_rendered
    u'<span title="Custom" class="found_custom">CUSTOM</span>-<span title="El Nido - VOR-DME" class="found_navaid">HYP</span>-<span title="CHANGED NAME, Ohio" class="found_airport">KVTA</span>-<span title="MER" class="not_found">MER</span>'
    >>>
    >>> vta.delete()
    >>> vta.pk = 1000
    >>> vta.save()
    >>>
    >>> r.hard_render()
    >>> r.fancy_rendered
    u'<span title="Custom" class="found_custom">CUSTOM</span>-<span title="El Nido - VOR-DME" class="found_navaid">HYP</span>-<span title="CHANGED NAME, Ohio" class="found_airport">KVTA</span>-<span title="MER" class="not_found">MER</span>'
    >>>
    >>> vta = r.routebase_set.all()[2].airport
    >>> vta
    <Airport: KVTA>
    >>> vta.id
    1000
    """

    fancy_rendered =  models.TextField(blank=True, null=True)
    fallback_string = models.TextField(blank=True, null=True)
    simple_rendered = models.TextField(blank=True, null=True)
    kml_rendered =    models.TextField(blank=True, null=True)
    
    p2p = models.BooleanField()
    
    ##################################
    
    @classmethod
    def render_custom(cls, user):
        qs = cls.objects.filter(flight__user=user).filter(routebase__custom__isnull=False)
        for r in qs:
            r.easy_render()
        return qs.count()
    
    @classmethod
    def easy_render_all(cls):
        qs = cls.objects.all()
        for r in qs:
            r.easy_render()
        return qs.count()
    
    @classmethod
    def hard_render_all(cls):
        qs = cls.objects.all()
        for r in qs:
            r.hard_render()
        return qs.count()
    
    @classmethod
    def from_string(cls, r):
        return create_route_from_string(r)
    
    #################################
    
    def easy_render(self):
        """Rerenders the HTML for displaying the route. Takes info from the
           already defines routebases. For rerendering after updating Airport
           info, use hard_render()
        """
        fancy = []
        simple = []
        kml = []
        
        for rb in self.routebase_set.all().order_by('sequence'):
            
            dest = rb.destination()
            
            if rb.airport:
                class_ = "found_airport"
            elif rb.navaid:
                class_ = "found_navaid"
            elif rb.custom:
                class_ = "found_custom"
            else:
                class_ = "not_found"
                
            if getattr(dest, "location", None):       #dont write a kml if no coordinates are known
                kml.append("%s,%s" % (dest.location.x, dest.location.y), )
                
            if not rb.unknown:   
                fancy.append("<span title=\"%s\" class=\"%s\">%s</span>" % (dest.title_display(), class_, dest.identifier ), )
                simple.append(rb.destination().identifier)
            else:
                fancy.append("<span title=\"%s\" class=\"%s\">%s</span>" % (dest, class_, dest ), )
                simple.append(rb.destination())
            
        self.kml_rendered = "\n".join(kml)
        self.fancy_rendered = "-".join(fancy)
        self.simple_rendered = "-".join(simple)
        self.save()
        
    def hard_render(self):

        flight = self.flight
        fbs = self.fallback_string
        
        is_p2p, routebases = make_routebases_from_fallback_string(self)
        
        self.p2p = is_p2p
        
        #delete the current routebases, then add the new ones
        self.routebase_set.all().delete()
        for routebase in routebases:
            routebase.route = self
            routebase.save()
            
        self.easy_render()
    
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
                pass                # .location will fail if the point is unknown. Just skip this point if this happens
            
        return l

#####################################################################################################

class RouteBase(models.Model):
    route =    models.ForeignKey(Route)
    
    airport =  models.ForeignKey(Airport, null=True, blank=True)
    navaid =   models.ForeignKey(Navaid, null=True, blank=True)
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
            
        elif self.custom:
            return "custom: " + self.custom.identifier
            
        else:
            return "????"
            
    def destination(self):
        return self.airport or self.navaid or self.custom or self.unknown
    
######################################################################################################  

def create_route_from_string(fallback_string):
   
    if not fallback_string:
        return None
    
    route = Route(fallback_string=fallback_string, p2p=False)
    route.save()
    
    is_p2p, routebases = make_routebases_from_fallback_string(route)
    
    route.p2p = is_p2p
    
    for routebase in routebases:
        routebase.route = route
        routebase.save()
        
    route.easy_render()
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

###########################################################
########################################################### 
    
def find_navaid(ident, i, last_rb=None):
    """Searches the database for the navaid object according to ident. if it finds a match,
       returns the routebase object"""
           
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
        return RouteBase(navaid=navaid, sequence=i)
    
    return None
    
##############################################################################################

def find_custom(ident, i):
    """Tries to find the custom point, if it can't find one, it adds it to the user's
       custom list
    """
    user = share.get_display_user()
    custom,created = Custom.objects.get_or_create(user=user, identifier=ident[1:])

    routebase = RouteBase(custom=custom, sequence=i)

    return routebase

##############################################################################################

def find_airport(ident, i, p2p):
    airport = get_object_or_None(Airport, identifier=ident)
        
    if not airport and len(ident) == 3:                         # if the ident is 3 letters and no hit, try again with an added 'K'
        airport = get_object_or_None(Airport, identifier="K" + ident)

    if airport:
        p2p.append(airport.pk)          # a landing airport, eligable for p2p testing
        return RouteBase(airport=airport, sequence=i)

    return None

def make_routebases_from_fallback_string(route):
    """returns a list of RouteBase objects according to the fallback_string"""
    
    fbs = normalize(route.fallback_string)
    points = fbs.split()                        # MER-VGA -> ['MER', 'VGA']
    unknown = False
    p2p = []
    routebases = []
    
    for i, ident in enumerate(points):
    
        if ident[0] == "@":  #must be a navaid
        
            first_rb = len(routebases) == 0  # is this the first routebase? if so don't try to guess which navaid is closest to the previous point
            if not first_rb and not routebases[i-1].unknown:
                routebase = find_navaid(ident, i, last_rb=routebases[i-1])
            else:
                routebase = find_navaid(ident, i)
        
        elif ident[0] == "!":  #must be custom
        
            routebase = find_custom(ident, i)
            
        else:                  #must be an airport
            
            routebase = find_airport(ident, i, p2p=p2p)
            
        ########################################################################
       
        if not routebase:                                           # no routebase? must be unknown
            routebase = RouteBase(unknown=ident, sequence=i)
            
            if not ident[0] == "@":                                 # not a unidentified navaid, assume a landing
                p2p.append(ident)
        
        routebases.append(routebase)

    return len(set(p2p)) > 1, routebases
