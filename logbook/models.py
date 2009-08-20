from django.db import models
from django.contrib.auth.models import User

from plane.models import Plane
from route.models import Route
from constants import *

class Flight(models.Model):

    date =      models.DateField()
    user =      models.ForeignKey(User, blank=False)
    remarks =   models.TextField(blank=True)

    plane =    models.ForeignKey(Plane, blank=False, null=False)
    route =    models.ForeignKey(Route, blank=True, null=True)

    total =    models.FloatField(        "Total Time",            default="")
    sim_inst = models.FloatField(        "Simulated Instrument",  default=0)
    act_inst = models.FloatField(        "Actual Instrument",     default=0)
    night =    models.FloatField(        "Night",                 default=0)
    xc =       models.FloatField(        "Cross Country",         default=0)
    pic =      models.FloatField(        "PIC",                   default=0)
    sic =      models.FloatField(        "SIC",                   default=0)
    dual_g =   models.FloatField(        "Dual Given",            default=0)
    dual_r =   models.FloatField(        "Dual Received",         default=0)
    solo =     models.FloatField(        "Solo",                  default=0)

    day_l =    models.PositiveIntegerField(   "Day Landings",   default=0, null=False)
    night_l =  models.PositiveIntegerField(   "Night Landings", default=0, null=False)
    app =      models.PositiveIntegerField(   "Approaches",     default=0, null=False)

    holding =           models.BooleanField(                                  default=False)
    tracking =          models.BooleanField(  "Intercepting & Tracking",      default=False)
    pilot_checkride =   models.BooleanField(  "Pilot Checkride",              default=False)
    cfi_checkride =     models.BooleanField(  "CFI Checkride",                default=False)
    flight_review =     models.BooleanField(  "Flight Review",                default=False)
    ipc =               models.BooleanField(  "IPC",                          default=False)
    
    staging = models.BooleanField(default=False)

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
    
        if cn in DB_FIELDS and not cn == "route" and not cn == "app":       # any field in the databse, except for route, remarks, and app
            ret = getattr(self, cn)
            
        ####################################### # return these immediately because they are strings

        elif cn == "route" and self.route:
            return self.route.fancy_display()
        
        elif cn == "fixed_route" and self.route:
            return self.route
            
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
                
        elif cn == "t_pic" and self.plane.is_turbine():
            ret = self.pic

        elif cn == "mt" and self.plane.is_turbine():
            ret = self.pic

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

        elif cn == "p2p" and self.route:
            if self.route.is_p2p():
                ret = self.total

        #####################################

        if ret == "0" or ret == "0.0" or ret == 0:
            return ""
            
        elif format == "decimal" and type(ret) == type(0.0):
            return "%.1f" % ret
            
        elif format == "decimal" and type(ret) == type(0):
            return str(ret)
            
        elif format == "minutes" and type(ret) == type(0.0):
            value = str(ret)
            h,d = value.split(".")
            minutes = float("0." + d) * 60
            return str(h) + ":" + "%02.f" % minutes
            
        return ret

######################################################################################################

class NonFlight(models.Model):

    date =      models.DateField()
    user =      models.ForeignKey(User, blank=False)
    remarks =   models.TextField(blank=True)

    non_flying = models.IntegerField(choices=NON_FLYING_CHOICES, default=0, blank=False)

    def __unicode__(self):
        return u"%s -- %s" % (self.date, self.get_non_flying_display() )

######################################################################################################

class Columns(models.Model):
    user =      models.ForeignKey(User, blank=False, primary_key=True)
    
    date =      True
    route =     True
    plane =     True
    total =     True
    
    pic =       models.BooleanField(FIELDS[5],  default=True)
    sic =       models.BooleanField(FIELDS[6],  default=True)
    solo =      models.BooleanField(            default=True)
    dual_r =    models.BooleanField(FIELDS[9],  default=True)
    dual_g =    models.BooleanField(FIELDS[10], default=True)
    xc =        models.BooleanField(FIELDS[11], default=True)
    act_inst =  models.BooleanField(FIELDS[12], default=True)
    sim_inst =  models.BooleanField(FIELDS[13], default=True)
    night =     models.BooleanField(            default=True)

    
    night_l =   models.BooleanField(FIELDS[14], default=True)
    day_l =     models.BooleanField(FIELDS[15], default=True)
    app =       models.BooleanField(FIELDS[16], default=True)
    
    p2p =       models.BooleanField(FIELDS[17], default=False)
    multi =     models.BooleanField(FIELDS[18], default=False)
    m_pic =     models.BooleanField(FIELDS[19], default=False)
    sea =       models.BooleanField(FIELDS[20], default=False)
    sea_pic =   models.BooleanField(FIELDS[21], default=False)
    mes =       models.BooleanField(FIELDS[22], default=False)
    mes_pic =   models.BooleanField(FIELDS[23], default=False)
    turbine =   models.BooleanField(FIELDS[24], default=False)
    t_pic =     models.BooleanField(FIELDS[25], default=False)
    mt =        models.BooleanField(FIELDS[26], default=False)
    mt_pic =    models.BooleanField(FIELDS[27], default=False)
    
    complex =   models.BooleanField(FIELDS[28], default=True)
    hp =        models.BooleanField(FIELDS[29], default=True)
    
    person =    models.BooleanField(            default=True)
    remarks =   models.BooleanField(            default=True)

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
