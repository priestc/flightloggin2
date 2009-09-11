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

    from utils import QuerySet          ## add custom filters to custom manager
    
    objects =  QuerySetManager()        ## add custom filterset manager

    date =     models.DateField()
    user =     models.ForeignKey(User, blank=False)
    remarks =  models.TextField(blank=True)

    plane =    models.ForeignKey(Plane, blank=False, null=False)
    route =    models.ForeignKey(Route, blank=True, null=True)

    total =    models.FloatField(        "Total Time",            default="")
    pic =      models.FloatField(        "PIC",                   default=0)
    sic =      models.FloatField(        "SIC",                   default=0)
    solo =     models.FloatField(        "Solo",                  default=0)
    night =    models.FloatField(        "Night",                 default=0)
    dual_r =   models.FloatField(        "Dual Received",         default=0)
    dual_g =   models.FloatField(        "Dual Given",            default=0)
    xc =       models.FloatField(        "Cross Country",         default=0)
    act_inst = models.FloatField(        "Actual Instrument",     default=0)
    sim_inst = models.FloatField(        "Simulated Instrument",  default=0)
    
    night_l =  models.PositiveIntegerField(   "Night Landings", default=0, null=False)
    day_l =    models.PositiveIntegerField(   "Day Landings",   default=0, null=False)
    app =      models.PositiveIntegerField(   "Approaches",     default=0, null=False)

    holding =           models.BooleanField(                                  default=False)
    tracking =          models.BooleanField(  "Intercepting & Tracking",      default=False)
    pilot_checkride =   models.BooleanField(  "Pilot Checkride",              default=False)
    cfi_checkride =     models.BooleanField(  "CFI Checkride",                default=False)
    flight_review =     models.BooleanField(  "Flight Review",                default=False)
    ipc =               models.BooleanField(  "IPC",                          default=False)

    person =   models.CharField(                                        max_length=30, blank=True, null=True)
            
    def __unicode__(self):
        return u"%s -- %s" % (self.date, self.remarks)

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
        ret = ""
        
        if self.ipc:
            ret += "[IPC]"
            
        if self.pilot_checkride:
            ret += "[Pilot Checkride]"
            
        if self.cfi_checkride:
            ret += "[Instructor Checkride]"
            
        if self.flight_review:
            ret += "[Flight Review]"
            
        return ret   

    def column(self, cn, format="decimal", ret=0.0):
        """Returns a string that represents the column being passed"""
    
        if cn in DB_FIELDS and not cn == "app" and not cn == "total":       # any field in the databse, except for total, remarks, and app
            ret = getattr(self, cn)
            
        ####################################### # return these immediately because they are strings

        elif cn == "f_route" and self.route:
            if self.route.fancy_rendered:
                return mark_safe(self.route.fancy_rendered + "<span class='unformatted_route'>%s</span>" % self.route.fallback_string)
            else:
                return self.route.fallback_string
            
        elif cn == "s_route" and self.route:
            if self.route.fancy_rendered:
                return mark_safe(self.route.simple_rendered + "<span class='unformatted_route'>%s</span>" % self.route.fallback_string)
            else:
                return self.route.fallback_string
        
        elif cn == "r_route" and self.route:
            return mark_safe(self.route.fallback_string + "<span class='unformatted_route'>%s</span>" % self.route.fallback_string)
        
        elif cn == "rr_route" and self.route:                   # for the backup file
            return mark_safe(self.route.fallback_string)
        
        elif cn == "plane":
            return self.plane
        
        elif cn == "reg":
            return self.plane.tailnumber
        
        ########
            
        elif cn == "date_backup":
            return self.date
            
        elif cn == "tailnumber" and self.plane:
            return self.plane.tailnumber
            
        elif cn == "plane_type" and self.plane:
            return self.plane.type
                    
        elif cn == "events":
            return self.disp_events()
          
        elif cn == "app":
           return self.disp_app()
           
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

######################################################################################################

