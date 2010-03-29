from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.conf import settings

from plane.models import Plane
from route.models import Route
from constants import *
from utils import to_minutes
from fuel_burn import FuelBurn

from main.enhanced_model import QuerySetManager, EnhancedModel
from queryset_manager import FlightQuerySet


class Flight(EnhancedModel):

    objects =  QuerySetManager(FlightQuerySet)

    date =     models.DateField()
    user =     models.ForeignKey(User, blank=False, editable=False)
    remarks =  models.TextField(blank=True)

    plane =    models.ForeignKey(Plane, default=settings.UNKNOWN_PLANE_ID)
    
    route_string = models.TextField(blank=True, null=True)
    route =    models.ForeignKey(Route, related_name="flight")

    total =    models.FloatField("Total Time",            default=0)
    pic =      models.FloatField("PIC",                   default=0)
    sic =      models.FloatField("SIC",                   default=0)
    solo =     models.FloatField("Solo",                  default=0)
    night =    models.FloatField("Night",                 default=0)
    dual_r =   models.FloatField("Dual Received",         default=0)
    dual_g =   models.FloatField("Dual Given",            default=0)
    xc =       models.FloatField("Cross Country",         default=0)
    act_inst = models.FloatField("Actual Instrument",     default=0)
    sim_inst = models.FloatField("Simulated Instrument",  default=0)
    
    night_l =  models.PositiveIntegerField("Night Landings", default=0, null=False)
    day_l =    models.PositiveIntegerField("Day Landings",   default=0, null=False)
    app =      models.PositiveIntegerField("Approaches",     default=0, null=False)
    
    fuel_burn =         models.CharField("Fuel Burn", max_length=10, blank=True, null=True)

    holding =           models.BooleanField(                           default=False)
    tracking =          models.BooleanField("Intercepting & Tracking", default=False)
    pilot_checkride =   models.BooleanField("Pilot Checkride",         default=False)
    cfi_checkride =     models.BooleanField("CFI Checkride",           default=False)
    flight_review =     models.BooleanField("Flight Review",           default=False)
    ipc =               models.BooleanField("IPC",                     default=False)

    person =   models.CharField( max_length=60, blank=True, null=True)
    
    #### inner values below, not directly editable by users
    
    speed = models.FloatField("Speed", default=None, null=True)
    gallons = models.FloatField("Gallons", default=None, null=True)
    gph = models.FloatField("Gallons Per Hour", default=None, null=True)
    mpg = models.FloatField("Miles Per Gallon", default=None, null=True)
    
    class Meta:
        ordering = ["-id"]
        get_latest_by = 'date'
        
    def __unicode__(self):
        return u"%s -- %s" % (self.date, self.remarks)
    
    @models.permalink
    def get_absolute_url(self):
        """
        All perma links for each flight instance point to the owner user's
        logbook page
        """
        
        return ('logbook', [self.user.username])
    
    def save(self, *args, **kwargs):
        try:
            getattr(self, "user", None).username
        except:
            #user is not set, we now must get the current logged in user
            from share.middleware import share
            self.user = share.get_display_user()
        
        super(Flight,self).save(*args, **kwargs)
    
    @classmethod
    def render_airport(cls, airport=None, **filters):
        """
        Grab all flights to the passed in airport, and re-render them.
        This function is used to update routes when an identifier profile
        has changed.
        """
        
        from termcolor import colored
        
        if airport:
            flights = cls.objects.filter(route_string__icontains=airport)
        else:
            flights = cls.objects.filter(**filters)
                     
        for f in flights.order_by('-date').iterator():
            date = colored(f.date, 'blue')
            route = colored(f.route_string, 'blue', attrs=['bold'])
            print('{2}: {0} {1}'.format(date, route, f.user))
            f.render_route()
    
    def render_route(self):
        self.route = Route.from_string(self.route_string,
                                       user=self.user,
                                       date=self.date)
        self.save()
        
    def route_is_rendered(self):
        try:
            return self.route
        except:
            return False
        
    def conditions_of_flight(self):
        fields = ['pic', 'act_inst', 'sic', 'dual_g', 'dual_r', 'night']
        l = [FIELD_ABBV[field] for field in fields if self.column(field)]
        
        return ", ".join(l)
            
        
    def disp_app(self):
        if self.app == 0:
           app = ""
        else:
           app = str(self.app)
        
        if (self.holding or self.tracking) and self.app:
            app += " "
        
        if self.holding:
            app += "H"
            
        if self.tracking:
            app += "T"
                
        return app 
    
    def disp_events(self):
        """Returns the special events with HTML formatting, if no events,
        return nothing
        """
        
        ret = ""
        
        if self.ipc:
            ret += "[IPC]"
            
        if self.pilot_checkride:
            ret += "[Pilot Checkride]"
            
        if self.cfi_checkride:
            ret += "[Instructor Checkride]"
            
        if self.flight_review:
            ret += "[Flight Review]"
            
        if not ret:
            return ""
        else:    
            return mark_safe('<span class="remarks_tag">%s</span> ' % ret)

    def column(self, cn, format="decimal", ret=0.0):
        """Returns a string that represents the column being passed
        All output in strings except for date, which will be formatted later
        """
    
        if cn in NUMERIC_FIELDS: #all fields that are always 100% numeric
            ret = getattr(self, cn)
            
        #################### return these immediately because they are strings
        
        elif cn == "remarks":
            return self.disp_events() + self.remarks
        
        elif cn == "r_remarks":
            return self.remarks
        
        elif cn == "plane":
            return str(self.plane)
        
        elif cn == "reg":
            return self.plane.tailnumber
        
        elif cn == "type":
            return self.plane.type
            
        elif cn == "f_route":
            if self.route.fancy_rendered:
                # mark_safe because theres HTML code within
                return mark_safe(self.route.fancy_rendered or "")
            else:
                # or "" to prevent "None" from getting printed
                return self.route_string or ""
            
        elif cn == "s_route":
            if self.route.simple_rendered:
                return self.route.simple_rendered or ""
            else:
                return self.route_string or ""
                
        elif cn == "r_route":
            return self.route_string or ""
        
        elif cn == "route":
            return self.route_string or "" 
        
        ########
        
        elif cn == "date":
            return self.date
            
        elif cn == "tailnumber" and self.plane:
            return self.plane.tailnumber
            
        elif cn == "plane_type" and self.plane:
            return self.plane.type
          
        elif cn == "app":
           return self.disp_app()
       
        elif cn == "app_num_only":   #for the backup file, no 'H', or 'T'
            if self.app > 0:
                return self.app
            else:
                return ""
       
        ######################################
        
        elif cn == 'person':
            return self.person
        
        elif cn == "fo":
           if self.pic and (self.dual_g <= 0 and self.dual_r <= 0):
               return self.person
           else:
               return ""
               
        elif cn == "captain":
           if self.sic and (self.dual_g <= 0 and self.dual_r <= 0):
               return self.person
           else:
               return ""
           
        elif cn == "student":
           if self.dual_g:
               return self.person
           else:
               return ""
       
        elif cn == "instructor":
           if self.dual_r:
               return self.person
           else:
               return ""
           
        elif cn == "flying":
            ret = ""
            if self.pilot_checkride:
                ret += "P"
            if self.cfi_checkride:
                ret += "C"
            if self.ipc:
                ret += "I"
            if self.flight_review:
                ret += "B"
            if self.holding:
                ret += "H"
            if self.tracking:
                ret += "T"
            return ret
                     
        # return these immediately because
        # they are not times, so no hh:mm formatting
        
        elif cn == 'line_dist' and self.route:
            ret = "%.1f" % self.route.total_line_all
            if ret == "0.0":
                return ""
            return ret
        
        elif cn == 'km_line_dist':
            ret = "%.1f" % (self.route.total_line_all * 1.85200)
            if ret == "0.0":
                return ""
            return ret
        
        ##########
        
        elif cn == 'max_width' and self.route:
            ret = "%.1f" % self.route.max_width_all
            if ret == "0.0":
                return ""
            return ret
        
        elif cn == 'km_max_width' and self.route:
            ret = "%.1f" % (self.route.max_width_all * 1.85200)
            if ret == "0.0":
                return ""
            return ret
            
        ##########
        
        elif cn == 'speed':
            if self.speed:
                return "%.1f" % self.speed
            else:
                return ""

        elif cn == 'kmh_speed':
            if self.speed:
                return "%.1f" % (self.speed * 1.85200)
            else:
                return ""

        #########
            
        elif cn in ('liters', 'gallons', 'gph', 'mpg'):
            try:
                disp = self.get_fuel_burn().as_unit(cn)
            except:
                return ""
            
            if not self.fuel_burn:
                ## wrap the output in a span because this value did not come
                ## directly from the user, it was calculated implictly
                ## from the plane. Determined by checking to see if the
                ## fuel burn field on the flight is empty
                t = '<span class="indirect_fuel_burn">{disp}</span>'
                return t.format(disp=disp)
            return disp
            
        elif cn == 'fuel_burn':
            return self.fuel_burn or ""
        
        ######################################
        
        elif cn == 'atp_xc' and self.route.max_width_all > 49:
            ret = self.total
        
        elif cn == 'p61_xc' and self.route.max_width_land > 49:
            ret = self.total
        
        elif cn == "total" and not self.plane.is_sim():     #total
            ret = self.total
            
        elif cn == "sim" and self.plane.is_sim():           #sim
            ret = self.total
            
        elif cn == "total_s" and not self.plane.is_sim():   #total (sim)
            ret = self.total
            
        elif cn == "total_s" and self.plane.is_sim():
            ret = "(%s)" % self.total
            
        ######################################
        
        elif cn == 'day' and not self.plane.is_sim():
            ret = self.total - self.night
            if ret < 0:
                ret = 0
                
        elif cn == "t_pic" and self.plane.is_turbine():
            ret = self.pic

        elif cn == "mt" and self.plane.is_multi() and self.plane.is_turbine():
            ret = self.total

        elif cn == "mt_pic" and self.plane.is_multi() and self.plane.is_turbine():
            ret = self.pic

        elif cn == "m_pic" and self.plane.is_multi():
            ret = self.pic

        elif cn == "multi" and self.plane.is_multi():
            ret = self.total

        elif cn == "single" and self.plane.is_single():
            ret = self.total
            
        elif cn == "single_pic" and self.plane.is_single():
            ret = self.pic

        elif cn == "sea" and self.plane.is_sea():
            ret = self.total
            
        elif cn == "sea_pic" and self.plane.is_sea():
            ret = self.pic

        elif cn == "mes" and self.plane.is_mes():
            ret = self.total

        elif cn == "mes_pic" and self.plane.is_mes():
            ret = self.total
           
        elif cn == "turbine" and self.plane.is_turbine():
            ret = self.total
            
        elif cn == "complex" and self.plane.is_complex():
            ret = self.total
            
        elif cn == "hp" and self.plane.is_hp():
            ret = self.total
            
        elif cn == "tail" and self.plane.is_tail():
            ret = self.total
            
        elif cn == "jet" and self.plane.is_jet():
            ret = self.total
            
        elif cn == "jet_pic" and self.plane.is_jet():
            ret = self.pic

        elif cn == "p2p" and self.route:
            if self.route.p2p:
                ret = self.total

        #####################################

        if ret == "0" or ret == "0.0" or ret == 0:
            return ""
            
        elif format == "decimal" and type(ret) == type(0.0):
            # decimals are padded to one decimal, then converted to string
            return "%.1f" % ret
            
        elif type(ret) == type(5):
            # int's are straight converted to string and returned
            return str(ret)
            
        elif format == "minutes" and type(ret) == type(0.0):
            # convert to HH:MM
            return to_minutes(ret)
            
        return ret
    
    def get_fuel_burn(self):
        """
        Return the fuel burn for this flight as a FuelBurn object. If the
        flight has no fuel burn info, then create the object from the plane's
        default
        """
        
        mileage = self.route.total_line_all
        fb = self.fuel_burn
        
        if not fb:
            fb = getattr(self.plane, "fuel_burn", None)
        
        return FuelBurn(time=self.total, input=fb, mileage=mileage)
    
    @classmethod
    def make_pagination(cls, qs, profile, page):
        from django.core.paginator import Paginator, InvalidPage, EmptyPage
        
        #define how many flights will be on each page
        paginator = Paginator(qs, per_page=profile.per_page)

        try:
            page_of_flights = paginator.page(page)

        except (EmptyPage, InvalidPage):
            #if that page is invalid, use the last page
            page_of_flights = paginator.page(paginator.num_pages)
            page = paginator.num_pages

        b = range(1, page)[-5:]                        # before block
        a = range(page, paginator.num_pages+1)[1:6]    # after block
        
        return b, a, page_of_flights

