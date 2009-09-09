from django.db import models
from django.contrib.auth.models import User
from constants import *
from plane.constants import CATEGORY_CLASSES, FAKE_CLASSES

class Profile(models.Model):
    user =           models.ForeignKey(User, primary_key=True)

    dob =            models.DateField(             "Date of Birth",             blank=True, default="1900-01-01")
    style =          models.IntegerField(                                       choices=STYLES, default=1)
    date_format =    models.CharField(                                          blank=True, max_length=32, default="Y-m-d")

    real_name =      models.CharField(             "Real Name",                 blank=True, max_length=32)
    per_page =       models.PositiveIntegerField(  "Logbook Entries Per Page",  default=50)
    backup_email =   models.EmailField(            "Backup Email",              blank=True, help_text="Leave blank to use the email listed above")
    backup_freq =    models.IntegerField(          "Backup Frequency",          choices=BACKUP_FREQUENCY, default=0)
    type_str =       models.CharField(                                          blank=True, max_length=128)
    minutes =        models.BooleanField(  "Display times as HH:MM",            default=False)
    share =          models.BooleanField(  "Allow others to see your logbook?", default=True)

    def __unicode__(self):
        return u"%s - %s" % (self.user, self.real_name)

    class Meta:
        pass

class Entries(models.Model):
    user =          models.ForeignKey(User, blank=False, primary_key=True)
    pic =           models.BooleanField(default=True)
    sic =           models.BooleanField(default=True)
    solo =          models.BooleanField(default=True)
    dual_r =        models.BooleanField(default=True)
    dual_g =        models.BooleanField(default=True)
    act_inst =      models.BooleanField(default=True)
    sim_inst =      models.BooleanField(default=True)
    xc =            models.BooleanField(default=True)
    night =         models.BooleanField(default=True)

    app =           models.BooleanField(default=True)
    day_l =         models.BooleanField(default=True)
    night_l =       models.BooleanField(default=True)

    student =       models.BooleanField(default=True)
    instructor =    models.BooleanField(default=True)
    captain =       models.BooleanField(default=True)
    fo =            models.BooleanField(default=True)
    remarks =       models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" % (self.user, )

    def as_list(self):
        ret = []

        return ret


class AutoButton(models.Model):
    user =          models.ForeignKey(User, blank=False, primary_key=True)
    pic =           models.BooleanField(default=True)
    sic =           models.BooleanField(default=False)
    solo =          models.BooleanField(default=False)
    dual_r =        models.BooleanField(default=False)
    dual_g =        models.BooleanField(default=False)
    act_inst =      models.BooleanField(default=False)
    sim_inst =      models.BooleanField(default=False)
    xc =            models.BooleanField(default=False)
    night =         models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % (self.user, )
    
    def as_jslist(self):
        ret = []
        for field in ['pic','sic','solo','dual_g','dual_r','xc','night','sim_inst', 'act_inst']:
            if getattr(self, field):
                ret.append(field)
        return ret
        