class Columns(models.Model):
    user =      models.ForeignKey(User, blank=False, primary_key=True)
    
    date =      True
    
    plane =     models.BooleanField(FIELD_TITLES[FIELDS[1]],  default=True)
    reg =       models.BooleanField(FIELD_TITLES[FIELDS[2]],  default=False)
    
    f_route =   models.BooleanField(FIELD_TITLES[FIELDS[3]],  default=True)
    s_route =   models.BooleanField(FIELD_TITLES[FIELDS[4]],  default=False)
    r_route =   models.BooleanField(FIELD_TITLES[FIELDS[5]],  default=False)
    
    total_s =   models.BooleanField(FIELD_TITLES[FIELDS[6]],  default=True)
    total =     models.BooleanField(FIELD_TITLES[FIELDS[7]],  default=False)
    
    pic =       models.BooleanField(FIELD_TITLES[FIELDS[8]],  default=True)
    sic =       models.BooleanField(FIELD_TITLES[FIELDS[9]],  default=True)
    solo =      models.BooleanField(FIELD_TITLES[FIELDS[10]], default=True)
    dual_r =    models.BooleanField(FIELD_TITLES[FIELDS[11]], default=True)
    dual_g =    models.BooleanField(FIELD_TITLES[FIELDS[12]], default=True)
    xc =        models.BooleanField(FIELD_TITLES[FIELDS[13]], default=True)
    act_inst =  models.BooleanField(FIELD_TITLES[FIELDS[14]], default=True)
    sim_inst =  models.BooleanField(FIELD_TITLES[FIELDS[15]], default=True)
    night =     models.BooleanField(FIELD_TITLES[FIELDS[16]], default=True)
    night_l =   models.BooleanField(FIELD_TITLES[FIELDS[17]], default=True)
    day_l =     models.BooleanField(FIELD_TITLES[FIELDS[18]], default=True)
    app =       models.BooleanField(FIELD_TITLES[FIELDS[19]], default=True)
    
    p2p =       models.BooleanField(FIELD_TITLES[FIELDS[20]], default=False)
    multi =     models.BooleanField(FIELD_TITLES[FIELDS[21]], default=False)
    m_pic =     models.BooleanField(FIELD_TITLES[FIELDS[22]], default=False)
    sea =       models.BooleanField(FIELD_TITLES[FIELDS[23]], default=False)
    sea_pic =   models.BooleanField(FIELD_TITLES[FIELDS[24]], default=False)
    mes =       models.BooleanField(FIELD_TITLES[FIELDS[25]], default=False)
    mes_pic =   models.BooleanField(FIELD_TITLES[FIELDS[26]], default=False)
    turbine =   models.BooleanField(FIELD_TITLES[FIELDS[27]], default=False)
    t_pic =     models.BooleanField(FIELD_TITLES[FIELDS[28]], default=False)
    mt =        models.BooleanField(FIELD_TITLES[FIELDS[29]], default=False)
    mt_pic =    models.BooleanField(FIELD_TITLES[FIELDS[30]], default=False)
    
    complex =   models.BooleanField(FIELD_TITLES[FIELDS[31]], default=True)
    hp =        models.BooleanField(FIELD_TITLES[FIELDS[32]], default=True)
    
    sim =       models.BooleanField(FIELD_TITLES[FIELDS[33]], default=False)
    tail =      models.BooleanField(FIELD_TITLES[FIELDS[34]], default=False)
    jet =       models.BooleanField(FIELD_TITLES[FIELDS[35]], default=False)
    jet_pic =   models.BooleanField(FIELD_TITLES[FIELDS[36]], default=False)
    
    person =    models.BooleanField(FIELD_TITLES[FIELDS[37]], default=True)
    remarks =   models.BooleanField(FIELD_TITLES[FIELDS[38]], default=True)

    def as_list(self):
        ret=[]
        for column in FIELDS:
            if getattr(self, column):
                ret.append(column)

        return ret

    def header_row(self):
        ret = []
        for column in self.as_list():
            if FIELD_ABBV.get(column):
                name = FIELD_ABBV[column]
            else:
                name = FIELD_TITLES[column]

            ret.append("<td>" + name + "</td>")

        return "\n".join(ret)

    def __unicode__(self):
        return self.user.username