######################################################################################################

class Columns(models.Model):
    user =      models.ForeignKey(User, blank=False, primary_key=True)
    
    date =      True
    
    plane =     models.BooleanField(FIELD_TITLES['plane'],  default=True,
                    help_text="Plane's tailnumber and type.")
    reg =       models.BooleanField(FIELD_TITLES['reg'],  default=False,
                    help_text="Just the plane's registration (tailnumber)")
    
    f_route =   models.BooleanField(FIELD_TITLES['f_route'],  default=True,
                    help_text='Route with coloration and extra info on mouseover')
    s_route =   models.BooleanField(FIELD_TITLES['s_route'],  default=False,
                    help_text='Route cleaned up')
    r_route =   models.BooleanField(FIELD_TITLES['r_route'],  default=False,
                    help_text="Route exactly as it's entered")
    
    total_s =   models.BooleanField(FIELD_TITLES['total_s'],  default=True,
                    help_text='Total time in aircraft, with total time in simulators in parenthesis')
    total =     models.BooleanField(FIELD_TITLES['total'],  default=False,
                    help_text='Total time in aircraft (excluding simulators entirely)')
    
    pic =       models.BooleanField(FIELD_TITLES['pic'],  default=True)
    sic =       models.BooleanField(FIELD_TITLES['sic'],  default=True)
    solo =      models.BooleanField(FIELD_TITLES['solo'], default=True)
    dual_r =    models.BooleanField(FIELD_TITLES['dual_r'], default=True)
    dual_g =    models.BooleanField(FIELD_TITLES['dual_g'], default=True)
    xc =        models.BooleanField(FIELD_TITLES['xc'], default=True)
    act_inst =  models.BooleanField(FIELD_TITLES['act_inst'], default=True)
    sim_inst =  models.BooleanField(FIELD_TITLES['sim_inst'], default=True)
    day =       models.BooleanField(FIELD_TITLES['day'], default=False,
                    help_text='Night time subtracted from Total time')
    night =     models.BooleanField(FIELD_TITLES['night'], default=True)
    night_l =   models.BooleanField(FIELD_TITLES['night_l'], default=True)
    day_l =     models.BooleanField(FIELD_TITLES['day_l'], default=True)
    app =       models.BooleanField(FIELD_TITLES['app'], default=True,
                    help_text='Approaches with Holding (H) and Tracking (T) depicted')
    
    p2p =       models.BooleanField(FIELD_TITLES['p2p'], default=False,
                    help_text='Total time if the route depicts a non-local flight')
                    
    multi =     models.BooleanField(FIELD_TITLES['multi'], default=False,
                    help_text='Total time if the plane is multi-engine')
                    
    m_pic =     models.BooleanField(FIELD_TITLES['m_pic'], default=False,
                    help_text='PIC time if the plane is multi-engine')
                    
    single =    models.BooleanField(FIELD_TITLES['single'], default=False,
                    help_text='Total time if the plane is single-engine')
                    
    single_pic= models.BooleanField(FIELD_TITLES['single_pic'], default=False,
                    help_text='PIC time if the plane is single-engine')
                    
    sea =       models.BooleanField(FIELD_TITLES['sea'], default=False,
                    help_text='Total time if the plane is a single-engine or multi-engine seaplane')
                    
    sea_pic =   models.BooleanField(FIELD_TITLES['sea_pic'], default=False,
                    help_text='PIC time if the plane is a seaplane')
                    
    mes =       models.BooleanField(FIELD_TITLES['mes'], default=False,
                    help_text='Total time if the plane is a multi-engine seaplane')
                    
    mes_pic =   models.BooleanField(FIELD_TITLES['mes_pic'], default=False,
                    help_text='PIC time if the plane is a multi-engine seaplane')
                    
    turbine =   models.BooleanField(FIELD_TITLES['turbine'], default=False,
                    help_text='Total time if the plane is tagged as \'Turbine\'')
                    
    t_pic =     models.BooleanField(FIELD_TITLES['t_pic'], default=False,
                    help_text='PIC time if the plane is tagged as \'Turbine\'') 
                    
    mt =        models.BooleanField(FIELD_TITLES['mt'], default=False,
                    help_text='Total time if the plane is multi-engine and tagged as \'Turbine\'')
                    
    mt_pic =    models.BooleanField(FIELD_TITLES['mt_pic'], default=False,
                    help_text='PIC time if the plane is multi-engine and tagged as \'Turbine\'')
    
    complex =   models.BooleanField(FIELD_TITLES['complex'], default=True,
                    help_text='Total time if plane is tagged \'Complex\'')
                    
    hp =        models.BooleanField(FIELD_TITLES['hp'], default=True,
                    help_text='Total time if plane is tagged \'High Performance\' or \'HP\'')
    
    sim =       models.BooleanField(FIELD_TITLES['sim'], default=False,
                    help_text='Total time if plane is a Simulator, FTD, or PCATD')
                    
    tail =      models.BooleanField(FIELD_TITLES['tail'], default=False,
                    help_text='Total time if the plane is tagged as \'Tailwheel\'')
                    
    jet =       models.BooleanField(FIELD_TITLES['jet'], default=False,
                    help_text='Total time if the plane is tagged as \'Jet\'')
                    
    jet_pic =   models.BooleanField(FIELD_TITLES['jet_pic'], default=False,
                    help_text='PIC time if the plane is tagged as \'Jet\'')
                    
    line_dist = models.BooleanField(FIELD_TITLES['line_dist'], default=True,
                    help_text='Total distance of the route in Nautical Miles')
                    
    atp_xc =    models.BooleanField(FIELD_TITLES['atp_xc'], default=False,
                    help_text="Total time when the route's max width > 50 NM")

    p61_xc =    models.BooleanField(FIELD_TITLES['p61_xc'], default=False,
                    help_text="Total time when the route's max width > 50 NM (only counting landing points)")
    
    speed =     models.BooleanField(FIELD_TITLES['speed'], default=False,
                    help_text="Distance / Total, in Nautical Miles per hour (Knots)")
                    
    gph =       models.BooleanField(FIELD_TITLES['gph'], default=False,
                    help_text="Gallons of fuel burned per hour")
    
    mpg =       models.BooleanField(FIELD_TITLES['mpg'], default=False,
                    help_text="Nautical miles per gallon of fuel burned")
    
    gallons =   models.BooleanField(FIELD_TITLES['gallons'], default=False,
                    help_text="Gallons of fuel burned")
                    
    max_width = models.BooleanField(FIELD_TITLES['max_width'], default=False,
                    help_text='Maximum distance between any two points in the route')
                    
    person =    models.BooleanField(FIELD_TITLES['person'], default=True)
    
    instructor= models.BooleanField(FIELD_TITLES['instructor'], default=False,
                    help_text="'Person' if Dual Received is logged")
                    
    student =   models.BooleanField(FIELD_TITLES['student'], default=False,
                    help_text="'Person' if Dual Given is logged")
                    
    fo =        models.BooleanField(FIELD_TITLES['fo'], default=False,
                    help_text="'Person' if there is PIC time, and no dual is logged")
                    
    captain =   models.BooleanField(FIELD_TITLES['captain'], default=False,
                    help_text="'Person' if there is SIC time, and no dual is logged")
                    
    remarks =   models.BooleanField(FIELD_TITLES['remarks'], default=True)
    
    
                    
    class Meta:
        verbose_name_plural = 'Columns'

    def display_list(self):
        ret=[]
        for column in FIELDS:
            if getattr(self, column):
                ret.append(column)
        return ret
    
    def prefix_len(self):
        """number of prefix fields that are turned on"""
        cols = 0
        for column in PREFIX_FIELDS:
            if getattr(self, column):
                cols += 1
    
        return cols
    
    def agg_list(self):
        ret=[]
        for column in ALL_AGG_FIELDS:
            if getattr(self, column):
                ret.append(column)
        return ret

    def header_row(self):
        ret = []
        for column in self.display_list():
            if FIELD_ABBV.get(column):
                name = FIELD_ABBV[column]
            else:
                name = FIELD_TITLES[column]

            ret.append("<td>" + name + "</td>")

        return "\n".join(ret)

    def __unicode__(self):
        return self.user.username



