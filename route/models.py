import re

from django.contrib.gis.db import models
from django.db.models import Q

from annoying.functions import get_object_or_None
from share.middleware import share

from airport.models import Location

class Route(models.Model):
    """Represents a route the user went on for the flight
    
    >>> r=Route.from_string("!custom -> @hyp  //vta -= mer")
    >>> r
    <Route: CUSTOM-HYP-KVTA-MER>
    >>> r.kml_rendered
    '-120.400001526,37.2193984985\n-82.4617996216,40.0247001648'
    >>> r.fancy_rendered
    u'<span title="Custom" class="found_custom">CUSTOM</span>-<span title="El Nido - VOR-DME" class="found_navaid">HYP</span>-<span title="Newark, Ohio" class="found_airport">KVTA</span>-<span title="MER" class="not_found">MER</span>'
    >>>
    >>> vta=Airport.objects.get(identifier="KVTA")
    >>> vta.municipality = "CHANGED NAME"
    >>> vta.save()
    >>>
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
    
    overall_dist = models.FloatField(null=True, default=0)
    start_dist = models.FloatField(null=True, default=0)
    line_dist = models.FloatField(null=True, default=0)
    
    p2p = models.BooleanField()
    
    # a queryset of all airports, internal only
    a = None
    
    ##################################
    
    @classmethod
    def render_custom(cls, user):
        qs = cls.objects.filter(flight__user=user)\
                    .filter(routebase__location__loc_class=3)
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
    def hard_render_user(cls, user, username=""):
        if username:
            user=User.objects.get(username=username)
            
        qs = cls.objects.filter(user=user)
        for r in qs:
            r.hard_render()
        return qs.count()
    
    @classmethod
    def from_string(cls, r):
        return create_route_from_string(r)
    
    #################################
    
    def render_distances(self):
        a = self._get_Points()
        
        if not a:
            return ## nothing to measure from, keep the defaults
        
        self.start_dist = self.calc_start_dist(a)
    
    def _get_Points(self):
        if not self.a:
            self.a = Location.objects.filter(location__isnull=False,
                                             routebase__route=self).distinct()
        return self.a
    
    def calc_overall_dist(self, a):
        """returns the max distance between any two points in the
           route.a
        """
        
        mp = a.collect()
        ct = mp.envelope.centroid

        na = a.distance(ct)
        
        dist = []
        for p in na:
            dist.append(p.distance)
        
        #since we're measuring from the center, multiply by 2    
        diameter = max(dist) * 2
        
        return diameter.nm
    
    ################################
    
    def calc_start_dist(self, a):
        """Returns the max distance between any point in the route and the
           starting point. Used for ATP XC distance.
           
           >>> r=Route.from_string('kvta kuni')
           >>> r.start_distance()
           50.003471947098973
           >>> r=Route.from_string('kmer kvta')
           >>> r.start_distance()
           0.0
           >>> r=Route.from_string('kvta')
           >>> r.start_distance()
           0.0
           
        """
        
        mp = a.collect()
        start = a[0].location

        na = a.distance(start)
        
        dist = []
        for p in na:
            dist.append(p.distance)
            
        diameter = max(dist)
        
        return diameter.nm
    
    ################################
    
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
            loc_class = rb.get_loc_class()
            
            if loc_class == 1:
                class_ = "found_airport"
            elif loc_class == 2:
                class_ = "found_navaid"
            elif loc_class == 3:
                class_ = "found_custom"
            else:
                class_ = "not_found"
                
            #dont write a kml if no coordinates are known
            if getattr(dest, "location", None):
                kml.append("%s,%s" % (dest.location.x, dest.location.y), )
                
            if not rb.unknown:   
                fancy.append("<span title=\"%s\" class=\"%s\">%s</span>" %
                            (dest.title_display(), class_, dest.identifier ), )
                simple.append(rb.destination().identifier)
            else:
                fancy.append("<span title=\"%s\" class=\"%s\">%s</span>" %
                            (dest, class_, dest ), )
                simple.append(rb.destination())
            
        self.kml_rendered = "\n".join(kml)
        self.fancy_rendered = "-".join(fancy)
        self.simple_rendered = "-".join(simple)
        
        self.render_distances()
        
        self.save()
        
    def hard_render(self):
        """Recreate a new routebase set from the fallback_string, then
           re-render the variables
        """

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
        
    def as_listDEP(self):
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
                # .location will fail if the point is unknown.
                # Just skip this point if this happens
                pass
            
        return l

###############################################################################

class RouteBase(models.Model):
    
    route =    models.ForeignKey(Route)
    
    location =  models.ForeignKey(Location, null=True, blank=True)
    unknown =  models.CharField(max_length=30, blank=True, null=True)
    sequence = models.PositiveIntegerField()
    
    def __unicode__(self):
        
        loc_class = self.get_loc_class()
        
        if loc_class == 0:
            return "unknown: " + self.unknown
        
        elif loc_class == 1:
            return "airport: " + self.location.identifier
        
        elif loc_class == 2:
            return "navaid: " + self.location.identifier
            
        elif loc_class == 3:
            return "custom: " + self.location.identifier
            
    def destination(self):
        return self.location or self.unknown
    
    def get_loc_class(self):
        return getattr(self.destination(), "loc_class", 0)
    
###############################################################################  

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
       alpha numeric characters with clean seperators
    """
    
    import re
    string = string.upper()
    string = string.replace("LOCAL", " ")
    string = string.replace(" TO ", " ")
    return re.sub(r'[^A-Z0-9!@]+', ' ', string).strip()

