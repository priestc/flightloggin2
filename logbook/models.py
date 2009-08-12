from django.db import models
from django.contrib.auth.models import User

from plane.models import Plane
from airport.models import Airport
from constants import *

class Flight(models.Model):

    date =      models.DateField()
    user =      models.ForeignKey(User, blank=False)
    remarks =   models.TextField(blank=True)

    plane =    models.ForeignKey(Plane, blank=False, null=False)
    route =    models.ForeignKey("Route", blank=True, null=True)

    total =    models.DecimalField(             "Total Time",           max_digits=4, decimal_places=1, default=0, null=False)
    sim_inst = models.DecimalField(             "Simulated Instrument", max_digits=4, decimal_places=1, default=0, null=False)
    act_inst = models.DecimalField(             "Actual Instrument",    max_digits=4, decimal_places=1, default=0, null=False)
    night =    models.DecimalField(             "Night",                max_digits=4, decimal_places=1, default=0, null=False)
    xc =       models.DecimalField(             "Cross Country",        max_digits=4, decimal_places=1, default=0, null=False)
    pic =      models.DecimalField(             "PIC",                  max_digits=4, decimal_places=1, default=0, null=False)
    sic =      models.DecimalField(             "SIC",                  max_digits=4, decimal_places=1, default=0, null=False)
    dual_g =   models.DecimalField(             "Dual Given",           max_digits=4, decimal_places=1, default=0, null=False)
    dual_r =   models.DecimalField(             "Dual Received",        max_digits=4, decimal_places=1, default=0, null=False)
    solo =     models.DecimalField(             "Solo",                 max_digits=4, decimal_places=1, default=0, null=False)

    day_l =    models.PositiveIntegerField(     "Day Landings",                                         default=0, null=False)
    night_l =  models.PositiveIntegerField(     "Night Landings",                                       default=0, null=False)
    app =      models.PositiveIntegerField(     "Approaches",                                           default=0, null=False)

    holding =           models.BooleanField(                                            default=False)
    tracking =          models.BooleanField(            "Intercepting & Tracking",      default=False)
    pilot_checkride =   models.BooleanField(            "Pilot Checkride",              default=False)
    cfi_checkride =     models.BooleanField(            "CFI Checkride",                default=False)
    flight_review =     models.BooleanField(            "Flight Review",                default=False)
    ipc =               models.BooleanField(            "IPC",                          default=False)

    person =   models.CharField(                                        max_length=30, blank=True, null=True)

    def __unicode__(self):
        return u"%s -- %s" % (self.date, self.remarks)

    class Meta:
        ordering = ["date", "id"]

    def column(self, cn):
        ret = "0"
        try:
            ret = str(getattr(self, cn))

        except AttributeError:

            if cn == "t_pic" and self.plane.is_turbine():
                ret = self.pic

            if cn == "mt" and self.plane.is_turbine():
                ret = self.pic

            if cn == "mt_pic" and self.plane.is_multi() and self.plane.is_turbine():
                    ret = self.pic

            if cn == "m_pic" and self.plane.is_multi():
                ret = self.pic

            if cn == "multi" and self.plane.is_multi():
                ret = self.total

            if cn == "sea" and self.plane.is_sea():
                ret = self.sim_inst

            if cn == "mes" and self.plane.is_mes():
                ret = self.total

            if cn == "mes_pic" and self.plane.is_mes():
                ret = self.total
               
            if cn == "turbine" and self.plane.is_turbine():
                ret = self.total

            if cn == "p2p" and self.route:
                if route.is_p2p():
                    ret = self.total

        #####################################
        if cn == "date":
            return ret

        if ret == "0" or ret == "0.0":
            return ""
        else:
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

class Route(models.Model):
    def __unicode__(self):
        ret = []

        for point in self.routebase_set.all():
            ret.append(point)

        return "-".join(ret)

    def fancy_display(self):
        ret = []
        for point in self.routebase_set.all():
            ret.append("<span title='%s'>%s</span>" % (point.location_summary(), point.identifier, ) )

        return "-".join(ret)

    def is_p2p(self):
        return True 

class RouteBase(models.Model):
    route =    models.ForeignKey("Route")
    airport =  models.ForeignKey(Airport)
    sequence = models.PositiveIntegerField()


class Columns(models.Model):
    user =              models.ForeignKey(User, blank=False, primary_key=True)

    total =     models.BooleanField(default=True)
    pic =               models.BooleanField(FIELDS[5],  default=True)
    sic =               models.BooleanField(FIELDS[6],  default=True)
    solo =              models.BooleanField(            default=True)
    dual_r =    models.BooleanField(FIELDS[9],  default=True)
    dual_g =    models.BooleanField(FIELDS[10], default=True)
    act_inst =  models.BooleanField(FIELDS[12], default=True)
    sim_inst =  models.BooleanField(FIELDS[13], default=True)
    xc =                models.BooleanField(FIELDS[11], default=True)
    night =             models.BooleanField(            default=True)

    app =               models.BooleanField(FIELDS[16], default=True)
    day_l =             models.BooleanField(FIELDS[15], default=True)
    night_l =   models.BooleanField(FIELDS[14], default=True)
    person =    models.BooleanField(            default=True)
    remarks =   models.BooleanField(            default=True)

    p2p =       models.BooleanField(FIELDS[17], default=False)
    turbine =   models.BooleanField(FIELDS[24], default=False)
    multi =     models.BooleanField(FIELDS[18], default=False)
    mt =        models.BooleanField(FIELDS[26], default=False)
    sea =       models.BooleanField(FIELDS[20], default=False)
    m_pic =     models.BooleanField(FIELDS[19], default=False)
    mt_pic =    models.BooleanField(FIELDS[27], default=False)
    t_pic =     models.BooleanField(FIELDS[25], default=False)
    mes =       models.BooleanField(FIELDS[22], default=False)
    sea_pic =   models.BooleanField(FIELDS[21], default=False)
    mes_pic =   models.BooleanField(FIELDS[23], default=False)

    date =      True
    route =     True
    plane =     True

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
                name = FIELD_TITLE[column]

            ret.append("<td>" + name + "</td>")

        return "\n".join(ret)

    def __unicode__(self):
        return self.user.username
