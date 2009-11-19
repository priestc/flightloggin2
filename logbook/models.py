from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from plane.models import Plane
from route.models import Route
from constants import *
from utils import to_minutes
    
class QuerySetManager(models.Manager):
    def get_query_set(self):
        return self.model.QuerySet(self.model)
    
    def __getattr__(self, name):
        return getattr(self.get_query_set(), name)


class Flight(models.Model):
    """
    >>> from django.contrib.auth.models import User
    >>> me=User.objects.get(pk=1)
    >>>
    >>> from plane.models import Plane
    >>> p = Plane(tailnumber="N800U", cat_class=2, tags='complex, hp')
    >>> p.save()
    >>>
    >>> from route.models import Route
    >>> r = Route.from_string("vta-uni-vta")
    >>>
    >>> f = Flight(user=me, total=1.0, pic=2.0, dual_g=3.0, plane=p, route=r)
    >>> f.column('multi')
    '1.0'
    >>> f.column('p2p')
    '1.0'
    >>> f.column('hp')
    '1.0'
    """

    from utils import QuerySet          ## add custom filters to custom manager
    
    objects =  QuerySetManager()        ## add custom filterset manager

    date =     models.DateField()
    user =     models.ForeignKey(User, blank=False, editable=False)
    remarks =  models.TextField(blank=True)

    plane =    models.ForeignKey(Plane, default=1) # 1 = 'unknown' plane
    route =    models.ForeignKey(Route, related_name="flight")

    total =    models.FloatField(    "Total Time",            default=0)
    pic =      models.FloatField(    "PIC",                   default=0)
    sic =      models.FloatField(    "SIC",                   default=0)
    solo =     models.FloatField(    "Solo",                  default=0)
    night =    models.FloatField(    "Night",                 default=0)
    dual_r =   models.FloatField(    "Dual Received",         default=0)
    dual_g =   models.FloatField(    "Dual Given",            default=0)
    xc =       models.FloatField(    "Cross Country",         default=0)
    act_inst = models.FloatField(    "Actual Instrument",     default=0)
    sim_inst = models.FloatField(    "Simulated Instrument",  default=0)
    
    night_l =  models.PositiveIntegerField(   "Night Landings", default=0, null=False)
    day_l =    models.PositiveIntegerField(   "Day Landings",   default=0, null=False)
    app =      models.PositiveIntegerField(   "Approaches",     default=0, null=False)

    holding =           models.BooleanField(                           default=False)
    tracking =          models.BooleanField("Intercepting & Tracking", default=False)
    pilot_checkride =   models.BooleanField("Pilot Checkride",         default=False)
    cfi_checkride =     models.BooleanField("CFI Checkride",           default=False)
    flight_review =     models.BooleanField("Flight Review",           default=False)
    ipc =               models.BooleanField("IPC",                     default=False)

    person =   models.CharField( max_length=60, blank=True, null=True)
            
    def __unicode__(self):
        return u"%s -- %s" % (self.date, self.remarks)
    
    @models.permalink
    def get_absolute_url(self):
        return ('logbook', [self.user.username])
    
    @classmethod
    def goon(cls, *args, **kwargs):
        from annoying.functions import get_object_or_None
        return get_object_or_None(cls,  *args, **kwargs)
    
    def save(self, *args, **kwargs):
        from share.middleware import share
        try:
            getattr(self, "user", None).username
        except:
            #user is not set, we now must get the current logged in user
            from share.middleware import share
            self.user = share.get_display_user()
        
        super(Flight,self).save(*args, **kwargs)
        
    class Meta:
        ordering = ["date", "id"]
        
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
            return mark_safe("<span class=\"flying_event\">%s</span> " % ret)

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
                return mark_safe(self.route.fancy_rendered)
            else:
                return self.route.fallback_string or ""
            
        elif cn == "s_route":
            if self.route.simple_rendered:
                return self.route.simple_rendered or ""
            else:
                return self.route.fallback_string or ""
                
        elif cn == "r_route":
            return self.route.fallback_string or ""
        
        elif cn == "route":
            return self.route.fallback_string or ""
        
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
           if self.pic and self.dual_g <= 0:
               return self.person
           else:
               return ""
               
        elif cn == "captain":
           if self.sic:
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
                     
        ################################### return these immediately because
        # they are distances, no hh:mm formatting
        
        elif cn == 'line_dist' and self.route:
            ret = "%.1f" % self.route.total_line_all
            if ret == "0.0":
                return ""
            return ret
        
        elif cn == 'max_width' and self.route:
            ret = "%.1f" % self.route.max_width_all
            if ret == "0.0":
                return ""
            return ret
        
        elif cn == 'speed' and self.route and self.total > 0:
            ret = "%.1f" % (self.route.total_line_all / self.total)
            if ret == "0.0":
                return ""
            return ret
        
        
        elif cn == 'atp_xc'  and self.route and self.route.max_width_all > 49:
            ret = self.total

        ######################################
        
        elif cn == "total" and not self.plane.is_sim():     #total
            ret = self.total
            
        elif cn == "sim" and self.plane.is_sim():           #sim
            ret = self.total
            
        elif cn == "total_s" and not self.plane.is_sim():   #total (sim)
            ret = self.total
            
        elif cn == "total_s" and self.plane.is_sim():
            ret = "(%s)" % self.total
            
        ######################################
        
        elif cn == 'day':
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
            
        elif format == "decimal" and type(ret) == type(0.0):    # decimals are padded to one decimal space, converted to string, then returned
            return "%.1f" % ret
            
        elif type(ret) == type(5):                              # int's are straight converted to string and returned
            return str(ret)
            
        elif format == "minutes" and type(ret) == type(0.0):    # convert to HH:MM
            return to_minutes(ret)
            
        return ret
    
    @classmethod
    def make_pagination(cls, qs, profile, page):
        from django.core.paginator import Paginator, InvalidPage, EmptyPage
        
        
        paginator = Paginator(qs, per_page=profile.per_page)		#define how many flights will be on each page

        try:
            page_of_flights = paginator.page(page)

        except (EmptyPage, InvalidPage):
            page_of_flights = paginator.page(paginator.num_pages)		#if that page is invalid, use the last page
            page = paginator.num_pages

        b = range(1, page)[-5:]                        # before block
        a = range(page, paginator.num_pages+1)[1:6]    # after block
        
        return b, a, page_of_flights

