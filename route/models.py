import re

from django.contrib.gis.db import models
from django.db.models import Q

from annoying.functions import get_object_or_None
from share.middleware import share

from airport.models import Location

###############################################################################

class RouteBase(models.Model):
    
    route =    models.ForeignKey("Route")
    
    location =  models.ForeignKey(Location, null=True, blank=True)
    unknown =  models.CharField(max_length=30, blank=True, null=True)
    sequence = models.PositiveIntegerField()
    
    land = models.BooleanField()
    
    def __unicode__(self):
        
        loc_class = self.get_loc_class()
        
        if loc_class == 0:
            ret = "unknown: %s" % self.unknown
        
        elif loc_class == 1:
            ret = "airport: %s" % self.location.identifier
        
        elif loc_class == 2:
            ret = "navaid: %s" % self.location.identifier
            
        elif loc_class == 3:
            ret = "custom: %s" % self.location.identifier
        
        if not self.land:
            ret = ret + " (NO LAND)"
            
        return ret
        
    def destination(self):
        return self.location or self.unknown
    
    def get_loc_class(self):
        return getattr(self.destination(), "loc_class", 0)
    
###############################################################################

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
    >>> vta = r.routebase_set.all()[2].location
    >>> vta
    <Location: KVTA>
    >>> vta.id
    1000
    """

    fancy_rendered =  models.TextField(blank=True, null=True)
    fallback_string = models.TextField(blank=True, null=True)
    simple_rendered = models.TextField(blank=True, null=True)
    kml_rendered =    models.TextField(blank=True, null=True)
    
    max_width_all = models.FloatField(null=True, default=0)
    max_width_land = models.FloatField(null=True, default=0)
    
    max_start_all = models.FloatField(null=True, default=0)
    max_start_land = models.FloatField(null=True, default=0)
    
    max_line_all = models.FloatField(null=True, default=0)
    max_line_land = models.FloatField(null=True, default=0)
    
    p2p = models.BooleanField()
    
    # a queryset of all landing points and all points, internal only
    land_points = None
    all_points = None
    
    def __unicode__(self):
        return self.simple_rendered or "err"
    
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
        """Re-renders ALL instances of Routes in the database. Easy render
           is not an expensive operation (relatively), so this isn't
           needing to be done in patches like hard_render.
        """
        qs = cls.objects.all()
        for r in qs:
            r.easy_render()
        return qs.count()
    
    @classmethod
    def hard_render_user(cls, user=None, username=None):
        if username:
            from django.contrib.auth.models import User
            user=User.objects.get(username=username)
            
        from django.db.models import Max
        qs = cls.objects.filter(flight__user=user).annotate(fid=Max('flight__id'))
        for r in qs:
            r.hard_render(user=user, flight_id=r.fid)
            
        return qs.count()
    
    @classmethod
    def from_string(cls, r, user=None):
        # so we know which user to make the custom points from
        # if no user explicitly given, try t get the currently logged in user
        if not user:
            user = share.get_display_user()
            
        return MakeRoute(r, user=user).get_route()
    
    #################################
    
    def render_distances(self):
        all_points = self._get_AllPoints()
        
        if not all_points:
            return ## nothing to measure, keep the defaults
        
        land_points = self._get_LandingPoints()
        
        self.all_start_dist = self.calc_start_dist(all_points)
        self.start_dist = self.calc_start_dist(land_points)
        
        self.all_overall_dist = self.calc_overall_dist(all_points)
        self.overall_dist = self.calc_overall_dist(land_points)
        
        self.all_line_dist = self.calc_line_dist(all_points)
        self.line_dist = self.calc_line_dist(land_points)
        
    #################################
    
    def _get_LandingPoints(self):
        """return a queryset containing all points where a landing took
           place.
        """
        
        if not self.land_points:
            self.land_points = Location.objects.filter(
                    location__isnull=False,    # has valid coordinates
                    routebase__route=self,     # is connected to this route
                    routebase__land=True,      # depicts a landing
            ).distinct()
            
        return self.land_points
    
    def _get_AllPoints(self):
        """return a queryset of all points, regardless whether a landing
           was done there or not
        """
        
        if not self.all_points:
            self.all_points = Location.objects.filter(
                    location__isnull=False,
                    routebase__route=self,
            ).distinct()
            
            self.line_kml = self.all_points.make_line().kml
            
        return self.all_points
    
    def calc_overall_dist(self, a=None):
        """returns the max distance between any two points in the
           route.a
        """
        
        if not a:
            a = self._get_AllPoints()
        
        mp = a.collect()
        ct = mp.envelope.centroid
        
        dist = []
        from utils import coord_dist
        for i,po in enumerate(mp): 
            dist.append(coord_dist(po, ct))
        
        #since we're measuring from the center, multiply by 2    
        diameter = max(dist) * 2
        
        return diameter
    
    ################################
    
    def calc_start_dist(self, a=None):
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
        
        if not a:
            a = self._get_AllPoints()
        
        mp = a.collect()
        start = a[0].location
        
        dist = []
        from utils import coord_dist
        for i,po in enumerate(mp):
            dist.append(coord_dist(po, start))
         
        return max(dist)
    
    def calc_line_dist(self, a=None):
        """returns the distance between each point in the route"""
        if not a:
            a = self._get_AllPoints()
            
        ls = a.make_line()
        
        dist = []
        from utils import coord_dist
        for i,po in enumerate(ls):
            try:
                next = ls[1+i]
            except:
                pass
            else:
                from django.contrib.gis.geos import Point
                dist.append(coord_dist(Point(po), Point(next)))
         
        return sum(dist)
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
        
    def hard_render(self, user=None, username=None, flight_id=None):
        """Spawns a new Route object from itself, and connects it to
           the flight that the old route was connected to. And then returns the
           newly created Route instance
        """
        if not flight_id:
            try:
                flight_id = self.flight.all()[0].id
            except IndexError:  #no flight associated with this route
                pass
            
        if (not user) and username:
            from django.contrib.auth.models import User
            user = User.objects.get(username=username)
            
        if not user and not username:
            user = share.get_display_user()
        
        new_route = MakeRoute(self.fallback_string, user).get_route()
        
        if flight_id:
            from logbook.models import Flight
            flight = Flight.objects.get(pk=flight_id)
            flight.route = new_route
            flight.save()
        
        return new_route
    
###############################################################################
  
class MakeRoute(object):
    """creates a route object from a string. The constructor takes a user
       instance because it needs to know which "namespace" to use for
       looking up custom places.
    """
    
    def __init__(self, fallback_string, user):
        self.user=user
       
        if not fallback_string:
            self.route = None
            return None
        
        route = Route(fallback_string=fallback_string, p2p=False)
        route.save()
        
        is_p2p, routebases = self.make_routebases_from_fallback_string(route)
        
        route.p2p = is_p2p
        
        for routebase in routebases:
            routebase.route = route
            routebase.save()
            
        route.easy_render()
        
        self.route = route
    
    def get_route(self):
        return self.route
    
    ###########################################################
    ###########################################################
   
            
    def normalize(self, string):
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
        
    def find_navaid(self, ident, i, last_rb=None):
        """Searches the database for the navaid object according to ident.
           if it finds a match,returns the routebase object
        """
               
        if last_rb:
            navaid = Location.objects.filter(loc_class=2, identifier=ident)
            #if more than 1 navaids come up,
            if navaid.count() > 1:
                #run another query to find the nearest
                last_point = last_rb.location 
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
                                                  identifier=ident)
        if navaid:
            return RouteBase(location=navaid, sequence=i)
        
        return None
        
    ###############################################################################

    def find_custom(self, ident, i, force=False):
        """Tries to find the custom point, if it can't find one, and force = True,
           it adds it to the user's custom list.
        """
        
        if force:
            cu,cr = Location.objects.get_or_create(user=self.user,
                                                  loc_class=3,
                                                  identifier=ident)
        else:
            cu = get_object_or_None(Location, loc_class=3,
                                              user=self.user,
                                              identifier=ident)

        if cu:
            return RouteBase(location=cu, sequence=i)
        else:
            return None

    ###############################################################################

    def find_airport(self, ident, i, p2p):
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

    def make_routebases_from_fallback_string(self, route):
        """returns a list of RouteBase objects according to the fallback_string,
        basically hard_render()
        """
        
        fbs = self.normalize(route.fallback_string)
        points = fbs.split()                        # MER-VGA -> ['MER', 'VGA']
        unknown = False
        p2p = []
        routebases = []
        
        for i, ident in enumerate(points):
        
            if "@" in ident:        # "@" means we didn't land
                land = False
            else:
                land = True
                
            if "!" in ident:        # "!" means it's a custom place
                custom = True
            else:
                custom = False
                
            #replace all the control characters now that we know their purpose
            ident = ident.replace('!','').replace('@','')
                
            if not land and not custom:     # must be a navaid
                # is this the first routebase? if so don't try to guess which
                # navaid is closest to the previous point
                
                first_rb = len(routebases) == 0  
                if not first_rb and not routebases[i-1].unknown:
                    routebase = self.find_navaid(ident, i, last_rb=routebases[i-1])
                else:
                    routebase = self.find_navaid(ident, i)
            
            elif custom:
                # force=True means if it can't find the 'custom', then make it
                routebase = self.find_custom(ident, i, force=True)
                
            else:                  #must be an airport  
                routebase = self.find_airport(ident, i, p2p=p2p)
                if not routebase:
                    # if the airport can't be found, see if theres a 'custom'
                    # bythe same identifier
                    routebase = self.find_custom(ident, i, force=False)
                
            #######################################################################
           
            # no routebase? must be unknown
            if not routebase:
                routebase = RouteBase(unknown=ident, sequence=i)
                
                # not a unidentified navaid, assume a landing
                if not ident[0] == "@":
                    p2p.append(ident)
            
            routebase.land = land
            routebases.append(routebase)

        return len(set(p2p)) > 1, routebases