###################
## SIGNALS BELOW ##
###################

def render_route(sender, **kwargs):
    """
    Fill in the speed and fuel burn columns
    """
    
    flight = kwargs['instance']
    
    if not flight.route_is_rendered():
        flight.render_route()
    
    route = flight.route
    
    #####
    
    time = flight.total    
    distance = route.total_line_all

    if distance > 0 and time > 0:  ## avoid zero division
        speed = distance / time
        flight.speed = speed
    else:
        speed = None
    
    #####
    
    if flight.fuel_burn or flight.plane.fuel_burn:
        
        if flight.fuel_burn:
            fb = FuelBurn(input=flight.fuel_burn, time=time, mileage=distance)
        else:
            fb = FuelBurn(input=flight.plane.fuel_burn, time=time, mileage=distance)
        
        flight.gallons = fb.as_unit('gallons', for_db=True)
        flight.gph = fb.as_unit('gph', for_db=True)
        flight.mpg = fb.as_unit('mpg', for_db=True)

models.signals.pre_save.connect(render_route, sender=Flight)

###############################################################################

def expire_logbook_cache(sender, **kwargs):
    """
    When the user save new preferences, expire the caches on all logbook
    pages. This function is called two was: one was is by the Profile
    save signal, where sender will be the profile class, and the other way
    is by the edit_logbook signasl, in which the user instance will be the
    sender
    """
    
    from utils import expire_all, expire_logbook_cache_page
    
    page = kwargs.get('page', None)
    
    if page:
        user = sender
        expire_logbook_cache_page(user, page)
        
    elif getattr(sender, "__name__", "ff") == "Profile":
        profile = kwargs.pop('instance')
        expire_all(profile=profile)

    else:
        user = sender
        expire_all(user=user)
    
    
from profile.models import Profile 
models.signals.post_save.connect(expire_logbook_cache, sender=Profile)

from backup.models import edit_logbook
edit_logbook.connect(expire_logbook_cache)
