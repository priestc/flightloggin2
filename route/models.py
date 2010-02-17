import re

from django.contrib.gis.db import models
from django.db.models import Q

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
        
        loc_class = self.loc_class
        
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
    
    def custom(self):
        """
        Returns true if the location is a custom identifier
        """
        
        return self.location.loc_class == 3
        
    def destination(self):
        """
        Returns the location object, or a string that represents the
        identifier if unknown
        """
        
        return self.location or self.unknown
    
    @property
    def loc_class(self):
        """
        return the type of location, zero if it has no location
        """
        
        return getattr(self.destination(), "loc_class", 0)
    
    def admin_loc_class(self):
        try:
            return getattr(self.destination(), "get_loc_class_display")() 
        except:
            return "Unknown"
    
    def owner(self):
        """
        Return the owner of the routebase. Only used in the admin
        """
        
        try:
            return self.route.flight.all()[0].user.username
        except IndexError:
            return "not connected to any flights"
    
###############################################################################

from main.queryset_manager import QuerySetManager

class Route(models.Model):
    """
    Represents a route the user went on for the flight
    """
    
    ## add custom filters to custom manager
    from queryset_manager import RouteQuerySet as QuerySet
    objects = QuerySetManager()        ## add custom filterset manager

    fancy_rendered =  models.TextField(blank=True, null=True)
    fallback_string = models.TextField(blank=True, null=True)
    simple_rendered = models.TextField(blank=True, null=True)
    kml_rendered =    models.TextField(blank=True, null=True)
    
    max_width_all =   models.FloatField(null=True, default=0)
    max_width_land =  models.FloatField(null=True, default=0)
    
    max_start_all =   models.FloatField(null=True, default=0)
    max_start_land =  models.FloatField(null=True, default=0)
    
    total_line_all =  models.FloatField(null=True, default=0)
    total_line_land = models.FloatField(null=True, default=0)
    
    p2p = models.BooleanField(default=False)
    
    # a queryset of all landing points and all points, internal only
    land_points = None
    all_points = None
    
    def __unicode__(self):
        return self.simple_rendered or "Empty"
    
    def owner(self):
        """
        Return the owner of the route. Only used in the admin
        """
        
        try:
            return self.flight.all()[0].user.username
        except IndexError:
            return "??"
    
    ##################################
    
    @classmethod
    def get_profiles(cls, val, field):
        """
        Returns the profiles of the users who have flown in this
        route
        """
        
        kwarg = {"user__flight__route__%s__iexact" % field: val}
        
        from profile.models import Profile
        return Profile.objects\
                   .filter(**kwarg)\
                   .filter(social=True)\
                   .values('user__username', 'user__id', 'logbook_share')\
                   .order_by('user__username')\
                   .distinct()
    
    
    @classmethod
    def render_custom(cls, user):
        qs = cls.objects.filter(flight__user=user)\
                    .filter(routebase__location__loc_class=3)
        for r in qs:
            r.easy_render()
        return qs.count()
    
    @classmethod
    def easy_render_all(cls):
        """
        Re-renders ALL instances of Routes in the database. Easy render
        is not an expensive operation (relatively), so this isn't
        needing to be done in patches like hard_render.
        """
        
        from multiprocessing import Process

        qs = cls.objects.order_by('-id')
        
        def chunks(l, n):
            for i in xrange(0, len(l), n):
                yield l[i:i+n]
     
        def actor(chunk):
            for r in chunk:
                r.easy_render()
     
        a=0
        for chunk in chunks(qs, 500):
            print "CHUNK----", a
            
            p = Process(target=actor, args=(chunk,))
            p.start()
            p.join()
            
            a += 1
            
            
    
    @classmethod
    def hard_render_user(cls, username=None, user=None, no_dupe=True):
        """
        Hard re-render all routes for the given username
        """
        
        if username:
            from django.contrib.auth.models import User
            user=User.objects.get(username=username)
        
        kwargs = {'flight__user': user}
        
        if no_dupe:
            # only apply to routes that have zero routebases. Routes with no
            # routebases occur after all locations are deleted (which often
            # happens when the locations database is updated)
            kwargs.update({'routebase__isnull': True})
            
        from django.db.models import Max
        qs = cls.objects.filter(**kwargs)\
                        .distinct()\
                        .annotate(fid=Max('flight__id'))
        for r in qs:
            r.hard_render(user=user, flight_id=r.fid)
            
        return qs.count()
    
    @classmethod
    def hard_render_unknowns(cls):
        routes = cls.objects.filter(routebase__unknown__isnull=False)
        
        for r in routes:
            r.hard_render()
    
    @classmethod
    def from_string(cls, raw_route_string, user=None):
        """
        Create a route object from a waw string
        """
        
        # so we know which user to make the custom points from
        # if no user explicitly given, try to get the currently logged in user
        if not user:
            user = share.get_display_user()
            
        return MakeRoute(raw_route_string, user=user).get_route()
    
    #################################
    
    def render_distances(self):
        all_points = self._get_AllPoints()
        
        if not all_points or all_points.count() == 1:
            return ## nothing to measure, keep the defaults
        
        land_points = self._get_LandingPoints()
        
        self.max_start_all = self.calc_max_start(all_points)
        self.max_start_land = self.calc_max_start(land_points)
        
        self.max_width_all = self.calc_max_width(all_points)
        self.max_width_land = self.calc_max_width(land_points)
        
        self.total_line_all = self.calc_total_line(points="all")
        self.total_line_land = self.calc_total_line(points="land")
        
    #################################
    
    def _get_LandingPoints(self):
        """
        return a queryset containing all points where a landing took place.
        """
        
        if not self.land_points:
            self.land_points = Location.objects.filter(
                    location__isnull=False,    # has valid coordinates
                    routebase__route=self,     # is connected to this route
                    routebase__land=True,      # depicts a landing
            ).distinct()
            
        return self.land_points
    
    def _get_AllPoints(self):
        """
        Return a queryset of all points, regardless whether a landing
        was done there or not
        """
        
        if not self.all_points:
            self.all_points = Location.objects.filter(
                    location__isnull=False,
                    routebase__route=self,
            ).distinct()
            
            #self.line_kml = self.all_points.make_line().kml
            
        return self.all_points
    
    def calc_max_width(self, a=None):
        """
        returns the max distance between any two points in the route
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
    
    def get_users(self):
        """
        Returns all users who have flown this exact route
        """
        
        from django.contrib.auth.models import User
        return User.objects.filter(profile__social=True)\
                   .filter(flight__route__simple_rendered=self.simple_rendered)
    
    ################################
    
    def calc_max_start(self, a=None):
        """
        Returns the max distance between any point in the route and the
        starting point. Used for ATP XC distance.
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
    
    def calc_total_line(self, points="all"):
        """
        returns the distance between each point in the route
        """
        
        rbs = self.routebase_set.order_by('sequence')          
            
        if points == "land":
            rbs = rbs.exclude(land=False)
        
        # convert to [(lat,lng), ...] while maintaining the same order
        # skipping any routebase that has no location
        points = [(rb.location.location.x, rb.location.location.y)
                        for rb in rbs if rb.location and rb.location.location]
        
        dist = []
        from utils import coord_dist
        for i,po in enumerate(points):
            try:
                next = points[1+i]
            except IndexError:
                pass
            else:
                from django.contrib.gis.geos import Point
                dist.append(coord_dist(Point(po), Point(next)))
         
        return sum(dist)
    
    ################################
    
    def easy_render(self):
        """
        Rerenders the HTML for displaying the route. Takes info from the
        already defines routebases. For rerendering after updating Airport
        info, use hard_render() 120414 210991
        problem: 169668
        """
        
        fancy = []
        simple = []
        kml = []
        
        rbs = self.routebase_set.all().order_by('sequence')
        
        if not rbs:
            # a route was made, but no routebases were attached, must
            # be a local flight
            simple = ["Local"]
            fancy = ["<span title='Local Flight' class='local'>Local</span>"]
        
        for rb in rbs:
            
            dest = rb.destination()
            loc_class = rb.loc_class
            
            if loc_class == 1:
                class_ = "found_airport"
            elif loc_class == 2:
                class_ = "found_navaid"
            elif loc_class == 3:
                class_ = "found_custom"
            elif loc_class == 0:
                class_ = "not_found"
                
            if not rb.land:
                class_ += " noland"
            else:
                class_ += " land"
                
            # only write a kml if coordinates are known
            if getattr(dest, "location", None):
                kml.append("%s,%s" % (dest.location.x, dest.location.y), )
                
            if loc_class > 0:   
                fancy.append("<span title=\"%s\" class=\"%s\">%s</span>" %
                            (dest.title_display(), class_, dest.identifier ), )
                simple.append(rb.destination().identifier)
                
            elif loc_class == 0:
                fancy.append("<span title=\"%s\" class=\"%s\">%s</span>" %
                            (dest, class_, dest ), )
                simple.append(rb.destination())
            
        self.kml_rendered = "\n".join(kml)
        self.fancy_rendered = "-".join(fancy)
        self.simple_rendered = "-".join(simple)
        
        self.render_distances()
        
        self.save()
        
    def hard_render(self, user=None, username=None, flight_id=None):
        """
        Spawns a new Route object based on it's own fallback_string,
        connects it to the flight that the old route was connected to.
        Then returns the newly created Route instance. This is used to
        redo all the routebases after the navaid/airport database has been
        updated and all the primary keys are changed.
        """
        
        if not flight_id:
            try:
                f = self.flight.all()[0]
                
            except IndexError:  
                # no flight associated with this route
                pass
            
            else:
                flight_id = f.id
                user = f.user
            
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
    """
    creates a route object from a string. The constructor takes a user
    instance because it needs to know which "namespace" to use for
    looking up custom places.
    """
    
    def __init__(self, fallback_string, user):
        self.user=user
       
        if not fallback_string:     #return empty route
            self.route = Route()
            self.route.save()
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
        """
        removes all cruf away from the route string, returns only the
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
        """
        Searches the database for the navaid object according to ident.
        if it finds a match, creates and returns a routebase object
        """
               
        if last_rb:
            navaid = Location.objects.filter(loc_class=2, identifier=ident)
            #if more than 1 navaids come up,
            if navaid.count() > 1:
                #run another query to find the nearest
                last_point = last_rb.location 
                navaid = navaid.distance(last_point.location)\
                               .order_by('distance')[0]
                               
            elif navaid.count() == 0:
                navaid = None
            else:
                navaid = navaid[0]
        else:
            # no previous routebases,
            # dont other with the extra queries trying to find the nearest 
            # based on the last
            navaid = Location.goon(loc_class=2,
                                   identifier=ident)
        if navaid:
            return RouteBase(location=navaid, sequence=i)
        else:
            # wasn't a navaid, maybe it was an airport that they flew over?
            return self.find_airport(ident, i)
        
        return None
        
    ###########################################################################

    def find_custom(self, ident, i, force=False):
        """
        Tries to find the custom point, if it can't find one, and
        force = True, it adds it to the user's custom list.
        """
        
        ident = ident[:8]
        
        if force:
            cu,cr = Location.objects.get_or_create(user=self.user,
                                                  loc_class=3,
                                                  identifier=ident)
        else:
            cu = Location.goon(loc_class=3,
                               user=self.user,
                               identifier=ident)

        if cu:
            return RouteBase(location=cu, sequence=i)
        else:
            return None

    ###########################################################################

    def find_airport(self, ident, i):
        airport = Location.goon(loc_class=1, identifier=ident)
            
        if not airport and len(ident) == 3:
            # if the ident is 3 letters and no hit, try again with an added 'K'
            airport = Location.goon(loc_class=1,
                                    identifier="K%s" % ident)

        if airport:
            return RouteBase(location=airport, sequence=i)
        
        return None

    def make_routebases_from_fallback_string(self, route):
        """
        returns a list of RouteBase objects according to the fallback_string,
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
                routebase = self.find_airport(ident, i)
                if not routebase:
                    # if the airport can't be found, see if theres a 'custom'
                    # by the same identifier
                    routebase = self.find_custom(ident, i, force=False)
                
            #######################################################################
           
            # no routebase? must be unknown
            if not routebase:
                routebase = RouteBase(unknown=ident, sequence=i)
            
            routebase.land = land
            routebases.append(routebase)
            
            if land:
                loc = routebase.location or ident
                p2p.append(loc)

        return len(set(p2p)) > 1, routebases