######################################################################################################

class Columns(models.Model):
    user =      models.ForeignKey(User, blank=False, primary_key=True)
    
    date =      True
    
    plane =     models.BooleanField(FIELD_TITLES[FIELDS[1]],  default=True,
                    help_text='Plane\'s tailnumber and type.')
    reg =       models.BooleanField(FIELD_TITLES[FIELDS[2]],  default=False,
                    help_text='Just the plane\'s registration (tailnumber)')
    
    f_route =   models.BooleanField(FIELD_TITLES[FIELDS[3]],  default=True,
                    help_text='Route with coloration and extra info on mouseover')
    s_route =   models.BooleanField(FIELD_TITLES[FIELDS[4]],  default=False,
                    help_text='Route cleaned up')
    r_route =   models.BooleanField(FIELD_TITLES[FIELDS[5]],  default=False,
                    help_text='Route exactly as it\'s entered')
    
    total_s =   models.BooleanField(FIELD_TITLES[FIELDS[6]],  default=True,
                    help_text='Total time in aircraft, with total time in simulators in parenthesis')
    total =     models.BooleanField(FIELD_TITLES[FIELDS[7]],  default=False,
                    help_text='Total time in aircraft (excluding simulators entirely)')
    
    pic =       models.BooleanField(FIELD_TITLES[FIELDS[8]],  default=True)
    sic =       models.BooleanField(FIELD_TITLES[FIELDS[9]],  default=True)
    solo =      models.BooleanField(FIELD_TITLES[FIELDS[10]], default=True)
    dual_r =    models.BooleanField(FIELD_TITLES[FIELDS[11]], default=True)
    dual_g =    models.BooleanField(FIELD_TITLES[FIELDS[12]], default=True)
    xc =        models.BooleanField(FIELD_TITLES[FIELDS[13]], default=True)
    act_inst =  models.BooleanField(FIELD_TITLES[FIELDS[14]], default=True)
    sim_inst =  models.BooleanField(FIELD_TITLES[FIELDS[15]], default=True)
    day =       models.BooleanField(FIELD_TITLES[FIELDS[16]], default=False,
                    help_text='Night time subtracted from Total time')
    night =     models.BooleanField(FIELD_TITLES[FIELDS[17]], default=True)
    night_l =   models.BooleanField(FIELD_TITLES[FIELDS[18]], default=True)
    day_l =     models.BooleanField(FIELD_TITLES[FIELDS[19]], default=True)
    app =       models.BooleanField(FIELD_TITLES[FIELDS[20]], default=True,
                    help_text='Approaches with Holding (H) and Tracking (T) depicted')
    
    p2p =       models.BooleanField(FIELD_TITLES[FIELDS[21]], default=False,
                    help_text='Total time if the route depicts a non-local flight')
                    
    multi =     models.BooleanField(FIELD_TITLES[FIELDS[22]], default=False,
                    help_text='Total time if the plane is multi-engine')
                    
    m_pic =     models.BooleanField(FIELD_TITLES[FIELDS[23]], default=False,
                    help_text='PIC time if the plane is multi-engine and tagged as \'Turbine\'')
                    
    sea =       models.BooleanField(FIELD_TITLES[FIELDS[24]], default=False,
                    help_text='Total time if the plane is a single-engine or multi-engine seaplane')
                    
    sea_pic =   models.BooleanField(FIELD_TITLES[FIELDS[25]], default=False,
                    help_text='PIC time if the plane is a seaplane')
                    
    mes =       models.BooleanField(FIELD_TITLES[FIELDS[26]], default=False,
                    help_text='Total time if the plane is a multi-engine seaplane')
                    
    mes_pic =   models.BooleanField(FIELD_TITLES[FIELDS[27]], default=False,
                    help_text='PIC time if the plane is a multi-engine seaplane')
                    
    turbine =   models.BooleanField(FIELD_TITLES[FIELDS[28]], default=False,
                    help_text='Total time if the plane is tagged as \'Turbine\'')
                    
    t_pic =     models.BooleanField(FIELD_TITLES[FIELDS[29]], default=False,
                    help_text='PIC time if the plane is tagged as \'Turbine\'') 
                    
    mt =        models.BooleanField(FIELD_TITLES[FIELDS[30]], default=False,
                    help_text='Total time if the plane is multi-engine and tagged as \'Turbine\'')
                    
    mt_pic =    models.BooleanField(FIELD_TITLES[FIELDS[31]], default=False,
                    help_text='PIC time if the plane is multi-engine and tagged as \'Turbine\'')
    
    complex =   models.BooleanField(FIELD_TITLES[FIELDS[32]], default=True,
                    help_text='Total time if plane is tagged \'Complex\'')
                    
    hp =        models.BooleanField(FIELD_TITLES[FIELDS[33]], default=True,
                    help_text='Total time if plane is tagged \'High Performance\' or \'HP\'')
    
    sim =       models.BooleanField(FIELD_TITLES[FIELDS[34]], default=False,
                    help_text='Total time if plane is a Simulator, FTD, or PCATD')
                    
    tail =      models.BooleanField(FIELD_TITLES[FIELDS[35]], default=False,
                    help_text='Total time if the plane is tagged as \'Tailwheel\'')
                    
    jet =       models.BooleanField(FIELD_TITLES[FIELDS[36]], default=False,
                    help_text='Total time if the plane is tagged as \'Jet\'')
                    
    jet_pic =   models.BooleanField(FIELD_TITLES[FIELDS[37]], default=False,
                    help_text='PIC time if the plane is tagged as \'Jet\'')
                    
    line_dist = models.BooleanField(FIELD_TITLES[FIELDS[38]], default=True,
                    help_text='Total distance of the route in Nautical Miles')
                    
    atp_xc =    models.BooleanField(FIELD_TITLES[FIELDS[39]], default=False,
                    help_text="Total time when the route's max width > 50 NM")

    speed =     models.BooleanField(FIELD_TITLES[FIELDS[40]], default=False,
                    help_text="Distance / Total, in Nautical Miles per hour (Knots)")
                    
    max_width = models.BooleanField(FIELD_TITLES[FIELDS[41]], default=False,
                    help_text='Maximum distance between any two points in the route')
                    
    
    person =    models.BooleanField(FIELD_TITLES[FIELDS[42]], default=True)
    
    
    instructor= models.BooleanField(FIELD_TITLES[FIELDS[43]], default=False,
                    help_text='\'Person\' if Dual Received is logged')
                    
    student =   models.BooleanField(FIELD_TITLES[FIELDS[44]], default=False,
                    help_text='\'Person\' if Dual Given is logged')
                    
    fo =        models.BooleanField(FIELD_TITLES[FIELDS[45]], default=False,
                    help_text='\'Person\' if PIC time is logged')
                    
    captain =   models.BooleanField(FIELD_TITLES[FIELDS[46]], default=False,
                    help_text='\'Person\' if there is SIC time logged')
                    
    remarks =   models.BooleanField(FIELD_TITLES[FIELDS[47]], default=True) 
                    
    class Meta:
        verbose_name_plural = 'Columns'

    def all_list(self):
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
        for column in self.all_list():
            if FIELD_ABBV.get(column):
                name = FIELD_ABBV[column]
            else:
                name = FIELD_TITLES[column]

            ret.append("<td>" + name + "</td>")

        return "\n".join(ret)

    def __unicode__(self):
        return self.user.username