###########################################################
########################################################### 
    
def find_navaid(ident, i, last_rb=None):
    """Searches the database for the navaid object according to ident.
       if it finds a match,returns the routebase object
    """
           
    if last_rb:
        navaid = Location.objects.filter(loc_class=2, identifier=ident[1:])
        #if more than 1 navaids come up,
        if navaid.count() > 1:
            #run another query to find the nearest
            last_point = last_rb.airport or last_rb.navaid 
            navaid = navaid.distance(last_point.location).order_by('distance')[0]  
        elif navaid.count() == 0:
            navaid = None
        else:
            navaid = navaid[0]
    else:
        # no previous routebases,
        # dont other with the extra queries trying to find the nearest 
        # based on the last
        navaid = get_object_or_None(Location, loc_class=2,
                                              identifier=ident[1:])
    if navaid:
        return RouteBase(location=navaid, sequence=i)
    
    return None
    
###############################################################################

def find_custom(ident, i, force=False):
    """Tries to find the custom point, if it can't find one, and force = True,
       it adds it to the user's custom list.
    """
    
    user = share.get_display_user()
    if force:
        cu,cr = Location.objects.get_or_create(user=user,
                                              loc_class=3,
                                              identifier=ident)
    else:
        cu = get_object_or_None(Location, loc_class=3,
                                          user=user,
                                          identifier=ident)

    if cu:
        return RouteBase(location=cu, sequence=i)
    else:
        return None

###############################################################################

def find_airport(ident, i, p2p):
    airport = get_object_or_None(Location, loc_class=1, identifier=ident)
        
    if not airport and len(ident) == 3:
        # if the ident is 3 letters and no hit, try again with an added 'K'
        airport = get_object_or_None(Location, loc_class=1,
                                               identifier="K%s" % ident)

    if airport:
        # a landing airport, eligable for p2p testing
        p2p.append(airport.pk)          
        return RouteBase(location=airport, sequence=i)
    
    return None

def make_routebases_from_fallback_string(route):
    """returns a list of RouteBase objects according to the fallback_string,
    basically hard_render()
    """
    
    fbs = normalize(route.fallback_string)
    points = fbs.split()                        # MER-VGA -> ['MER', 'VGA']
    unknown = False
    p2p = []
    routebases = []
    
    for i, ident in enumerate(points):
    
        if ident[0] == "@":  #must be a navaid
            # is this the first routebase? if so don't try to guess which
            # navaid is closest to the previous point
            
            first_rb = len(routebases) == 0  
            if not first_rb and not routebases[i-1].unknown:
                routebase = find_navaid(ident, i, last_rb=routebases[i-1])
            else:
                routebase = find_navaid(ident, i)
        
        elif ident[0] == "!":  #must be custom
            # force=True means if it can't find the 'custom', then make it
            routebase = find_custom(ident[1:], i, force=True)
            
        else:                  #must be an airport
            
            routebase = find_airport(ident, i, p2p=p2p)
            if not routebase:
                # if the airport can't be found, see if theres a 'custom'
                # bythe same identifier
                routebase = find_custom(ident, i, force=False)
            
        #######################################################################
       
        # no routebase? must be unknown
        if not routebase:
            routebase = RouteBase(unknown=ident, sequence=i)
            
            # not a unidentified navaid, assume a landing
            if not ident[0] == "@":
                p2p.append(ident)
        
        routebases.append(routebase)

    return len(set(p2p)) > 1, routebases
